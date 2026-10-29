"""Emit a KiCad 8/9 schematic sheet from a component + net list.

Why this exists: the board has ~9 blocks and a few hundred connections. Writing
s-expressions by hand is error-prone; this builds them from a declarative block
description, then kicad-cli runs ERC over the result.

How connections are made: a label placed exactly on a pin's endpoint is a
connection in KiCad, so the generator emits labels at pin coordinates instead of
routing wire segments. That is electrically identical, survives rearranging the
sheet in the GUI, and cannot produce the almost-touching-wire bugs that hand
placement does. Tidy the visual layout in Eeschema afterwards; the netlist is
already right.

Usage:
    python tools/schgen.py blocks/01_power_input.py out.kicad_sch
"""
import re
import sys
import uuid
import importlib.util
from pathlib import Path

KICAD_SYMBOLS = Path(r"C:\Program Files\KiCad\9.0\share\kicad\symbols")


def _uuid():
    return str(uuid.uuid4())


def _find_block(txt, name):
    """Return the s-expression text of (symbol "<name>" ...) from a library."""
    start = txt.find(f'(symbol "{name}"')
    if start < 0:
        return None
    depth = 0
    for i in range(start, len(txt)):
        if txt[i] == "(":
            depth += 1
        elif txt[i] == ")":
            depth -= 1
            if depth == 0:
                return txt[start : i + 1]
    return None


class SymbolLib:
    """Loads KiCad symbol libraries and flattens 'extends' inheritance."""

    def __init__(self, extra_libs=()):
        self._cache = {}
        self._libs = {p.stem: p for p in KICAD_SYMBOLS.glob("*.kicad_sym")}
        for p in extra_libs:
            self._libs[Path(p).stem] = Path(p)

    def _raw(self, libname, symname):
        txt = self._libs[libname].read_text(encoding="utf-8")
        return _find_block(txt, symname)

    def get(self, libid):
        """libid is 'Library:Symbol'. Returns (flattened_body, pins)."""
        if libid in self._cache:
            return self._cache[libid]
        libname, symname = libid.split(":", 1)
        raw = self._raw(libname, symname)
        if raw is None:
            raise KeyError(f"symbol not found: {libid}")

        ext = re.search(r'\(extends "([^"]+)"\)', raw)
        if ext:
            parent_raw = self._raw(libname, ext.group(1))
            if parent_raw is None:
                raise KeyError(f"parent symbol not found: {libname}:{ext.group(1)}")
            # Keep the child's properties, take the parent's graphics and pins:
            # every (symbol "<name>_N_M" ...) sub-unit block.
            units = re.findall(r'\(symbol "[^"]*_\d+_\d+"', parent_raw)
            body = raw.replace(ext.group(0), "")
            for u in units:
                blk = _find_block(parent_raw, u[len('(symbol "') :].rstrip('"'))
                if blk:
                    # rename sub-units to this symbol's name
                    blk = re.sub(
                        r'^\(symbol "[^"]*?(_\d+_\d+)"',
                        lambda m: f'(symbol "{symname}{m.group(1)}"',
                        blk,
                    )
                    body = body.rstrip()[:-1] + "\n" + blk + "\n)"
            raw = body

        # Inside a .kicad_sch, cached symbols are named by full lib id
        # ("Device:R"), not by the bare library name ("R"), and sub-units follow
        # the same prefix. Getting this wrong makes KiCad segfault rather than
        # report a missing symbol.
        # Only the top-level symbol takes the "Lib:Name" form. Sub-units keep
        # their bare names ("R_0_1"), exactly as Eeschema writes them — prefixing
        # those makes the sheet fail to load.
        raw = re.sub(
            r'^\(symbol "' + re.escape(symname) + r'"',
            f'(symbol "{libid}"',
            raw,
        )

        # KiCad 9 .kicad_sym symbols carry their own (embedded_fonts ...) field.
        # Eeschema does not write it inside a schematic's cached lib_symbols, and
        # its presence makes the sheet fail to load.
        raw = re.sub(r"\n\s*\(embedded_fonts (?:yes|no)\)", "", raw)

        pins = {}
        names = {}
        for m in re.finditer(
            r"\(pin\s+\S+\s+\S+\s*\(at\s+([-\d.]+)\s+([-\d.]+)\s+([\d.]+)\)"
            r"[\s\S]*?\(name\s+\"([^\"]*)\""
            r"[\s\S]*?\(number\s+\"([^\"]+)\"",
            raw,
        ):
            x, y, _rot, name, num = m.groups()
            pins[num] = (float(x), float(y))
            # Several pins share a name (VDD, VSS); keep every number per name so
            # a block can say "all VDD pins" once.
            names.setdefault(name, []).append(num)
        self._names = getattr(self, "_names", {})
        self._names[libid] = names

        # strip the outer (symbol "name" ... ) wrapper's name so we can re-emit
        self._cache[libid] = (raw, pins)
        return self._cache[libid]


def generate(block, out_path):
    lib = SymbolLib(extra_libs=block.EXTRA_LIBS if hasattr(block, "EXTRA_LIBS") else ())
    # Must match the root-sheet UUID recorded in the .kicad_pro, or KiCad
    # crashes while resolving symbol instance paths.
    sheet_uuid = getattr(block, "SHEET_UUID", "3f1c0a52-0001-4000-8000-000000000001")
    project = Path(out_path).stem

    lib_symbols = []
    instances = []
    labels = []
    seen = set()

    for part in block.PARTS:
        libid = part["lib"]
        body, pins = lib.get(libid)
        if libid not in seen:
            seen.add(libid)
            lib_symbols.append(body)

        x, y = part["at"]
        inst_uuid = _uuid()
        # Reference, Value, Footprint and Datasheet are mandatory fields; KiCad
        # refuses to load a sheet whose symbols are missing Datasheet.
        props = [
            ("Reference", part["ref"], 0, -2.54),
            ("Value", part.get("value", ""), 0, 2.54),
            ("Footprint", part.get("fp", ""), 0, 5.08),
            ("Datasheet", part.get("datasheet", "~"), 0, 7.62),
            ("Description", part.get("desc", ""), 0, 10.16),
        ]
        prop_txt = "\n".join(
            f'\t\t(property "{n}" "{v}"\n'
            f"\t\t\t(at {x + dx} {y + dy} 0)\n"
            f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)"
            + ("\n\t\t\t\t(hide yes)" if n in ("Footprint", "Datasheet", "Description") else "")
            + "\n\t\t\t)\n\t\t)"
            for n, v, dx, dy in props
        )
        pin_txt = "\n".join(
            f'\t\t(pin "{num}"\n\t\t\t(uuid \"{_uuid()}\")\n\t\t)' for num in pins
        )
        # Without an (instances) block Eeschema treats the symbol as
        # unannotated and leaves it out of the netlist entirely.
        inst_block = (
            f'\t\t(instances\n\t\t\t(project "{project}"\n'
            f'\t\t\t\t(path "/{sheet_uuid}"\n'
            f'\t\t\t\t\t(reference "{part["ref"]}")\n\t\t\t\t\t(unit 1)\n'
            f"\t\t\t\t)\n\t\t\t)\n\t\t)"
        )
        instances.append(
            f'\t(symbol\n\t\t(lib_id "{libid}")\n\t\t(at {x} {y} 0)\n'
            f"\t\t(unit 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n"
            f"\t\t(on_board yes)\n\t\t(dnp no)\n\t\t(uuid \"{inst_uuid}\")\n"
            f"{prop_txt}\n{pin_txt}\n{inst_block}\n\t)"
        )

        # A block may address pins by name ("PA5", "VDD") instead of number.
        # Pin names that appear on several pins (VDD, VSS) label all of them.
        nets = dict(part.get("nets", {}))
        for pin_name, net in part.get("by_name", {}).items():
            numbers = lib._names[libid].get(pin_name)
            if not numbers:
                raise KeyError(f"{libid}: no pin named {pin_name!r}")
            for num in numbers:
                nets[num] = net
        part = dict(part, nets=nets)

        # pins left open on purpose get a no-connect flag, so ERC can tell them
        # apart from pins that were forgotten
        for num in part.get("nc", []):
            px, py = pins[str(num)]
            labels.append(f'\t(no_connect\n\t\t(at {x + px} {y - py})\n\t\t(uuid "{_uuid()}")\n\t)')

        # labels at pin endpoints = connections
        for num, net in part["nets"].items():
            px, py = pins[str(num)]
            ax, ay = x + px, y - py  # sheet Y is inverted vs symbol Y
            labels.append(
                f'\t(label "{net}"\n\t\t(at {ax} {ay} 0)\n'
                f"\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n"
                f"\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid \"{_uuid()}\")\n\t)"
            )

    sheet = (
        "(kicad_sch\n\t(version 20250114)\n\t(generator \"schgen\")\n"
        "\t(generator_version \"9.0\")\n"
        f'\t(uuid "{sheet_uuid}")\n'
        f'\t(paper "{getattr(block, "PAPER", "A3")}")\n'
        f'\t(title_block\n\t\t(title "{block.TITLE}")\n\t\t(date "{block.DATE}")\n'
        f'\t\t(rev "{block.REV}")\n\t)\n'
        "\t(lib_symbols\n"
        + "\n".join("\t\t" + b.replace("\n", "\n\t") for b in lib_symbols)
        + "\n\t)\n"
        + "\n".join(instances)
        + "\n"
        + "\n".join(labels)
        + '\n\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n'
        "\t(embedded_fonts no)\n)\n"
    )
    Path(out_path).write_text(sheet, encoding="utf-8")
    print(f"wrote {out_path}: {len(block.PARTS)} parts, {len(labels)} connections")


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("block", sys.argv[1])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    generate(mod, sys.argv[2])

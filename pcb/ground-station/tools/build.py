"""Build one ground station schematic from its block files, then check it.

    python tools/build.py power
    python tools/build.py main

Each block file in <board>/blocks is a declarative part and net list (see
schgen.py). This tiles the blocks onto one sheet, writes
<board>/ground-station-<board>.kicad_sch, exports the netlist and reports any net
that reaches only one pin, which is how a typo in a net name shows up. Then it
runs KiCad's electrical rules check.

The sheet layout is only for reading. Connections are made by labels on the pin
ends, so moving symbols around in Eeschema afterwards does not change the netlist.
"""
import importlib.util
import json
import re
import subprocess
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KICAD = Path(r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe")
SHEET_UUID = "6a1d2e30-0001-4000-8000-0000000000{:02d}"

COLUMN_PITCH = 300
ROW_PITCH = 180

LIBS = {
    "tar_gs": ("${KIPRJMOD}/../lib/tar_gs", ROOT / "lib" / "tar_gs.kicad_sym"),
    "tar_fc": ("${KIPRJMOD}/../../network-drone-fc/lib/tar_fc", ROOT.parent / "network-drone-fc" / "lib" / "tar_fc.kicad_sym"),
}


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def project_files(board_dir, name, sheet_uuid):
    pro = board_dir / f"{name}.kicad_pro"
    if not pro.exists():
        pro.write_text(json.dumps({
            "meta": {"filename": pro.name, "version": 3},
            "sheets": [[sheet_uuid, "Root"]],
            "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
            "boards": [], "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
            "text_variables": {},
        }, indent=2), encoding="utf-8")
    sym = "".join(
        f'  (lib (name "{n}")(type "KiCad")(uri "{u}.kicad_sym")(options "")(descr ""))\n'
        for n, (u, _) in LIBS.items())
    fp = "".join(
        f'  (lib (name "{n}")(type "KiCad")(uri "{u}.pretty")(options "")(descr ""))\n'
        for n, (u, _) in LIBS.items())
    (board_dir / "sym-lib-table").write_text(f"(sym_lib_table\n  (version 7)\n{sym})\n", encoding="utf-8")
    (board_dir / "fp-lib-table").write_text(f"(fp_lib_table\n  (version 7)\n{fp})\n", encoding="utf-8")


def main(board):
    sys.path.insert(0, str(HERE))
    import schgen

    board_dir = ROOT / board
    name = f"ground-station-{board}"
    sheet_uuid = SHEET_UUID.format(1 if board == "power" else 2)
    project_files(board_dir, name, sheet_uuid)

    blocks = sorted((board_dir / "blocks").glob("*.py"))
    parts, expected_single = [], set()
    for i, b in enumerate(blocks):
        mod = load(b)
        dx, dy = (i % 2) * COLUMN_PITCH, (i // 2) * ROW_PITCH
        for p in mod.PARTS:
            q = dict(p)
            q["at"] = (p["at"][0] + dx, p["at"][1] + dy)
            parts.append(q)
        expected_single |= set(getattr(mod, "EXPECTED_SINGLE", ()))
        print(f"  {b.name:28s} {len(mod.PARTS):3d} parts")

    refs = [p["ref"] for p in parts]
    dupes = {r for r in refs if refs.count(r) > 1}
    if dupes:
        print("DUPLICATE REFERENCES:", sorted(dupes))
        return 1

    combined = types.SimpleNamespace(
        TITLE=f"TAR Team 1 ground station: {board} board", DATE="2026-10-28", REV="A",
        PAPER="A1", PARTS=parts, EXTRA_LIBS=[str(p) for _, p in LIBS.values()],
        SHEET_UUID=sheet_uuid,
    )
    out = board_dir / f"{name}.kicad_sch"
    schgen.generate(combined, out)

    net = board_dir / f"{name}.net"
    r = subprocess.run([str(KICAD), "sch", "export", "netlist", "--output", str(net), str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("netlist export FAILED:", r.stdout.strip(), r.stderr.strip())
        return 1
    txt = net.read_text(encoding="utf-8")
    nets = {}
    for chunk in re.split(r"\(net \(code ", txt[txt.find("(nets"):])[1:]:
        nm = re.search(r'\(name "([^"]*)"\)', chunk).group(1).lstrip("/")
        nets[nm] = re.findall(r'\(ref "([^"]+)"\) \(pin "([^"]+)"', chunk)
    dangling = {n: v for n, v in nets.items()
                if len(v) == 1 and not n.startswith("unconnected") and n not in expected_single}
    print(f"\n{len(set(refs))} components, {len(nets)} nets")
    if dangling:
        print(f"DANGLING NETS ({len(dangling)}), each reaching only one pin:")
        for n, v in sorted(dangling.items()):
            print(f"  {n:22s} {v[0][0]}.{v[0][1]}")

    erc = board_dir / f"{name}-erc.rpt"
    subprocess.run([str(KICAD), "sch", "erc", "--severity-error", "--output", str(erc), str(out)],
                   capture_output=True, text=True)
    summary = re.search(r"\*\* ERC messages: .*", erc.read_text(encoding="utf-8"))
    print("ERC (errors only):", summary.group(0) if summary else "no summary")
    return 1 if dangling else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

"""Write lib/tar_gs.kicad_sym: the ground station symbols KiCad's own libraries do not have.

    python tools/mklib.py

Each symbol is a plain box with pins down the left and right. Pin numbers are the
part's own pad numbers, checked against its datasheet:

- TPS259470A (TI SLVSFC9C, Table 5-1, RPW package)
- VoCore2 (vocore.io/v2.html pin table; pins without a chip pin number are given
  names here and get pad numbers when the footprint is drawn)
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "lib" / "tar_gs.kicad_sym"
GRID = 2.54


def pin(kind, name, num, x, y, angle, hidden=False):
    return (
        f'\t\t\t(pin {kind} line\n\t\t\t\t(at {x:.2f} {y:.2f} {angle})\n\t\t\t\t(length 2.54)'
        + ("\n\t\t\t\t(hide yes)" if hidden else "")
        + f'\n\t\t\t\t(name "{name}"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)'
        + f'\n\t\t\t\t(number "{num}"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)'
    )


def prop(name, value, y, hide):
    return (
        f'\t\t(property "{name}" "{value}"\n\t\t\t(at 0 {y:.2f} 0)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)'
        + ("\n\t\t\t\t(hide yes)" if hide else "")
        + "\n\t\t\t)\n\t\t)"
    )


def box(name, ref, footprint, desc, datasheet, left, right, width=20.32):
    """left/right: lists of (kind, name, number); None leaves a gap."""
    rows = max(len(left), len(right))
    top = (rows - 1) * GRID / 2 + GRID
    half = width / 2
    pins = []
    for side, items in ((-1, left), (1, right)):
        for i, p in enumerate(items):
            if p is None:
                continue
            kind, pname, num = p
            y = (rows - 1) * GRID / 2 - i * GRID
            x = side * (half + 2.54)
            pins.append(pin(kind, pname, num, x, y, 0 if side < 0 else 180))
    body = (
        f'\t\t(symbol "{name}_0_1"\n\t\t\t(rectangle\n\t\t\t\t(start {-half:.2f} {top:.2f})\n\t\t\t\t(end {half:.2f} {-top:.2f})\n'
        "\t\t\t\t(stroke\n\t\t\t\t\t(width 0.254)\n\t\t\t\t\t(type default)\n\t\t\t\t)\n\t\t\t\t(fill\n\t\t\t\t\t(type background)\n\t\t\t\t)\n\t\t\t)\n\t\t)"
    )
    return (
        f'\t(symbol "{name}"\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n'
        + prop("Reference", ref, top + 1.27, False) + "\n"
        + prop("Value", name, -top - 1.27, False) + "\n"
        + prop("Footprint", footprint, -top - 3.81, True) + "\n"
        + prop("Datasheet", datasheet, -top - 6.35, True) + "\n"
        + prop("Description", desc, -top - 8.89, True) + "\n"
        + body + "\n"
        + f'\t\t(symbol "{name}_1_1"\n' + "\n".join(pins) + "\n\t\t)\n\t)"
    )


TPS = box(
    "TPS259470ARPW", "U", "tar_gs:Texas_RPW0010A_VQFN-HR-10_2x2mm",
    "2.7-23 V, 5.5 A eFuse, adjustable OVLO, active current limit, auto-retry, FLT output, ILM current monitor",
    "https://www.ti.com/lit/ds/symlink/tps25947.pdf",
    left=[("power_in", "IN", "5"), ("input", "EN/UVLO", "1"), ("input", "OVLO", "2"),
          ("passive", "DVDT", "7"), ("passive", "ITIMER", "10"), ("power_in", "GND", "8")],
    right=[("power_out", "OUT", "6"), ("open_collector", "~{FLT}", "4"), ("open_collector", "AUXOFF", "3"),
           ("output", "ILM", "9")],
)

VOCORE = box(
    "VoCore2", "M", "tar_gs:VoCore2",
    "VoCore2 MT7628 Linux Wi-Fi module, 25.6 mm castellated; power and GND pins are named, chip pins use their MT7628 numbers",
    "https://vocore.io/v2.html",
    left=[("power_in", "+5.0VI", "5VA"), ("power_in", "+5.0VI", "5VB"), None,
          ("input", "RXD1", "148"), ("output", "TXD1", "147"), None,
          ("input", "RXD2", "40"), ("output", "TXD2", "42"), None,
          ("input", "RST", "138"), None,
          ("power_in", "GND", "GA"), ("power_in", "GND", "GB"), ("power_in", "GND", "GC"), ("power_in", "GND", "GD")],
    right=[("bidirectional", "P0TP", "35"), ("bidirectional", "P0TN", "36"),
           ("bidirectional", "P0RP", "33"), ("bidirectional", "P0RN", "34"), None,
           ("output", "TXD0", "30"), ("input", "RXD0", "31"), None,
           ("power_out", "+3.3VO", "3V3")],
    width=25.4,
)

OUT.write_text(
    "(kicad_symbol_lib\n\t(version 20241209)\n\t(generator \"mklib\")\n\t(generator_version \"9.0\")\n"
    + TPS + "\n" + VOCORE + "\n)\n",
    encoding="utf-8",
)
print("wrote", OUT)

"""check.py: checks the electrical rules check cannot make, on both boards.

    python tools/check.py

1. Every footprint named in the schematics exists in KiCad's libraries or the
   project's (the two still to be drawn are listed, not failed).
2. The power board's J7 and the main board's J3 carry the same net on every pin.
3. On the main board, each ESP32 pin has one job, the dock current inputs are on
   ADC1, and no strapping pin is used.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FP_DIRS = [Path(r"C:\Program Files\KiCad\9.0\share\kicad\footprints"),
           ROOT.parent / "network-drone-fc" / "lib", ROOT / "lib"]
TO_DRAW = {"tar_gs:Texas_RPW0010A_VQFN-HR-10_2x2mm", "tar_gs:VoCore2"}


def netlist(board):
    txt = (ROOT / board / f"ground-station-{board}.net").read_text(encoding="utf-8")
    comps = dict(re.findall(r'\(comp \(ref "([^"]+)"\)[\s\S]*?\(footprint "([^"]*)"\)', txt))
    pins = {}
    for chunk in re.split(r"\(net \(code ", txt[txt.find("(nets"):])[1:]:
        nm = re.search(r'\(name "([^"]*)"\)', chunk).group(1).lstrip("/")
        for ref, pin in re.findall(r'\(ref "([^"]+)"\) \(pin "([^"]+)"', chunk):
            pins[(ref, pin)] = nm
    return comps, pins


def fp_exists(fp):
    lib, name = fp.split(":", 1)
    for d in FP_DIRS:
        if (d / f"{lib}.pretty" / f"{name}.kicad_mod").exists():
            return True
    return False


fails = 0
nets = {}
for board in ("power", "main"):
    comps, pins = netlist(board)
    nets[board] = pins
    missing = sorted({fp for fp in comps.values() if fp and not fp_exists(fp)})
    todo = [m for m in missing if m in TO_DRAW]
    bad = [m for m in missing if m not in TO_DRAW]
    print(f"{board}: {len(comps)} parts, footprints missing: {bad or 'none'}; still to draw: {todo or 'none'}")
    fails += len(bad)

link_p = {int(p): n for (r, p), n in nets["power"].items() if r == "J7"}
link_m = {int(p): n for (r, p), n in nets["main"].items() if r == "J3"}
diff = [(p, link_p.get(p), link_m.get(p)) for p in range(1, 21) if link_p.get(p) != link_m.get(p)]
print("link J7 <-> J3:", "all 20 pins match" if not diff else diff)
fails += len(diff)

esp = {int(p): n for (r, p), n in nets["main"].items() if r == "U1"}
# chip pin -> GPIO for the pins this check cares about (ESP32-S3 datasheet, QFN56)
gpio = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4, 10: 5, 11: 6, 12: 7, 13: 8, 14: 9, 15: 10, 16: 11, 17: 12, 18: 13,
        19: 14, 21: 15, 22: 16, 23: 17, 24: 18, 27: 21, 38: 33, 39: 34, 40: 35, 41: 36, 44: 39, 45: 40,
        49: 43, 50: 44, 51: 45, 52: 46}
signal = {p: n for p, n in esp.items() if p in gpio and not n.startswith("unconnected")}
dup = {n for n in signal.values() if list(signal.values()).count(n) > 1}
straps = [gpio[p] for p, n in signal.items() if gpio[p] in (3, 45, 46)]
adc1 = all(1 <= gpio[p] <= 10 for p, n in signal.items() if n.endswith("_ILM_A"))
print(f"ESP32: {len(signal)} GPIOs used; duplicates: {dup or 'none'}; strapping pins used: {straps or 'none'} "
      f"(GPIO0 is BOOT on purpose); dock current inputs on ADC1: {adc1}")
fails += len(dup) + len(straps) + (not adc1)
print("FAILED" if fails else "all checks pass")

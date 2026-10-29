"""Block 3: two 5.3 V bucks for the docks (LMR33630A, 400 kHz, 3 A each).

Each buck feeds two docks. Four chargers at their 0.925 A input limit draw 3.7 A
in all, so each buck carries about 1.85 A, and 3 A if both of its docks sit at the
1.5 A switch limit. Two bucks also mean one failing takes down only two docks.

The output is 5.3 V rather than 5.0 V to cover the loss in the spring contacts at
about 1 A, while staying under the drone eFuse's 6.0 V cut-off and the dock
switches' own 6.1 V cut-off.

Component values are TI's for 5 V at 400 kHz (SNVSAN3F, Table 9-2: L 8 uH, COUT
4 x 22 uF, RFBT 100k, CIN 10 uF + 220 nF, CBOOT 100 nF, CVCC 1 uF). RFBB is 23.2k
instead of 24.9k: VOUT = 1.0 V x (1 + 100k / 23.2k) = 5.31 V. Pinout: Table 6-1,
DDA package.
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"


def buck(n, ref_u, refs, x0, y0):
    out, sw, boot, fb, vcc = f"+5V3_{n}", f"SW_{n}", f"BOOT_{n}", f"FB_{n}", f"VCC_{n}"
    rc, rl, ra, rb, ci1, ci2, cb, cv, co1, co2, co3, co4 = refs
    return [
        dict(ref=ref_u, lib="Regulator_Switching:LMR33630ADDA", value="LMR33630ADDAR",
             fp="Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias", at=(x0 + 40, y0),
             nets={1: "GND", 2: "VIN_SYS", 3: "VIN_SYS", 5: fb, 6: vcc, 7: boot, 8: sw, 9: "GND"},
             nc=[4]),
        dict(ref=ci1, lib="Device:C", value="10uF 50V", fp="Capacitor_SMD:C_1210_3225Metric",
             at=(x0, y0), nets={1: "VIN_SYS", 2: "GND"}),
        dict(ref=ci2, lib="Device:C", value="220nF 50V", fp="Capacitor_SMD:C_0603_1608Metric",
             at=(x0 + 10, y0), nets={1: "VIN_SYS", 2: "GND"}),
        dict(ref=cb, lib="Device:C", value="100nF 25V", fp=C0402, at=(x0 + 60, y0 - 20),
             nets={1: boot, 2: sw}),
        dict(ref=cv, lib="Device:C", value="1uF 16V", fp=C0402, at=(x0 + 20, y0 + 20),
             nets={1: vcc, 2: "GND"}),
        # Coilcraft XAL6060-822ME: 8.2 uH, saturation well above the 3 A limit.
        dict(ref=rl, lib="Device:L", value="8.2uH XAL6060-822ME",
             fp="Inductor_SMD:L_Coilcraft_XAL6060-XXX", at=(x0 + 75, y0), nets={1: sw, 2: out}),
        dict(ref=ra, lib="Device:R", value="100k 1%", fp=R, at=(x0 + 90, y0 + 10), nets={1: out, 2: fb}),
        dict(ref=rb, lib="Device:R", value="23.2k 1%", fp=R, at=(x0 + 90, y0 + 25), nets={1: fb, 2: "GND"}),
        dict(ref=co1, lib="Device:C", value="22uF 16V", fp="Capacitor_SMD:C_1210_3225Metric",
             at=(x0 + 100, y0), nets={1: out, 2: "GND"}),
        dict(ref=co2, lib="Device:C", value="22uF 16V", fp="Capacitor_SMD:C_1210_3225Metric",
             at=(x0 + 108, y0), nets={1: out, 2: "GND"}),
        dict(ref=co3, lib="Device:C", value="22uF 16V", fp="Capacitor_SMD:C_1210_3225Metric",
             at=(x0 + 116, y0), nets={1: out, 2: "GND"}),
        dict(ref=co4, lib="Device:C", value="22uF 16V", fp="Capacitor_SMD:C_1210_3225Metric",
             at=(x0 + 124, y0), nets={1: out, 2: "GND"}),
        dict(ref=f"#FLG1{n}", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(x0 + 100, y0 - 15), nets={1: out}),
    ]


# EN (pin 3) tied to VIN: always on whenever there is input power. PG (pin 4) is
# not used.
PARTS = (
    buck("A", "U3", ["-", "L1", "R10", "R11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19"], 20, 50)
    + buck("B", "U4", ["-", "L2", "R12", "R13", "C20", "C21", "C22", "C23", "C24", "C25", "C26", "C27"], 20, 130)
)

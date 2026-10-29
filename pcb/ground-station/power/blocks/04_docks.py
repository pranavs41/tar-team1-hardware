"""Block 4: four dock outputs, each through its own TPS259470A eFuse.

Each dock's walls are bare metal, so a short across them is expected. The eFuse
limits the current to 1.5 A, retries by itself after a fault (the "A" version),
and keeps one dock's fault from touching the others (TI SLVSFC9C).

Per dock n:
  RILM 2.21k sets the limit: ILIM = 3334 / RILM = 1.51 A (Equation 7). The ILM pin
    voltage also reads the dock current: VILM = IOUT x RILM x 182 uA/A, so 0.37 V
    at 0.925 A and 0.61 V at the 1.5 A limit (Equation 9). DOCKn_ILM goes to the
    main board's ADC.
  EN/UVLO comes from the main board (DOCKn_EN, 3.3 V logic, threshold 1.2 V). The
    100k pull-down keeps the dock off when the main board is unplugged or booting.
  OVLO 412k / 100k from IN: cuts the dock off above 1.2 V x 5.12 = 6.14 V, in case
    a buck fails high. The drone's own eFuse cuts off at 6.0 V.
  ~FLT is open drain, low on a fault; the pull-up is on the main board.
  DVDT and ITIMER open: fastest turn-on and fastest overcurrent response.
  A TVS on each output for static on the exposed walls, and an LED showing the
  dock is powered.

Docks 1 and 2 run from buck A (+5V3_A), docks 3 and 4 from buck B (+5V3_B).
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"


def dock(n, src, refs, x0, y0):
    u, r_ilm, r_en, r_ov1, r_ov2, c_in, c_out, d_tvs, r_led, d_led, j = refs
    en, flt, ilm, out, ov = f"DOCK{n}_EN", f"DOCK{n}_FLT", f"DOCK{n}_ILM", f"DOCK{n}_OUT", f"DOCK{n}_OVLO"
    return [
        dict(ref=u, lib="tar_gs:TPS259470ARPW", value="TPS259470ARPWR",
             fp="tar_gs:Texas_RPW0010A_VQFN-HR-10_2x2mm", at=(x0 + 40, y0),
             nets={5: src, 1: en, 2: ov, 8: "GND", 6: out, 4: flt, 9: ilm},
             nc=[3, 7, 10]),
        dict(ref=c_in, lib="Device:C", value="1uF 16V", fp=C0402, at=(x0, y0), nets={1: src, 2: "GND"}),
        dict(ref=r_en, lib="Device:R", value="100k", fp=R, at=(x0 + 10, y0 + 15), nets={1: en, 2: "GND"}),
        dict(ref=r_ov1, lib="Device:R", value="412k 1%", fp=R, at=(x0 + 20, y0 + 15), nets={1: src, 2: ov}),
        dict(ref=r_ov2, lib="Device:R", value="100k 1%", fp=R, at=(x0 + 20, y0 + 25), nets={1: ov, 2: "GND"}),
        dict(ref=r_ilm, lib="Device:R", value="2.21k 1%", fp=R, at=(x0 + 60, y0 + 15), nets={1: ilm, 2: "GND"}),
        dict(ref=c_out, lib="Device:C", value="1uF 16V", fp=C0402, at=(x0 + 70, y0), nets={1: out, 2: "GND"}),
        # SMAJ6.0A: 6.0 V standoff, above the 5.3 V wall voltage.
        dict(ref=d_tvs, lib="Device:D_TVS", value="SMAJ6.0A", fp="Diode_SMD:D_SMA",
             at=(x0 + 80, y0), nets={1: out, 2: "GND"}),
        # 1.5 mA at 5.3 V.
        dict(ref=r_led, lib="Device:R", value="2.2k", fp=R, at=(x0 + 90, y0 - 10), nets={1: out, 2: f"LED_D{n}"}),
        dict(ref=d_led, lib="Device:LED", value="GREEN", fp="LED_SMD:LED_0603_1608Metric",
             at=(x0 + 90, y0 + 5), nets={1: "GND", 2: f"LED_D{n}"}),
        # JST XH, 2.5 mm, rated 3 A: a 2-wire lead to the dock's two walls.
        dict(ref=j, lib="Connector_Generic:Conn_01x02", value=f"DOCK {n}",
             fp="Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical", at=(x0 + 105, y0),
             nets={1: out, 2: "GND"}),
    ]


PARTS = (
    dock(1, "+5V3_A", ["U5", "R14", "R15", "R16", "R17", "C28", "C29", "D5", "R18", "D6", "J3"], 20, 40)
    + dock(2, "+5V3_A", ["U6", "R19", "R20", "R21", "R22", "C30", "C31", "D7", "R23", "D8", "J4"], 20, 80)
    + dock(3, "+5V3_B", ["U7", "R24", "R25", "R26", "R27", "C32", "C33", "D9", "R28", "D10", "J5"], 20, 120)
    + dock(4, "+5V3_B", ["U8", "R29", "R30", "R31", "R32", "C34", "C35", "D11", "R33", "D12", "J6"], 20, 160)
)

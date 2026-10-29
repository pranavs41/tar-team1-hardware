"""Block 5: the 20-pin link to the power board, dock signal conditioning, mounting holes.

J3 matches the power board's J7 pin for pin (see power/blocks/05_link.py).

  DOCKn_EN   straight from the ESP32. The power board holds them low with 100k
             until the ESP32 drives them.
  DOCKn_FLT  open drain from each eFuse, pulled up to +3V3 here with 10k.
  DOCKn_ILM  the eFuse's current monitor voltage (0 to about 0.6 V), through
             1k and 100 nF (a 0.1 ms filter against ribbon-cable pickup) to the
             ESP32's ADC1. Read it with the ADC's 0 dB range.
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"

PARTS = [
    dict(ref="J3", lib="Connector_Generic:Conn_02x10_Odd_Even", value="LINK",
         fp="Connector_IDC:IDC-Header_2x10_P2.54mm_Vertical", at=(40, 80),
         nets={1: "VIN_SYS", 2: "VIN_SYS", 3: "GND", 4: "GND",
               5: "DOCK1_EN", 6: "DOCK2_EN", 7: "DOCK3_EN", 8: "DOCK4_EN",
               9: "DOCK1_FLT", 10: "DOCK2_FLT", 11: "DOCK3_FLT", 12: "DOCK4_FLT",
               13: "DOCK1_ILM", 14: "DOCK2_ILM", 15: "DOCK3_ILM", 16: "DOCK4_ILM",
               17: "GND", 18: "GND", 19: "GND", 20: "GND"}),
]
for n in range(1, 5):
    PARTS += [
        dict(ref=f"R{49 + n}", lib="Device:R", value="10k", fp=R, at=(90 + 12 * n, 50),
             nets={1: "+3V3", 2: f"DOCK{n}_FLT"}),
        dict(ref=f"R{53 + n}", lib="Device:R", value="1k", fp=R, at=(90 + 12 * n, 90),
             nets={1: f"DOCK{n}_ILM", 2: f"DOCK{n}_ILM_A"}),
        dict(ref=f"C{59 + n}", lib="Device:C", value="100nF", fp=C0402, at=(90 + 12 * n, 110),
             nets={1: f"DOCK{n}_ILM_A", 2: "GND"}),
    ]
PARTS += [
    dict(ref=f"H{i}", lib="Mechanical:MountingHole", value="M3", fp="MountingHole:MountingHole_3.2mm_M3",
         at=(170 + 10 * i, 40), nets={})
    for i in range(1, 5)
]

"""Block 1: main board power.

VIN_SYS (12 to 20 V) arrives from the power board on the link (block 5). The 5 V
buck, the 3.3 V regulator and their parts are the flight controller's, checked
there (docs/circuits/03-power.md), with input parts rated for 20 V instead of a
2S battery:

  +5V       AP63205 buck, 2 A: the VoCore2 (up to 0.5 A) and the three regulators
  +3V3      TLV75733, 1 A: the ESP32-S3
  +3V3_F9P  TPS7A2033, 300 mA, low noise: the ZED-F9P and its antenna
  +3V3_M10  TPS7A2033: the MAX-M10S

Worst case on +5V is about 1.1 A. The ZED-F9P manual asks for a clean 3.3 V LDO
with no inductor or ferrite between it and the module (UBX-18010802, 4.2), so each
receiver has its own.

USB-C (block 2) also feeds +5V through D1, so the ESP32 can be flashed with the
power board unplugged. That is not enough to run the VoCore2.
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"

PARTS = [
    dict(ref="C1", lib="Device:C", value="10uF 50V", fp="Capacitor_SMD:C_1210_3225Metric",
         at=(20, 60), nets={1: "VIN_SYS", 2: "GND"}),
    dict(ref="C2", lib="Device:C", value="100nF 50V", fp=C0402, at=(30, 60), nets={1: "VIN_SYS", 2: "GND"}),
    # EN divider as on the flight controller: the buck starts above about 5.9 V.
    # At 20 V in, EN sits at 3.8 V.
    dict(ref="R1", lib="Device:R", value="143k 1%", fp=R, at=(40, 75), nets={1: "VIN_SYS", 2: "BUCK_EN"}),
    dict(ref="R2", lib="Device:R", value="34k 1%", fp=R, at=(40, 85), nets={1: "BUCK_EN", 2: "GND"}),
    dict(ref="U3", lib="tar_fc:AP63205WU-7", value="AP63205WU-7",
         fp="tar_fc:TSOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL", at=(60, 60),
         nets={1: "+5V", 2: "BUCK_EN", 3: "VIN_SYS", 4: "GND", 5: "BUCK_SW", 6: "BUCK_BST"}),
    dict(ref="C3", lib="Device:C", value="100nF", fp=C0402, at=(75, 45), nets={1: "BUCK_BST", 2: "BUCK_SW"}),
    # Samsung CIGW252010EH4R7MNE, 4.7 uH, 2.2 A saturation. Peak current at 20 V in
    # and 1.2 A out is about 1.6 A.
    dict(ref="L1", lib="Device:L", value="4.7uH CIGW252010EH4R7MNE",
         fp="Inductor_SMD:L_1008_2520Metric", at=(85, 60), nets={1: "BUCK_SW", 2: "+5V"}),
    dict(ref="C4", lib="Device:C", value="22uF 16V", fp="Capacitor_SMD:C_0805_2012Metric",
         at=(100, 60), nets={1: "+5V", 2: "GND"}),
    dict(ref="C5", lib="Device:C", value="22uF 16V", fp="Capacitor_SMD:C_0805_2012Metric",
         at=(108, 60), nets={1: "+5V", 2: "GND"}),

    dict(ref="U4", lib="tar_fc:TLV75733PDRVR", value="TLV75733PDRVR",
         fp="tar_fc:TDFN-6_L2.0-W2.0-P0.65-TL-EP", at=(140, 60),
         nets={1: "+3V3", 3: "GND", 4: "+5V", 6: "+5V", 7: "GND"}, nc=[2, 5]),
    dict(ref="C6", lib="Device:C", value="1uF", fp=C0402, at=(125, 75), nets={1: "+5V", 2: "GND"}),
    dict(ref="C7", lib="Device:C", value="1uF", fp=C0402, at=(155, 75), nets={1: "+3V3", 2: "GND"}),

    dict(ref="U5", lib="tar_fc:TPS7A2033PDBVR", value="TPS7A2033PDBVR",
         fp="tar_fc:SOT-23-5_L2.9-W1.6-P0.95-LS2.8-BR", at=(140, 100),
         nets={1: "+5V", 2: "GND", 3: "+5V", 5: "+3V3_F9P"}, nc=[4]),
    dict(ref="C8", lib="Device:C", value="1uF", fp=C0402, at=(125, 115), nets={1: "+5V", 2: "GND"}),
    dict(ref="C9", lib="Device:C", value="1uF", fp=C0402, at=(155, 115), nets={1: "+3V3_F9P", 2: "GND"}),

    dict(ref="U6", lib="tar_fc:TPS7A2033PDBVR", value="TPS7A2033PDBVR",
         fp="tar_fc:SOT-23-5_L2.9-W1.6-P0.95-LS2.8-BR", at=(140, 140),
         nets={1: "+5V", 2: "GND", 3: "+5V", 5: "+3V3_M10"}, nc=[4]),
    dict(ref="C10", lib="Device:C", value="1uF", fp=C0402, at=(125, 155), nets={1: "+5V", 2: "GND"}),
    dict(ref="C11", lib="Device:C", value="1uF", fp=C0402, at=(155, 155), nets={1: "+3V3_M10", 2: "GND"}),

    # Power LED on +3V3, as on the flight controller.
    dict(ref="R3", lib="Device:R", value="1k", fp=R, at=(180, 60), nets={1: "+3V3", 2: "LED_PWR"}),
    dict(ref="D2", lib="Device:LED", value="RED", fp="LED_SMD:LED_0603_1608Metric",
         at=(180, 75), nets={1: "GND", 2: "LED_PWR"}),

    dict(ref="#FLG01", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(20, 40), nets={1: "VIN_SYS"}),
    dict(ref="#FLG02", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(30, 40), nets={1: "GND"}),
    dict(ref="#FLG03", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(100, 40), nets={1: "+5V"}),
    dict(ref="#FLG07", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(155, 40), nets={1: "+3V3"}),
]

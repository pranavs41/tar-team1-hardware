"""Block 2: 12 V barrel jack through an ideal diode, and the VIN_SYS bulk capacitance.

The LM74700 drives Q1 as a diode with about 20 mV of drop: current flows from the
jack into VIN_SYS but never back out, so the jack and the USB-C input can both be
plugged in and whichever is higher runs the station. A jack plug wired the wrong
way round is blocked (the LM74700 is rated to -65 V). Pinout: TI SNOSD17G
Table 5-1, DBV package.

Nets:
  JACK_IN  the jack's centre pin, 12 V nominal, up to 20 V
  VIN_SYS  the joined input rail
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"

PARTS = [
    # Wuerth 694106106102, 2.0 x 5.5 mm. Pin 1 is the centre pin. Pad 3 (the
    # switch) is not used.
    dict(ref="J2", lib="Connector:Barrel_Jack", value="694106106102",
         fp="Connector_BarrelJack:BarrelJack_Wuerth_694106106102_2.0x5.5mm", at=(30, 60),
         nets={1: "JACK_IN", 2: "GND"}),
    # Bidirectional, so a reversed plug does not forward-bias it and short the
    # adapter. Standoff 22 V for a 20 V adapter; clamps at 35.5 V, under the
    # LMR33630's 36 V input limit.
    dict(ref="D3", lib="Device:D_TVS", value="SMBJ22CA", fp="Diode_SMD:D_SMB",
         at=(50, 75), nets={1: "JACK_IN", 2: "GND"}),
    dict(ref="C8", lib="Device:C", value="1uF 50V", fp="Capacitor_SMD:C_0805_2012Metric",
         at=(60, 75), nets={1: "JACK_IN", 2: "GND"}),

    dict(ref="U2", lib="Power_Management:LM74700", value="LM74700QDBVRQ1",
         fp="Package_TO_SOT_SMD:SOT-23-6", at=(100, 80),
         nets={1: "JK_VCAP", 2: "GND", 3: "JACK_IN", 4: "VIN_SYS", 5: "JK_GATE", 6: "JACK_IN"}),
    # Charge pump capacitor from VCAP to ANODE, 0.1 uF (datasheet conditions).
    dict(ref="C9", lib="Device:C", value="100nF 25V", fp=C0402, at=(85, 95), nets={1: "JK_VCAP", 2: "JACK_IN"}),
    # Infineon 60 V, 2.8 mOhm. Source to the jack (ANODE), drain to VIN_SYS (CATHODE).
    dict(ref="Q1", lib="Transistor_FET:BSC028N06LS3", value="BSC028N06LS3G",
         fp="Package_TO_SOT_SMD:TDSON-8-1", at=(100, 55),
         nets={1: "JACK_IN", 2: "JACK_IN", 3: "JACK_IN", 4: "JK_GATE", 5: "VIN_SYS"}),

    # VIN_SYS bulk. This also gives the TPS25730 the 47 uF or more it wants on PPHV.
    dict(ref="C10", lib="Device:C_Polarized", value="100uF 35V polymer",
         fp="Capacitor_SMD:CP_Elec_8x10", at=(140, 60), nets={1: "VIN_SYS", 2: "GND"}),
    dict(ref="C11", lib="Device:C", value="10uF 50V", fp="Capacitor_SMD:C_1210_3225Metric",
         at=(150, 60), nets={1: "VIN_SYS", 2: "GND"}),

    # Input power LED: 1.8 mA at 20 V, 1 mA at 12 V.
    dict(ref="R9", lib="Device:R", value="10k", fp="Resistor_SMD:R_0603_1608Metric",
         at=(170, 50), nets={1: "VIN_SYS", 2: "LED_VIN"}),
    dict(ref="D4", lib="Device:LED", value="GREEN", fp="LED_SMD:LED_0603_1608Metric",
         at=(170, 65), nets={1: "GND", 2: "LED_VIN"}),
    dict(ref="#FLG04", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(40, 45), nets={1: "JACK_IN"}),
    dict(ref="#FLG05", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(140, 45), nets={1: "VIN_SYS"}),
]

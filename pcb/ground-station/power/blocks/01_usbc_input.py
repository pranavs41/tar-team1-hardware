"""Block 1: USB-C power delivery input (TPS25730D).

The TPS25730D asks the charger for 12 to 20 V (ADCIN1 = 12 V minimum, ADCIN2 = 20 V
maximum) at 1.5 A operating, 3 A maximum (ADCIN3 = 1, ADCIN4 = 5), all set with
resistors, so it needs no programming (TI SLVSGP9, Tables 8-1 and 8-3 to 8-6).
Its built-in switch blocks current flowing back out of the port, so PPHV joins the
barrel jack's path directly on VIN_SYS.

Values follow TI's example schematic (Figure 9-3) and Recommended Capacitance
(section 6.4). The surge diode D2 and TVS D1 follow sections 6.1 and 8.5.

Nets:
  VBUS_C   the USB-C VBUS, 5 to 20 V
  VIN_SYS  the station's input rail after both inputs join, 12 to 20 V
  PD_3V3, PD_1V5   the controller's own LDO outputs (no external load)
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"

PARTS = [
    # GCT USB4105-GF-A, the same socket and footprint as the flight controller's J2.
    # Only VBUS, GND and the two CC pins are used.
    dict(ref="J1", lib="tar_fc:TYPE-C16PIN2MD", value="USB4105-GF-A",
         fp="tar_fc:USB-C-SMD_TYPE-C-16PIN-2MD-073", at=(30, 60),
         nets={"A4B9": "VBUS_C", "B4A9": "VBUS_C", "A1B12": "GND", "B1A12": "GND",
               "13": "GND", "14": "GND", "A5": "CC1", "B5": "CC2"},
         nc=["A6", "A7", "A8", "B6", "B7", "B8"]),

    # TVS2200: 22 V standoff, breaks down between the 21 V a 20 V source may reach
    # and the TPS25730's 28 V absolute maximum, as TI asks in section 6.1.
    dict(ref="D1", lib="Power_Protection:TVS2200DRV", value="TVS2200DRVR",
         fp="Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm", at=(55, 75),
         by_name={"IN": "VBUS_C", "GND": "GND"}),
    # Schottky from VBUS to ground against the negative kick of a cable unplugged
    # under load (section 8.5).
    dict(ref="D2", lib="Device:D_Schottky", value="B340A-13-F",
         fp="Diode_SMD:D_SMA", at=(70, 75), nets={1: "VBUS_C", 2: "GND"}),

    dict(ref="U1", lib="Interface_USB:TPS25730D", value="TPS25730DREFR",
         fp="Package_DFN_QFN:Texas_REF0038A_WQFN-38-2EP_6x4mm_P0.4", at=(120, 70),
         nets={1: "PD_3V3", 2: "PD_ADC1", 3: "PD_3V3", 4: "PD_1V5", 5: "PD_ADC3",
               7: "PD_1V5", 8: "GND", 9: "GND",
               11: "GND", 12: "GND", 14: "GND", 16: "GND", 17: "GND", 31: "GND", 34: "GND", 39: "GND",
               15: "PD_DRAIN", 30: "PD_DRAIN", 40: "PD_DRAIN",
               18: "PD_FAULT_IN", 20: "VIN_SYS", 23: "VBUS_C", 32: "VBUS_C",
               26: "PD_RSV26", 27: "PD_RSV27", 36: "PD_RSV36",
               28: "CC1", 29: "CC2", 38: "PD_VIN3V3"},
         # status outputs, all open drain, not used
         nc=[6, 10, 13, 19, 37]),

    # VBUS: 1 to 10 uF rated 25 V; 4.7 uF at 50 V keeps most of it at 20 V.
    dict(ref="C1", lib="Device:C", value="4.7uF 50V", fp="Capacitor_SMD:C_1206_3216Metric",
         at=(80, 50), nets={1: "VBUS_C", 2: "GND"}),
    dict(ref="C2", lib="Device:C", value="10nF 50V", fp=C0402, at=(88, 50), nets={1: "VBUS_C", 2: "GND"}),
    # CC filter: 200 to 480 pF.
    dict(ref="C3", lib="Device:C", value="330pF 50V", fp=C0402, at=(160, 50), nets={1: "CC1", 2: "GND"}),
    dict(ref="C4", lib="Device:C", value="330pF 50V", fp=C0402, at=(168, 50), nets={1: "CC2", 2: "GND"}),
    # LDO_3V3 5 to 25 uF, LDO_1V5 4.5 to 12 uF, VIN_3V3 5 uF or more.
    dict(ref="C5", lib="Device:C", value="10uF 10V", fp="Capacitor_SMD:C_0603_1608Metric",
         at=(80, 100), nets={1: "PD_3V3", 2: "GND"}),
    dict(ref="C6", lib="Device:C", value="4.7uF 10V", fp="Capacitor_SMD:C_0603_1608Metric",
         at=(88, 100), nets={1: "PD_1V5", 2: "GND"}),
    # VIN_3V3 has no supply on this board, so the controller always runs from VBUS
    # (TI's "dead battery" start-up), which is the stand-alone mode.
    dict(ref="C7", lib="Device:C", value="10uF 10V", fp="Capacitor_SMD:C_0603_1608Metric",
         at=(96, 100), nets={1: "PD_VIN3V3", 2: "GND"}),

    # ADCIN1 = decoded 2 (12 V minimum): divider 0.107 against a 0.1074 target.
    dict(ref="R1", lib="Device:R", value="100k 1%", fp=R, at=(150, 100), nets={1: "PD_3V3", 2: "PD_ADC1"}),
    dict(ref="R2", lib="Device:R", value="12k 1%", fp=R, at=(150, 110), nets={1: "PD_ADC1", 2: "GND"}),
    # ADCIN3 = decoded 1: divider 0.0475 against a 0.0475 target. With ADCIN4 tied
    # to LDO_1V5 (decoded 5) this asks for 1.5 A operating, 3 A maximum.
    dict(ref="R3", lib="Device:R", value="100k 1%", fp=R, at=(160, 100), nets={1: "PD_3V3", 2: "PD_ADC3"}),
    dict(ref="R4", lib="Device:R", value="4.99k 1%", fp=R, at=(160, 110), nets={1: "PD_ADC3", 2: "GND"}),
    # FAULT_IN high = no fault.
    dict(ref="R5", lib="Device:R", value="10k", fp=R, at=(170, 100), nets={1: "PD_3V3", 2: "PD_FAULT_IN"}),
    # Reserved pins 26, 27, 36 to GND through 10k, as in TI's example.
    dict(ref="R6", lib="Device:R", value="10k", fp=R, at=(180, 100), nets={1: "PD_RSV26", 2: "GND"}),
    dict(ref="R7", lib="Device:R", value="10k", fp=R, at=(188, 100), nets={1: "PD_RSV27", 2: "GND"}),
    dict(ref="R8", lib="Device:R", value="10k", fp=R, at=(196, 100), nets={1: "PD_RSV36", 2: "GND"}),
]

PWR = dict(lib="power:PWR_FLAG", value="PWR_FLAG", fp="")
PARTS += [
    dict(PWR, ref="#FLG01", at=(40, 40), nets={1: "VBUS_C"}),
    dict(PWR, ref="#FLG02", at=(40, 120), nets={1: "GND"}),
    # VIN_3V3 is left without a supply on purpose (see C7), so it is flagged here
    # to tell the rules check that.
    dict(PWR, ref="#FLG03", at=(100, 120), nets={1: "PD_VIN3V3"}),
]

# PD_DRAIN joins the controller's three DRAIN pins to each other only; the copper
# spreads heat from the internal switch.
EXPECTED_SINGLE = set()

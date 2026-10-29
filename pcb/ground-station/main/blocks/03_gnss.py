"""Block 3: ZED-F9P RTK base and the MAX-M10S reference receiver.

ZED-F9P (u-blox UBX-21044850 Table 12 for pins, UBX-18010802 for integration):
  - VCC on its own clean LDO (+3V3_F9P), 10 uF and 100 nF at the pins.
  - V_BCKP tied to VCC with 2.2 uF: no backup battery, so it cold-starts at power
    up, which a base surveying in each session does anyway (section 4.2.2).
  - V_USB to GND and the USB pins open, since USB is not used (section 4.2).
  - D_SEL open selects UART on pins 42 and 43. UART1 to the ESP32 carries the
    survey-in setup and the RTCM corrections out.
  - UART2 (pins 26, 27), the correction port, comes out on J8 for an external radio
    or a laptop.
  - Active survey antenna on an SMA. It is powered from VCC_RF through 10 ohm, a
    ferrite bead and a 47 nH bias inductor, with 100 nF filtering, exactly the
    parts in Table 42 (section 4.4.1.3).
  - TIMEPULSE drives an LED (4 mA capable): it blinks once a second with a fix.
  - RESET_N to the ESP32 (driven open drain only); SAFEBOOT_N to a test pad.
  - Antenna supervisor pins, I2C, TX_READY, EXTINT and RTK_STAT are not used.

MAX-M10S: the flight controller's block (docs/circuits/04-sensors.md), on its own
LDO. It sits beside the F9P's antenna and is the same receiver the drones carry, so
the station can measure the error that receiver sees and send it to the drones.
Passive antenna on a U.FL; fit L5 and use an active antenna if wanted.
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"

F9P_GND = [1, 3, 12, 14, 32, 37, 41, 48, 55]
F9P_RESERVED = [8, 9, 10, 11, 13, 15, 16, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30, 31, 35, 52, 54]

PARTS = [
    dict(ref="U7", lib="RF_GPS:ZED-F9P", value="ZED-F9P-04B", fp="RF_GPS:ublox_ZED", at=(100, 90),
         nets={**{p: "GND" for p in F9P_GND},
               2: "F9P_RF", 7: "F9P_VCC_RF", 33: "+3V3_F9P", 34: "+3V3_F9P", 36: "+3V3_F9P",
               38: "GND", 42: "F9P_TXD", 43: "F9P_RXD", 26: "F9P_RXD2", 27: "F9P_TXD2",
               49: "F9P_RESET_N", 50: "F9P_SAFEBOOT_N", 53: "F9P_TP"},
         nc=F9P_RESERVED + [4, 5, 6, 19, 20, 39, 40, 44, 45, 46, 47, 51]),
    dict(ref="C40", lib="Device:C", value="10uF 6.3V", fp=C0603, at=(60, 60), nets={1: "+3V3_F9P", 2: "GND"}),
    dict(ref="C41", lib="Device:C", value="100nF", fp=C0402, at=(68, 60), nets={1: "+3V3_F9P", 2: "GND"}),
    dict(ref="C42", lib="Device:C", value="2.2uF", fp=C0402, at=(76, 60), nets={1: "+3V3_F9P", 2: "GND"}),

    # Antenna bias (UBX-18010802 Figure 45, Table 42).
    dict(ref="R30", lib="Device:R", value="10", fp=R, at=(150, 40), nets={1: "F9P_VCC_RF", 2: "F9P_ANT_PWR"}),
    dict(ref="C43", lib="Device:C", value="100nF 16V", fp=C0402, at=(160, 55), nets={1: "F9P_ANT_PWR", 2: "GND"}),
    dict(ref="FB1", lib="Device:FerriteBead", value="BLM15HB121SH1", fp="Inductor_SMD:L_0402_1005Metric",
         at=(170, 40), nets={1: "F9P_ANT_PWR", 2: "F9P_ANT_FB"}),
    dict(ref="L4", lib="Device:L", value="47nH LQG15HS47NJ02", fp="Inductor_SMD:L_0402_1005Metric",
         at=(185, 40), nets={1: "F9P_ANT_FB", 2: "F9P_RF"}),
    # Edge-mount SMA for the survey antenna cable.
    dict(ref="J4", lib="Connector:Conn_Coaxial", value="SMA 132289",
         fp="Connector_Coaxial:SMA_Amphenol_132289_EdgeMount", at=(200, 90), nets={1: "F9P_RF", 2: "GND"}),

    # TIMEPULSE LED, 1.3 mA.
    dict(ref="R31", lib="Device:R", value="1k", fp=R, at=(150, 120), nets={1: "F9P_TP", 2: "F9P_TP_A"}),
    dict(ref="D6", lib="Device:LED", value="BLUE", fp="LED_SMD:LED_0603_1608Metric",
         at=(150, 135), nets={1: "GND", 2: "F9P_TP_A"}),
    dict(ref="TP1", lib="Connector:TestPoint", value="SAFEBOOT", fp="TestPoint:TestPoint_Pad_D1.0mm",
         at=(60, 140), nets={1: "F9P_SAFEBOOT_N"}),
    # Correction UART2 out to a header: 1 GND, 2 F9P TXD2, 3 F9P RXD2, 4 +3V3_F9P.
    dict(ref="J8", lib="Connector_Generic:Conn_01x04", value="F9P UART2",
         fp="Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical", at=(60, 170),
         nets={1: "GND", 2: "F9P_TXD2", 3: "F9P_RXD2", 4: "+3V3_F9P"}),

    # MAX-M10S, wired as on the flight controller.
    dict(ref="U8", lib="tar_fc:MAX-M10S-00B", value="MAX-M10S-00B",
         fp="tar_fc:SMD-18_L10.1-W9.7-P1.10-TL_SKG09F", at=(100, 210),
         nets={1: "GND", 2: "M10_TXD", 3: "M10_RXD", 7: "+3V3_M10", 8: "+3V3_M10",
               10: "GND", 11: "M10_RF", 12: "GND", 14: "M10_VCC_RF"},
         nc=[4, 5, 6, 9, 13, 15, 16, 17, 18]),
    dict(ref="C44", lib="Device:C", value="10uF 6.3V", fp=C0603, at=(60, 200), nets={1: "+3V3_M10", 2: "GND"}),
    dict(ref="C45", lib="Device:C", value="100nF", fp=C0402, at=(68, 200), nets={1: "+3V3_M10", 2: "GND"}),
    dict(ref="C46", lib="Device:C", value="10nF", fp=C0402, at=(150, 230), nets={1: "M10_VCC_RF", 2: "GND"}),
    dict(ref="L5", lib="Device:L", value="27nH DNP", fp="Inductor_SMD:L_0402_1005Metric",
         at=(160, 210), nets={1: "M10_VCC_RF", 2: "M10_RF"}),
    dict(ref="J5", lib="tar_fc:U.FL-R-SMT-1", value="U.FL M10",
         fp="tar_fc:RF-SMD_FRF05002-JSS103M", at=(180, 210), nets={1: "M10_RF", 2: "GND", 3: "GND"}),

    dict(ref="#FLG05", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(40, 60), nets={1: "+3V3_F9P"}),
    dict(ref="#FLG06", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(40, 200), nets={1: "+3V3_M10"}),
]

# F9P_RESET_N and the M10 and F9P UART nets end at the ESP32 in block 2.

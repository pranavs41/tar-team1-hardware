"""Block 2: ESP32-S3 station processor, USB-C, crystal, buttons, LEDs, spare header.

The processor core is the flight controller's, part for part and value for value
(docs/circuits/01-mcu.md and 02-usb.md): supply decoupling, the 2.0 nH filter on
VDD3P3, the 40 MHz crystal with its 24 nH series inductor, the CHIP_PU and GPIO0
pull-ups, the antenna pi network and U.FL, and USB-C with its ESD chip. The two
solder-pad pairs for reset and boot become real buttons, since this board has room.

What the processor does here: switch and watch the four docks (enable, fault and
current on each), read the ZED-F9P and the MAX-M10S, and pass data to and from the
VoCore2.

Pin plan (ESP32-S3 datasheet, ESP32-S3FN8, chip pin numbers):
  6, 7, 9, 10   GPIO1, 2, 4, 5    DOCK1..4_ILM_A  dock current, ADC1 channels
  11 to 14      GPIO6 to 9        DOCK1..4_FLT    dock fault inputs
  15 to 18      GPIO10 to 13      DOCK1..4_EN     dock enable outputs
  19            GPIO14            VOC_RST         VoCore2 reset, drive low to reset
  21, 22        GPIO15, 16        M10_RXD, M10_TXD  UART2 to the MAX-M10S
  23, 24        GPIO17, 18        F9P_RXD, F9P_TXD  UART1 to the ZED-F9P
  27            GPIO21            F9P_RESET_N     open drain only
  38 to 41      GPIO33 to 36      SPARE1..4       to J9
  44, 45        GPIO39, 40        LED_Y, LED_G
  49, 50        U0TXD, U0RXD      VOC_RXD1, VOC_TXD1  UART0 to the VoCore2's UART1
GPIO0, 3, 45 and 46 are strapping pins and are left alone. Pins 28 and 30 to 35
belong to the in-package flash. The ESP32's own console runs over USB.

UART0 also prints the ESP32's boot log, which lands harmlessly on the VoCore2's
UART1. The VoCore2's TXD1 (pin 147) is one of its own start-up mode pins and must
stay high at power-up; GPIO44 has no pull-down, so nothing here pulls it low.
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"


def cap(ref, value, net, at, fp=C0402):
    return dict(ref=ref, lib="Device:C", value=value, fp=fp, at=at, nets={1: net, 2: "GND"})


PARTS = [
    dict(ref="U1", lib="MCU_Espressif:ESP32-S3", value="ESP32-S3FN8",
         fp="Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP4x4mm", at=(120, 90),
         nets={1: "ESP_ANT", 2: "VDD3P3", 3: "VDD3P3", 4: "CHIP_PU", 5: "BOOT",
               6: "DOCK1_ILM_A", 7: "DOCK2_ILM_A", 9: "DOCK3_ILM_A", 10: "DOCK4_ILM_A",
               11: "DOCK1_FLT", 12: "DOCK2_FLT", 13: "DOCK3_FLT", 14: "DOCK4_FLT",
               15: "DOCK1_EN", 16: "DOCK2_EN", 17: "DOCK3_EN", 18: "DOCK4_EN",
               19: "VOC_RST", 20: "+3V3", 21: "M10_RXD", 22: "M10_TXD",
               23: "F9P_RXD", 24: "F9P_TXD", 25: "USB_DN", 26: "USB_DP", 27: "F9P_RESET_N",
               29: "VDD_SPI", 38: "SPARE1", 39: "SPARE2", 40: "SPARE3", 41: "SPARE4",
               44: "LED_Y", 45: "LED_G", 46: "+3V3", 49: "VOC_RXD1", 50: "VOC_TXD1",
               53: "XTAL_N", 54: "XTAL_P_CHIP", 55: "+3V3", 56: "+3V3", 57: "GND"},
         nc=[8, 28, 30, 31, 32, 33, 34, 35, 36, 37, 42, 43, 47, 48, 51, 52]),

    # VDD3P3 (radio power amplifier): 2.0 nH from +3V3, 0.1 uF at the pins, and a
    # 10 uF reservoir on the +3V3 side.
    dict(ref="L2", lib="Device:L", value="2.0nH", fp="Inductor_SMD:L_0402_1005Metric",
         at=(80, 50), nets={1: "+3V3", 2: "VDD3P3"}),
    cap("C20", "0.1uF", "VDD3P3", (90, 50)),
    cap("C21", "10uF 6.3V", "+3V3", (70, 50), C0603),
    # +3V3 decoupling at VDD3P3_RTC, VDD3P3_CPU and VDDA, as on the flight controller.
    cap("C22", "0.1uF", "+3V3", (70, 130)), cap("C23", "1uF", "+3V3", (78, 130)),
    cap("C24", "10uF 6.3V", "+3V3", (86, 130), C0603), cap("C25", "1uF", "+3V3", (94, 130)),
    cap("C26", "10nF", "+3V3", (102, 130)), cap("C27", "0.1uF", "+3V3", (110, 130)),
    cap("C28", "0.1uF", "+3V3", (118, 130)), cap("C29", "1uF", "+3V3", (126, 130)),
    cap("C30", "0.1uF", "+3V3", (134, 130)), cap("C31", "0.1uF", "+3V3", (142, 130)),
    # VDD_SPI: the in-package flash supply.
    cap("C32", "0.1uF", "VDD_SPI", (160, 130)), cap("C33", "1uF", "VDD_SPI", (168, 130)),

    # CHIP_PU: 10k up, 1 uF down for the power-on delay, button to reset.
    dict(ref="R10", lib="Device:R", value="10k", fp=R, at=(60, 70), nets={1: "+3V3", 2: "CHIP_PU"}),
    cap("C34", "1uF", "CHIP_PU", (60, 85)),
    dict(ref="SW1", lib="Switch:SW_Push", value="RESET", fp="Button_Switch_SMD:SW_SPST_TL3342",
         at=(50, 85), nets={1: "CHIP_PU", 2: "GND"}),
    # GPIO0: 10k up; hold BOOT while pressing RESET for download mode.
    dict(ref="R11", lib="Device:R", value="10k", fp=R, at=(60, 100), nets={1: "+3V3", 2: "BOOT"}),
    dict(ref="SW2", lib="Switch:SW_Push", value="BOOT", fp="Button_Switch_SMD:SW_SPST_TL3342",
         at=(50, 110), nets={1: "BOOT", 2: "GND"}),

    # 40 MHz crystal, 10 pF load, with 15 pF on each side and 24 nH in series on
    # XTAL_P, as on the flight controller (Espressif's reference design).
    dict(ref="X1", lib="tar_fc:Q22FA12800101", value="FA-128 40MHz 10pF",
         fp="tar_fc:CRYSTAL-SMD_4P-L2.0-W1.6-BL", at=(160, 60),
         nets={1: "XTAL_P", 2: "GND", 3: "XTAL_N", 4: "GND"}),
    dict(ref="L3", lib="Device:L", value="24nH", fp="Inductor_SMD:L_0402_1005Metric",
         at=(175, 50), nets={1: "XTAL_P_CHIP", 2: "XTAL_P"}),
    cap("C35", "15pF", "XTAL_P", (150, 75)), cap("C36", "15pF", "XTAL_N", (170, 75)),

    # Antenna: 0 ohm and two empty pi-network pads, then a U.FL. The station's radio
    # link is the VoCore2; the ESP32's own Wi-Fi and Bluetooth are for setup and
    # debugging, and work without an antenna at short range.
    dict(ref="R12", lib="Device:R", value="0", fp=R, at=(200, 60), nets={1: "ESP_ANT_UFL", 2: "ESP_ANT"}),
    dict(ref="C37", lib="Device:C", value="DNP", fp=C0402, at=(195, 75), nets={1: "ESP_ANT", 2: "GND"}),
    dict(ref="C38", lib="Device:C", value="DNP", fp=C0402, at=(205, 75), nets={1: "ESP_ANT_UFL", 2: "GND"}),
    dict(ref="J2", lib="tar_fc:U.FL-R-SMT-1", value="U.FL-R-SMT-1",
         fp="tar_fc:RF-SMD_FRF05002-JSS103M", at=(220, 60),
         nets={1: "ESP_ANT_UFL", 2: "GND", 3: "GND"}),

    # USB-C for programming, as on the flight controller.
    dict(ref="J1", lib="tar_fc:TYPE-C16PIN2MD", value="USB4105-GF-A",
         fp="tar_fc:USB-C-SMD_TYPE-C-16PIN-2MD-073", at=(30, 170),
         nets={"A4B9": "VBUS", "B4A9": "VBUS", "A1B12": "GND", "B1A12": "GND", "13": "GND", "14": "GND",
               "A5": "USB_CC1", "B5": "USB_CC2", "A6": "D+", "B6": "D+", "A7": "D-", "B7": "D-"},
         nc=["A8", "B8"]),
    dict(ref="R13", lib="Device:R", value="5.1k", fp=R, at=(50, 190), nets={1: "USB_CC1", 2: "GND"}),
    dict(ref="R14", lib="Device:R", value="5.1k", fp=R, at=(58, 190), nets={1: "USB_CC2", 2: "GND"}),
    dict(ref="U2", lib="Power_Protection:USBLC6-2SC6", value="USBLC6-2SC6",
         fp="Package_TO_SOT_SMD:SOT-23-6", at=(80, 170),
         nets={1: "D-", 2: "GND", 3: "D+", 4: "USB_DP", 5: "VBUS", 6: "USB_DN"}),
    cap("C39", "100nF", "VBUS", (65, 190)),
    # USB powers +5V through a Schottky for flashing without the power board.
    dict(ref="D3", lib="Device:D_Schottky", value="1N5819HW", fp="Diode_SMD:D_SOD-123",
         at=(100, 160), nets={1: "+5V", 2: "VBUS"}),

    # Status LEDs on GPIO39 and GPIO40, values from the flight controller.
    dict(ref="R15", lib="Device:R", value="1k", fp=R, at=(200, 150), nets={1: "LED_Y", 2: "LED_Y_A"}),
    dict(ref="D4", lib="Device:LED", value="YELLOW", fp="LED_SMD:LED_0603_1608Metric",
         at=(200, 165), nets={1: "GND", 2: "LED_Y_A"}),
    dict(ref="R16", lib="Device:R", value="470", fp=R, at=(210, 150), nets={1: "LED_G", 2: "LED_G_A"}),
    dict(ref="D5", lib="Device:LED", value="GREEN", fp="LED_SMD:LED_0603_1608Metric",
         at=(210, 165), nets={1: "GND", 2: "LED_G_A"}),

    # Spare GPIOs for later: a sensor, a fan, a buzzer.
    dict(ref="J9", lib="Connector_Generic:Conn_01x06", value="SPARE",
         fp="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical", at=(240, 120),
         nets={1: "+3V3", 2: "SPARE1", 3: "SPARE2", 4: "SPARE3", 5: "SPARE4", 6: "GND"}),

    dict(ref="#FLG04", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(40, 150), nets={1: "VBUS"}),
    # VDD3P3 is fed through L2 and VDD_SPI is the flash supply the chip makes itself.
    dict(ref="#FLG08", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(90, 35), nets={1: "VDD3P3"}),
    dict(ref="#FLG09", lib="power:PWR_FLAG", value="PWR_FLAG", fp="", at=(160, 115), nets={1: "VDD_SPI"}),
]

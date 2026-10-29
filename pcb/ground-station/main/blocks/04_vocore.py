"""Block 4: VoCore2 mesh radio and the Ethernet jack.

Pin numbers are the VoCore2's own (vocore.io/v2.html): the MT7628 chip pin where
there is one, and names for the power and ground pads, which get numbers when the
footprint is drawn.

  +5.0VI      +5V, up to 500 mA; 22 uF and 100 nF beside it
  RXD1, TXD1  UART1 to the ESP32 (pins 148, 147). UART2 is the VoCore2's Linux
              console and UART0's TXD (pin 30) is a start-up mode pin that must
              stay low, so neither is used for data (see docs/hardware-reference.md)
  RXD2, TXD2  the console, brought out to J7 for a USB-serial adapter
  RST         to the ESP32 (pin 138, pull low to reset)
  P0          Ethernet port 0 (pins 33 to 36) to the RJ45 jack

The Wi-Fi antenna is on the VoCore2 itself: its onboard antenna, or an external
5 to 8 dBi antenna on its U.FL socket through a pigtail.

RJ45: Wuerth 7499010121A, transformer and jack in one. VoCore's page does not say
whether the MT7628's PHY wants the transformer centre taps tied to 3.3 V or to
ground through a capacitor, so both are provided. The cable-side 75 ohm
terminations and their 1000 pF capacitor are inside the jack; pin 8 is their
ground end, so it goes straight to GND. Centre taps: C53 and C54 (100 nF to GND) are
fitted, R40 and R41 (0 ohm to +3V3) are not. Check against the MT7628 reference
design before ordering, and swap if it calls for 3.3 V.
"""

R = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"

PARTS = [
    dict(ref="M1", lib="tar_gs:VoCore2", value="VoCore2", fp="tar_gs:VoCore2", at=(90, 90),
         nets={"5VA": "+5V", "5VB": "+5V", "GA": "GND", "GB": "GND", "GC": "GND", "GD": "GND",
               "148": "VOC_RXD1", "147": "VOC_TXD1", "40": "VOC_CON_RX", "42": "VOC_CON_TX",
               "138": "VOC_RST", "35": "ETH_TXP", "36": "ETH_TXN", "33": "ETH_RXP", "34": "ETH_RXN"},
         nc=["30", "31", "3V3"]),
    dict(ref="C50", lib="Device:C", value="22uF 10V", fp="Capacitor_SMD:C_0805_2012Metric",
         at=(50, 60), nets={1: "+5V", 2: "GND"}),
    dict(ref="C51", lib="Device:C", value="100nF", fp=C0402, at=(58, 60), nets={1: "+5V", 2: "GND"}),

    # Console header: 1 GND, 2 VoCore2 RXD2 (adapter TX goes here), 3 VoCore2 TXD2.
    dict(ref="J7", lib="Connector_Generic:Conn_01x03", value="VOCORE CONSOLE",
         fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", at=(40, 130),
         nets={1: "GND", 2: "VOC_CON_RX", 3: "VOC_CON_TX"}),

    # RJ45 with magnetics. TD = the PHY's transmit pair.
    dict(ref="J6", lib="Connector:RJ45_Wuerth_7499010121A", value="7499010121A",
         fp="Connector_RJ:RJ45_Wuerth_7499010121A_Horizontal", at=(180, 90),
         nets={1: "ETH_TXP", 2: "ETH_TCT", 3: "ETH_TXN", 4: "ETH_RXP", 5: "ETH_RCT", 6: "ETH_RXN",
               8: "GND", "SH": "GND"},
         nc=[7, 9, 10, 11, 12]),
    dict(ref="C53", lib="Device:C", value="100nF", fp=C0402, at=(150, 130), nets={1: "ETH_TCT", 2: "GND"}),
    dict(ref="C54", lib="Device:C", value="100nF", fp=C0402, at=(160, 130), nets={1: "ETH_RCT", 2: "GND"}),
    dict(ref="R40", lib="Device:R", value="0 DNP", fp=R, at=(150, 145), nets={1: "+3V3", 2: "ETH_TCT"}),
    dict(ref="R41", lib="Device:R", value="0 DNP", fp=R, at=(160, 145), nets={1: "+3V3", 2: "ETH_RCT"}),
]

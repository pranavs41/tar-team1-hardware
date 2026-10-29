"""Block 5: the 20-pin link to the main board, and the mounting holes.

A 2 x 10, 2.54 mm boxed header and a ribbon cable. Pin 1 to pin 20 match the main
board's J3 one for one:

  1, 2    VIN_SYS out to the main board (it draws about 0.5 A at 12 V)
  3, 4    GND
  5 to 8   DOCK1_EN to DOCK4_EN, from the main board
  9 to 12  DOCK1_FLT to DOCK4_FLT, to the main board (open drain, pulled up there)
  13 to 16 DOCK1_ILM to DOCK4_ILM, dock current readings, to the main board's ADC
  17 to 20 GND, one beside each group so the ribbon has returns spread along it
"""

PARTS = [
    dict(ref="J7", lib="Connector_Generic:Conn_02x10_Odd_Even", value="LINK",
         fp="Connector_IDC:IDC-Header_2x10_P2.54mm_Vertical", at=(40, 60),
         nets={1: "VIN_SYS", 2: "VIN_SYS", 3: "GND", 4: "GND",
               5: "DOCK1_EN", 6: "DOCK2_EN", 7: "DOCK3_EN", 8: "DOCK4_EN",
               9: "DOCK1_FLT", 10: "DOCK2_FLT", 11: "DOCK3_FLT", 12: "DOCK4_FLT",
               13: "DOCK1_ILM", 14: "DOCK2_ILM", 15: "DOCK3_ILM", 16: "DOCK4_ILM",
               17: "GND", 18: "GND", 19: "GND", 20: "GND"}),
    dict(ref="H1", lib="Mechanical:MountingHole", value="M3", fp="MountingHole:MountingHole_3.2mm_M3", at=(100, 40), nets={}),
    dict(ref="H2", lib="Mechanical:MountingHole", value="M3", fp="MountingHole:MountingHole_3.2mm_M3", at=(110, 40), nets={}),
    dict(ref="H3", lib="Mechanical:MountingHole", value="M3", fp="MountingHole:MountingHole_3.2mm_M3", at=(120, 40), nets={}),
    dict(ref="H4", lib="Mechanical:MountingHole", value="M3", fp="MountingHole:MountingHole_3.2mm_M3", at=(130, 40), nets={}),
]

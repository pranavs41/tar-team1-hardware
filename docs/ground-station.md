# Ground station boards

The ground station charges up to four drones, runs the RTK base and the mesh radio, and gives a laptop a way in. It has two boards in one box, joined by a 20-pin ribbon cable:

| Board | Owner | What it does |
|---|---|---|
| Power and dock board | Pranav | Takes power from USB-C or a 12 V jack and drives the four docks' charging walls |
| Main board | Rishab | ESP32-S3 station processor, ZED-F9P RTK base, MAX-M10S reference receiver, VoCore2 mesh radio, Ethernet jack |

Keeping them apart keeps the dock current away from the GPS and the radio, and either board can be redone without touching the other.

Status: schematics drafted on 2026-10-28, not yet reviewed. Layout waits for the station CAD, which sets the board sizes and where the docks sit.

## Where the files are

| What | Where |
|---|---|
| Schematic sources, one Python file per block | `pcb/ground-station/power/blocks/`, `pcb/ground-station/main/blocks/` |
| KiCad projects | `pcb/ground-station/power/`, `pcb/ground-station/main/` |
| Schematics as PDF | `schematics/ground-station-power-schematic.pdf`, `schematics/ground-station-main-schematic.pdf` |
| Symbols KiCad does not have (the dock eFuse and the VoCore2) | `pcb/ground-station/lib/tar_gs.kicad_sym`, made by `tools/mklib.py` |

The block files are the source. Each one lists its parts and which net every pin goes to, with the reason for each choice next to it. `python tools/build.py power` (or `main`) turns them into the KiCad schematic, exports the netlist, reports any net that reaches only one pin, and runs KiCad's electrical rules check. `python tools/check.py` then checks what the rules check cannot: that every footprint exists, that the two ends of the ribbon cable match pin for pin, and that the ESP32's pins are each used once.

Results on 2026-10-28: both boards 0 errors in the rules check, no single-pin nets, all checks pass.

## Power and dock board

```
USB-C (12-20 V PD) --> TPS25730D --+
                                   +--> VIN_SYS --> LMR33630 A (5.3 V) --> dock 1, dock 2
12 V jack --> LM74700 + FET -------+            --> LMR33630 B (5.3 V) --> dock 3, dock 4
                                   |
                                   +--> ribbon to the main board
```

| Block | Part | Why |
|---|---|---|
| USB-C input | TI TPS25730D, USB-C power delivery sink | Asks the charger for 12 to 20 V at 1.5 A, 3 A at most, set by resistors, so it needs no programming or firmware. Its built-in switch stops current flowing back out of the port when the jack is also plugged in. TVS2200 and a Schottky diode on VBUS protect it, as TI's datasheet asks |
| 12 V jack | Wuerth 2.0 x 5.5 mm jack, TI LM74700 ideal diode with an Infineon BSC028N06LS3 FET | Lets the jack and USB-C share VIN_SYS: whichever is higher runs the station, and neither feeds the other. A plug wired backwards is blocked. Takes 12 to 20 V |
| Dock supplies | Two TI LMR33630A bucks, 3 A each, 5.31 V out | Four chargers at their 0.925 A limit draw 3.7 A, so each buck carries about 1.85 A. With two, one failure takes down two docks, not four |
| Dock switches | Four TI TPS259470A eFuses | Each dock limited to 1.5 A and retries by itself after a short, so a screwdriver across the walls trips that dock only. Cuts the dock off above 6.14 V in case a buck fails high. Reports its fault, and gives a voltage proportional to the dock's current so the station can tell when a drone is docked and charging |
| Dock outputs | JST XH 2-pin, a TVS and a green LED per dock | The lead to each dock's two walls; the TVS catches static on the bare metal; the LED shows the dock is live |

Why 5.3 V on the walls: the spring contacts lose some voltage at about 1 A, the drone's charger works from about 4.3 V, and both the drone's eFuse and the dock eFuse cut off near 6.0 to 6.1 V. 5.3 V leaves margin both ways.

The docks are off until the main board turns them on. A 100k resistor holds each enable low, so an unplugged or rebooting main board leaves the walls dead.

## Main board

| Block | Part | Why |
|---|---|---|
| Power | Diodes AP63205 buck (5 V, 2 A), TI TLV75733 (3.3 V for the ESP32), two TI TPS7A2033 (3.3 V for each GPS) | Copied from the flight controller, with input parts rated for 20 V. Worst case on 5 V is about 1.1 A. Each GPS gets its own quiet regulator, as u-blox asks for the F9P |
| Processor | ESP32-S3FN8 with the flight controller's crystal, decoupling, USB-C and antenna circuit | Switches and watches the docks, reads both GPS receivers, and passes data to the VoCore2. Reset and boot are real buttons here |
| RTK base | u-blox ZED-F9P with an SMA for an active survey antenna | Antenna power and filtering use the exact parts in u-blox's integration manual (Table 42). UART1 goes to the ESP32; UART2, the correction port, comes out on a 4-pin JST-SH for an external radio or a laptop. A blue LED blinks once a second with a fix |
| Reference receiver | u-blox MAX-M10S, wired as on the flight controller | The same receiver the drones carry, beside the F9P. The station knows exactly where it is, so it can measure that receiver's error and send it to the drones |
| Mesh radio | VoCore2 | Same module as the drones. UART1 to the ESP32 (pins 147 and 148), its Linux console on a 3-pin header, reset from the ESP32. Its own antenna, or an external 5 to 8 dBi one on its U.FL |
| Ethernet | Wuerth 7499010121A, jack and transformer in one | Backup way in for a laptop when there is a lot of mapping data; normally the laptop uses Wi-Fi |
| Link | 2 x 10 header, pull-ups on the fault lines, a 1k and 100 nF filter on each current reading | The ribbon from the power board |
| Spare | 6-pin header with four GPIOs | For a sensor, fan or buzzer later |

ESP32 pin plan:

| GPIO | Job |
|---|---|
| 1, 2, 4, 5 | dock 1 to 4 current (ADC1) |
| 6 to 9 | dock 1 to 4 fault |
| 10 to 13 | dock 1 to 4 enable |
| 14 | VoCore2 reset |
| 15, 16 | UART2 to the MAX-M10S |
| 17, 18 | UART1 to the ZED-F9P |
| 21 | ZED-F9P reset (open drain only) |
| 33 to 36 | spare header |
| 39, 40 | yellow and green LEDs |
| 43, 44 | UART0 to the VoCore2's UART1 |

The strapping pins (GPIO3, 45 and 46) are left alone, and GPIO0 is the boot button. The ESP32's own console runs over USB. The dock current readings are 0 to about 0.6 V, so read them with the ADC's 0 dB range: 0.37 V is one drone charging at full rate, 0.61 V is the 1.5 A limit.

## Still open

| Item | What is needed |
|---|---|
| Two footprints to draw | TI's RPW (VQFN-HR, 2 x 2 mm) land pattern for the dock eFuses, and the VoCore2's 25.6 mm castellated outline. Both at layout, from the datasheet and vocore.io drawings |
| Ethernet centre taps | VoCore does not say whether the MT7628's PHY wants the transformer centre taps tied to 3.3 V or decoupled to ground. Both are on the board: two 100 nF to ground fitted, two 0 ohm to 3.3 V not fitted. Check against MediaTek's MT7628 reference design before ordering |
| Barrel jack pin 1 | The symbol takes pin 1 as the centre pin. Confirm on Wuerth's drawing for 694106106102 before layout |
| Board sizes and dock positions | From Jadon's station CAD |
| Battery | 100 Wh USB-C power delivery bank or a small power station, still to be agreed (see `TASKS.md`) |
| Part numbers to confirm in stock | Especially the TPS25730D, the TPS259470A, the ZED-F9P (about $200) and the XAL6060 inductors |

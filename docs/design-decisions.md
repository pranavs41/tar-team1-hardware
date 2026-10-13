# Design decisions

Why the network drone flight controller is built the way it is. Add a row when a decision changes, don't rewrite history.

| Date | Decision | Why |
|---|---|---|
| 2026-09-26 | Bare chips only, no modules or breakout boards | Team rule; we design every support circuit ourselves |
| 2026-09-26 | ESP32-S3FN8 (bare QFN-56) as the MCU | Wi-Fi/BLE for the relay mesh, native USB, 8 MB flash in package; the MINI-1U module stays in `lib/` as a fallback only |
| 2026-09-26 | 2S battery, input stage tolerates up to 4S | 2S is more efficient for hovering relay nodes and lets a plain buck make 5 V (1S would need buck-boost) |
| 2026-09-26 | Bought 20 × 20 4-in-1 ESC, not integrated | ESC power stage is noisy and risky on a first board |
| 2026-09-26 | Board 36 × 36 mm, M2 holes on a 20 × 20 pattern | Everything fits on one side, so the whole board reflows on a hot plate in one pass |
| 2026-09-26 | All parts on the top side; bottom has only test pads | Our only assembly method is a hot plate |
| 2026-09-26 | ICM-42688-P for the rate loop | Fast, low-latency SPI gyro and accelerometer |
| 2026-09-26 | BMP581 barometer | Lowest noise of the options, 2 × 2 mm |
| 2026-09-26 | u-blox MAX-M10S GPS with U.FL antenna | Drones reference an RTK ground station for landing |
| 2026-09-26 | Wi-Fi antenna on U.FL, RF pi network footprints kept | Antenna can mount high for stacking; matching can be tuned later with a VNA |
| 2026-09-26 | USB-C is the only programming port | Native USB flashes and debugs with no extra chip; UART0 test pads are the fallback |
| 2026-09-26 | Charging is a separate board | Out of scope for the FC |
| 2026-09-27 | SMAJ18A TVS instead of SMAJ15A | SMAJ15A breaks down at 16.7 V, below a full 4S pack |
| 2026-09-27 | Separate low-noise `+3V3_SENS` rail for sensors | Keeps ESP32 radio TX current spikes out of the IMU and barometer supply |
| 2026-09-27 | Dropped the BNO085 | Overlaps the ICM-42688-P (both are accel and gyro). Its fused output is too slow for the rate loop, orientation fusion runs fine on the ESP32 as on Betaflight and PX4 boards, and its magnetometer would sit centimetres from motor currents. Saves about $20, a dozen parts and five ESP32 pins. If heading is needed later, add a small I2C magnetometer or use the GPS puck's compass. |
| 2026-09-30 | ESC connector follows the Betaflight 4-in-1 order (GND, VBAT, CUR, TLM, M1 to M4) | Most 20 × 20 ESCs use it; confirm against the ESC before ordering |
| 2026-09-30 | I2C and UART ports use the Dronecode order (VCC, signal, signal, GND) | Off-the-shelf cables fit |
| 2026-09-30 | Charging-board port carries DOCK_DET (GPIO18) and AUX_ADC (GPIO8, ADC1); ESC telemetry moved to GPIO17 | ADC2 is unusable while Wi-Fi runs, so the port needed an ADC1 pin; GPIO17 was freed by dropping the BNO085 |
| 2026-09-30 | Mounting holes are plain 2.2 mm holes with no copper ring | Nothing needs to connect to the screws; copper rings only made clearance to the connectors harder |
| 2026-09-30 | USB diode D1 sits by the I2C port on the left edge, not next to the USB-C | The right edge is full; D1 only carries the 5 V feed, so a longer trace costs nothing |
| 2026-09-30 | RESET and BOOT are pad pairs on the bottom, not pushbuttons | Only needed for recovery; USB resets the chip for normal flashing; frees the top edge |
| 2026-09-30 | 3 mm keep-out around each mounting hole | Room for a 6 mm soft-mount grommet or standoff, per the team review |
| 2026-09-30 | Spare UART port dropped to test pads TP17/TP18 | With the 3 mm keep-out there is one connector slot per edge; GPS, USB-C, ESC and the I2C port take four, the charging port takes the top-right |
| 2026-09-30 | Twelve more bottom-side test pads (SPI, I2C, GPS UART, ESC telemetry) | Every bus can be probed when a chip doesn't answer; they cost nothing on a single-side assembly |
| 2026-10-01 | Board grows to 36 × 39 mm (3 mm strip along the top) | The charging port J7 was 1.5 mm from hole H2; with the strip every top-side part clears every hole centre by 3 mm, so the ESC's grommets or nuts fit at all four corners |
| 2026-10-01 | Mounting holes 3.2 mm (M3) instead of 2.2 mm | The ESC the team picked (30 A 4-in-1, 5.4 g) has M3 holes on the 20 mm pattern; the FC has to take the same screws and grommets |
| 2026-10-02 | ESP32 pins reassigned for routing (motors GPIO11/13/16/6, SPI on GPIO33 to 35 and 47, I2C GPIO37/38, LEDs GPIO39/40, dock detect GPIO9, GPS RX GPIO18, ESC telemetry GPIO10, battery sense GPIO4) | A 0.6 mm via fits beside only every other 0.4 mm pitch pin, so the pins that must leave on the bottom layer are spaced out and the rest escape on top; the routing matrix makes any GPIO equivalent for these signals |
| 2026-10-02 | IMU INT2/FSYNC left open | The ESP32 pin was needed as a motor escape; the datasheet allows the pin to float |
| 2026-10-02 | R2 (0 Ω jumper in XTAL_P) removed | The crystal sits against the chip; the footprint only lengthened the trace |
| 2026-10-02 | Test pads cut from 18 to 7, each placed on a via of its net | No bottom-layer room near the ESP32 for the bus pads; a pad on a via costs no extra copper |
| 2026-10-02 | `+3V3` on a solid inner plane (L3), `+5V` and `+3V3_SENS` as top-layer tracks | Thirteen `+3V3` pads scattered across the board; a plane plus one via each is fewer vias than tracks would need |
| 2026-10-02 | Two vias in pads (C6 pin 1, J5 pin 1, both `+3V3`) and one in the GPS cap C30's GND pad | No clear spot beside those pads; expect a little solder wicking there when hand soldering |
| 2026-10-02 | Power tree kept as buck to 5 V then two LDOs, after checking SpeedyBee, Betaflight F4, Pixhawk 6C and Espressif's guidance | Same tree on every one of them; the ESP32 LDO's 0.22 W average is inside its rating on a board with planes, and the LDO keeps switching noise off the radio rail |
| 2026-10-02 | 470 µF 35 V low-ESR electrolytic required on the ESC's battery pads, listed in the BOM and bring-up | Standard on every FPV build; the FC's 10 µF ceramic alone does not filter motor noise, and the can does not fit under a 36 mm board |
| 2026-10-02 | C35, 100 µF 25 V polymer tantalum on VBAT, bottom side, lower-left corner | Largest low-ESR part that fits; the 470 µF can FPV builds use does not. Bottom side because the top is full; the corner is outside the ESC's outline so it does not touch the stack |
| 2026-10-02 | C16 (buck input) 0805 to 1206, crystal X1 moved up 0.6 mm to make room | A 1206 keeps about 7 µF at 2S and 4 µF at 4S against 5 and 2.5 for the 0805; the courtyard now touches R9 and C12's, which is a warning, not a clearance problem |
| 2026-10-02 | U4 (ESP32 LDO) SOT-23-5 to WSON-6 with thermal pad, TLV75733PDRVR | 100 °C/W instead of 231 on the JEDEC board; the thermally enhanced SOT-23 (DYD) is on back-order; the WSON needs the hot plate, which the top side gets anyway |
| 2026-10-08 | J5 power pin moved from 3.3 V to 5 V; J5 is now the sensor port for the TF-Luna | The sensor needs 3.7 to 5.2 V; I2C stays at 3.3 V because the bus is open-drain with pull-ups to the 3.3 V sensor rail |
| 2026-10-08 | J6 added: 5 V UART port for the VoCore2 networking module, top-entry JST-SH in the bottom-right corner | The team replaced the SiK radio with the VoCore2; no edge has room for a fifth side-entry connector |
| 2026-10-08 | J6's TX and RX share GPIO2 and GPIO10 with the ESC current and telemetry pins of J4 | The ESP32 has no escapable pins left (a via fits beside every other pin only, and the two free pins are boxed in by the motor lanes); those two lines already reach that corner and the chosen 8-bit ESC is not expected to drive them |
| 2026-10-08 | Buck inductor must saturate at 2 A or more | Sensor and radio raise the worst-case 5 V load from 0.38 A to 0.93 A, which puts the inductor peak at 1.09 A on 2S and 1.27 A on 4S |
| 2026-10-08 | Schematic fix: the battery wire is split where C35 joins it | A junction on an unbroken wire does not connect in KiCad, so since C35 was added the schematic had the buck input on a separate net from VBAT; the board was right throughout, and a pin-by-pin comparison of schematic and board now shows no differences |
| 2026-10-11 | Ground via beside the USB socket moved 0.06 mm | It was 0.20 mm from the socket's mounting slot, under the fab's 0.25 mm hole spacing; found by a pre-order check, since KiCad does not compare vias against slots |
| 2026-10-11 | I2C runs at 100 kHz when the obstacle sensor is attached | The sensor cable slows the edges past the 400 kHz limit with 4.7 kΩ pull-ups; 2.2 kΩ at R12 and R13 would restore 400 kHz |
| 2026-10-11 | Charging port J7 becomes a 7-pin JST-SH: BATT+, GND, SDA, SCL, /PG, STAT, CD | The charging board uses a BQ25887 and wants I2C, two status lines and a disable line, and feeds the battery to the flight controller. A 7-pin JST-GH would sit on the GPS module's pads; the JST-SH is 3 mm narrower |
| 2026-10-11 | The charging board's VBAT_SENSE pin is not brought over | The board already measures the battery on GPIO4, and BATT+ on J7 is the same net. No ESP32 pin was left to read a second copy |
| 2026-10-11 | Net names DOCK_DET and AUX_ADC become CHG_PG (GPIO9) and CHG_STAT (GPIO8); CHG_CD is new on GPIO7 | The lines changed job. Power good from the charger doubles as the docked signal |
| 2026-10-11 | ESC telemetry track rerouted through the top layer between R1's pads | GPIO7 had no way out from under the chip until that track moved |
| 2026-10-11 | Landing sensor port J8 added, top-entry JST-SH on the right edge | The swarm drones carry a second, downward distance sensor. A side-entry JST-GH would put bare pads inside the 3 mm clear zone of hole H2 |
| 2026-10-11 | I2C pull-ups R12 and R13 change from 4.7 kΩ to 2.2 kΩ | The bus now leaves the board on three cables |
| 2026-10-11 | Two more courtyard overlaps accepted: J8 with H2 and J8 with U2 | The outlines overlap, the parts do not. J8's body and pads are more than 3.2 mm from the hole centre |
| 2026-10-11 | New tracks use horizontal, vertical and 45 degree runs only | Easier to read and to edit by hand than the any-angle tracks elsewhere on the board |
| 2026-10-12 | USB-C mounting slots lengthened 0.4 mm, to 1.7 mm and 1.4 mm | The GCT USB4105's legs are wider than the socket the footprint was drawn for. The longer slots take either part. Four tracks and three vias moved by 0.1 to 0.15 mm to stay clear |
| 2026-10-12 | USB-C locating peg holes changed from 0.7 mm to 0.65 mm | Leaves room between the hole's copper ring and the VBUS pads at a 0.127 mm spacing rule. The pegs are 0.5 mm |
| 2026-10-12 | Six tight spots opened up by 0.015 to 0.03 mm | The board now passes at 0.127 mm spacing, which OSH Park and Aisler need |
| 2026-10-12 | Green LED D3 changed to Würth 150060VS75000 | The first choice needed 3.2 V and would barely light from 3.3 V. This one lights at 2.0 to 2.4 V. R7 stays 470 Ω |
| 2026-10-12 | J4 pin order changed to GND, VBAT, MOTOR1 to MOTOR4, ESC_TELEM, ESC_CUR | The team's ESC prints −, +, 1, 2, 3, 4, N, C on its connector. With the old order a straight cable would have put motor signals on the wrong pins |
| 2026-10-12 | Motor numbers moved between ESP32 pins: motor 1 GPIO16, motor 2 GPIO6, motor 3 GPIO11, motor 4 GPIO13 | Any of these pins can send DShot, so renumbering them meant only two motor tracks had to move on the board |
| 2026-10-13 | Board fab is OSH Park, four-layer prototype service | A US fab, as the team prefers, and the smallest order is three boards |
| 2026-10-13 | Tab pads on J4 and J7 trimmed by 0.03 to 0.09 mm on the side facing the board edge | OSH Park asks for 0.38 mm between copper and the edge. The pads were at 0.31 to 0.375 mm |
| 2026-10-13 | Copper rings around the USB-C slots widened from 0.10 to 0.12 mm | OSH Park's minimum ring is 0.1016 mm, and the old rings measured just under it |
| 2026-10-13 | Antenna traces left at 0.3 mm on OSH Park's stack | About 59 Ω by calculation. The traces are short, so the mismatch costs under 0.1 dB |
| 2026-10-13 | Assembly by stencil and hot plate, top side in one pass | All reflowed parts are on the top. C35 on the bottom and the USB socket's legs are soldered by hand |
| 2026-10-13 | Battery changed to the OVONIC 2S 1100 mAh high-voltage pack with an XT30 plug | The 1000 mAh pack first picked has a small JST plug built for a few amps, and this drone draws over 20 A at full throttle. The new pack is full at 8.7 V, which the board accepts. Charging it to 8.4 V is safe and gives a little less than its full capacity |
| 2026-10-13 | Compass added off the board: an Adafruit LIS3MDL breakout on the J5 or J8 cable | The drone flies outdoors on its own and the board has no magnetometer. I2C is a shared bus, so it needs no new pin or connector. It sits on a cable so it can be mounted away from the motor currents |

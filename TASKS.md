# Hardware tasks

Who is building what, and where each piece meets someone else's. Tick a box when a task is done and add new ones under your own name.

Last updated 2026-10-11.

## Owners

| Person | Owns | Status |
|---|---|---|
| Pranav | networking drone flight controller PCB, then the mapping drone PCB | flight controller nearly done |
| Daniel | CAD for the drone frame and the battery holder | in progress |
| Rishab | charging board | in progress |
| Jadon | ground station CAD, including the space and rails for charging | in progress |

## Pranav: flight controller, then mapping drone PCB

Networking drone flight controller, rev A:

- [x] Schematic complete, electrical rules check clean
- [x] Board placed and routed, design rules check clean
- [x] Power budget checked
- [x] Sensor port (J5) and radio port (J6) added
- [x] Charging port (J7) enlarged to 7 pins and landing sensor port (J8) added
- [ ] Give one of the two TF-Lunas a new I2C address before both are fitted
- [x] Pin reference written: [`docs/hardware-reference.md`](docs/hardware-reference.md)
- [ ] Decide how to get the gyro: it is out of stock at every authorised distributor (options in [`docs/parts-list.md`](docs/parts-list.md))
- [ ] Ask the purchasing or research-security office which sourcing rule applies to the project
- [ ] Choose the board fab, then recheck the antenna trace width on that fab's layer stack
- [x] Six tight spots opened up, so the board passes a 0.127 mm spacing rule (OSH Park, Aisler)
- [x] USB-C footprint's mounting slots lengthened for the GCT socket
- [x] Green LED changed to a type that lights at about 2 V
- [x] ESC pinout checked against the seller's picture; J4 changed to the ESC's order (−, +, 1, 2, 3, 4, N, C)
- [ ] With the real ESC and cable: confirm with a multimeter which end is pin 1, and pull the C and N wires
- [x] Choose the buck inductor (4.7 µH, saturation current 2 A or more)
- [x] Fill in part numbers for the resistors, capacitors, LEDs and diodes
- [x] Pinout and pad-pitch audit against the datasheets
- [ ] Pad shapes and pin 1 orientation checked against each datasheet's land pattern drawing
- [x] Antenna trace width checked for 50 Ω on the fab's layer stack
- [x] Fab capability check and gerber export dry run
- [ ] Export gerbers and order rev A
- [ ] Write the bring-up test firmware
- [ ] Assemble and run the [bring-up checklist](docs/bring-up.md)

The full plan, with what each check proves, is in [`docs/pcb-test-plan.md`](docs/pcb-test-plan.md).

Mapping drone PCB:

- [ ] Collect requirements: sensors, compute, battery voltage, size
- [ ] Schematic
- [ ] Layout

## Daniel: frame and battery holder

- [ ] Frame CAD
- [ ] Battery holder CAD
- [ ] Stress simulation in SolidWorks before printing
- [ ] Bare-frame tests: arm bending, arm twist, screw holes, battery holder
- [ ] Drop test at flying weight
- [ ] Tied-down throttle and vibration tests on the finished drone

How to run each test and what counts as a pass is in [`docs/frame-test-plan.md`](docs/frame-test-plan.md).

What the frame has to fit, all from the flight controller:

- The board is 36 × 39 mm with four M3 holes on a 20 × 20 mm square. A 3D model is in [`cad/network-drone-fc.step`](cad/network-drone-fc.step) and the dimensions are in [`cad/README.md`](cad/README.md).
- The radio port J6 points straight up from the bottom-right corner and needs clear space above it for a plug and cable.
- Cables leave on every edge: USB-C on the right, ESC at the bottom, obstacle sensor on the left, charging board at the top right.
- The landing sensor port J8 is on the right edge just below the charging connector and points straight up, like J6. It also needs clear space above it.
- A second distance sensor faces down for landing and connects by cable to J8. It needs a mount on the underside with a clear view of the ground.
- The battery is now a 1000 mAh pack, larger and heavier than the 800 mAh one first planned. Size the battery holder from the real pack.
- The charging board needs a place on the frame, close to the battery, with its 7-pin cable reaching the top-right corner of the flight controller.
- The obstacle sensor (TF-Luna) mounts at the front and connects by cable to J5 on the left edge.
- Two antennas need a place: Wi-Fi from J1 at the lower right, GPS from J3 at the top left.

## Rishab: charging board

- [ ] Charging board schematic
- [ ] Charging board layout

- [ ] Check the parts against the BQ25887 datasheet (the open points are listed in the charging board page)
- [ ] Agree the dock voltage and current with Jadon

The plan, the parts list and the checks still open are in [`docs/charging-board.md`](docs/charging-board.md).

How it connects to the flight controller, through J7 (7-pin JST-SH, part SM07B-SRSS-TB, cable wired straight through):

| J7 pin | Signal | Notes |
|---|---|---|
| 1 | BATT+ | battery positive. Powers the flight controller, 1 A at most. Charge current does not go through this pin |
| 2 | GND | |
| 3 | SDA | I2C. The pull-ups are on the flight controller |
| 4 | SCL | I2C |
| 5 | /PG | to GPIO9. Low when the charger has input power, so low means docked |
| 6 | STAT | to GPIO8. Low while charging |
| 7 | CD | from GPIO7. High stops charging. Must read as low when left floating |

Three things differ from the charging board's first list: there is no VBAT_SENSE pin, because the flight controller already measures the battery and had no pin left for a second reading; the 10 kΩ pull-ups are not needed, because the flight controller supplies them; and /INT is not connected.

## Jadon: ground station

- [ ] Ground station CAD
- [ ] Space and rails for charging

## Charging concept

The current idea: a conductive material on the outside of the propeller guard slides into conductive rails on the ground station, and the drone charges through that contact.

That one idea crosses three people's work, so these points need an agreed answer:

| Question | Who it touches |
|---|---|
| Which part of the guard is positive and which is ground, and how the drone is kept from docking the wrong way round | Daniel, Jadon, Rishab |
| The size, spacing and position of the contacts on the guard, so they line up with the rails | Daniel, Jadon |
| What voltage and current the rails supply | Jadon, Rishab |
| How the wire gets from the guard contacts to the charging board | Daniel, Rishab |
| What stops the two exposed contacts from shorting on something metal in flight or in the case | Rishab |
| How the drone knows it is seated, which is what the charger's power-good line on J7 pin 5 is for | Rishab, Pranav |

## Reference

- Every connector and pin on the flight controller: [`docs/hardware-reference.md`](docs/hardware-reference.md)
- Whole-drone parts list with weights and prices: [`docs/parts-list.md`](docs/parts-list.md)
- How the flight controller gets tested: [`docs/pcb-test-plan.md`](docs/pcb-test-plan.md)
- How the frame gets tested: [`docs/frame-test-plan.md`](docs/frame-test-plan.md)

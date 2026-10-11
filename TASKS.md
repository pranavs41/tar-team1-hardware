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
- [x] Pin reference written: [`docs/hardware-reference.md`](docs/hardware-reference.md)
- [ ] Decide how to get the gyro: it is out of stock at every authorised distributor (options in [`docs/parts-list.md`](docs/parts-list.md))
- [ ] Ask the purchasing or research-security office which sourcing rule applies to the project
- [ ] Choose the board fab. For a US or European fab, six spots need 0.006 mm more spacing and the antenna trace width needs rechecking
- [ ] Widen the USB-C footprint's mounting slots for the GCT socket
- [ ] Pick a green LED that lights at about 2 V, or change R7
- [ ] Confirm the ESC's connector pinout against J4, and whether it outputs current or telemetry
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
- The obstacle sensor (TF-Luna) mounts at the front and connects by cable to J5 on the left edge.
- Two antennas need a place: Wi-Fi from J1 at the lower right, GPS from J3 at the top left.

## Rishab: charging board

- [ ] Charging board schematic
- [ ] Charging board layout

How it connects to the flight controller, through J7 (4-pin JST-GH):

| J7 pin | Signal | Notes |
|---|---|---|
| 1 | GND | |
| 2 | DOCK_DET | digital. The flight controller pulls it high; pull it to ground when the drone is docked |
| 3 | AUX_ADC | analog, must stay under 3.1 V |
| 4 | spare | not connected |

There is no power on J7 in either direction. Charge current goes from the charging board to the battery directly, not through the flight controller. Protection for pins 2 and 3 belongs on the charging board.

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
| How the drone knows it is seated, which is what DOCK_DET on J7 is for | Rishab, Pranav |

## Reference

- Every connector and pin on the flight controller: [`docs/hardware-reference.md`](docs/hardware-reference.md)
- Whole-drone parts list with weights and prices: [`docs/parts-list.md`](docs/parts-list.md)
- How the flight controller gets tested: [`docs/pcb-test-plan.md`](docs/pcb-test-plan.md)
- How the frame gets tested: [`docs/frame-test-plan.md`](docs/frame-test-plan.md)

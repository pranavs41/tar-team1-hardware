# Hardware tasks

Who is building what, and where each piece meets someone else's. Tick a box when a task is done and add new ones under your own name.

Last updated 2026-10-25.

## Owners

| Person | Owns | Status |
|---|---|---|
| Pranav | networking drone flight controller PCB, then the ground station PCBs with Rishab | flight controller ordered |
| Rishab | networking drone charging board, then the ground station PCBs with Pranav | charging board ordered |
| Rihan | mapping drone PCB, and its power management and charging board | starting |
| Jadon | ground station CAD, including the space and rails for charging | in progress |
| Daniel | CAD for the drone frame and the battery holder, then likely the ground station | in progress |

## Pranav: flight controller, then ground station PCBs

Networking drone flight controller, rev A:

- [x] Schematic complete, electrical rules check clean
- [x] Board placed and routed, design rules check clean
- [x] Power budget checked
- [x] Sensor port (J5) and radio port (J6) added
- [x] Charging port (J7) enlarged to 7 pins and landing sensor port (J8) added
- [ ] Give one of the two TF-Lunas a new I2C address before both are fitted
- [ ] Firmware: cap the throttle so the battery current stays under about 25 A (the XT30's burst rating is 30 A)
- [ ] Measure one motor's thrust and current on a scale, then put the real numbers into `tools/drone_power_sim.py`
- [ ] Compass: wire the LIS3MDL breakout into the J5 or J8 cable, mount it away from the battery leads, calibrate on the finished drone
- [x] Pin reference written: [`docs/hardware-reference.md`](docs/hardware-reference.md)
- [x] Gyro source found: Newark, an authorised distributor
- [ ] Ask the purchasing or research-security office which sourcing rule applies to the project
- [x] Board fab chosen: OSH Park. Antenna trace rechecked on its layer stack (about 59 Ω, left as is)
- [x] Parts list checked against every footprint on the board
- [x] Six tight spots opened up, so the board passes a 0.127 mm spacing rule (OSH Park, Aisler)
- [x] USB-C footprint's mounting slots lengthened for the GCT socket
- [x] Green LED changed to a type that lights at about 2 V
- [x] ESC pinout checked against the seller's picture; J4 changed to the ESC's order (−, +, 1, 2, 3, 4, N, C)
- [ ] With the real ESC and cable: confirm with a multimeter which end is pin 1, and pull the C wire
- [x] Choose the buck inductor (4.7 µH, saturation current 2 A or more)
- [x] Fill in part numbers for the resistors, capacitors, LEDs and diodes
- [x] Pinout and pad-pitch audit against the datasheets
- [ ] Pad shapes and pin 1 orientation checked against each datasheet's land pattern drawing
- [x] Antenna trace width checked for 50 Ω on the fab's layer stack
- [x] Fab capability check and gerber export dry run
- [x] Order files made: [`pcb/network-drone-fc/production/rev-A/`](pcb/network-drone-fc/production/rev-A/order-notes.md)
- [x] Order rev A: boards from OSH Park, stencil from OSH Stencils, parts from DigiKey
- [x] Order sheet for the rest of the drone written: [`docs/drone-order-sheet.md`](docs/drone-order-sheet.md)
- [x] Battery settled: OVONIC 2S 1100 mAh with an XT30 plug
- [ ] Later: decide on and order the carbon fiber subframe (left off the order sheet on 2026-10-13)
- [ ] Order the drone components from [`docs/full-order-sheet.md`](docs/full-order-sheet.md)
- [ ] Write the bring-up test firmware
- [ ] Assemble and run the [bring-up checklist](docs/bring-up.md)

The full plan, with what each check proves, is in [`docs/pcb-test-plan.md`](docs/pcb-test-plan.md).

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
- The battery is now the OVONIC 2S 1100 mAh pack, larger and heavier than the 800 mAh one first planned. Size the battery holder from the real pack.
- The charging board needs a place on the frame, close to the battery, with its 7-pin cable reaching the top-right corner of the flight controller.
- The obstacle sensor (TF-Luna) mounts at the front and connects by cable to J5 on the left edge.
- Two antennas need a place: Wi-Fi from J1 at the lower right, GPS from J3 at the top left.

## Rishab: charging board

- [ ] Charging board schematic
- [ ] Charging board layout

- [ ] Check the parts against the BQ25887 datasheet (the open points are listed in the charging board page)
- [ ] The charging board parts are on the team order sheet as provisional ([`docs/full-order-sheet.md`](docs/full-order-sheet.md)). Check every part number and size against your schematic before the order goes in. The battery is now a high-voltage 2S pack (full at 8.7 V); charging it to 8.4 V is safe
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

## Rihan: mapping drone PCB

The mapping drone carries a Jetson Orin Nano and a camera. Most of the networking drone flight controller can be reused: the processor block (ESP32-S3, crystal, flash, USB-C, antenna circuit), the gyro, barometer, GPS, ESC connector, LEDs, test pads and ports. The KiCad project is in [`pcb/network-drone-fc/`](pcb/network-drone-fc/) and every pin is listed in [`docs/hardware-reference.md`](docs/hardware-reference.md).

- [ ] Collect requirements: camera, Jetson power mode, battery voltage, frame and ESC size
- [ ] Power for the Jetson: it draws 7 to 25 W depending on its power mode, far more than the flight controller's 2 A buck. Plan a separate supply sized for it
- [ ] A serial link from the flight controller to the Jetson. The networking drone board has no free UART, so the pin plan changes here
- [ ] If the battery is 3S or 4S: change surge diode D5 from SMAJ12A to SMAJ18A, recheck the battery divider, and pick a charger chip that handles that cell count (the BQ25887 is 2S only)
- [ ] Power management and charging board for the mapping drone
- [ ] Schematic
- [ ] Layout

## Pranav and Rishab: ground station PCBs

What the ground station needs:

| Requirement | Plan |
|---|---|
| RTK GPS | A ZED-F9P base, plus a MAX-M10S beside it, the same receiver the drones carry. See "Getting the drones home" below |
| Mesh radio | A VoCore2, the same module as on the drones, on the same 802.11s mesh |
| Strong radio | An external 2.4 GHz antenna, 5 to 8 dBi, on the VoCore2's U.FL socket through a pigtail, mounted high |
| Compute | Anyone's laptop, beside the station on its own battery, so the station does not power it. It joins a Wi-Fi network the station's VoCore2 runs alongside the mesh. An RJ45 jack on the station board is the backup for heavy mapping data, since Wi-Fi to the laptop shares airtime with the mesh. The VoCore2's USB is host only, so a laptop cannot plug into it by USB |
| Charging | Four docks to start. A dock charging board powers the charging walls; see the charging concept below |
| Power | Wall outlet or battery for outdoor use, through one input; see "Power" below |

### Getting the drones home

The drones' GPS, the MAX-M10S, is a single-band receiver, so it cannot reach centimetre RTK accuracy. The station helps it three ways at once, and the drone uses whichever is working:

1. **Corrections to the drones.** The F9P base sends RTCM corrections over the mesh. Newer M10 firmware accepts them for about 0.5 to 1 m. Check that the drones' MAX-M10S firmware supports RTCM input.
2. **The station's own M10 error.** The station knows exactly where its M10 sits, from the F9P, so it measures that M10's error and sends it to the drones. Each drone subtracts it from its own reading. Receivers of the same type close together see nearly the same error, which leaves about 0.5 to 1.5 m.
3. **Direct comparison.** The drone's position is compared with the F9P's. This is the fallback, good to about 1 to 3 m.

That gets a drone to the right dock to within about a metre. The last metre uses a rod or post on the station as a target for the forward TF-Luna. The TF-Luna only measures distance along a narrow beam (about 2°), not direction, so the drone yaws slowly and takes the heading with the shortest distance as the bearing to the post. Make the target wide enough to catch the beam, a flat plate or a post of a few centimetres rather than a thin rod. The downward TF-Luna holds the height, and the shape of the walls guides the guard the last few centimetres.

Centimetre RTK on the drones would need a dual-band receiver such as the ZED-F9P. Keeping the F9P on the station leaves that open for a later revision.

- [ ] RTK base: ZED-F9P with a survey-style antenna, surveyed in when the station is set up
- [ ] A MAX-M10S at the station beside the F9P antenna, to measure the error the drones see
- [ ] Software at the station that sends the RTCM corrections and the M10 error over the mesh
- [ ] Check the drones' MAX-M10S firmware for RTCM input
- [ ] Docking target on the station for the forward TF-Luna; agree its size and position with Jadon

### Power

With the laptop on its own battery, the station's load is small:

| Load | Power |
|---|---|
| Four drones charging at once, each charger capped at 0.925 A from 5 V | about 18.5 W |
| VoCore2, ZED-F9P, MAX-M10S, a small processor for the station | about 2.5 W |
| Total from the input, with about 90 % converter efficiency | about 23 W |

Recharging one drone takes about 10 Wh (an 8 Wh pack plus losses), and a flat pack takes a little over two hours. Running all four docks flat out for three hours uses about 70 Wh. A 100 Wh battery covers a three-hour session with margin.

The plan is one DC input that either the wall or a battery feeds:

- USB-C power delivery at 20 V and at least 45 W. A wall USB-C charger and a USB-C power bank or power station then use the same socket and cable. The station board needs a USB-C PD sink controller for this (STMicroelectronics STUSB4500, or TI's TPS25730)
- Optionally a 12 V barrel jack as a second input, joined to the first through an ideal-diode controller (such as TI's LM74700) so either one can power the station
- Outdoor battery: a bought USB-C PD power bank of about 100 Wh (the airline limit, if the station ever travels), or a small power station of 250 Wh or more for long days. A custom pack is not needed at this load

- [ ] Agree the battery with the team: a 100 Wh USB-C PD bank or a small power station
- [ ] Input stage on the station board: USB-C PD sink at 20 V, optional 12 V jack, ideal-diode joining
- [ ] A station processor, reusing the flight controller's ESP32-S3 block, to read the F9P and the M10, switch and monitor the four docks, and talk to the VoCore2 over UART1. The VoCore2's UART2 is its console and UART0's TX is a start-up mode pin, so neither is free for this

### Charging and radio

- [ ] Dock charging board: a 5 V buck rated 5 A or more from the 20 V input, then one current-limited switch per dock (about 1.5 A each, four docks), so a short across the walls trips that dock only and recovers by itself
- [ ] Set the wall voltage to about 5.2 to 5.4 V, to cover the loss in the spring contacts while staying under the drone eFuse's 6.0 V cut-off
- [ ] Radio board or mount for the VoCore2 and the external antenna, plus a backup RJ45 jack and its magnetics on the VoCore2's Ethernet port
- [ ] Agree the dock current and the connector to the walls with Jadon

## Jadon: ground station

- [ ] Ground station CAD
- [ ] Space and rails for charging

## Charging concept

The plan: a conductive material on the outside of the propeller guard, and the ground station's walls spring against it when the drone docks. One side of the drone is 5 V and the other is ground, so each dock has a 5 V wall and a ground wall. A drone docked the wrong way round is not damaged: its eFuse blocks the reversed voltage, and it just doesn't charge.

That one idea crosses three people's work, so these points need an agreed answer:

| Question | Who it touches |
|---|---|
| Which part of the guard is positive and which is ground, and how the drone is kept from docking the wrong way round | Daniel, Jadon, Rishab |
| The size, spacing and position of the contacts on the guard, so they line up with the rails | Daniel, Jadon |
| What voltage and current the walls supply | Pranav, Rishab, Jadon |
| How the wire gets from the guard contacts to the charging board | Daniel, Rishab |
| What stops the two exposed contacts from shorting on something metal in flight or in the case | Rishab |
| How the drone knows it is seated, which is what the charger's power-good line on J7 pin 5 is for | Rishab, Pranav |

## Reference

- Every connector and pin on the flight controller: [`docs/hardware-reference.md`](docs/hardware-reference.md)
- Whole-drone parts list with weights and prices: [`docs/parts-list.md`](docs/parts-list.md)
- How the flight controller gets tested: [`docs/pcb-test-plan.md`](docs/pcb-test-plan.md)
- How the frame gets tested: [`docs/frame-test-plan.md`](docs/frame-test-plan.md)

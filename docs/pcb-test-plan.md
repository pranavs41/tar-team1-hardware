# PCB test plan

How we find out whether the flight controller works. A board cannot be proven before it is built, so the plan removes risk in three stages: checks on the design files, checks on the bench, and checks in flight.

## Stage 1: before ordering

Checks that software can run, all passing as of 2026-10-11:

| Check | What it proves | State |
|---|---|---|
| Electrical rules check | no unconnected or conflicting pins in the schematic | done, 0 errors |
| Design rules check | nothing shorts, and the spacing is something the fab can build | done, 0 errors |
| Schematic against board, pin by pin | the board is the circuit that was drawn | done, all 296 pins match |
| Power budget | regulators, tracks and connectors are sized for the load | done, see [power-budget.md](power-budget.md) |

Checks that software cannot run. These are where first boards usually fail, and none of them is done yet:

- [ ] **Footprint and pinout audit.** Compare every chip's footprint with its datasheet: pin 1 position, pin order, pad size and spacing. A footprint that does not match the real part passes every automatic check and still gives a dead board.
- [ ] **Antenna trace impedance.** The Wi-Fi and GPS traces are 0.3 mm wide. Calculate the width that gives 50 Ω on the fab's 4-layer stack and adjust if it differs.
- [ ] **ESC connector pinout.** Confirm the real ESC's pin order against J4, and whether it drives the current and telemetry pins.
- [ ] **Paper test.** Print the board at 1:1 and lay the real parts on the pads.
- [ ] **Second reader.** A teammate checks the schematic against the manufacturers' reference designs.
- [ ] **Fab check.** Upload the gerbers to the fab's online checker before paying.

## Stage 2: on the bench

The step-by-step list is [bring-up.md](bring-up.md). Its order matters: each step protects the next one.

| Step | Why it comes here |
|---|---|
| Look for solder bridges | cheapest fault to find, most expensive to power up |
| Measure each rail to ground with no power | finds shorts before they can burn anything |
| Power from a bench supply with a 100 mA limit | a fault trips the limit instead of destroying a chip |
| Measure the four rails | proves the regulators work before anything depends on them |
| Connect USB | proves the processor is alive and can be flashed |
| Read each sensor's ID | the only proof that the hidden solder joints under a chip took |
| GPS, ports, radio, heat | one new thing at a time, so a failure points at one cause |
| Motors, props off | last, because it is the only step that can hurt someone |

Tools: a multimeter, a bench supply with a current limit, a USB-C cable, and a thermocouple or infrared thermometer. An oscilloscope helps for the 5 V rail and the motor signals.

- [ ] **Test firmware.** The checklist needs a small program that blinks the LEDs, reads each sensor's ID, prints GPS data, talks over both ports and spins each motor. It does not exist yet.

## Stage 3: in use

Things that only show on a finished drone:

- [ ] Wi-Fi range with the real antenna, compared with a known-good ESP32 board
- [ ] GPS time to first fix, outdoors
- [ ] Gyro noise with the motors running
- [ ] Temperature of regulator U4 after ten minutes of Wi-Fi traffic
- [ ] The 5 V rail during a full-throttle punch on a nearly empty battery

## Is the routing efficient?

There is no single score for routing. What can be measured:

| Measure | Value |
|---|---|
| Design rule errors | 0 |
| Vias | 159: about half tie ground together, 14 feed the 3.3 V plane, the rest carry signals |
| Typical track length | 22% longer than a straight line between its pads |
| Right-angle or sharper corners | 0 |
| Ground plane | one unbroken layer under the whole board |

At this board's speeds, the length of an ordinary track makes no measurable difference. Four areas are sensitive to layout: the antenna traces, the crystal, the buck regulator's switching loop, and noise reaching the gyro. Those were routed by hand from the manufacturers' layout guidance. Only the stage 2 and stage 3 measurements can say whether they were done well enough.

## What to expect

Order five boards, build one or two, and plan for a revision B. For a first board with a bare radio chip, a second revision is normal.

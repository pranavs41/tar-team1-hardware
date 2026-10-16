# PCB test plan

How we find out whether the flight controller works. A board cannot be proven before it is built, so the plan removes risk in three stages: checks on the design files, checks on the bench, and checks in flight.

## Stage 1: before ordering

Checks KiCad runs by itself, all passing as of 2026-10-11:

| Check | What it proves | State |
|---|---|---|
| Electrical rules check | no unconnected or conflicting pins in the schematic | done, 0 errors |
| Design rules check | nothing shorts, and the spacing is something the fab can build | done, 0 errors |
| Schematic against board, pin by pin | the board is the circuit that was drawn | done, all 305 pins match |
| Power budget | regulators, tracks and connectors are sized for the load | done, see [power-budget.md](power-budget.md) |

Further checks run on 2026-10-11. The results are in the next section.

- [x] **Pinout audit.** Every chip's schematic pins compared with the pin functions in its datasheet.
- [x] **Footprint pitch.** Pad spacing of every chip and connector measured on the board against the package's nominal pitch.
- [x] **Antenna trace impedance.** Calculated for the fab's 4-layer stack.
- [x] **Fab capability.** Track widths, via sizes, hole spacing, solder mask strips and silkscreen text against JLCPCB's limits.
- [x] **Gerber export.** All layers, drill files and the placement file export without errors.
- [x] **Circuit calculations.** Crystal loading, I2C rise time, battery divider, LED currents, regulator headroom, voltage ratings.

Checks that still need a person and the real parts:

- [ ] **Pad shapes and pin 1 orientation.** The audit above proves the pin numbers and the pitch. It does not prove each pad is the right length and width, or that pin 1 sits on the correct corner. Compare each footprint with the land pattern drawing in its datasheet.
- [x] **ESC connector pinout.** Checked against the seller's picture on 2026-10-12. The ESC's order is −, +, 1, 2, 3, 4, N, C, which did not match, so J4 was changed to it. Still to do with the real part: confirm with a multimeter which end of the cable is pin 1.
- [ ] **Paper test.** Print the board at 1:1 and lay the real parts on the pads.
- [ ] **Second reader.** A teammate checks the schematic against the manufacturers' reference designs.
- [ ] **Fab check.** Upload the gerbers to the fab's online checker before paying.

## Results of the 2026-10-11 run

| Check | Result |
|---|---|
| Electrical rules check | 0 errors, 0 warnings |
| Design rules check | 0 errors. Five courtyard overlaps remain, all explained in the decision log |
| KiCad's schematic parity check | 2 items left, both expected: the USB socket's two locating pegs are tied to ground on the board and have no schematic pin |
| Schematic against board, pin by pin | 305 pins, 0 differences |
| Pinout audit | 11 parts checked, all correct: ESP32-S3, buck, both regulators, IMU, barometer, GPS, USB protection, crystal, ESC connector, TVS |
| Footprint pitch | 13 parts checked, all within 0.03 mm of nominal |
| Narrowest track | 0.15 mm, against a fab minimum of 0.09 mm |
| Vias | 0.3 mm hole with a 0.15 mm ring, against minimums of 0.3 and 0.13 mm |
| Closest two holes | 0.26 mm wall to wall, against a minimum of 0.25 mm |
| Thinnest solder mask strip | 0.20 mm, against a minimum of about 0.1 mm |
| Gerber export | 11 layers, 2 drill files, placement file with 71 parts |
| Antenna traces | about 56 Ω by calculation, against a 50 Ω target |
| Crystal loading | 9.5 to 11.5 pF, against the crystal's 10 pF |
| Battery divider | 0.55 to 1.53 V on the ADC pin across 2S empty to 4S full, against a 3.1 V limit |
| LED currents | 1.3 mA each |
| I2C rise time | 93 ns on the board alone with the 2.2 kΩ pull-ups. About 370 ns with both sensors and the charging board attached, which is over the 300 ns limit for 400 kHz and well inside the 1000 ns limit for 100 kHz |

Three things from this run are worth knowing.

**One problem was found and fixed.** A ground via sat 0.20 mm from the USB socket's mounting slot, under the fab's 0.25 mm. KiCad's own check does not compare vias against slots, so it had passed. The via moved 0.06 mm and now clears by 0.26 mm.

**The antenna traces are close enough.** A 0.3 mm trace on this stack works out near 56 Ω by the standard formula, and a result reported from JLCPCB's own calculator puts 50 Ω at about 0.29 mm, so the true value lies somewhere between 45 and 56 Ω. Each trace is under a fifth of a wavelength long, and at that length a mismatch of this size costs less than 0.1 dB. No change is needed. If the board is ever built on a different stack, recalculate.

**Run the I2C bus at 100 kHz.** Each cable adds capacitance, and with three of them (two sensors and the charging board) the signal edges are too slow for 400 kHz even with the 2.2 kΩ pull-ups now fitted. At 100 kHz the limit is 1000 ns and there is plenty of margin. The cable capacitance in this calculation is a cautious guess, so measure the real rise time with an oscilloscope at bring-up.

The checks were run again the same day after the charging connector grew to seven pins and the landing sensor port was added. The numbers in the table are from that second run.

The board checks were run a third time on 2026-10-12, after the USB socket's mounting slots were lengthened by 0.4 mm and six tight spots were opened up. The design rules check still shows 0 errors, at the board's own 0.12 mm spacing and at 0.127 mm. The longer slots came within 0.18 mm of the same ground via, so it moved again and the closest two holes are back at 0.26 mm. The green LED is now a 2.0 to 2.4 V type and draws 2 to 3 mA; the red and yellow stay at 1.3 mA.

On 2026-10-13 the board was checked against OSH Park's published limits for its four-layer service, and three small changes followed. Four connector tab pads were trimmed by up to 0.09 mm so that no copper is closer than 0.38 mm to the board edge. The copper rings around the four USB slots were widened to 0.12 mm. Every part in the parts list was also compared with the footprint on the board, by package and by count, and with the polarity of the diodes, LEDs and the large capacitor: all 69 match, and the three empty footprints (C14, C15, L3) are the only ones without a part. Pad shapes were not compared against each datasheet's drawing; the paper test above covers that.

On 2026-10-13 every track on the board was redrawn as horizontal, vertical and 45 degree runs. 206 of the 552 segments had run at other angles. Each was split into straight and 45 degree pieces between the same two ends, with the design rules check choosing which way each bend went; the last twelve were rerouted. The board still passes the design rules check with 0 errors at 0.12 mm and at 0.127 mm, with nothing unconnected, and the schematic and board still match pin for pin. Two 90 degree corners remain, on short stubs beside the processor where a 45 degree corner would come too close to the next pin.

The same day a per-branch current check was added, [`tools/current_check.py`](../tools/current_check.py). It traces each power path through the real copper, from the regulator or connector to each load, and checks every track and via against the current of the branches it carries. All 179 pieces on those paths are inside their rating at the average current. The highest is the USB input at 59%, which only matters on the bench. The largest voltage drops at peak current are 96 mV on the USB input, 23 mV to the networking module and 11 mV from the battery to the 5 V regulator.

On 2026-10-14 the long diagonal runs were straightened. About 30% of the track length on each layer had run at 45 degrees across the board. Each diagonal run longer than 0.6 mm became a horizontal and a vertical leg with a small 45 degree chamfer at the corner, and the longest few were given L or Z shapes where a simple corner would not fit. Diagonal track is now 16% of the length on the top layer and 10% on the bottom, almost all of it short corner chamfers. The remaining runs over 1 mm add up to 21 mm, mostly where a track follows the board's rounded corners. At the same time the board's own spacing rule was raised from 0.12 mm to OSH Park's 0.127 mm, so every check now enforces the fab's limit directly. The design rules check shows 0 errors, nothing is unconnected, the schematic and board match, and the current check passes on all 275 pieces of copper on the power paths.

Later on 2026-10-14, after the datasheet audit, four changes went in: the battery cut-off (R14, R15, and C16 down to 0805), three supply capacitors under the processor (C37 to C39), and the 24 nH crystal inductor L4. The checks were run again. The electrical rules check shows 0 errors. The design rules check shows 0 errors at 0.127 mm, with nothing unconnected and the same seven accepted courtyard overlaps. The schematic and board match, apart from the USB socket's two pegs as before. The current check passes on all 273 pieces of copper on the power paths.

### Pre-order review, 2026-10-16

Six separate reviews went over the board before ordering: the processor and its radio, crystal and USB; power and current; the sensors and GPS; every connector against the device on the other end; every footprint against the land pattern of the part number being bought; and the fab rules and order files. None found anything that would stop the board working. They found these, which were fixed:

- Copper had been poured 0.30 mm from the board edge, under OSH Park's 0.381 mm. It now stops at 0.45 mm.
- C33 would have stopped the radio's UART. It is now not fitted.
- The stencil had paste openings on the four empty footprints. They are gone.
- The radio supply had no 10 µF near the processor. C40 adds one.
- A via inside one of the gyro's pads would have drained its solder. It moved off the pad.
- D5's battery pad sat 0.19 mm from a motor pin of J4. It is now 0.54 mm.
- Silkscreen is now clipped at pad openings, and the plot settings no longer add drill marks.

After the fixes the electrical rules check shows 0 errors. The design rules check shows 0 errors at 0.127 mm, with nothing unconnected and the same seven accepted courtyard overlaps. The schematic and board match, and the current check passes on all 273 pieces of copper on the power paths.

What was left for rev B is listed in the decision log. Also from the review, for the build rather than the board:

- Wire the charging board's battery leads to the ESC's battery pads.
- Pull the C and N wires from the ESC cable on the networking drone.
- Remove the compass breakout's pull-up resistors.
- Wire the Pololu cables by pin number, not colour.

Two unused GPS pins were also confirmed against the u-blox integration manual: V_BCKP and VIO_SEL are both meant to be left open in a 3.3 V design with no backup battery.

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
| Vias | 163: about half tie ground together, 14 feed the 3.3 V plane, the rest carry signals |
| Typical track length | 22% longer than a straight line between its pads |
| Right-angle or sharper corners | 0 |
| Ground plane | one unbroken layer under the whole board |

At this board's speeds, the length of an ordinary track makes no measurable difference. Four areas are sensitive to layout: the antenna traces, the crystal, the buck regulator's switching loop, and noise reaching the gyro. Those were routed by hand from the manufacturers' layout guidance. Only the stage 2 and stage 3 measurements can say whether they were done well enough.

## What to expect

Order five boards, build one or two, and plan for a revision B. For a first board with a bare radio chip, a second revision is normal.

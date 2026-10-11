# Frame test plan

How to find out whether a printed frame is good enough to fly, using a table, a clamp, some weights and the flight controller itself. Run the tests in order. The early ones need only the bare frame, so a bad design is caught before any electronics go on it.

## What the frame has to survive

These numbers are estimates. Replace them once the parts are weighed and the motor's thrust table is checked.

| Load | Rough size |
|---|---|
| Whole drone weight | 130 to 150 g |
| Thrust per motor in hover | about 35 g |
| Thrust per motor at full throttle | 150 to 200 g |
| Crash | many times the drone's weight, for a few milliseconds |

Stiffness matters more than strength. A frame that survives but flexes shakes the gyro, and a shaking gyro makes the drone hard to tune. If a stiffness test fails, fix that before looking at crash strength.

## Before printing: simulate it

SolidWorks has a built-in stress simulation. Fix the four centre mounting holes, apply the full-throttle thrust upward at each motor mount, and look at where the stress concentrates.

Two cautions when reading the result:

- Printed plastic is weaker between layers than within them, often about half the strength of the solid material. Either enter reduced material values or treat the simulation as a map of weak spots, not as a pass or fail.
- Print orientation decides where the part breaks. Arms should be printed so the layers run along the arm, not across it.

## Tests on the bare frame

| # | Test | How | Pass |
|---|---|---|---|
| 1 | Arm bending | Clamp the centre of the frame to a table. Hang 500 g from one motor mount, which is full thrust with a safety factor of about 3. Measure how far the tip moves with calipers or a ruler. Repeat on every arm. | Tip moves less than about 1 mm, springs fully back when the weight comes off, no cracking sounds |
| 2 | Arm twist | Same clamp. Push sideways on a motor mount with a known weight, so the arm twists along its length. | Very little twist. Twist shows up in flight as wobble and poor yaw control |
| 3 | Screw holes | Fit and remove the motor screws and the M3 stack screws five times each. | Threads or inserts still hold, no cracks around the holes |
| 4 | Battery holder | Fit a battery or a 45 g dummy. Pull on it with about ten times its weight, roughly 450 g, then shake the frame hard by hand. | Battery does not shift or come out |

## Tests with weight on board

| # | Test | How | Pass |
|---|---|---|---|
| 5 | Drop | Fit dummy weights where the battery, motors and boards will sit, so the frame carries its real flying weight. Drop it from 1 m onto a hard floor, flat, on an arm tip, and on a prop guard. Repeat from 2 m. | No cracks, especially between print layers, at arm roots and around screw holes |
| 6 | Charging contacts | Slide the prop guard into the ground station rails 50 to 100 times. | Contact is made every time, and the conductive material has not worn through or peeled |

## Tests on the finished drone

Props on, drone strapped firmly to a bench, safety glasses, nobody in line with the propellers.

| # | Test | How | Pass |
|---|---|---|---|
| 7 | Tied-down throttle | Raise the throttle slowly to full and hold for 30 seconds. | Nothing loosens, no visible arm flex, motor mounts stay cool enough to touch afterwards |
| 8 | Vibration | During the same run, log the gyro from the flight controller while sweeping the throttle from idle to full. | No sharp peak in the gyro noise at any throttle. A peak means part of the frame resonates at that motor speed |

For test 8, the motors spin up to roughly 59,000 rpm on a full 2S battery, which is about 1 kHz. Hover sits around half of that. A frame resonance anywhere in the range the motors pass through will show as a spike in the log.

## If a test fails

| Symptom | Usual fix |
|---|---|
| Arm bends or twists too much | thicker arm, a deeper cross-section, more wall layers, or a stiffer material |
| Cracks between layers | change the print orientation, raise the print temperature, add walls |
| Cracks at screw holes | add material around the hole, use heat-set threaded inserts |
| Motor mount softens | the material is too close to its softening point. PLA softens near 60 °C; use PETG or nylon |
| Resonance peak | stiffen that arm, or add a soft mount between the frame and the flight controller stack |

Materials, from least to most suitable: PLA is stiff but brittle and softens with heat. PETG is tougher and handles heat better. Nylon or carbon-filled filament is the strongest and stiffest if the printer can run it.

## Record

Keep one row per frame version so the next print has something to beat.

| Frame version | Material | Weight | Arm deflection at 500 g | Drop result | Resonance | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

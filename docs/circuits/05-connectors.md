# 5. Connectors

Everything that leaves the board goes through one of these. The ESC connector is the only one that carries real current; the rest are small signal ports.

## ESC (J4, JST-SH 8 pin)

The flight controller stacks on a bought 20 × 20 mm 4-in-1 ESC, and this one cable carries everything between them.

| Pin | Net | What it is |
|---|---|---|
| 1 | GND | |
| 2 | VBAT | battery voltage, the board's only power input |
| 3 | ESC_CUR | current sense, an analog voltage from the ESC (shared with the radio port, see J6) |
| 4 | ESC_TELEM | ESC telemetry, a UART signal into the ESP32 (shared with the radio port, see J6) |
| 5 to 8 | MOTOR1 to MOTOR4 | DShot signals out to the four motors |

This is the pin order most Betaflight-style 4-in-1 ESCs use (GND, VBAT, current, telemetry, M1 to M4), but there is no standard that forces it. Check the pinout printed on the ESC you buy before ordering boards; if it differs, the labels on J4's pins in the schematic are the only thing to change.

The board has no battery connector of its own. VBAT arrives here from the ESC's battery pads, which is why the TVS and the buck's input capacitor sit close to this connector on the PCB.

Solder a low-ESR electrolytic capacitor, 470 µF 35 V, across the ESC's battery pads, as close to the pads as the leads allow. Every commercial build does this and most ESC manuals require it. The motors draw current in sharp pulses and throw voltage spikes back when they brake; the capacitor soaks those up at the source, before they reach the FC's VBAT line and show up as gyro noise. The FC carries its own 100 µF polymer capacitor (C35) and the TVS as the second line, but a bigger capacitor at the ESC is still the right first line. Keep the capacitor's leads short and its polarity right: on an electrolytic the stripe is the negative lead.

C33 (100 nF from ESC_CUR to GND) smooths the current-sense signal before it reaches the ESP32's ADC on GPIO2, the same job the 100 nF does on the battery divider. Leave C33 off the board when the radio port J6 is in use, because that same line then carries UART data and 100 nF would round its edges.

## Sensor port (J5, JST-GH 4 pin, 5 V I2C)

Pins: 5 V, SCL, SDA, GND. This is the port for the obstacle sensor, a Benewake TF-Luna, which mounts at the front of the drone on a cable.

The power pin is 5 V, not 3.3 V. The TF-Luna needs 3.7 to 5.2 V, so the pin was moved from the 3.3 V rail to the 5 V rail. The two signal pins did not change: I2C is an open-drain bus, which means nothing on it ever drives a line high. Devices only pull the lines low, and the 4.7 kΩ pull-ups near the barometer lift them back to 3.3 V. So the bus sits at 3.3 V no matter what voltage the sensor runs on, and the TF-Luna's signal pins are 3.3 V parts anyway.

The warning that comes with this: do not plug a 3.3 V-only device into J5. Its power pin would see 5 V.

The TF-Luna starts up in UART mode. Tying its pin 5 to ground selects I2C, so the cable does that:

| J5 pin | Signal | TF-Luna pin |
|---|---|---|
| 1 | 5 V | 1 (+5V) |
| 2 | SCL | 3 (TXD/SCL) |
| 3 | SDA | 2 (RXD/SDA) |
| 4 | GND | 4 (GND) and 5 (mode select) |

Pin 6 of the sensor stays unconnected. Its I2C address is 0x10, which does not collide with the barometer. The sensor draws about 70 mA on average and 150 mA in peaks.

## Radio port (J6, JST-SH 4 pin, top entry, 5 V UART)

Pins: 5 V, TX, RX, GND. This is the port for the networking module, a VoCore2, which is a small Linux router that carries the drone-to-drone Wi-Fi link. It needs 4.5 to 5.5 V at up to about 0.4 A on startup, and its UART pins are 3.3 V, the same as the ESP32's.

| J6 pin | Signal | ESP32 | Connects to on the VoCore2 |
|---|---|---|---|
| 1 | 5 V | | power in |
| 2 | TX, flight controller to radio | GPIO2 | a UART RX pin |
| 3 | RX, radio to flight controller | GPIO10 | a UART TX pin |
| 4 | GND | | ground |

The connector points straight up from the board, in the bottom-right corner. Every edge of the board already has a side-entry connector on it, and a top-entry part is the only kind that fits in the corner that was left. Its outline comes within 2.8 mm of the H3 hole centre, 0.2 mm inside the 3 mm keep-out, but its body and pads are more than 3.3 mm away, so a 6 mm grommet or nut still clears it.

The two data lines are shared with the ESC connector. J6 pin 2 is the same net as J4 pin 3 (ESC_CUR), and J6 pin 3 is the same net as J4 pin 4 (ESC_TELEM). The reason is the ESP32 package: a via only fits beside every other pin, every usable escape was already taken, and the two free pins that remained are boxed in by the motor signals. These two lines already ran to that corner of the board, and small 8-bit ESCs like the one the team chose have no current-sense or telemetry output, so on this build they would have gone unused.

That makes it one or the other per drone:

- If the ESC has no current or telemetry output (the expected case), plug the radio into J6 and leave C33 off.
- If a future ESC does drive those two pins, leave those two wires out of the ESC cable when the radio is fitted. Two outputs on one wire would fight each other.

Firmware sets GPIO2 as a UART transmit pin and GPIO10 as a UART receive pin. Any ESP32-S3 pin can take any UART signal, so nothing else changes.

The sensor port and the charging port use the Dronecode connector order (VCC, signal, signal, GND), so off-the-shelf JST-GH cables fit them.

## Charging board port (J7, JST-GH 4 pin)

Pins: GND, DOCK_DET, AUX_ADC, spare.

- DOCK_DET goes to GPIO9. The charging board pulls it to a definite level when the drone is docked; firmware can enable the ESP32's internal pull-up and treat low as docked.
- AUX_ADC goes to GPIO8, which is on ADC1 so it keeps working while Wi-Fi is on. Whatever the charging board puts here must stay under 3.1 V. C34 (100 nF to GND) steadies the reading.

Protection for these two lines lives on the charging board, by agreement with that team.

On the board this port sits at the top right, in a 3 mm strip added above the mounting-hole line. Before that strip existed the connector body was 1.5 mm from the H2 hole, which left no room for the ESC's grommet or a nut on top; now it clears the hole centre by 5 mm.

## Test points and recovery pads

Seven bare pads on the bottom of the board, each sitting on a via of its net. TP1 and TP2 are UART0 TX and RX, the fallback console and flashing path if USB fails. TP3 to TP6 are VBAT, +5V, +3V3 and +3V3_SENS for checking the rails during bring-up. TP13 is I2C SCL, handy for confirming the bus is alive when the barometer or the port does not answer.

The first layout had eighteen pads, one for every bus line. Routing showed there was no room for most of them: a pad needs a clear 1 mm circle on the bottom copper, and the bottom layer around the ESP32 is full of motor and USB tracks. The IMU SPI lines, SDA, the GPS UART, ESC telemetry and the spare UART lost their pads. They can still be probed on the component pads themselves with a fine tip.

JP1 (RESET) and JP2 (BOOT) are pairs of pads, one on the signal and one on GND, in place of pushbuttons. Shorting a pair with tweezers does what the button would have. USB flashing resets the chip by itself, so these only matter for recovering a board whose firmware has crashed the USB port: short BOOT, short and release RESET, release BOOT.

They are all on the bottom because there is nothing to solder there, so they don't affect the single-side hot-plate assembly.

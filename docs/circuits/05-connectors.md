# 5. Connectors

Everything that leaves the board goes through one of these. The ESC connector is the only one that carries real current; the rest are small signal ports.

## ESC (J4, JST-SH 8 pin)

The flight controller stacks on a bought 20 × 20 mm 4-in-1 ESC, and this one cable carries everything between them.

| Pin | Net | What it is |
|---|---|---|
| 1 | GND | |
| 2 | VBAT | battery voltage, the board's only power input |
| 3 to 6 | MOTOR1 to MOTOR4 | DShot signals out to the four motors |
| 7 | ESC_TELEM | the ESC's "N" pad (shared with the radio port, see J6) |
| 8 | ESC_CUR | current sense, an analog voltage from the ESC's "C" pad (shared with the radio port, see J6) |

This is the order printed on the team's ESC: −, +, 1, 2, 3, 4, N, C. The board first used the order most Betaflight-style ESCs use (GND, VBAT, current, telemetry, M1 to M4). There is no standard that forces either one, which is why the pinout was checked against the real ESC before ordering boards, and the board was changed to match.

With the networking module fitted, pull the C wire out of the ESC cable. The N pad is labelled "No Output" by the seller, so its wire does nothing and can stay. Pin 8 is the line the ESP32 transmits on to the module, and the ESC's current output would fight it. Before the first power-up, check with a multimeter that the cable brings the ESC's − to pin 1 and + to pin 2.

The board has no battery connector of its own. VBAT arrives here from the ESC's battery pads, which is why the TVS and the buck's input capacitor sit close to this connector on the PCB.

Solder a low-ESR electrolytic capacitor, 470 µF 35 V, across the ESC's battery pads, as close to the pads as the leads allow. Every commercial build does this and most ESC manuals require it. The motors draw current in sharp pulses and throw voltage spikes back when they brake; the capacitor soaks those up at the source, before they reach the FC's VBAT line and show up as gyro noise. The FC carries its own 100 µF polymer capacitor (C35) and the TVS as the second line, but a bigger capacitor at the ESC is still the right first line. Keep the capacitor's leads short and its polarity right: on an electrolytic the stripe is the negative lead.

C33 (100 nF from ESC_CUR to GND) smooths the current-sense signal before it reaches the ESP32's ADC on GPIO2, the same job the 100 nF does on the battery divider. Leave C33 off the board when the radio port J6 is in use, because that same line then carries UART data and 100 nF would round its edges.

## Sensor port (J5, JST-GH 4 pin, 5 V I2C)

Pins: 5 V, SCL, SDA, GND. This is the port for the obstacle sensor, a Benewake TF-Luna, which mounts at the front of the drone on a cable.

The power pin is 5 V, not 3.3 V. The TF-Luna needs 3.7 to 5.2 V, so the pin was moved from the 3.3 V rail to the 5 V rail. The two signal pins did not change: I2C is an open-drain bus, which means nothing on it ever drives a line high. Devices only pull the lines low, and the 2.2 kΩ pull-ups near the barometer lift them back to 3.3 V. So the bus sits at 3.3 V no matter what voltage the sensor runs on, and the TF-Luna's signal pins are 3.3 V parts anyway.

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

The two data lines are shared with the ESC connector. J6 pin 2 is the same net as J4 pin 8 (ESC_CUR), and J6 pin 3 is the same net as J4 pin 7 (ESC_TELEM). The reason is the ESP32 package: a via only fits beside every other pin, every usable escape was already taken, and the two free pins that remained are boxed in by the motor signals. These two lines already ran to that corner of the board, and the networking drone has no use for the ESC's current reading. The team's ESC does have a current pad ("C"), which is why its wire comes out of the cable on a drone that carries the networking module.

That makes it one or the other per drone:

- If the ESC has no current or telemetry output (the expected case), plug the radio into J6 and leave C33 off.
- If a future ESC does drive those two pins, leave those two wires out of the ESC cable when the radio is fitted. Two outputs on one wire would fight each other.

Firmware sets GPIO2 as a UART transmit pin and GPIO10 as a UART receive pin. Any ESP32-S3 pin can take any UART signal, so nothing else changes.

The sensor port uses the Dronecode connector order (VCC, signal, signal, GND), so off-the-shelf JST-GH cables fit it.

## Charging board port (J7, JST-SH 7 pin)

Pins: BATT+, GND, SDA, SCL, /PG, STAT, CD. The charging board carries a BQ25887, a chip that charges a 2S battery from a 5 V dock and keeps the two cells balanced. Its design notes are in [charging-board.md](../charging-board.md).

What each line is for:

- **BATT+ and GND** power the flight controller from the battery. BATT+ joins the board's VBAT net, the same net the ESC connector feeds, so the board runs from whichever cable is plugged in. The pin is rated 1 A and the board draws 0.8 A at its worst, so this pin is for the flight controller only. Charge current, up to 2 A, must go from the charger to the battery on its own wires.
- **SDA and SCL** put the charger on the I2C bus. Over I2C the flight controller can read the battery and cell voltages, the charge current and any fault, and can change the charge settings.
- **/PG** (power good) goes to GPIO9. The charger pulls it low when it has good input power, which only happens on the dock, so this is also the "I am docked" signal.
- **STAT** goes to GPIO8. Low while charging, released when charging is done, blinking at 1 Hz on a fault. C34 (100 nF to GND) is left over from when this pin was an analog input. It does no harm here, since the signal changes at most once a second.
- **CD** (charge disable) comes from GPIO7. Driving it high stops the charger. If the ESP32 is in reset or unpowered the pin floats, and the charger's own pull-down keeps charging enabled, so a dead flight controller cannot block charging. Confirm that pull-down in the BQ25887 datasheet, and add a 100 kΩ resistor to ground on the charging board if it is not there.

/PG and STAT are open-drain, so they need a pull-up. Firmware enables the ESP32's internal ones. The I2C pull-ups are R12 and R13 on this board. That is why J7 has no 3.3 V pin.

Why seven pins and not the eight the charging board first listed: its eighth pin was a divided copy of the battery voltage. This board already measures VBAT on GPIO4, and with BATT+ wired in that is the same voltage. The ESP32 also had no pin left to read it with.

Why a JST-SH and not a JST-GH like the old port: a 7-pin JST-GH is 12 mm wide, and in this corner its body would sit on top of the GPS module's solder pads. The JST-SH is 9 mm wide and fits with room on both sides. Both families are rated 1 A per pin.

GPIO7 was one of the pins that had no way out from under the chip. Reaching it meant moving one existing track: the ESC telemetry line now dips to the top layer and passes between the two pads of R1, which freed the gap GPIO7 needed. The charge-disable track then runs on the bottom layer around the right side of the H2 mounting hole.

## Landing sensor port (J8, JST-SH 4 pin, top entry, 5 V I2C)

Pins: 5 V, SCL, SDA, GND, the same as J5. The swarm drones carry two distance sensors, one facing forward for obstacles on J5 and one facing down for landing on J8.

Both ports share one I2C bus, and two TF-Lunas both start at address 0x10. Before fitting them, connect one sensor by itself and send it the command that changes and saves its address (0x11 is free). After that the two can share the bus.

The bus now leaves the board on three cables: two sensors and the charger. Every cable adds capacitance, which slows the rising edge of the signal, because the only thing pulling a line high is a resistor. For that reason R12 and R13 dropped from 4.7 kΩ to 2.2 kΩ. With all three cables fitted the edges take about 370 ns, comfortable at 100 kHz, which allows 1000 ns, and too slow for 400 kHz, which allows 300 ns. So run this bus at 100 kHz.

The I2C tracks to J7 and J8 are long. They run on the bottom layer down the left edge and along the top edge, about 60 mm each. At 100 kHz that length does not matter.

## Test points and recovery pads

Eight bare pads on the bottom of the board, each sitting on a via of its net. TP1 and TP2 are UART0 TX and RX, the fallback console and flashing path if USB fails. TP3 to TP6 are VBAT, +5V, +3V3 and +3V3_SENS for checking the rails during bring-up. TP13 is I2C SCL, handy for confirming the bus is alive when the barometer or the port does not answer. TP14 is ground, for the meter's black lead; it sits on a ground via about 6 mm from the 3.3 V pad. Each pad has its signal name printed beside it.

The first layout had eighteen pads, one for every bus line. Routing showed there was no room for most of them: a pad needs a clear 1 mm circle on the bottom copper, and the bottom layer around the ESP32 is full of motor and USB tracks. The IMU SPI lines, SDA, the GPS UART, ESC telemetry and the spare UART lost their pads. They can still be probed on the component pads themselves with a fine tip.

JP1 (RESET) and JP2 (BOOT) are pairs of pads, one on the signal and one on GND, in place of pushbuttons. Shorting a pair with tweezers does what the button would have. USB flashing resets the chip by itself, so these only matter for recovering a board whose firmware has crashed the USB port: short BOOT, short and release RESET, release BOOT.

They are all on the bottom because there is nothing to solder there, so they don't affect the single-side hot-plate assembly.

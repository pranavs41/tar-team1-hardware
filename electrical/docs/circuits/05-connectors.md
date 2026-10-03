# 5. Connectors

Everything that leaves the board goes through one of these. The ESC connector is the only one that carries real current; the rest are small signal ports.

## ESC (J4, JST-SH 8 pin)

The flight controller stacks on a bought 20 × 20 mm 4-in-1 ESC, and this one cable carries everything between them.

| Pin | Net | What it is |
|---|---|---|
| 1 | GND | |
| 2 | VBAT | battery voltage, the board's only power input |
| 3 | ESC_CUR | current sense, an analog voltage from the ESC |
| 4 | ESC_TELEM | ESC telemetry, a UART signal into the ESP32 |
| 5 to 8 | MOTOR1 to MOTOR4 | DShot signals out to the four motors |

This is the pin order most Betaflight-style 4-in-1 ESCs use (GND, VBAT, current, telemetry, M1 to M4), but there is no standard that forces it. Check the pinout printed on the ESC you buy before ordering boards; if it differs, the labels on J4's pins in the schematic are the only thing to change.

The board has no battery connector of its own. VBAT arrives here from the ESC's battery pads, which is why the TVS and the buck's input capacitor sit close to this connector on the PCB.

Solder a low-ESR electrolytic capacitor, 470 µF 35 V, across the ESC's battery pads, as close to the pads as the leads allow. Every commercial build does this and most ESC manuals require it. The motors draw current in sharp pulses and throw voltage spikes back when they brake; the capacitor soaks those up at the source, before they reach the FC's VBAT line and show up as gyro noise. The FC carries its own 100 µF polymer capacitor (C35) and the TVS as the second line, but a bigger capacitor at the ESC is still the right first line. Keep the capacitor's leads short and its polarity right: on an electrolytic the stripe is the negative lead.

C33 (100 nF from ESC_CUR to GND) smooths the current-sense signal before it reaches the ESP32's ADC on GPIO2, the same job the 100 nF does on the battery divider.

## I2C port (J5, JST-GH 4 pin)

Pins: VCC (+3V3), SCL, SDA, GND. It shares the I2C bus with the barometer, so the 4.7 kΩ pull-ups near the BMP581 serve this port too and anything plugged in should not add its own strong pull-ups. This is the port for a downward-facing time-of-flight sensor if docking needs one.

Both the I2C port and the charging port use the Dronecode connector order (VCC, signal, signal, GND), so off-the-shelf cables fit.

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

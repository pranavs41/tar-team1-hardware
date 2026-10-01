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

C33 (100 nF from ESC_CUR to GND) smooths the current-sense signal before it reaches the ESP32's ADC on GPIO2, the same job the 100 nF does on the battery divider.

## I2C port (J5, JST-GH 4 pin)

Pins: VCC (+3V3), SCL, SDA, GND. It shares the I2C bus with the barometer, so the 4.7 kΩ pull-ups near the BMP581 serve this port too and anything plugged in should not add its own strong pull-ups. This is the port for a downward-facing time-of-flight sensor if docking needs one.

## UART port (J6, JST-GH 4 pin)

Pins: VCC (+5V), TX, RX, GND. TX is the ESP32's output (GPIO37) and RX its input (GPIO38). It runs on 5 V because the things likely to plug in, a telemetry radio or a companion computer, usually want 5 V.

Both the I2C and UART ports use the Dronecode connector order (VCC, signal, signal, GND), so off-the-shelf cables fit.

## Charging board port (J7, JST-GH 4 pin)

Pins: GND, DOCK_DET, AUX_ADC, spare.

- DOCK_DET goes to GPIO18. The charging board pulls it to a definite level when the drone is docked; firmware can enable the ESP32's internal pull-up and treat low as docked.
- AUX_ADC goes to GPIO8, which is on ADC1 so it keeps working while Wi-Fi is on. Whatever the charging board puts here must stay under 3.1 V. C34 (100 nF to GND) steadies the reading.

Protection for these two lines lives on the charging board, by agreement with that team.

## Test points

Six bare pads on the bottom of the board: UART0 TX and RX (TP1, TP2) for a fallback console and flashing path, and VBAT, +5V, +3V3, +3V3_SENS (TP3 to TP6) for checking the rails during bring-up. They are on the bottom because there is nothing to solder, so they don't affect the single-side hot-plate assembly.

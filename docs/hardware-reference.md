# Hardware reference: network drone flight controller, rev A

One page with every connector, pin, voltage and limit on the board. If you are wiring something to the flight controller or writing firmware for it, start here. The reasons behind each choice are in the [circuit guides](circuits/README.md) and the [decision log](design-decisions.md).

## The board

| | |
|---|---|
| Size | 36 mm wide × 39 mm tall, 1.6 mm thick, 2 mm corner radius |
| Mounting | four 3.2 mm holes for M3, on a 20 × 20 mm square, 8 mm in from the left, right and bottom edges and 11 mm from the top |
| Clear zone | nothing on the top side within 3 mm of a hole centre, so a 6 mm grommet, nut or standoff fits |
| Layers | 4: top signals and parts, solid ground, solid 3.3 V, bottom signals |
| Weight | about 8 g assembled (estimate, not weighed yet) |
| Processor | ESP32-S3FN8, bare chip, Wi-Fi and Bluetooth LE, 8 MB flash |
| Battery | 2S (6.0 to 8.4 V). The input parts tolerate up to 4S (16.8 V). Never 6S |
| Stacks on | a 20 × 20 mm 4-in-1 ESC, through one 8-pin cable |

## Connectors

| Ref | Where on the board | Type | For |
|---|---|---|---|
| J4 | bottom edge, centre | JST-SH 8-pin, 1.0 mm, side entry | the ESC: battery in, motor signals out |
| J2 | right edge | USB-C | flashing, serial console, bench power |
| J5 | left edge | JST-GH 4-pin, 1.25 mm, side entry | obstacle sensor (TF-Luna), 5 V I2C |
| J6 | bottom-right corner | JST-SH 4-pin, 1.0 mm, top entry | networking module (VoCore2), 5 V UART |
| J7 | top-right corner | JST-GH 4-pin, 1.25 mm, side entry | charging board |
| J1 | lower right | U.FL | 2.4 GHz Wi-Fi antenna |
| J3 | top-left corner | U.FL | GPS antenna |

Pin 1 is marked on the silkscreen of every connector.

### J4, ESC

| Pin | Signal | Direction | Notes |
|---|---|---|---|
| 1 | GND | | |
| 2 | VBAT | in | the board's only flight power input, up to 0.7 A |
| 3 | ESC_CUR | in | analog current sense, GPIO2. Shared with J6 pin 2 |
| 4 | ESC_TELEM | in | ESC telemetry UART, GPIO10. Shared with J6 pin 3 |
| 5 | MOTOR1 | out | DShot, GPIO11 |
| 6 | MOTOR2 | out | DShot, GPIO13 |
| 7 | MOTOR3 | out | DShot, GPIO16 |
| 8 | MOTOR4 | out | DShot, GPIO6 |

This is the usual Betaflight order. Check it against the ESC's own pinout before plugging in, because nothing forces ESC makers to follow it.

### J5, obstacle sensor

| Pin | Signal | TF-Luna pin |
|---|---|---|
| 1 | 5 V out | 1 (+5V) |
| 2 | SCL | 3 (TXD/SCL) |
| 3 | SDA | 2 (RXD/SDA) |
| 4 | GND | 4 (GND) and 5 (mode select) |

The cable ties the sensor's pin 5 to ground, which puts it in I2C mode. Its pin 6 stays unconnected. The power pin is 5 V, so never plug a 3.3 V-only device into J5.

### J6, networking module

| Pin | Signal | ESP32 | Connects to on the VoCore2 |
|---|---|---|---|
| 1 | 5 V out | | power in (4.5 to 5.5 V) |
| 2 | TX, flight controller to module | GPIO2 | a UART RX pin |
| 3 | RX, module to flight controller | GPIO10 | a UART TX pin |
| 4 | GND | | ground |

Signal levels are 3.3 V on both sides. The two data pins are the same wires as J4 pins 3 and 4, so a drone uses either the ESC's current and telemetry outputs or the networking module, not both. The ESC the team chose is not expected to have those outputs. Capacitor C33 is left off the board when J6 is used.

### J7, charging board

| Pin | Signal | ESP32 | Notes |
|---|---|---|---|
| 1 | GND | | |
| 2 | DOCK_DET | GPIO9 | digital input. Firmware enables the internal pull-up; the charging board pulls the line low when docked |
| 3 | AUX_ADC | GPIO8 | analog input, 100 nF to ground. Must stay under 3.1 V |
| 4 | not connected | | spare |

There is no power pin. The flight controller neither powers the charging board nor takes charge current from it. Protection for the two signal lines is on the charging board.

### J2, USB-C

USB 2.0 full speed straight into the ESP32 (GPIO19 is D−, GPIO20 is D+). The board shows up as "USB JTAG/serial debug unit" with no driver chip. USB 5 V also powers the board through a diode, enough for the board on its own but not with the sensor and the networking module plugged in.

### J1 and J3, antennas

Both are U.FL sockets (also sold as IPEX or MHF1). J1 takes any 2.4 GHz antenna. J3 takes a GPS L1 antenna; a passive one works as built, an active one needs inductor L3 fitted. Never transmit on Wi-Fi with nothing plugged into J1.

## ESP32 pin assignment

| GPIO | Chip pin | Signal | Use |
|---|---|---|---|
| 0 | 5 | BOOT | pad pair JP2 on the bottom; short to enter download mode |
| 2 | 7 | ESC_CUR | UART TX to the networking module (J6), or ESC current on ADC1 |
| 4 | 9 | VBAT_SENSE | battery voltage divided by 11, on ADC1 |
| 6 | 11 | MOTOR4 | DShot |
| 8 | 13 | AUX_ADC | charging board analog input, ADC1 |
| 9 | 14 | DOCK_DET | charging board digital input |
| 10 | 15 | ESC_TELEM | UART RX from the networking module (J6), or ESC telemetry |
| 11 | 16 | MOTOR1 | DShot |
| 13 | 18 | MOTOR2 | DShot |
| 16 | 22 | MOTOR3 | DShot |
| 18 | 24 | GPS_RX | UART RX, data from the GPS |
| 19 | 25 | USB D− | |
| 20 | 26 | USB D+ | |
| 33 | 38 | SPI_MOSI | IMU |
| 34 | 39 | SPI_SCK | IMU |
| 35 | 40 | ICM_CS | IMU chip select, 10 kΩ pull-up |
| 36 | 41 | GPS_TX | UART TX, data to the GPS |
| 37 | 42 | I2C_SDA | barometer and J5, 4.7 kΩ pull-up to 3.3 V |
| 38 | 43 | I2C_SCL | barometer and J5, 4.7 kΩ pull-up to 3.3 V |
| 39 | 44 | Yellow | yellow LED, high is on |
| 40 | 45 | Green | green LED, high is on |
| 43 | 49 | U0TXD | test pad TP1, boot log and fallback flashing |
| 44 | 50 | U0RXD | test pad TP2 |
| 47 | 37 | SPI_MISO | IMU |
| 48 | 36 | ICM_INTR | IMU data-ready interrupt |

Reset (CHIP_PU, chip pin 4) is pad pair JP1. GPIO3, 45 and 46 are boot straps and are left floating. GPIO1, 5, 7, 12, 14, 15, 17, 21, 26, 41 and 42 are unused but cannot be brought out: there is no room for another via beside those pins.

Any GPIO can carry any UART, SPI or I2C signal on this chip, so firmware only needs this table.

## Bus addresses and devices

| Bus | Device | Address or note |
|---|---|---|
| I2C | BMP581 barometer (on board) | 0x46 |
| I2C | TF-Luna obstacle sensor (on J5) | 0x10. Run the bus at 100 kHz when it is plugged in |
| SPI | ICM-42688-P gyro and accelerometer | chip select GPIO35, interrupt GPIO48 |
| UART | u-blox MAX-M10S GPS | TX GPIO36, RX GPIO18 |
| UART | VoCore2 networking module (on J6) | TX GPIO2, RX GPIO10 |

## Power

| Rail | Made by | Feeds | Limit |
|---|---|---|---|
| VBAT | battery, through J4 pin 2 | buck regulator, voltage divider | 6 to 16.8 V in; the J4 pin is rated 1 A |
| +5V | AP63205 buck, or USB | both 3.3 V regulators, J5 pin 1, J6 pin 1 | 2 A regulator; plan for 1 A total |
| +3V3 | TLV75733 | ESP32, LEDs | 1 A regulator, 0.36 A peak used |
| +3V3_SENS | TPS7A2033, low noise | IMU, barometer, GPS | 0.3 A regulator, 25 mA used |

| What is plugged in | 5 V current, average | 5 V current, peak |
|---|---|---|
| board alone | 0.14 A | 0.38 A |
| TF-Luna on J5 | +0.07 A | +0.15 A |
| VoCore2 on J6 | +0.23 A | +0.40 A |
| all of it | 0.44 A | 0.93 A |

From a 2S battery that is 0.33 A on average and 0.70 A at the worst moment. The motors do not draw through this board at all.

## Lights, test pads and recovery

| Item | Where | What it is |
|---|---|---|
| D2, red | lower left | on whenever 3.3 V is up |
| D3, green | lower left | GPIO40 |
| D4, yellow | lower left | GPIO39 |
| TP1, TP2 | bottom side | UART0 TX and RX: boot log, and flashing if USB fails |
| TP3 to TP6 | bottom side | VBAT, +5V, +3V3, +3V3_SENS |
| TP13 | bottom side | I2C SCL |
| JP1 | bottom side | RESET: short the pair with tweezers |
| JP2 | bottom side | BOOT: hold shorted while tapping RESET to force download mode |

## Rules that prevent damage

1. Battery is 2S. Up to 4S is tolerated. 6S destroys the input protection.
2. J5 supplies 5 V. No 3.3 V-only devices on it.
3. Nothing over 3.1 V into AUX_ADC (J7 pin 3).
4. Do not run Wi-Fi with no antenna on J1.
5. Use the ESC's current and telemetry pins or the networking module, not both. Leave C33 off when the module is used.
6. A 470 µF 35 V low-ESR capacitor goes on the ESC's battery pads before the motors ever spin.
7. C35 on the bottom is polarised: its stripe faces the VBAT side marked on the silkscreen.
8. The buck inductor must be 4.7 µH with a saturation current of 2 A or more.
9. The top side is soldered on a hot plate or with hot air. Four parts have pads underneath that an iron cannot reach: the ESP32, the IMU, the barometer and regulator U4.

## Where the files are

| Folder | Contents |
|---|---|
| [`pcb/`](../pcb/) | the KiCad 9 project: board, schematic source and part library |
| [`schematics/`](../schematics/) | the schematic as a PDF, for reading without KiCad |
| [`cad/`](../cad/) | 3D model of the board (STEP), board pictures, frame CAD |
| [`docs/`](.) | this page, the design document, circuit guides, power budget, bring-up checklist |

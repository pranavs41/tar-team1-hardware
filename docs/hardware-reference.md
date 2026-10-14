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
| Battery | 2S only (6.0 V empty to 8.7 V full on the high-voltage pack). Never 3S or more: the surge diode starts conducting above about 13 V |
| Stacks on | a 20 × 20 mm 4-in-1 ESC, through one 8-pin cable |

## Connectors

| Ref | Where on the board | Type | For |
|---|---|---|---|
| J4 | bottom edge, centre | JST-SH 8-pin, 1.0 mm, side entry | the ESC: battery in, motor signals out |
| J2 | right edge | USB-C | flashing, serial console, bench power |
| J5 | left edge | JST-GH 4-pin, 1.25 mm, side entry | obstacle sensor (TF-Luna), 5 V I2C |
| J6 | bottom-right corner | JST-SH 4-pin, 1.0 mm, top entry | networking module (VoCore2), 5 V UART |
| J7 | top-right corner | JST-SH 7-pin, 1.0 mm, side entry | charging board: battery, I2C and three status lines |
| J8 | right edge, below J7 | JST-SH 4-pin, 1.0 mm, top entry | landing sensor (downward ToF), 5 V I2C |
| J1 | lower right | U.FL | 2.4 GHz Wi-Fi antenna |
| J3 | top-left corner | U.FL | GPS antenna |

Pin 1 is marked on the silkscreen of every connector.

### J4, ESC

| Pin | Signal | Direction | Notes |
|---|---|---|---|
| 1 | GND | | |
| 2 | VBAT | in | the board's only flight power input, up to 0.7 A |
| 3 | MOTOR1 | out | DShot, GPIO16. ESC pad "1" |
| 4 | MOTOR2 | out | DShot, GPIO6. ESC pad "2" |
| 5 | MOTOR3 | out | DShot, GPIO11. ESC pad "3" |
| 6 | MOTOR4 | out | DShot, GPIO13. ESC pad "4" |
| 7 | ESC_TELEM | in | GPIO10. ESC pad "N", which the seller's diagram labels "No Output". Shared with J6 pin 3 |
| 8 | ESC_CUR | in | analog current sense, GPIO2. ESC pad "C". Shared with J6 pin 2 |

This is the order printed on the team's ESC (the AERO SELFIE 30 A 4-in-1): −, +, 1, 2, 3, 4, N, C. It is not the usual Betaflight order, so a different ESC may need its cable rewired.

Two things to do on the cable:

- **Check which end is pin 1.** The ESC's picture shows the order but not which end of its socket a given cable calls pin 1. With the cable plugged into the ESC only, use a multimeter to confirm that the wire reaching J4 pin 1 is the ESC's − and the wire reaching pin 2 is +. On the cable in the seller's diagram the − wire is black and sits at one end. A reversed cable puts battery voltage on the wrong pins.
- **Pull the C wire out of the cable when the networking module is fitted.** J4 pin 8 is the same line the ESP32 uses to talk to the module on J6. The ESC drives its C pad with a current reading, and the two outputs would fight. The N pad has no output, so its wire can stay.

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

Signal levels are 3.3 V on both sides. The two data pins are the same wires as J4 pins 7 and 8, so a drone uses either the ESC's current and telemetry outputs or the networking module, not both. The team's ESC has a current output on its C pad, so that wire must come out of the ESC cable when the module is fitted. Capacitor C33 is left off the board when J6 is used.

### J7, charging board

| Pin | Signal | ESP32 | Notes |
|---|---|---|---|
| 1 | BATT+ | | battery positive, joined to VBAT on the board. Powers the flight controller, 1 A at most |
| 2 | GND | | |
| 3 | SDA | GPIO37 | the same I2C bus as the barometer and the two sensor ports |
| 4 | SCL | GPIO38 | |
| 5 | /PG | GPIO9 | input. Low means the charger has good input power, so the drone is on the dock |
| 6 | STAT | GPIO8 | input. Low while charging, high when done or idle, blinking on a fault. Has 100 nF to ground (C34) |
| 7 | CD | GPIO7 | output. High stops charging, low or floating lets it run |

This is the charging board's own pin order, minus its pin 8. Pin 8 was VBAT_SENSE, a divided copy of the battery voltage. The flight controller already measures the battery through its own divider on GPIO4, on the same wire that pin 1 brings in, so a second copy adds nothing and the connector stays at seven pins.

/PG and STAT are open-drain outputs on the charger: they can pull low but not drive high. Firmware turns on the ESP32's internal pull-ups for GPIO8 and GPIO9. The I2C pull-ups are already on this board (R12 and R13). So the four 10 kΩ pull-up resistors in the charging board's parts list are not needed, and there is no 3.3 V pin on J7 for them to connect to.

Pin 1 is at the right-hand end of the connector, nearest the board corner.

### J8, landing sensor

| Pin | Signal | TF-Luna pin |
|---|---|---|
| 1 | 5 V out | 1 (+5V) |
| 2 | SCL | 3 (TXD/SCL) |
| 3 | SDA | 2 (RXD/SDA) |
| 4 | GND | 4 (GND) and 5 (mode select) |

The same four signals in the same order as J5, for the downward-facing distance sensor used for landing. The connector is a JST-SH that points straight up, like J6, because a side-entry JST-GH would not fit between the charging connector, the mounting hole and the USB socket. Pin 1 is the end nearest the USB socket.

### Compass, on the J5 or J8 cable

The board has no compass of its own. An outdoor autonomous drone needs one to know which way it points while hovering, so a small magnetometer board is added on a cable. It has no connector of its own on the flight controller. I2C is a shared bus, so the compass joins the same four wires as one of the distance sensors.

| Compass board pad | Joins this wire of the J5 or J8 cable |
|---|---|
| VIN | pin 1, 5 V |
| SCL | pin 2, SCL |
| SDA | pin 3, SDA |
| GND | pin 4, GND |

The board chosen is Adafruit's LIS3MDL breakout. It has its own regulator and level shifting, so the 5 V on pin 1 is fine. A board without a regulator (most Qwiic boards) would be damaged by 5 V. Its two small sockets are wired in Qwiic order, which is not J5's or J8's order, so use its solder pads and wire by name.

**Remove the breakout's two I2C pull-up resistors before fitting it.** On the Adafruit board they pull SDA and SCL up to its VIN, which is 5 V here. Together with the flight controller's 2.2 kΩ pull-ups to 3.3 V, the bus would idle at about 3.6 V, at the limit of the barometer and the ESP32. The board's own pull-ups are enough, and the breakout's level shifter still works without them.

Where it goes matters more than how it is wired. The wires carrying motor current make a magnetic field that changes with throttle, and it swamps the Earth's field at close range. Mount the compass as far from the battery leads, the ESC and the motor wires as the frame allows, on top and towards the front or on a short mast. Twist the two battery leads together. Calibrate the compass on the finished drone, and check the heading with the motors running before trusting it in flight.

J6 and J8 are the same connector type. Swapping their plugs by mistake damages nothing, since both have 5 V on pin 1 and ground on pin 4, but neither device will work until they are swapped back.

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
| 6 | 11 | MOTOR2 | DShot |
| 7 | 12 | CHG_CD | output to the charger: high stops charging |
| 8 | 13 | CHG_STAT | input from the charger: charge status |
| 9 | 14 | CHG_PG | input from the charger: power good, which also means docked |
| 10 | 15 | ESC_TELEM | UART RX from the networking module (J6), or ESC telemetry |
| 11 | 16 | MOTOR3 | DShot |
| 13 | 18 | MOTOR4 | DShot |
| 16 | 22 | MOTOR1 | DShot |
| 18 | 24 | GPS_RX | UART RX, data from the GPS |
| 19 | 25 | USB D− | |
| 20 | 26 | USB D+ | |
| 33 | 38 | SPI_MOSI | IMU |
| 34 | 39 | SPI_SCK | IMU |
| 35 | 40 | ICM_CS | IMU chip select, 10 kΩ pull-up |
| 36 | 41 | GPS_TX | UART TX, data to the GPS |
| 37 | 42 | I2C_SDA | barometer, J5, J7 and J8, 2.2 kΩ pull-up to 3.3 V |
| 38 | 43 | I2C_SCL | barometer, J5, J7 and J8, 2.2 kΩ pull-up to 3.3 V |
| 39 | 44 | Yellow | yellow LED, high is on |
| 40 | 45 | Green | green LED, high is on |
| 43 | 49 | U0TXD | test pad TP1, boot log and fallback flashing |
| 44 | 50 | U0RXD | test pad TP2 |
| 47 | 37 | SPI_MISO | IMU |
| 48 | 36 | ICM_INTR | IMU data-ready interrupt |

Reset (CHIP_PU, chip pin 4) is pad pair JP1. GPIO3, 45 and 46 are boot straps and are left floating. GPIO1, 5, 12, 14, 15, 17, 21, 26, 41 and 42 are unused but cannot be brought out: there is no room for another via beside those pins.

Any GPIO can carry any UART, SPI or I2C signal on this chip, so firmware only needs this table.

## Bus addresses and devices

| Bus | Device | Address or note |
|---|---|---|
| I2C | BMP581 barometer (on board) | 0x46 |
| I2C | TF-Luna obstacle sensor (on J5) | 0x10. Run the bus at 100 kHz when anything is plugged into J5, J7 or J8 |
| I2C | landing sensor (on J8) | a second TF-Luna also starts at 0x10, so one of the two must be given a new address once, for example 0x11 |
| I2C | LIS3MDL compass (on the J5 or J8 cable) | 0x1C, or 0x1E with its address pad bridged. Neither clashes |
| I2C | BQ25887 charger (on J7) | 0x6B. The datasheet says 0x6A in one paragraph and 0x6B everywhere else, so scan the bus at bring-up. Neither clashes |
| SPI | ICM-42688-P gyro and accelerometer | chip select GPIO35, interrupt GPIO48 |
| UART | u-blox MAX-M10S GPS | TX GPIO36, RX GPIO18 |
| UART | VoCore2 networking module (on J6) | TX GPIO2, RX GPIO10 |

## Power

| Rail | Made by | Feeds | Limit |
|---|---|---|---|
| VBAT | battery, through J4 pin 2 or J7 pin 1 | buck regulator, voltage divider | 6 to 8.7 V in; each of those pins is rated 1 A |
| +5V | AP63205 buck, or USB | both 3.3 V regulators, J5 pin 1, J6 pin 1, J8 pin 1 | 2 A regulator; plan for 1.1 A total |
| +3V3 | TLV75733 | ESP32, LEDs | 1 A regulator, 0.36 A peak used |
| +3V3_SENS | TPS7A2033, low noise | IMU, barometer, GPS | 0.3 A regulator, 25 mA used |

| What is plugged in | 5 V current, average | 5 V current, peak |
|---|---|---|
| board alone | 0.14 A | 0.38 A |
| TF-Luna on J5 | +0.07 A | +0.15 A |
| second TF-Luna on J8 | +0.07 A | +0.15 A |
| VoCore2 on J6 | +0.23 A | +0.40 A |
| all of it | 0.51 A | 1.08 A |

From a 2S battery that is 0.38 A on average and 0.81 A at the worst moment. The motors do not draw through this board at all.

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

1. Battery is 2S only. A 3S or larger pack makes the surge diode D5 conduct and can destroy it.
2. J5 and J8 supply 5 V. No 3.3 V-only devices on them. J8 looks like a Qwiic or STEMMA QT socket but is not wired like one, so never plug one of those cables into it.
3. J7 pin 1 is the battery, up to 8.7 V, and it is rated 1 A. It is there to power the flight controller. Charge current must reach the battery on its own wires, never through this pin.
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

# 4. Sensors

All the sensors run from `+3V3_SENS`, the low-noise rail from U5. Keeping them off the ESP32's rail stops radio transmit bursts from showing up as noise in the readings (see [3. Power](03-power.md)).

## IMU (U6, ICM-42688-P)

The ICM-42688-P has a 3-axis gyroscope and a 3-axis accelerometer. The flight controller's rate loop reads the gyro thousands of times a second to keep the drone level, so the IMU sits on SPI, the fastest bus the ESP32 has, and can run at up to 32 kHz with very little delay.

We started with a second IMU on the board, a BNO085, which does sensor fusion on its own processor and outputs orientation directly. We dropped it because the ICM-42688-P covers the same sensors, the BNO085's fused output is too slow for the rate loop, and the orientation math runs fine on the ESP32 the way it does on Betaflight and PX4 boards. The decision is logged in [design-decisions.md](../design-decisions.md).

### Power

| Pin | Name | Connects to | Capacitors to GND |
|---|---|---|---|
| 8 | VDD | `+3V3_SENS` | C25 0.1 µF and C26 2.2 µF |
| 5 | VDDIO | `+3V3_SENS` | C27 10 nF |
| 6, 7, 11 | GND, RESV | GND | |

VDD powers the sensor itself and VDDIO powers its I/O pins. The values come from the bypass capacitor list in TDK's datasheet. Pins 7 and 11 are reserved pins that the datasheet says to ground. Pins 2, 3 and 10 are reserved pins that can be left open, so they have no-connect flags.

My first version had C26 sitting between the rail and VDD instead of from VDD to GND. A capacitor blocks DC, so VDD had no power at all and the chip would never have answered. Every decoupling capacitor goes from the power pin to GND, never in the supply path.

### SPI

| IMU pin | Name | Label | ESP32 pin |
|---|---|---|---|
| 12 | AP_CS | `ICM_CS` | 15 (GPIO10) |
| 13 | AP_SCLK | `SPI_SCK` | 17 (GPIO12) |
| 14 | AP_SDI | `SPI_MOSI` | 16 (GPIO11) |
| 1 | AP_SDO | `SPI_MISO` | 18 (GPIO13) |

The IMU names its data pins from its own side: SDI is data coming in and SDO is data going out. So SDI goes to the ESP32's MOSI (master out, slave in) and SDO goes to MISO. Getting these backwards is the usual SPI mistake, and the symptom is a chip that never responds.

R11 is a 10 kΩ pull-up from `ICM_CS` to `+3V3_SENS`. The ICM-42688-P starts up in I2C mode and only switches to SPI after it sees CS go low. While the ESP32 is booting its pins float for a moment, and a floating CS can catch noise and confuse the IMU. The pull-up holds CS high (deselected) until the firmware takes over.

### Interrupts

INT1 (pin 4) goes to `ICM_INTR` on ESP32 pin 21 (GPIO15). The IMU pulses it when a new sample is ready, so the firmware reads each sample once, right when it arrives, instead of polling.

INT2/FSYNC/CLKIN (pin 9) goes to `ICM_INT2` on ESP32 pin 14 (GPIO9). This pin can be a second interrupt, a frame sync input, or an external clock input, and some flight firmware feeds it a precise clock to tighten timing. Wiring it to a spare GPIO keeps all three options open and means it never floats.

### Placement

The IMU goes near the centre of the board, where vibration is lowest and it's closest to the drone's centre of rotation. Keep it away from the buck regulator and its inductor, whose magnetic field and heat add noise. Its capacitors sit right against pins 8 and 5.

## Barometer (U7, BMP581)

The barometer measures air pressure, which gives altitude to within a few centimetres and is what holds the drone at a steady height. It only needs reading a few dozen times a second, so it sits on I2C, the slower two-wire bus, and saves the SPI pins for the IMU.

### Power

VDD (pin 10) and VDDIO (pin 1) both go to `+3V3_SENS`, each with a 100 nF capacitor to GND (C28 and C29). Pins 3, 8 and 9 are ground.

### I2C

| Pin | Name | Connects to |
|---|---|---|
| 2 | SCK | `I2C_SCL`, ESP32 pin 39 (GPIO34) |
| 4 | SDI | `I2C_SDA`, ESP32 pin 38 (GPIO33) |
| 6 | CSB | `+3V3_SENS` |
| 5 | SDO | GND |
| 7 | INT | no-connect |

The chip can speak SPI or I2C and checks CSB at power-up: high means I2C. SDO sets the I2C address: tied to GND it is 0x46, tied high it would be 0x47. The chip reuses its SPI pin names, so SCK is the I2C clock and SDI is the I2C data.

R12 and R13 (4.7 kΩ from SDA and SCL to `+3V3_SENS`) are the bus pull-ups. I2C lines are open-drain: chips can only pull them low, and nothing drives them high. The resistors pull them back up when nobody is pulling down. One pair serves the whole bus, including the spare I2C port.

INT is left unconnected. Firmware reads the sensor on a timer, and pins 19 and 22 are free if someone wants the data-ready interrupt later.

### Placement

Keep the barometer away from the buck regulator's heat and from the LEDs, and on the finished drone cover it with a small piece of open-cell foam so prop wash doesn't show up as altitude jumps.

## GPS (U8, MAX-M10S)

The GPS gives the drone a position to reference against the RTK ground station for landing. It talks to the ESP32 over a UART.

### Power

VCC (pin 8) and V_IO (pin 7) are tied together to `+3V3_SENS`, with C30 (10 µF) and C31 (100 nF) to GND. u-blox allows VCC and V_IO to be one supply for a 3.3 V design. VIO_SEL (pin 15) stays open, which selects the 3.3 V I/O range; it would be grounded for a 1.8 V design. V_BCKP (pin 6) is open because there is no backup battery; the manual says to leave it open in that case. The cost is a cold start after every power cycle, which the time-to-fix budget allows.

### UART

TXD (pin 2) goes to `GPS_RX` on ESP32 pin 41 and RXD (pin 3) to `GPS_TX` on pin 40. The names are from the ESP32's side: the GPS transmits into the ESP32's receive pin.

### Antenna

RF_IN (pin 11) goes to J3, a U.FL connector, so the antenna can mount up high on the drone. The trace between them must be 50 Ω, short, with ground on the layer below and ground vias along both sides, the same rules as the Wi-Fi antenna trace. RF_IN is DC-blocked inside the module and the module has its own LNA and SAW filter, so a passive patch antenna needs nothing else.

L3 (27 nH, not fitted) and C32 (10 nF) form a bias-T for an active antenna. VCC_RF (pin 14) is a filtered copy of VCC the module provides for exactly this. Fitting L3 puts that voltage on the antenna line, which powers an active antenna's built-in amplifier through the same cable that carries the signal. With a passive antenna L3 stays off, because many passive patches are a DC short and would drag VCC_RF to ground.

Everything else (TIMEPULSE, EXTINT, RESET_N, SAFEBOOT_N, LNA_EN, SDA, SCL) is left open as the integration manual allows.

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

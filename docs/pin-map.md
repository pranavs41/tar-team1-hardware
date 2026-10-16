# ESP32-S3FN8 pin map

Net names match the labels in the schematic exactly. Firmware should use this table.

The pins were reassigned on 2026-10-02 to make the board routable: the chip's right-hand side has room for only every other pin to escape through a via, so the pins that need a via are spread out and the rest leave on the top layer. Every signal on this chip can be moved to any GPIO through its internal routing matrix, so the firmware pays nothing for the shuffle.

| Pin | GPIO | Net | Connects to |
|---|---|---|---|
| 4 | CHIP_PU | none | RESET pad pair JP1 |
| 5 | GPIO0 | none | BOOT pad pair JP2 (strapping pin) |
| 7 | GPIO2 | `ESC_CUR` | Radio port J6 pin 2, UART TX to the VoCore2. Same net as J4 pin 8 (ESC current sense, ADC1): use one or the other |
| 9 | GPIO4 | `VBAT_SENSE` | Battery divider (ADC1) |
| 11 | GPIO6 | `MOTOR2` | ESC motor 2 (DShot) |
| 12 | GPIO7 | `CHG_CD` | Charging board port, output: high stops charging |
| 13 | GPIO8 | `CHG_STAT` | Charging board port, charge status input |
| 14 | GPIO9 | `CHG_PG` | Charging board port, power good input (low when docked) |
| 15 | GPIO10 | `ESC_TELEM` | Radio port J6 pin 3, UART RX from the VoCore2. Same net as J4 pin 7 (ESC telemetry): use one or the other |
| 16 | GPIO11 | `MOTOR3` | ESC motor 3 (DShot) |
| 18 | GPIO13 | `MOTOR4` | ESC motor 4 (DShot) |
| 22 | GPIO16 | `MOTOR1` | ESC motor 1 (DShot) |
| 24 | GPIO18 | `GPS_RX` | GPS TXD |
| 25 | GPIO19 | `USB_DN` | USB D− |
| 26 | GPIO20 | `USB_DP` | USB D+ |
| 36 | GPIO48 | `ICM_INTR` | ICM-42688-P interrupt |
| 37 | GPIO47 | `SPI_MISO` | ICM-42688-P SPI |
| 38 | GPIO33 | `SPI_MOSI` | ICM-42688-P SPI |
| 39 | GPIO34 | `SPI_SCK` | ICM-42688-P SPI |
| 40 | GPIO35 | `ICM_CS` | ICM-42688-P chip select |
| 41 | GPIO36 | `GPS_TX` | GPS RXD |
| 42 | GPIO37 | `I2C_SDA` | BMP581, I2C port |
| 43 | GPIO38 | `I2C_SCL` | BMP581, I2C port |
| 44 | GPIO39 | `Yellow` | Yellow status LED |
| 45 | GPIO40 | `Green` | Green status LED |
| 49 | U0TXD | none | Test pad TP1 (boot log / fallback console) |
| 50 | U0RXD | none | Test pad TP2 |

Not connected: pins 6, 8, 10, 17, 19, 21, 23, 27, 28, 47, 48, 51, 52. Pins 6, 10, 17, 19, 21, 23, 27, 28, 47 and 48 (GPIO1, 5, 12, 14, 15, 17, 21, 26, 41, 42) are free for later use. Pins 30 to 35 are the in-package flash and must stay unconnected.

Keep GPIO3, GPIO45 and GPIO46 floating: they are strapping pins, and GPIO45 selects the flash voltage (must be low for our 3.3 V flash).

Ports: J5 is the sensor port (5 V, SCL, SDA, GND) for the TF-Luna on the I2C bus at address 0x10. J6 is the radio port (5 V, TX GPIO2, RX GPIO10, GND) for the VoCore2. J7 is the charging board port (BATT+, GND, SDA, SCL, /PG on GPIO9, STAT on GPIO8, CD on GPIO7). J8 is the landing sensor port, wired like J5 (5 V, SCL, SDA, GND).

Test pads on the bottom: TP1 U0TXD, TP2 U0RXD, TP3 VBAT, TP4 +5V, TP5 +3V3, TP6 +3V3_SENS, TP13 I2C_SCL. Each one sits on a via of its net.

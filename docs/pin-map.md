# ESP32-S3FN8 pin map

Net names match the labels in the schematic exactly. Firmware should use this table.

| Pin | GPIO | Net | Connects to |
|---|---|---|---|
| 5 | GPIO0 | — | BOOT button (strapping pin) |
| 6 | GPIO1 | `VBAT_SENSE` | Battery divider (ADC1) |
| 7 | GPIO2 | `ESC_CUR` | ESC current sense (ADC1) |
| 9 | GPIO4 | `MOTOR1` | ESC motor 1 (DShot) |
| 10 | GPIO5 | `MOTOR2` | ESC motor 2 |
| 11 | GPIO6 | `MOTOR3` | ESC motor 3 |
| 12 | GPIO7 | `MOTOR4` | ESC motor 4 |
| 13 | GPIO8 | `ESC_TELEM` | ESC telemetry (UART RX) |
| 15 | GPIO10 | `ICM_CS` | ICM-42688-P chip select |
| 16 | GPIO11 | `SPI_MOSI` | IMU SPI bus |
| 17 | GPIO12 | `SPI_SCK` | IMU SPI bus |
| 18 | GPIO13 | `SPI_MISO` | IMU SPI bus |
| 19 | GPIO14 | `BNO_CS` | BNO085 chip select |
| 21 | GPIO15 | `ICM_INTR` | ICM-42688-P interrupt |
| 22 | GPIO16 | `BNO_INTR` | BNO085 H_INTN |
| 23 | GPIO17 | `BNO_RST` | BNO085 NRST |
| 24 | GPIO18 | `BNO_WAKE` | BNO085 PS0/WAKE |
| 25 | GPIO19 | `USB_DN` | USB D− |
| 26 | GPIO20 | `USB_DP` | USB D+ |
| 36 | GPIO48 | `Yellow` | Yellow status LED |
| 37 | GPIO47 | `Green` | Green status LED |
| 38 | GPIO33 | `I2C_SDA` | BMP581, I2C port |
| 39 | GPIO34 | `I2C_SCL` | BMP581, I2C port |
| 40 | GPIO35 | `GPS_TX` | GPS RXD |
| 41 | GPIO36 | `GPS_RX` | GPS TXD |
| 42 | GPIO37 | `UART_TX` | Spare UART port |
| 43 | GPIO38 | `UART_RX` | Spare UART port |
| 49 | U0TXD | — | Test pad TP1 (boot log / fallback console) |
| 50 | U0RXD | — | Test pad TP2 |

Not connected: pins 8, 14, 27, 28, 44, 45, 47, 48, 51, 52. Pins 30–35 are the in-package flash and must stay unconnected.

Keep GPIO3, GPIO45 and GPIO46 floating: they are strapping pins, and GPIO45 selects the flash voltage (must be low for our 3.3 V flash).

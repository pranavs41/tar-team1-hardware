# Flight controller parts order, rev A

One DigiKey order: every part soldered onto the flight controller, for 1 board, with spare small resistors, capacitors and LEDs. Seller is DigiKey unless the note says otherwise. Prices were read on 2026-10-11; check stock and price on the day.

Three bare boards are being ordered, so there will be two spare boards with no parts. There is one of each chip, so a part damaged during soldering means a second order.

The same list as a spreadsheet is [`fc-parts-order.csv`](fc-parts-order.csv), and as a file DigiKey's upload tool reads, [`bom-digikey.csv`](bom-digikey.csv).

| Qty | Part number | What it is | Maker | Each | Line total | Note |
|---|---|---|---|---|---|---|
| 1 | [ESP32-S3FN8](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3FN8/15822446) | ESP32-S3 processor | Espressif | $4.17 | $4.17 |  |
| 1 | [MAX-M10S-00B](https://www.digikey.com/en/products/detail/u-blox/MAX-M10S-00B/15712906) | GPS module | u-blox | $11.42 | $11.42 |  |
| 1 | [ICM-42688-P](https://www.digikey.com/en/products/detail/tdk-invensense/ICM-42688-P/10824934) | Gyro and accelerometer | TDK InvenSense | $4.86 | $4.86 | Out of stock at DigiKey on 2026-10-11. Try Newark or Arrow. No brokers |
| 1 | [BMP581](https://www.digikey.com/en/products/detail/bosch-sensortec/BMP581/16036134) | Barometer | Bosch Sensortec | $3.35 | $3.35 | Out of stock at DigiKey on 2026-10-11. Try Mouser |
| 1 | [AP63205WU-7](https://www.digikey.com/en/products/detail/diodes-incorporated/AP63205WU-7/9858432) | 5 V buck regulator | Diodes Incorporated | $0.89 | $0.89 | Out of stock at DigiKey on 2026-10-11. Try Mouser |
| 1 | [TLV75733PDRVR](https://www.digikey.com/en/products/detail/texas-instruments/TLV75733PDRVR/8038260) | 3.3 V regulator, 1 A | Texas Instruments | $0.48 | $0.48 |  |
| 1 | [TPS7A2033PDBVR](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A2033PDBVR/13566866) | 3.3 V low-noise regulator | Texas Instruments | $0.35 | $0.35 | Out of stock at DigiKey on 2026-10-11. Try Mouser |
| 1 | [USBLC6-2SC6](https://www.digikey.com/en/products/detail/stmicroelectronics/USBLC6-2SC6/1040559) | USB protection | STMicroelectronics | $0.54 | $0.54 |  |
| 1 | [FA-128 40.0000MF10Z-K3](https://www.digikey.com/en/products/detail/epson/FA-128-40-0000MF10Z-K3/2514630) | 40 MHz crystal, 10 pF, ±10 ppm | Epson | $1.11 | $1.11 |  |
| 1 | [TCJD107M025R0055](https://www.digikey.com/en/products/detail/avx-corporation/TCJD107M025R0055/4990375) | 100 µF 25 V polymer capacitor | Kyocera AVX | $3.65 | $3.65 |  |
| 1 | [SMAJ18A](https://www.digikey.com/en/products/detail/littelfuse-inc/SMAJ18A/762282) | Battery surge diode | Littelfuse | $0.51 | $0.51 |  |
| 1 | [1N5819HW-7-F](https://www.digikey.com/en/products/detail/diodes-incorporated/1N5819HW-7-F/814970) | Schottky diode, 1 A 40 V, SOD-123 | Diodes Incorporated | $0.31 | $0.31 |  |
| 3 | [150060RS75000](https://www.digikey.com/en/products/result?keywords=150060RS75000) | LED 0603, red | Würth Elektronik | $0.15 | $0.45 |  |
| 3 | [150060VS75000](https://www.digikey.com/en/products/result?keywords=150060VS75000) | LED 0603, yellow-green | Würth Elektronik | $0.15 | $0.45 |  |
| 3 | [150060YS75000](https://www.digikey.com/en/products/result?keywords=150060YS75000) | LED 0603, yellow | Würth Elektronik | $0.15 | $0.45 |  |
| 1 | [SM08B-SRSS-TB](https://www.digikey.com/en/products/detail/jst-sales-america-inc/SM08B-SRSS-TB-LF-SN/926714) | ESC connector, JST-SH 8-pin | JST | $0.85 | $0.85 | DigiKey lists it as SM08B-SRSS-TB(LF)(SN) |
| 1 | [SM04B-GHS-TB](https://www.digikey.com/en/products/result?keywords=SM04B-GHS-TB) | Obstacle sensor port, JST-GH 4-pin | JST | $0.39 | $0.39 | Out of stock at DigiKey on 2026-10-11. Try Mouser. Listed as SM04B-GHS-TB(LF)(SN) |
| 1 | [SM07B-SRSS-TB](https://www.digikey.com/en/products/result?keywords=SM07B-SRSS-TB) | Charging port, JST-SH 7-pin | JST | $0.80 | $0.80 | DigiKey lists it as SM07B-SRSS-TB(LF)(SN) |
| 2 | [BM04B-SRSS-TB](https://www.digikey.com/en/products/detail/jst-sales-america-inc/BM04B-SRSS-TB/926696) | Radio port and landing sensor port, JST-SH 4-pin top entry | JST | $0.53 | $1.06 | DigiKey lists it as BM04B-SRSS-TB(LF)(SN) |
| 2 | [U.FL-R-SMT-1(10)](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/U-FL-R-SMT-1-10/2391570) | Antenna sockets, U.FL | Hirose | $1.67 | $3.34 |  |
| 1 | [USB4105-GF-A](https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441) | USB-C socket, 16-pin | GCT | $0.80 | $0.80 |  |
| 1 | [CIGW252010EH4R7MNE](https://www.digikey.com/en/products/result?keywords=CIGW252010EH4R7MNE) | Buck inductor, 4.7 µH, 2.2 A saturation | Samsung Electro-Mechanics | $0.29 | $0.29 |  |
| 10 | [LQG15HS2N0B02D](https://www.digikey.com/en/products/result?keywords=LQG15HS2N0B02D) | Radio supply inductor, 2.0 nH | Murata | $0.10 | $1.00 |  |
| 20 | [GRM155R71C104KA88J](https://www.digikey.com/en/products/result?keywords=GRM155R71C104KA88J) | 0.1 µF 16 V, 0402 | Murata | $0.10 | $2.00 |  |
| 10 | [CL05A105KP5NNNC](https://www.digikey.com/en/products/result?keywords=CL05A105KP5NNNC) | 1 µF 10 V, 0402 | Samsung Electro-Mechanics | $0.10 | $1.00 |  |
| 10 | [GRM155R71H103KA88D](https://www.digikey.com/en/products/result?keywords=GRM155R71H103KA88D) | 10 nF 50 V, 0402 | Murata | $0.10 | $1.00 |  |
| 10 | [GRM1555C1H150JA01D](https://www.digikey.com/en/products/result?keywords=GRM1555C1H150JA01D) | 15 pF 50 V, 0402 | Murata | $0.10 | $1.00 |  |
| 10 | [GRM155R61C225KE11J](https://www.digikey.com/en/products/result?keywords=GRM155R61C225KE11J) | 2.2 µF 16 V, 0402 | Murata | $0.22 | $2.20 |  |
| 10 | [GRM188R60J106ME47D](https://www.digikey.com/en/products/result?keywords=GRM188R60J106ME47D) | 10 µF 6.3 V, 0603 | Murata | $0.12 | $1.20 |  |
| 10 | [GRM21BR61A226ME51L](https://www.digikey.com/en/products/result?keywords=GRM21BR61A226ME51L) | 22 µF 10 V, 0805 | Murata | $0.19 | $1.90 |  |
| 1 | [GRM319R61E106KA12D](https://www.digikey.com/en/products/detail/murata-electronics/GRM319R61E106KA12D/2334921) | 10 µF 25 V, 1206 | Murata | $0.47 | $0.47 |  |
| 10 | [RC0402FR-0710KL](https://www.digikey.com/en/products/result?keywords=RC0402FR-0710KL) | 10 kΩ 1%, 0402 | Yageo | $0.10 | $1.00 |  |
| 10 | [RC0402FR-075K1L](https://www.digikey.com/en/products/result?keywords=RC0402FR-075K1L) | 5.1 kΩ 1%, 0402 | Yageo | $0.10 | $1.00 |  |
| 10 | [RC0402FR-071KL](https://www.digikey.com/en/products/result?keywords=RC0402FR-071KL) | 1 kΩ 1%, 0402 | Yageo | $0.10 | $1.00 |  |
| 10 | [RC0402FR-072K2L](https://www.digikey.com/en/products/result?keywords=RC0402FR-072K2L) | 2.2 kΩ 1%, 0402 | Yageo | $0.10 | $1.00 |  |
| 10 | [RC0402FR-07470RL](https://www.digikey.com/en/products/detail/yageo/RC0402FR-07470RL/726619) | 470 Ω 1%, 0402 | Yageo | $0.10 | $1.00 |  |
| 10 | [RC0402FR-07100KL](https://www.digikey.com/en/products/result?keywords=RC0402FR-07100KL) | 100 kΩ 1%, 0402 | Yageo | $0.10 | $1.00 |  |
| 10 | [RC0402JR-070RL](https://www.digikey.com/en/products/result?keywords=RC0402JR-070RL) | 0 Ω link, 0402 | Yageo | $0.10 | $1.00 |  |
| | | **Total before shipping and tax** | | | **$59.29** | |

Links without a product page go to a DigiKey search for the part number. Not in this order: the bare boards, the stencil, and the motors, ESC and other drone parts.

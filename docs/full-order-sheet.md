# Full order sheet: networking drone

Everything to buy for **one drone**, except the bare circuit boards and the stencil, which are ordered separately ([rev A order sheet](../pcb/network-drone-fc/production/rev-A/order-notes.md)).

Flight controller parts are for 1 board, with spare small resistors, capacitors and LEDs. Three bare boards are being ordered, so two will stay empty as spares. Prices were read between 2026-10-11 and 2026-10-14, before shipping and tax. The same sheet as a spreadsheet: [`full-order-sheet.csv`](full-order-sheet.csv). A short version with only item, quantity, link and cost is [`order-sheet-simple.csv`](order-sheet-simple.csv).

The charging board parts are **provisional**. Rishab's schematic is not final, the small parts' sizes (0603, 0805) are assumed, their prices are rough, and several part numbers have not been checked against a live listing. The charging board's own bare board is not on this sheet. Details: [charging-board.md](charging-board.md).

Left for later: the carbon fiber subframe Daniel linked (https://www.amazon.com/dp/B08ZNQCHP8).

## Drone parts

| Seller | Qty | Part | What it is | Each | Line total | Note |
|---|---|---|---|---|---|---|
| Pyrodrone | 4 | [RCINPower GTS V3 1303 8000KV Plus](https://pyrodrone.com/products/rcinpower-gts-v3-1303-8000kv-plus-2-3-inch-cinewhoop-micro-motor-gold-orange) | Motor | $20.99 | $83.96 | In stock 2026-10-13. A fifth as a spare is worth considering |
| Amazon | 1 | [AERO SELFIE 30 A 4-in-1 ESC](https://www.amazon.com/dp/B0DQSLQH87) | ESC, 2 to 4S, 20 mm holes, comes with its 8-pin cable | $28.90 | $28.90 |  |
| Amazon | 2 | [Benewake TF-Luna](https://www.amazon.com/dp/B0DKCSF8C5) | Distance sensor, one forward and one down | $25.99 | $51.98 |  |
| RaceDayQuads | 1 | [Gemfan Hurricane 3018, pack of 8](https://www.racedayquads.com/products/gemfan-hurricane-3018-durable-bi-blade-3-prop-8-pack-1-5mm-choose-your-color) | Propellers, 1.5 mm hole, 4 clockwise and 4 counter-clockwise | $4.99 | $4.99 | Pick a colour that shows in stock |
| VoCore | 1 | [VoCore2](https://vocore.io/#store) | Wi-Fi networking module | $21.48 | $21.48 | Bought from the store section of the maker's front page. Ships from China. Confirm the price in the cart |
| DigiKey | 1 | [FXP73.07.0100A](https://www.digikey.com/en/products/detail/taoglas-limited/FXP73-07-0100A/2332703) | 2.4 GHz Wi-Fi antenna, U.FL plug | $5.41 | $5.41 |  |
| DigiKey | 1 | [2065600100](https://www.digikey.com/en/products/result?keywords=2065600100) | GPS antenna, U.FL plug | $4.16 | $4.16 |  |
| DigiKey | 1 | [EEU-FR1V471](https://www.digikey.com/en/products/detail/panasonic-industry/EEU-FR1V471/2433575) | 470 uF 35 V capacitor for the ESC's battery pads | $1.08 | $1.08 | Out of stock 2026-10-11, due 2026-11-09. Any 470 uF 35 V low-ESR radial capacitor works |
| DigiKey | 1 | [GHR-04V-S](https://www.digikey.com/en/products/detail/jst-sales-america-inc/GHR-04V-S/807816) | Plug housing for the forward sensor cable, JST-GH 4-pin | $0.20 | $0.20 | Price approximate |
| DigiKey | 2 | [AGHGH28K152](https://www.digikey.com/en/products/detail/jst-sales-america-inc/AGHGH28K152/6009449) | Pre-crimped JST-GH wire, 150 mm | $0.49 | $0.98 | Price approximate. If the link fails, search the part number |
| Adafruit | 1 | [Adafruit LIS3MDL magnetometer breakout (product 4479)](https://www.adafruit.com/product/4479) | Compass, 1.5 g | $9.95 | $9.95 | Shares the I2C wires of the J5 or J8 cable. Runs from that cable's 5 V. Mount it away from the battery leads and ESC |
| Pololu | 2 | [Pololu 5521](https://www.pololu.com/product/5521) | JST-SH 4-pin cable, bare wires on one end, 30 cm | $2.04 | $4.08 | One for the downward sensor, one for the VoCore2 |
| Amazon | 1 | [M2 nylon standoff, screw and nut kit, 180 pieces (HVAZI or similar)](https://www.amazon.com/s?k=HVAZI+M2+nylon+standoff+screw+nut+kit+180) | Hardware for the flight controller and ESC stack | $9.99 | $9.99 | M2, not M3: an M3 nut would not sit flat on top of the board at three holes. M2 passes through the M3 holes. Link is a search; pick a black M2 nylon kit with standoffs, screws and nuts. One kit covers several drones |
| RaceDayQuads | 1 | [XT30 connector](https://www.racedayquads.com/products/xt30-connector-male-or-female) | Battery connector, male | $0.99 | $0.99 | Male, for the ESC's battery lead. The battery comes with its own XT30 |
| Amazon | 1 | [OVONIC 2S 1100 mAh 7.6 V 60C battery, pack of 2](https://www.amazon.com/dp/B0D318NL5W) | Battery | not read |  | Pack of 2. High-voltage type, XT30 plug, 60C. Price not read, so it is not in the total |

Total: **$228.15**, plus the battery

## Flight controller parts, for 1 board

| Seller | Qty | Part | What it is | Each | Line total | Note |
|---|---|---|---|---|---|---|
| DigiKey | 1 | [ESP32-S3FN8](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3FN8/15822446) | ESP32-S3 processor | $4.17 | $4.17 |  |
| DigiKey | 1 | [MAX-M10S-00B](https://www.digikey.com/en/products/detail/u-blox/MAX-M10S-00B/15712906) | GPS module | $11.42 | $11.42 |  |
| Newark | 1 | [ICM-42688-P](https://www.newark.com/invensense/icm-42688-p/mems-module-x-y-z-1-71v/dp/77AH4524) | Gyro and accelerometer | $4.86 | $4.86 | Buy from Newark |
| DigiKey | 1 | [BMP581](https://www.digikey.com/en/products/detail/bosch-sensortec/BMP581/16036134) | Barometer | $3.35 | $3.35 | Out of stock everywhere on 2026-10-13. DigiKey restock due 2026-11-04. Backorder it there or wait |
| Mouser | 1 | [AP63205WU-7](https://www.mouser.com/ProductDetail/Diodes-Incorporated/AP63205WU-7) | 5 V buck regulator | $0.89 | $0.89 | Buy from Mouser, DigiKey has none. Take the price from Mouser's page |
| DigiKey | 1 | [TLV75733PDRVR](https://www.digikey.com/en/products/detail/texas-instruments/TLV75733PDRVR/8038260) | 3.3 V regulator, 1 A | $0.48 | $0.48 |  |
| Texas Instruments | 1 | [TPS7A2033PDBVR](https://www.ti.com/product/TPS7A20/part-details/TPS7A2033PDBVR) | 3.3 V low-noise regulator | $0.35 | $0.35 | Buy direct from ti.com. Not the TPS7A0233, which is a different, noisier part |
| DigiKey | 1 | [USBLC6-2SC6](https://www.digikey.com/en/products/detail/stmicroelectronics/USBLC6-2SC6/1040559) | USB protection | $0.54 | $0.54 |  |
| DigiKey | 1 | [FA-128 40.0000MF10Z-K3](https://www.digikey.com/en/products/detail/epson/FA-128-40-0000MF10Z-K3/2514630) | 40 MHz crystal, 10 pF, ±10 ppm | $1.11 | $1.11 |  |
| DigiKey | 1 | [TCJD107M025R0055](https://www.digikey.com/en/products/detail/avx-corporation/TCJD107M025R0055/4990375) | 100 µF 25 V polymer capacitor | $3.65 | $3.65 |  |
| DigiKey | 1 | [SMAJ18A](https://www.digikey.com/en/products/detail/littelfuse-inc/SMAJ18A/762282) | Battery surge diode | $0.51 | $0.51 |  |
| DigiKey | 1 | [1N5819HW-7-F](https://www.digikey.com/en/products/detail/diodes-incorporated/1N5819HW-7-F/814970) | Schottky diode, 1 A 40 V, SOD-123 | $0.31 | $0.31 |  |
| DigiKey | 3 | [150060RS75000](https://www.digikey.com/en/products/result?keywords=150060RS75000) | LED 0603, red | $0.15 | $0.45 |  |
| DigiKey | 3 | [150060VS75000](https://www.digikey.com/en/products/result?keywords=150060VS75000) | LED 0603, yellow-green | $0.15 | $0.45 |  |
| DigiKey | 3 | [150060YS75000](https://www.digikey.com/en/products/result?keywords=150060YS75000) | LED 0603, yellow | $0.15 | $0.45 |  |
| DigiKey | 1 | [SM08B-SRSS-TB](https://www.digikey.com/en/products/detail/jst-sales-america-inc/SM08B-SRSS-TB-LF-SN/926714) | ESC connector, JST-SH 8-pin | $0.85 | $0.85 | DigiKey lists it as SM08B-SRSS-TB(LF)(SN) |
| LCSC | 1 | [SM04B-GHS-TB](https://www.lcsc.com/product-detail/Wire-To-Board-Connector_JST-SM04B-GHS-TB-LF-SN_C189895.html) | Obstacle sensor port, JST-GH 4-pin | $0.39 | $0.39 | LCSC ships from China. Or wait for DigiKey, restock due 2026-11-16 |
| DigiKey | 1 | [SM07B-SRSS-TB](https://www.digikey.com/en/products/result?keywords=SM07B-SRSS-TB) | Charging port, JST-SH 7-pin | $0.80 | $0.80 | DigiKey lists it as SM07B-SRSS-TB(LF)(SN) |
| DigiKey | 2 | [BM04B-SRSS-TB](https://www.digikey.com/en/products/detail/jst-sales-america-inc/BM04B-SRSS-TB/926696) | Radio port and landing sensor port, JST-SH 4-pin top entry | $0.53 | $1.06 | DigiKey lists it as BM04B-SRSS-TB(LF)(SN) |
| DigiKey | 2 | [U.FL-R-SMT-1(10)](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/U-FL-R-SMT-1-10/2391570) | Antenna sockets, U.FL | $1.67 | $3.34 |  |
| DigiKey | 1 | [USB4105-GF-A](https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441) | USB-C socket, 16-pin | $0.80 | $0.80 |  |
| DigiKey | 1 | [CIGW252010EH4R7MNE](https://www.digikey.com/en/products/result?keywords=CIGW252010EH4R7MNE) | Buck inductor, 4.7 µH, 2.2 A saturation | $0.29 | $0.29 |  |
| DigiKey | 10 | [LQG15HS2N0B02D](https://www.digikey.com/en/products/result?keywords=LQG15HS2N0B02D) | Radio supply inductor, 2.0 nH | $0.10 | $1.00 |  |
| DigiKey | 20 | [GRM155R71C104KA88J](https://www.digikey.com/en/products/result?keywords=GRM155R71C104KA88J) | 0.1 µF 16 V, 0402 | $0.10 | $2.00 |  |
| DigiKey | 10 | [CL05A105KP5NNNC](https://www.digikey.com/en/products/result?keywords=CL05A105KP5NNNC) | 1 µF 10 V, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [GRM155R71H103KA88D](https://www.digikey.com/en/products/result?keywords=GRM155R71H103KA88D) | 10 nF 50 V, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [GRM1555C1H150JA01D](https://www.digikey.com/en/products/result?keywords=GRM1555C1H150JA01D) | 15 pF 50 V, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [GRM155R61C225KE11J](https://www.digikey.com/en/products/result?keywords=GRM155R61C225KE11J) | 2.2 µF 16 V, 0402 | $0.22 | $2.20 |  |
| DigiKey | 10 | [GRM188R60J106ME47D](https://www.digikey.com/en/products/result?keywords=GRM188R60J106ME47D) | 10 µF 6.3 V, 0603 | $0.12 | $1.20 |  |
| DigiKey | 10 | [GRM21BR61A226ME51L](https://www.digikey.com/en/products/result?keywords=GRM21BR61A226ME51L) | 22 µF 10 V, 0805 | $0.19 | $1.90 |  |
| DigiKey | 1 | [GRM319R61E106KA12D](https://www.digikey.com/en/products/detail/murata-electronics/GRM319R61E106KA12D/2334921) | 10 µF 25 V, 1206 | $0.47 | $0.47 |  |
| DigiKey | 10 | [RC0402FR-0710KL](https://www.digikey.com/en/products/result?keywords=RC0402FR-0710KL) | 10 kΩ 1%, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [RC0402FR-075K1L](https://www.digikey.com/en/products/result?keywords=RC0402FR-075K1L) | 5.1 kΩ 1%, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [RC0402FR-071KL](https://www.digikey.com/en/products/result?keywords=RC0402FR-071KL) | 1 kΩ 1%, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [RC0402FR-072K2L](https://www.digikey.com/en/products/result?keywords=RC0402FR-072K2L) | 2.2 kΩ 1%, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [RC0402FR-07470RL](https://www.digikey.com/en/products/detail/yageo/RC0402FR-07470RL/726619) | 470 Ω 1%, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [RC0402FR-07100KL](https://www.digikey.com/en/products/result?keywords=RC0402FR-07100KL) | 100 kΩ 1%, 0402 | $0.10 | $1.00 |  |
| DigiKey | 10 | [RC0402JR-070RL](https://www.digikey.com/en/products/result?keywords=RC0402JR-070RL) | 0 Ω link, 0402 | $0.10 | $1.00 |  |

Total: **$59.29**

## Charging board parts, for 1 board (provisional)

| Seller | Qty | Part | What it is | Each | Line total | Note |
|---|---|---|---|---|---|---|
| DigiKey | 1 | [BQ25887RGER](https://www.digikey.com/en/products/result?keywords=BQ25887RGER) | 2S boost charger with cell balancing, 4 x 4 mm QFN | $5.80 | $5.80 | Provisional until Rishab's schematic is final. Texas Instruments. Stock was very low on 2026-10-11; ti.com sells direct |
| DigiKey | 1 | [LM73100RPWR](https://www.digikey.com/en/products/result?keywords=LM73100RPWR) | Ideal diode with overvoltage cut-off, 2.7 to 23 V, 2 x 2 mm QFN | $1.60 | $1.60 | Provisional until Rishab's schematic is final. Texas Instruments. Replaces the LM66100, which was rated only to 6 V. Rated to 28 V, survives -15 V (a reversed dock), cuts off above the voltage set by its two resistors. Price approximate |
| DigiKey | 10 | [RC0603FR-0740K2L](https://www.digikey.com/en/products/result?keywords=RC0603FR-0740K2L) | 40.2 kohm 1% resistor, 0603 (overvoltage cut-off, top) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Yageo. With 10 kohm below it, cuts the charger off above about 6.0 V |
| DigiKey | 10 | [RC0603FR-0710KL](https://www.digikey.com/en/products/result?keywords=RC0603FR-0710KL) | 10 kohm 1% resistor, 0603 (overvoltage cut-off, bottom) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Yageo |
| DigiKey | 1 | [DFE252012F-1R0M](https://www.digikey.com/en/products/result?keywords=DFE252012F-1R0M) | Power inductor 1 uH, shielded | $0.31 | $0.31 | Provisional until Rishab's schematic is final. Murata. The inductor TI's datasheet uses. Peak current here is about 1.6 A (0.925 A input plus half of a 1.35 A ripple) |
| DigiKey | 1 | [SMBJ5.0A-13-F](https://www.digikey.com/en/products/result?keywords=SMBJ5.0A-13-F) | 5 V surge diode on the dock input | $0.40 | $0.40 | Provisional until Rishab's schematic is final. Diodes Incorporated. Clamps near 9 V, which the LM73100 (28 V) and the charger's input (20 V) both survive |
| DigiKey | 1 | [1206L110THYR](https://www.digikey.com/en/products/result?keywords=1206L110THYR) | Resettable fuse, about 1 A hold, 1206 | $0.50 | $0.50 | Provisional until Rishab's schematic is final. Littelfuse. Part number from memory, confirm it is a 1206 fuse of about 1 A hold and 6 V or more |
| DigiKey | 10 | [RC0603FR-071K2L](https://www.digikey.com/en/products/result?keywords=RC0603FR-071K2L) | 1.2 kohm 1% resistor, 0603 (input current limit) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Yageo. Input limit = 1110 / 1200 ohm = 0.925 A typical (datasheet K_ILIM 1110) |
| DigiKey | 10 | [RC0603FR-07300RL](https://www.digikey.com/en/products/result?keywords=RC0603FR-07300RL) | 300 ohm 1% resistor, 0603 (cell balancing midpoint) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Yageo. 0603 assumed |
| DigiKey | 10 | [RC0603FR-075K23L](https://www.digikey.com/en/products/result?keywords=RC0603FR-075K23L) | 5.23 kohm 1% resistor, 0603 (thermistor bias, top) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Yageo. Datasheet value for a 103AT thermistor is 5.24 kohm; 5.23 kohm is the nearest 1% value |
| DigiKey | 10 | [RC0603FR-0730K1L](https://www.digikey.com/en/products/result?keywords=RC0603FR-0730K1L) | 30.1 kohm 1% resistor, 0603 (thermistor bias, bottom) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Yageo. Datasheet value is 30.31 kohm; 30.1 kohm is the nearest 1% value |
| DigiKey | 2 | [RC2512FK-0741R2L](https://www.digikey.com/en/products/result?keywords=RC2512FK-0741R2L) | 41.2 ohm 1% resistor, 1 W, 2512 (balancing current set) | $0.40 | $0.80 | Provisional until Rishab's schematic is final. Yageo. Sets about 100 mA of balancing current (4.2 V / 41.2 ohm) and dissipates about 0.43 W, inside the 1 W rating |
| DigiKey | 1 | [103AT-2](https://www.digikey.com/en/products/result?keywords=103AT-2) | 10 kohm battery thermistor | $1.50 | $1.50 | Provisional until Rishab's schematic is final. Semitec. Must touch the battery |
| DigiKey | 10 | [GRM188R71E105KA12D](https://www.digikey.com/en/products/result?keywords=GRM188R71E105KA12D) | 1 uF 25 V capacitor, 0603 (VBUS) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Murata. Datasheet: at least 1 uF at VBUS, 25 V rating preferred for a 5 V input |
| DigiKey | 10 | [GRM21BR61E106KA73L](https://www.digikey.com/en/products/result?keywords=GRM21BR61E106KA73L) | 10 uF 25 V capacitor, 0805 (PMID and BAT) | $0.25 | $2.50 | Provisional until Rishab's schematic is final. Murata. Datasheet: 10 uF at PMID with a 25 V rating; the same part works at BAT |
| DigiKey | 10 | [GRM188R71H473KA61D](https://www.digikey.com/en/products/result?keywords=GRM188R71H473KA61D) | 47 nF 50 V capacitor, 0603 (bootstrap) | $0.10 | $1.00 | Provisional until Rishab's schematic is final. Murata. 0603 assumed |
| DigiKey | 10 | [GRM188R61C475KAAJD](https://www.digikey.com/en/products/result?keywords=GRM188R61C475KAAJD) | 4.7 uF 16 V capacitor, 0603 (REGN) | $0.15 | $1.50 | Provisional until Rishab's schematic is final. Murata. 0603 assumed |
| DigiKey | 4 | [GRM21BR61C226ME44L](https://www.digikey.com/en/products/result?keywords=GRM21BR61C226ME44L) | 22 uF 16 V capacitor, 0805 (output) | $0.45 | $1.80 | Provisional until Rishab's schematic is final. Murata. Datasheet: at least 44 uF at SNS, 16 V or more, so two per board |
| DigiKey | 1 | [SM07B-SRSS-TB](https://www.digikey.com/en/products/result?keywords=SM07B-SRSS-TB) | 7-pin JST-SH connector to the flight controller | $0.80 | $0.80 | Provisional until Rishab's schematic is final. JST. Same part as J7 on the flight controller |
| DigiKey | 1 | [B3B-XH-A](https://www.digikey.com/en/products/result?keywords=B3B-XH-A) | 3-pin JST-XH header for the battery's balance plug | $0.15 | $0.15 | Provisional until Rishab's schematic is final. JST |
| DigiKey | 2 | [SHR-07V-S-B](https://www.digikey.com/en/products/detail/jst-sales-america-inc/SHR-07V-S-B/759871) | 7-pin JST-SH plug housing, both ends of the cable to the flight controller | $0.15 | $0.30 | Provisional until Rishab's schematic is final. JST |
| DigiKey | 7 | [ASSHSSH28K152](https://www.digikey.com/en/products/detail/jst-sales-america-inc/ASSHSSH28K152/6009452) | Pre-crimped JST-SH wire, 150 mm, one per cable pin | $0.46 | $3.22 | Provisional until Rishab's schematic is final. JST. Push one end of each wire into each housing, pin 1 to pin 1 |

Total: **$29.18**

## Sum

| | |
|---|---|
| Drone parts | $228.15 |
| Flight controller parts | $59.29 |
| Charging board parts | $29.18 |
| **Total before the battery, shipping and tax** | **$316.62** |

Links without a product page go to a DigiKey search for the part number.

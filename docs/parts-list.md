# Parts list and sourcing: networking drone

Everything that goes into one networking drone: what it is, who makes it, where to buy it, and what it costs. The team prefers not to source from China, so each part is listed with the country its maker is based in, and the sellers chosen are in the US or Europe.

To place the orders, use the two order sheets: [drone components](drone-order-sheet.md) and [the flight controller board and its parts](../pcb/network-drone-fc/production/rev-A/order-notes.md).

Prices were read from the sellers' pages on 2026-10-11, for a quantity of one, before shipping, tax and tariffs. Stock changes daily, so check again on the day of ordering.

## Cost of one drone

| Group | Cost |
|---|---|
| Flight controller parts, 69 placed components | $44.83 |
| Flight controller bare board, one of three from OSH Park | $7.25 |
| Motors, ESC, propellers | $117.85 |
| Networking module and two distance sensors (forward and downward) | $73.46 |
| Antennas, ESC capacitor, battery connector | $11.64 |
| Battery, 1000 mAh, priced from a similar pack | $12.99 |
| Charging board, rough figure | $16 |
| **Total for one drone** | **about $284** |

Three things move this number:

- The bare board's smallest order is three boards for $21.76, so the first drone carries the cost of all three.
- The gyro is out of stock at every authorised distributor. Buying it where it is in stock raises the total by about $16. See "Stock problems" below.
- The battery in the table further down is the 1000 mAh pack Daniel picked. Its price is not filled in yet, so the total uses a similar pack's price.
- The charging board's figure is a budget estimate. Its parts are in [charging-board.md](charging-board.md).

## What is and is not made outside China

Buying from a US seller does not change where a part was designed or built. This is the honest picture:

| Part | Maker's home country | Non-Chinese option at this size |
|---|---|---|
| Sensors, regulators, connectors, capacitors, resistors on the flight controller | US, Japan, Germany, Switzerland, Korea, Taiwan, UK | already non-Chinese |
| ESP32-S3 processor | China (Espressif, Shanghai) | none without redesigning the board around a different chip |
| Motors | China | none found. US-made motors start at about twice this size |
| ESC | China | none at 20 × 20 mm. A US-made one exists at $230 and 36 mm square |
| Battery | China | none found for small LiPo packs |
| Propellers | China | none found |
| XT30 battery connector | China | none that mates with an XT30 battery |
| VoCore2 networking module | China | yes, listed below |
| TF-Luna obstacle sensor | China | yes, listed below |
| Bare circuit board | depends on the fab | yes, US and European fabs listed below |

So a fully non-Chinese drone is not possible at this size with parts anyone sells today. What is possible: buy everything through US sellers, keep the whole flight controller except the processor non-Chinese, and swap the two modules that do have alternatives.

Which of these matters depends on the rule the team is working under. A rule about the seller is met by this list as written. A rule about where components are made is not, and cannot be at this size. Ask the university's purchasing or research-security office which one applies before ordering. This page is a parts list, not legal advice.

## Whole drone

| Part | Maker (home country) | Seller | Weight | Price |
|---|---|---|---|---|
| Flight controller, assembled | see the next section | DigiKey for parts, OSH Park for the board | ~8 g, estimate | $52.08 |
| RCINPower GTS V3 1303 8000KV Plus motors ×4 | RCINPower (China) | [Pyrodrone](https://pyrodrone.com/products/rcinpower-gts-v3-1303-8000kv-plus-2-3-inch-cinewhoop-micro-motor-gold-orange) | 5.6 g each, 22.4 g | $83.96 ($20.99 ×4) |
| 30 A 4-in-1 ESC, 2 to 4S, M3 holes on a 20 mm pattern | AERO SELFIE (maker not confirmed) | [Amazon](https://www.amazon.com/dp/B0DQSLQH87) | 5.4 g | $28.90 |
| 3-inch propellers, Gemfan Hurricane 3018, pack of 8 | Gemfan (China) | [RaceDayQuads](https://www.racedayquads.com/products/gemfan-hurricane-3018-durable-bi-blade-3-prop-8-pack-1-5mm-choose-your-color) | 0.75 g each, 3 g | $4.99 |
| 2S LiPo battery, URGENEX 1000 mAh, Daniel's pick | URGENEX (not confirmed) | [Amazon](https://www.amazon.com/dp/B0FFBB59TM) | TBD | TBD |
| VoCore2 Wi-Fi networking module | VoCore (China) | [VoCore](https://vocore.io/v2.html) | ~5 g, estimate | $21.48 |
| Benewake TF-Luna distance sensor ×2: one facing forward for obstacles, one facing down for landing | Benewake (China) | [Amazon](https://www.amazon.com/dp/B0DKCSF8C5) | <5 g each | $51.98 ($25.99 ×2) |
| Charging board, assembled | see [charging-board.md](charging-board.md) | DigiKey for parts | TBD | about $16 |
| 2.4 GHz Wi-Fi antenna, flexible, U.FL plug, Taoglas FXP73.07.0100A | Taoglas (Ireland) | [DigiKey](https://www.digikey.com/en/products/detail/taoglas-limited/FXP73-07-0100A/2332703) | about 1 g | $5.41 |
| GPS antenna, flat adhesive, U.FL plug, Molex 2065600100 | Molex (US) | [DigiKey](https://www.digikey.com/en/products/result?keywords=2065600100) | not listed | $4.16 |
| 470 µF 35 V low-ESR capacitor for the ESC, Panasonic EEU-FR1V471 | Panasonic (Japan) | [DigiKey](https://www.digikey.com/en/products/detail/panasonic-industry/EEU-FR1V471/2433575) | about 2 g | $1.08 |
| XT30 battery connector | Amass (China) | [RaceDayQuads](https://www.racedayquads.com/products/xt30-connector-male-or-female) | about 1 g | $0.99 |
| 3D-printed frame | printed by the team | files in [`cad/`](../cad/README.md) carbon fiber subframe https://www.amazon.com/Reinforced-Wheelbase-Carbon-Bottom-Quadcopter/dp/B08ZNQCHP8/ref=sr_1_1?crid=KFAKM5OMIWOK&dib=eyJ2IjoiMSJ9.nMJVtNsZQ_oGNWYmb8FzK_iFtN6wpS8Of1s_-ch9ROgJz7AxUfqlAeHzT8ppG-NPkk945n_YYTfsP1Ph_1kuDbjXE8BreueyT0bLxlX1KlepADgfhQZpNXiFr9qUcNRonJSNUwbq5fQYZ6XfjIgehdisM2wMxcenIicp57UTJYXCy5Q7s0flgPlP5ZVhKLbomsyGyQ8RLKROFUzAZV_eVthboUUE78WVHKYl37UF91LYOPsuPmjtpqemGI0dJ_ClCvi6tlf8oLSse70oSha9y_OERjE-oJ1sBj2_TRiCNjI.1AG53KmlGvJZcqg-mlnL5PVq3noEYU4YC4apGX4xgWw&dib_tag=se&keywords=3+inch+toothpick+frame+fpv&qid=1791853636&sprefix=3+inch+toothpick+frame+fp%2Caps%2C159&sr=8-| TBD from CAD | ~$0 |

Notes on this table:

- The propellers must fit the motor's 1.5 mm shaft. Confirm the motor's prop mount before ordering.
- The battery is now the 1000 mAh pack Daniel linked, in place of the 800 mAh first planned. Its price and weight were not readable from the listing, so fill them in from the order. The listing's title says "35C" and "JST Plug", so it may not have an XT30 and may need a different pack or a new plug; see the hold note in the [drone order sheet](drone-order-sheet.md). Check its discharge rating, that it has an XT30 plug, and that its balance plug has three wires, because the charging board needs the middle one. A similar 1000 mAh 2S pack weighs about 55 to 65 g.
- The landing sensor is assumed to be a second TF-Luna. If the team picks a different one for facing down, change this row. Two TF-Lunas share one I2C bus, so one of them must be given a new address before both are fitted.
- Other batteries in stock at Pyrodrone, both with XT30: [Tattu 850 mAh 2S 95C](https://pyrodrone.com/collections/2s-batteries/products/tattu-850mah-2s-7-6v-hv-95c-lipo-battery-long-pack-with-xt30-plug), 40 g, $10.99, and [GNB 930 mAh 2S 120C](https://pyrodrone.com/collections/2s-batteries/products/gaoneng-gnb-930mah-7-4v-2s-120c-lipo-battery-xt30), 54 g, $12.99. The Tattu is a high-voltage pack that charges to 8.7 V, which the board accepts.
- The GPS antenna listed is flat and has no amplifier listed. An active ceramic patch receives better: [Taoglas AP.12F.07.0045A](https://www.digikey.com/en/products/result?keywords=AP.12F.07.0045A), $18.02, and it needs inductor L3 fitted on the board.
- The Panasonic capacitor was out of stock at DigiKey on the day checked, due back 2026-11-09.

## Swaps that remove a Chinese-made module

| Replaces | Option | Maker (home country) | Seller | Price | What changes |
|---|---|---|---|---|---|
| TF-Luna | [VL53L4CX breakout](https://www.adafruit.com/product/5425) | Adafruit (US), sensor chip by STMicroelectronics (Switzerland) | Adafruit | $14.95 | range 6 m instead of 8 m. I2C only, runs on 3 to 5 V, so it plugs into J5 or J8 with the right cable |
| TF-Luna | [VL53L1X carrier](https://www.pololu.com/product/3415) | Pololu (US), sensor chip by STMicroelectronics | Pololu | $22.95 | range 4 m, weighs 0.5 g. I2C only, 2.6 to 5.5 V, plugs into J5 or J8 with the right cable |
| TF-Luna | [Garmin LIDAR-Lite v4 LED](https://www.sparkfun.com/garmin-lidar-lite-v4-led-distance-measurement-sensor.html) | Garmin (US) | SparkFun | $69.99 | range 10 m, weighs 14.6 g, needs 5 V |
| VoCore2 | [Raspberry Pi Zero 2 W](https://www.adafruit.com/product/5291) | Raspberry Pi (UK) | Adafruit | $19.05 | full Linux, 10 g, 65 × 30 mm, built-in antenna only. Out of stock when checked |

The two STMicroelectronics-based sensors are cheaper and lighter than the TF-Luna and need no board change, at the cost of range. The VoCore2 has no drop-in replacement: the Raspberry Pi is larger and heavier, and the frame would have to be designed around it.

## Flight controller parts

All from DigiKey. Quantity is per board.

| Refs | Part | Order number | Maker (home country) | Qty | Each | Total |
|---|---|---|---|---|---|---|
| U1 | ESP32-S3 processor | [ESP32-S3FN8](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3FN8/15822446) | Espressif (China) | 1 | $4.17 | $4.17 |
| U8 | GPS module | [MAX-M10S-00B](https://www.digikey.com/en/products/detail/u-blox/MAX-M10S-00B/15712906) | u-blox (Switzerland) | 1 | $11.42 | $11.42 |
| U6 | Gyro and accelerometer | [ICM-42688-P](https://www.digikey.com/en/products/detail/tdk-invensense/ICM-42688-P/10824934) | TDK InvenSense (US, Japan) | 1 | $4.86 | $4.86 |
| U7 | Barometer | [BMP581](https://www.digikey.com/en/products/detail/bosch-sensortec/BMP581/16036134) | Bosch Sensortec (Germany) | 1 | $3.35 | $3.35 |
| U3 | 5 V buck regulator | [AP63205WU-7](https://www.digikey.com/en/products/detail/diodes-incorporated/AP63205WU-7/9858432) | Diodes Incorporated (US) | 1 | $0.89 | $0.89 |
| U4 | 3.3 V regulator, 1 A | [TLV75733PDRVR](https://www.digikey.com/en/products/detail/texas-instruments/TLV75733PDRVR/8038260) | Texas Instruments (US) | 1 | $0.48 | $0.48 |
| U5 | 3.3 V low-noise regulator | [TPS7A2033PDBVR](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A2033PDBVR/13566866) | Texas Instruments (US) | 1 | $0.35 | $0.35 |
| U2 | USB protection | [USBLC6-2SC6](https://www.digikey.com/en/products/detail/stmicroelectronics/USBLC6-2SC6/1040559) | STMicroelectronics (Switzerland) | 1 | $0.54 | $0.54 |
| X1 | 40 MHz crystal, 10 pF, ±10 ppm | [FA-128 40.0000MF10Z-K3](https://www.digikey.com/en/products/detail/epson/FA-128-40-0000MF10Z-K3/2514630) | Epson (Japan) | 1 | $1.11 | $1.11 |
| C35 | 100 µF 25 V polymer capacitor | [TCJD107M025R0055](https://www.digikey.com/en/products/detail/avx-corporation/TCJD107M025R0055/4990375) | Kyocera AVX (US, Japan) | 1 | $3.65 | $3.65 |
| D5 | Battery surge diode | [SMAJ18A](https://www.digikey.com/en/products/detail/littelfuse-inc/SMAJ18A/762282) | Littelfuse (US) | 1 | $0.51 | $0.51 |
| D1 | Schottky diode, 1 A 40 V, SOD-123 | [1N5819HW-7-F](https://www.digikey.com/en/products/detail/diodes-incorporated/1N5819HW-7-F/814970) | Diodes Incorporated (US) | 1 | $0.31 | $0.31 |
| D2, D3, D4 | LEDs, 0603: red, yellow-green, yellow | 150060RS75000, 150060VS75000, 150060YS75000 | Würth Elektronik (Germany) | 3 | $0.15 | $0.45 |
| J4 | ESC connector, JST-SH 8-pin | [SM08B-SRSS-TB](https://www.digikey.com/en/products/detail/jst-sales-america-inc/SM08B-SRSS-TB-LF-SN/926714) | JST (Japan) | 1 | $0.85 | $0.85 |
| J5 | Obstacle sensor port, JST-GH 4-pin | SM04B-GHS-TB | JST (Japan) | 1 | $0.39 | $0.39 |
| J7 | Charging port, JST-SH 7-pin | SM07B-SRSS-TB | JST (Japan) | 1 | $0.80 | $0.80 |
| J6, J8 | Radio port and landing sensor port, JST-SH 4-pin top entry | [BM04B-SRSS-TB](https://www.digikey.com/en/products/detail/jst-sales-america-inc/BM04B-SRSS-TB/926696) | JST (Japan) | 2 | $0.53 | $1.06 |
| J1, J3 | Antenna sockets, U.FL | [U.FL-R-SMT-1(10)](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/U-FL-R-SMT-1-10/2391570) | Hirose (Japan) | 2 | $1.67 | $3.34 |
| J2 | USB-C socket, 16-pin | [USB4105-GF-A](https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441) | GCT (UK) | 1 | $0.80 | $0.80 |
| L2 | Buck inductor, 4.7 µH, 2.2 A saturation | CIGW252010EH4R7MNE | Samsung Electro-Mechanics (Korea) | 1 | $0.29 | $0.29 |
| L1 | Radio supply inductor, 2.0 nH | LQG15HS2N0B02D | Murata (Japan) | 1 | $0.10 | $0.10 |
| C1, C2, C7 to C9, C17, C24, C25, C28, C29, C31, C33, C34 | 0.1 µF 16 V, 0402 | GRM155R71C104KA88J | Murata (Japan) | 13 | $0.10 | $1.30 |
| C3, C5, C10, C11, C20 to C23 | 1 µF 10 V, 0402 | CL05A105KP5NNNC | Samsung Electro-Mechanics (Korea) | 8 | $0.10 | $0.80 |
| C6, C27, C32 | 10 nF 50 V, 0402 | GRM155R71H103KA88D | Murata (Japan) | 3 | $0.10 | $0.30 |
| C12, C13 | 15 pF 50 V, 0402 | GRM1555C1H150JA01D | Murata (Japan) | 2 | $0.10 | $0.20 |
| C26 | 2.2 µF 16 V, 0402 | GRM155R61C225KE11J | Murata (Japan) | 1 | $0.22 | $0.22 |
| C4, C30 | 10 µF 6.3 V, 0603 | GRM188R60J106ME47D | Murata (Japan) | 2 | $0.12 | $0.24 |
| C18, C19 | 22 µF 10 V, 0805 | GRM21BR61A226ME51L | Murata (Japan) | 2 | $0.19 | $0.38 |
| C16 | 10 µF 25 V, 1206 | [GRM319R61E106KA12D](https://www.digikey.com/en/products/detail/murata-electronics/GRM319R61E106KA12D/2334921) | Murata (Japan) | 1 | $0.47 | $0.47 |
| R1, R10, R11 | 10 kΩ 1%, 0402 | RC0402FR-0710KL | Yageo (Taiwan) | 3 | $0.10 | $0.30 |
| R4, R5 | 5.1 kΩ 1%, 0402 | RC0402FR-075K1L | Yageo (Taiwan) | 2 | $0.10 | $0.20 |
| R6, R8 | 1 kΩ 1%, 0402 | RC0402FR-071KL | Yageo (Taiwan) | 2 | $0.10 | $0.20 |
| R12, R13 | 2.2 kΩ 1%, 0402 | RC0402FR-072K2L | Yageo (Taiwan) | 2 | $0.10 | $0.20 |
| R7 | 470 Ω 1%, 0402 | [RC0402FR-07470RL](https://www.digikey.com/en/products/detail/yageo/RC0402FR-07470RL/726619) | Yageo (Taiwan) | 1 | $0.10 | $0.10 |
| R9 | 100 kΩ 1%, 0402 | RC0402FR-07100KL | Yageo (Taiwan) | 1 | $0.10 | $0.10 |
| R3 | 0 Ω link, 0402 | RC0402JR-070RL | Yageo (Taiwan) | 1 | $0.10 | $0.10 |
| | **Total, 69 parts** | | | | | **$44.83** |

The J7 price is an estimate from the neighbouring sizes of the same connector; the others were read from DigiKey. Each sensor also needs a cable: a JST-GH 4-pin lead for J5 and a JST-SH 4-pin lead for J8, each joined to the TF-Luna's own cable.

Not fitted, so not bought: C14 and C15 (antenna tuning) and L3 (27 nH, Murata LQG15HS27NJ02D, $0.10, only for an active GPS antenna).

Passive parts cost a few cents each in tens. Buy at least ten of every resistor and small capacitor; they are easy to lose and the extra cost is under two dollars.

## Stock problems

Checked 2026-10-11.

| Part | Status at DigiKey | What to do |
|---|---|---|
| ICM-42688-P gyro | out of stock, restock 2027-08. Also out at Mouser and Avnet | see below |
| AP63205WU-7 buck regulator | out of stock, restock 2027-01 | check Mouser on the day; listings there disagreed |
| BMP581 barometer | out of stock, restock 2026-11-04 | wait three weeks, or check Mouser |
| TPS7A2033PDBVR regulator | out of stock, restock late 2026-11 | wait, or check Mouser |
| SM04B-GHS-TB connector | out of stock, restock 2026-11-16 | wait, or check Mouser |

**The gyro is the real problem.** No authorised distributor had it. The one place showing stock was LCSC, a Chinese distributor, with 560 pieces at $20.50 each, four times the normal price. The choices:

1. Buy it from LCSC at $20.50. It is the same TDK part, but bought through a Chinese seller.
2. Check Newark, Arrow and Future on the day of ordering. Their listings were unclear or missing.
3. Change the board to a gyro that is in stock, such as a Bosch or STMicroelectronics part. That is a schematic and layout change, and a firmware driver change.

A second look on 2026-10-12 did not settle it. Search results showed Newark and Arrow each with about 1,300 pieces near $4.50, but a stock aggregator the same day showed Newark at zero. Open both sellers' own pages before choosing between the three options.

Brokers also list this part at very low prices. Parts from brokers are a known source of counterfeits, so avoid them.

## Board changes these parts needed

Two were made on 2026-10-12, and one is a choice at ordering time:

- **USB-C socket, done.** The board's footprint was drawn for a Chinese-made socket. The GCT part has the same pad and leg positions, but its mounting legs are wider. The four slots are now 0.4 mm longer (1.7 mm at the back, 1.4 mm at the front), which is the size GCT's drawing asks for. The original socket still fits the longer slots.
- **Green LED, done.** The first green LED listed needed 3.2 V to light and would have barely glowed on 3.3 V. The list now has a yellow-green type that lights at 2.0 to 2.4 V and draws about 2 to 3 mA through R7. No board change.
- **Crystal temperature range.** The crystal listed is rated −20 to 75 °C. The alternative FA-128 40.0000MF20X-K0 covers −40 to 85 °C at $0.55, with looser frequency stability and only a few hundred in stock.

## Bare board, made outside China

The board is 36 × 39 mm with four layers.

| Fab | Country | Smallest order | Lead time | Notes |
|---|---|---|---|---|
| [OSH Park](https://docs.oshpark.com/services/four-layer) | US | about $21.76 for three boards | 9 to 14 days | minimum spacing 0.127 mm |
| [Aisler](https://community.aisler.net/t/4-layer-1-6mm-enig-design-rules/3733) | Germany | about €19.50 for three boards | not confirmed | minimum spacing 0.125 mm |
| Eurocircuits | Belgium | quote only | 3 working days | minimum spacing 0.150 mm on the prototype service |

The board was drawn to a 0.12 mm spacing rule, slightly tighter than these fabs allow. Six spots were under OSH Park's 0.127 mm, each by 0.006 mm or less. They were opened up on 2026-10-12, and the board now passes the design rules check at 0.127 mm, so OSH Park and Aisler can both build it. Eurocircuits' 0.150 mm was not checked. The team is ordering from OSH Park, and the files and settings for that order are in [the rev A order sheet](../pcb/network-drone-fc/production/rev-A/order-notes.md). On OSH Park's four-layer stack the 0.3 mm antenna traces work out to about 59 Ω against a 50 Ω target. At their length that costs under 0.1 dB, so they were left as they are. An exact 50 Ω trace there would be about 0.38 mm wide.

## Regulations

The team said it prefers not to source from China because of regulations. Several US rules touch drones and Chinese components, and they differ in what they cover:

- Some apply only to work paid for with federal grant or contract money.
- Some restrict specific named companies.
- Some are about where a drone or its critical components were produced, not who sold them.
- Universities often add their own purchasing policy on top.

Which one applies to this project decides whether buying from US sellers is enough. The university's purchasing office or research-security office can answer that. Ask before the first order.

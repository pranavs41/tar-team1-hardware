# Order sheet: drone components

Everything one networking drone needs apart from the flight controller board and the parts soldered onto it. Those have their own sheet: [rev A order sheet](../pcb/network-drone-fc/production/rev-A/order-notes.md).

The current list to order from, with the flight controller parts included, is [the full order sheet](full-order-sheet.md). This page keeps the detail on how the cable parts are used.

Quantities are for **one drone**. Multiply every line by the number of drones being built. Prices were read on 2026-10-11 to 2026-10-13, before shipping and tax. Check stock on the day of ordering.

Two lines need a decision before they are ordered. They are marked **HOLD** and explained at the bottom.

## Pyrodrone

| Qty | Item | Link | Each | Total |
|---|---|---|---|---|
| 4 | RCINPower GTS V3 1303 8000KV Plus motor | [product page](https://pyrodrone.com/products/rcinpower-gts-v3-1303-8000kv-plus-2-3-inch-cinewhoop-micro-motor-gold-orange) | $20.99 | $83.96 |

In stock on 2026-10-13. Each motor is sold singly. A fifth as a spare is worth considering, since a crash usually costs a motor.

## RaceDayQuads

| Qty | Item | Link | Each | Total |
|---|---|---|---|---|
| 1 | Gemfan Hurricane 3018 propellers, pack of 8 (4 clockwise, 4 counter-clockwise), 1.5 mm hole | [product page](https://www.racedayquads.com/products/gemfan-hurricane-3018-durable-bi-blade-3-prop-8-pack-1-5mm-choose-your-color) | $4.99 | $4.99 |
| 1 | XT30 connector. **HOLD**, see the battery note | [product page](https://www.racedayquads.com/products/xt30-connector-male-or-female) | $0.99 | $0.99 |

The propeller's 1.5 mm hole matches the motor's 1.5 mm shaft. Pick a colour that shows as in stock.

## Amazon

| Qty | Item | Link | Each | Total |
|---|---|---|---|---|
| 1 | AERO SELFIE 30 A 4-in-1 ESC, 2 to 4S, 20 mm hole pattern, with its 8-pin cable | [product page](https://www.amazon.com/dp/B0DQSLQH87) | $28.90 | $28.90 |
| 2 | Benewake TF-Luna distance sensor (one faces forward, one faces down) | [product page](https://www.amazon.com/dp/B0DKCSF8C5) | $25.99 | $51.98 |
| 1 | OVONIC 2S 1100 mAh 7.6 V 60C battery with XT30 plug, pack of 2 | [product page](https://www.amazon.com/dp/B0D318NL5W) | not read | |
| 1 | Carbon fiber subframe, Daniel's pick. **HOLD** until Daniel confirms it | [product page](https://www.amazon.com/dp/B08ZNQCHP8) | not read | |

## DigiKey

These can go in the same cart as the flight controller parts.

| Qty | Item | Part number | Each | Total |
|---|---|---|---|---|
| 1 | 2.4 GHz Wi-Fi antenna, flexible, U.FL plug | [FXP73.07.0100A](https://www.digikey.com/en/products/detail/taoglas-limited/FXP73-07-0100A/2332703) | $5.41 | $5.41 |
| 1 | GPS antenna, flat adhesive, U.FL plug | [2065600100](https://www.digikey.com/en/products/result?keywords=2065600100) | $4.16 | $4.16 |
| 1 | 470 µF 35 V capacitor, soldered across the ESC's battery pads | [EEU-FR1V471](https://www.digikey.com/en/products/detail/panasonic-industry/EEU-FR1V471/2433575) | $1.08 | $1.08 |
| 1 | Plug housing for the forward sensor cable (J5), JST-GH 4-pin | [GHR-04V-S](https://www.digikey.com/en/products/detail/jst-sales-america-inc/GHR-04V-S/807816) | about $0.20 | $0.20 |
| 2 | Pre-crimped JST-GH wire, 150 mm, a socket on each end | [AGHGH28K152](https://www.digikey.com/en/products/detail/jst-sales-america-inc/AGHGH28K152/6009449) | about $0.49 | $0.98 |
| 2 | Plug housing for the charging board cable (J7), JST-SH 7-pin | [SHR-07V-S-B](https://www.digikey.com/en/products/detail/jst-sales-america-inc/SHR-07V-S-B/759871) | about $0.15 | $0.30 |
| 7 | Pre-crimped JST-SH wire, 150 mm, a socket on each end | [ASSHSSH28K152](https://www.digikey.com/en/products/detail/jst-sales-america-inc/ASSHSSH28K152/6009452) | $0.46 | $3.22 |

The capacitor was out of stock on 2026-10-11, due back 2026-11-09. Any 470 µF, 35 V, low-ESR radial capacitor from Panasonic, Nichicon or Rubycon does the same job.

The cable parts' prices are approximate, apart from the JST-SH wire, which was read from DigiKey on 2026-10-13 with about 23,000 in stock. If a link does not open, search DigiKey for the part number.

How the cable parts are used:

- **Forward sensor cable (J5).** Cut the two GH wires in half to get four leads with a socket on one end. Push them into the 4-pin housing and join the bare ends to the TF-Luna's own cable.
- **Charging board cable (J7).** Push the seven SH wires into a 7-pin housing at each end, pin 1 to pin 1. That makes the whole cable.

## Pololu

| Qty | Item | Link | Each | Total |
|---|---|---|---|---|
| 2 | JST-SH 4-pin cable, plug on one end and bare wires on the other, 30 cm | [item 5521](https://www.pololu.com/product/5521) | $2.04 | $4.08 |

One is for the downward sensor (J8), joined to that TF-Luna's cable. The other is for the networking module (J6), soldered to the VoCore2.

These plugs look like Qwiic or STEMMA QT cables, and the wire colours follow that standard, which is **not** the order J6 and J8 use. Wire them by pin number from [the hardware reference](hardware-reference.md), not by colour.

## VoCore

| Qty | Item | Link | Each | Total |
|---|---|---|---|---|
| 1 | VoCore2 Wi-Fi module | [vocore.io store](https://vocore.io/#store) | $21.48 | $21.48 |

The maker sells it from the store section of its own front page, with a cart and checkout there. There is no separate product page to link to. The price is the one recorded on 2026-10-11, so confirm it in the cart. This is the one item that ships from China: one to two weeks by air mail, or three to five days by DHL at a higher cost.

## Stack hardware

M2 nylon standoffs, screws and nuts, one kit for the whole build. M3 hardware does not fit: on the top of the board an M3 nut would sit on J8, J6 and D5. See [the full order sheet](full-order-sheet.md) for the link.

## Small items with no part chosen

| Item | Note |
|---|---|
| Motor mounting screws and propeller screws | check what comes in the motor's box first. The listing does not say |
| Heat-shrink tubing, thin | for the cable joins. Any 1.5 to 2 mm tube |

## Total for one drone

| Seller | Total |
|---|---|
| Pyrodrone | $83.96 |
| RaceDayQuads | $5.98 |
| Amazon, without the battery and subframe | $80.88 |
| DigiKey | $15.35 |
| Pololu | $4.08 |
| VoCore | $21.48 |
| WREKD, one kit for the whole build | $9.99 |
| **Sum** | **about $222** |

Add the battery, the subframe, shipping and tax.

## The holds

**Battery.** Settled on 2026-10-13: the OVONIC 2S 1100 mAh pack in the Amazon table, which comes with an XT30 plug. The URGENEX pack first picked has a small JST plug built for a few amps, and this drone draws over 20 A at full throttle.

**XT30 connector.** Which half to buy depends on what is already on the ESC's battery lead and on the battery. Order it once both are known.

**Carbon fiber subframe.** Daniel added the link. Confirm with him that it is the part he wants and how many.

# Parts list: networking drone

Everything that goes into one networking drone, with weight, where to buy it and what it costs. This table moved here from the team's Box note on 2026-10-11 and this copy is now the one to edit.

The parts soldered onto the flight controller are listed in the [README](../README.md) with their LCSC numbers. This page is the whole-drone view.

| Component | Weight | Need to purchase | Link | Price |
|---|---|---|---|---|
| ESP32-S3FN8, processor and Wi-Fi (on the PCB) | <1 g | Yes | [DigiKey](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3FN8/15822446) | $4.17 |
| ICM-42688-P IMU, gyro and accelerometer (on the PCB) | <1 g | Yes | [DigiKey](https://www.digikey.com/en/products/detail/tdk-invensense/ICM-42688-P/10824934) | $4.80 |
| MAX-M10S-00B GPS (on the PCB) | 0.5 g | Yes | [DigiKey](https://www.digikey.com/en/products/detail/u-blox/MAX-M10S-00B/15712906) | $11.42 |
| VoCore2-32MB-2xU.FL, OpenWrt Wi-Fi networking module | ~5 g, provisional, antenna allowance not yet measured | Yes | VoCore official store | $21.48 |
| RCINPower GTS V3 1303 8000KV Plus ×4, 2 to 3 inch motors | 5.6 g each, 22.4 g total | Yes | [Pyrodrone](https://pyrodrone.com/products/rcinpower-gts-v3-1303-8000kv-plus-2-3-inch-cinewhoop-micro-motor-gold-orange) | $83.96 total ($20.99 ×4) |
| 30 A 4-in-1 ESC, 2 to 4S (6 to 18 V), M3 holes on a 20 mm pattern | 5.4 g | Yes | AERO SELFIE 30A 4-in-1 brushless ESC (Amazon) | $28.90 |
| 2S LiPo, about 800 mAh, 45C or higher | ~45 g | Yes | [model not chosen yet](https://www.amazon.com/URGENEX-Battery-1000mAh-Rechargeable-Compatible/dp/B0FFBB59TM/ref=sr_1_1?crid=LACLY0AI0YAC&dib=eyJ2IjoiMSJ9.CJEXtKuY_dHG416KNuZnUbfHAL1MdDdxaMFR7FWIgSGsZfBsGdosZzWE2AosxRZwr5WiTk4rOKjlWbE0SyBaDBP4BKoWdq1N1LZg7P1VifGTahsPOGkcVpu4AO2sHZ6RR-M8Tb77edo1zooUAKZPm27d0xrV1Kq6GEWuC1YzDOKDwYDclnv1sJ5Bt5ccOupAdyRXTjmVAxC7s1gNsDmMUUmP5jrE3mgycoXdJGE3Y1AdhASarzqAZCZoGu7ddOw5XdKd_MIK8-YregXfdonO1eaus8JfGYx-aBHXs9QJ0oU.--_fb_vICGeM6ANhNaC29O8CsUI61aIgYzutNeYhxxI&dib_tag=se&keywords=2s%2B800mah%2Blipo&qid=1791737300&sprefix=2s%2B800mah%2Blip%2Caps%2C183&sr=8-1&th=1) | TBD |
| 3D-printed frame | TBD from CAD | No, printed | files linked in [`cad/`](../cad/README.md) | ~$0 |
| 3-inch propeller set and spares | ~6 g | Yes | not chosen yet | ~$15 budget |
| 5 V regulator | included in the PCB | No | built into the PCB (AP63205 buck), no separate BEC | $0 |
| PCB, flight controller: 36 × 39 mm, 4-layer, 1.6 mm thick, M3 holes on a 20 mm pattern | ~8 g, estimate | Yes | JLCPCB | ~$30 prototype budget |
| XT30 connector, wiring, capacitor | 6 to 8 g | Mostly no | existing parts and ESC hardware | ~$0 to 10 |
| Benewake TF-Luna, single-point sensor for obstacle avoidance | <5 g | Yes | [Amazon](https://www.amazon.com/dp/B0DKCSF8C5) | $25.99 |

## Totals so far

The first three rows are chips on the flight controller, so their weight is already inside the PCB's 8 g.

| | Value | What is missing |
|---|---|---|
| Weight | about 105 g | the frame, and measured weights for the PCB, VoCore2 and wiring |
| Cost per drone | about $226 | the battery, and wiring if any has to be bought |

Both numbers are estimates until the parts are on a scale and the battery is chosen.

## Still to decide

- Battery model. It needs 2S, around 800 mAh and 45C or more to supply the motors.
- Propellers. 3-inch, matched to the 1303 motors.
- Where the VoCore2 comes from. The table says the official store but has no link yet.
- Antennas for the flight controller's Wi-Fi (J1) and GPS (J3). They are not in the table. Both need a U.FL plug.
- A 470 µF 35 V low-ESR capacitor for the ESC's battery pads, if the "capacitor" in the wiring row is not already that part.

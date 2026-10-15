# Order sheet: networking drone flight controller, rev A

Status: ready to order, not ordered yet. Files made on 2026-10-13 from the board as it is in this repository.

This page is written for whoever places the order. There are three orders: the bare boards, a solder paste stencil, and the parts. They do not have to go in together. The parts can be ordered first, and the boards and stencil later. Every file named below is in this folder.

## Order 1: bare boards, OSH Park

Site: https://oshpark.com

1. Upload `network-drone-fc.kicad_pcb`. OSH Park reads KiCad board files directly. If the upload is refused, upload `gerbers.zip`, which is the same board as gerber and drill files.
2. Choose the **4 layer prototype** service.
3. On the preview page, check these before paying:

| What the preview should show | Value |
|---|---|
| Board size | 36 × 39 mm (1.42 × 1.54 in) |
| Layers | 4 |
| Corner shape | rounded, 2 mm radius |
| Large holes | four 3.2 mm mounting holes on a 20 mm square |
| Slots | four short slots on the right edge for the USB-C socket |
| Top layer | parts and most tracks |
| Bottom layer | a few tracks, one large capacitor footprint, test pads |

4. Quantity: 3 boards, which is the smallest order.

| Setting | Value |
|---|---|
| Thickness | 1.6 mm (the service's standard) |
| Finish | ENIG (the service's standard) |
| Price | about $21.76 for three boards before shipping. Confirm on the site |
| Lead time | 9 to 14 days by the site's own figure |

What the board was checked against: 0.127 mm track spacing, 0.15 mm narrowest track, 0.3 mm smallest hole, 0.1 mm copper ring around holes, 0.38 mm from copper to the board edge. Those are the limits published for this service. If the site's own check reports a problem, stop and send the message back before ordering.

## Order 2: solder paste stencil, OSH Stencils

Site: https://www.oshstencils.com (a separate company from OSH Park, with a similar name)

1. Upload `stencil-top-paste.gtp` as the paste layer and `stencil-outline.gm1` as the board outline. The site also accepts the `.kicad_pcb` file.
2. Top side only. The bottom side has eight hand-soldered parts (C35 to C39, R14 to R16) and needs no stencil.

| Setting | Value | Why |
|---|---|---|
| Material | stainless steel | lasts longer and holds fine openings better than polyimide film |
| Thickness | 4 mil (0.1 mm) | the processor's pads are 0.4 mm apart, and a thicker stencil puts down too much paste and bridges them |
| Quantity | 1 | |

The price is shown after upload. It has not been checked for this board.

## Order 3: parts, DigiKey

Site: https://www.digikey.com

Upload `bom-digikey.csv` with DigiKey's BOM or list upload tool. The columns are quantity, manufacturer part number, manufacturer, board reference and description.

| | |
|---|---|
| Lines | 37. Four parts are bought from other sellers, listed below |
| Quantities | enough for one board, with extra small resistors, capacitors and LEDs because they are easy to lose. Two of the three bare boards stay empty as spares |
| Cost with the spare small parts | about $62 at the prices read on 2026-10-11 to 2026-10-14 |
| Cost of parts for one board | $45.52 |

To build a second board, order every line again apart from the resistors and small capacitors, which already come in tens.

Four parts are bought elsewhere and are not in `bom-digikey.csv`, and one is still out of stock everywhere:

| Part | Number | Where |
|---|---|---|
| Gyro | ICM-42688-P | Newark: https://www.newark.com/invensense/icm-42688-p/mems-module-x-y-z-1-71v/dp/77AH4524 |
| 5 V regulator | AP63205WU-7 | Mouser: https://www.mouser.com/ProductDetail/Diodes-Incorporated/AP63205WU-7 |
| 3.3 V sensor regulator | TPS7A2033PDBVR | Texas Instruments: https://www.ti.com/product/TPS7A20/part-details/TPS7A2033PDBVR . Not the TPS7A0233, which is a different part |
| Sensor connector | SM04B-GHS-TB | LCSC, which ships from China, or wait for DigiKey's restock due 2026-11-16 |
| Barometer | BMP581 | in the DigiKey file. Out of stock everywhere on 2026-10-13, DigiKey restock due 2026-11-04 |

DigiKey lists JST connectors with a longer number, for example SM08B-SRSS-TB(LF)(SN). If the upload does not match one, search for the short number and pick the JST part.

Three footprints on the board are left empty on purpose and have no line in the file: C14, C15 and L3.

## Also needed for assembly

The team already has these, so they are not in any order.

- Solder paste, lead-free SAC305, no-clean, in a syringe. Standard SAC305 is preferred over low-temperature paste here, because low-temperature joints are brittle and this board lives on a vibrating frame.
- Flux pen or gel flux, and solder wick, for clearing bridges on the processor.
- Isopropyl alcohol for cleaning. Keep it away from the barometer (U7), which has an open vent hole.

## Assembly notes for the hot plate

- The board has almost no part labels printed on it, because there is no room. Place parts from `assembly-top.png`, which shows every reference and marks pin 1 in red.
- Everything on the top side goes on in one pass with the stencil and the hot plate.
- **C35**, the large 100 µF capacitor, is on the bottom side. Solder it by hand with an iron after the hot plate pass. The stripe on the part marks its positive end. Match it to the marked end of the footprint, which is the pad joined to the battery line.
- **Seven small 0402 parts on the bottom side**, soldered by hand after the hot plate pass, with flux and a fine tip. `assembly-bottom.png` shows where.
  - C36 (100 nF) beside the USB protection chip.
  - R16 (10 kΩ) beside the boot jumper.
  - R14 (143 kΩ) and R15 (34 kΩ) under the 5 V regulator. These are the battery cut-off, and swapping the two values breaks it. 0402 resistors carry no marking, so take each one straight from its labelled tape.
  - C37 (1 µF) under the crystal, and C38 and C39 (100 nF) under the processor's lower and upper edges.
- **The USB-C socket (J2)** has four legs that pass through slots. Its small pads reflow on the hot plate. Solder the four legs by hand afterwards.
- **JP1 and JP2** on the bottom are bare pad pairs, not parts. Leave them open.
- **Polarity matters** on D1, D5, the three LEDs, C35, and every chip. Pin 1 is marked on the silkscreen.
- Follow the paste maker's temperature profile. Do not hold the board at peak temperature longer than the profile says; the GPS module and the connectors' plastic are the parts that suffer first.
- After soldering, follow the bench checks in [`docs/pcb-test-plan.md`](../../../../docs/pcb-test-plan.md) before connecting a battery.

## What is not in these three orders

Motors, ESC, propellers, battery, the networking module, the two distance sensors, antennas and the ESC capacitor. Their links and prices are in [`docs/parts-list.md`](../../../../docs/parts-list.md). The charging board is a separate design and is not ready to order.

## Files in this folder

| File | What it is |
|---|---|
| `network-drone-fc.kicad_pcb` | the board, for OSH Park |
| `gerbers.zip` | the same board as 11 gerber layers and 2 drill files |
| `stencil-top-paste.gtp` | top paste layer, for the stencil |
| `stencil-outline.gm1` | board outline, for the stencil |
| `bom-digikey.csv` | parts and quantities, for DigiKey |
| `schematic.pdf` | the schematic these boards were made from |
| `assembly-top.png`, `assembly-bottom.png` | where every part goes, with its reference label. Pin 1 pads are red |

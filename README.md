# TAR Team 1 Hardware

Hardware for the Team 1 swarm mapping project (Texas Aerial Robotics, UT Austin).

Flight controller in progress by **Pranav Shivashankar**.

## Repository layout

```
electrical/
  DESIGN.md             design doc: requirements, block diagram, parts, power, board layout plan
  docs/
    circuits/           how every circuit works and why it's there, box by box
    design-decisions.md dated log of design decisions
    pin-map.md          ESP32 pin, net name and destination, for firmware
    datasheets.md       links to every datasheet and reference design
    bring-up.md         first power-on checklist
  pcb/
    network-drone-fc/   KiCad 9 project: schematic, PCB, schematic.pdf
      lib/              custom symbols, footprints, 3D models
      production/       gerbers, BOM and notes per board revision
mechanical/             frame and mount CAD, board STEP exports
```

## Network drone flight controller

KiCad 9 project in [`electrical/pcb/network-drone-fc/`](electrical/pcb/network-drone-fc/). Open `network-drone-fc.kicad_pro`. The design plan is in [`electrical/DESIGN.md`](electrical/DESIGN.md).

[View the schematic as a PDF](electrical/pcb/network-drone-fc/schematic.pdf) or the [placement render](electrical/pcb/network-drone-fc/placement-top.png) if you don't have KiCad. Regenerate it after schematic changes: `kicad-cli sch export pdf network-drone-fc.kicad_sch -o schematic.pdf`.

- 4-layer board, 36 × 39 mm, four 3.2 mm M3 holes on a 20 × 20 mm pattern so it stacks on a bought 20 × 20 4-in-1 ESC
- All parts on the top side only, so the whole board can be reflowed on a hot plate; test points (bare pads) may go on the bottom
- Designed for a 2S battery; input stage tolerates up to 4S

### Parts in `lib/tar_fc`

Symbols, footprints and 3D models (STEP) pulled from LCSC/EasyEDA. The project's library tables already point at them.

| Function | Part | LCSC |
|---|---|---|
| MCU, bare chip (8 MB flash in package) | ESP32-S3FN8 | C2913196 |
| MCU crystal, 40 MHz ±10 ppm | Q22FA12800101 (2016) | C255898 |
| MCU module (fallback only, not used) | ESP32-S3-MINI-1U-N8 | C2980299 |
| Flight IMU (SPI) | ICM-42688-P | C1850418 |
| Barometer | BMP581 | C5362283 |
| GPS | u-blox MAX-M10S | C4153167 |
| Antenna connector (ESP32 / GPS) | U.FL-R-SMT-1 | C88374 |
| 5 V buck (3.8 to 32 V in) | AP63205WU-7 | C2071056 |
| 3.3 V LDO, digital | TLV75733PDBVR | C485517 |
| 3.3 V LDO, sensors (low noise) | TPS7A2033PDBVR | C2862740 |
| Battery TVS (18 V standoff, safe up to 4S) | SMAJ18A | C908771 |
| GPS bias-T inductor, 27 nH (fit only for an active antenna) | Murata LQG15HS27NJ02D (0402) | C12669 |
| USB 5 V OR-ing diode | B5819W | C8598 |
| USB ESD | USBLC6-2SC6 | C7519 |
| USB-C (USB 2.0, 16-pin) | TYPE-C 16PIN 2MD(073) | C2765186 |
| ESC connector (8-pin JST-SH) | SM08B-SRSS-TB | C160407 |
| Peripheral port (4-pin JST-GH) | SM04B-GHS-TB (LCSC stock low; drop-in alt XY-SM04B-GHS-TB C51940118) | C189895 |
| VDD3P3 filter inductor, 2.0 nH ±0.1 nH, 900 mA | Murata LQG15HS2N0B02D (0402) | C2986275 |

From the stock KiCad libraries (already have 3D models):

- Passives: `Resistor_SMD` / `Capacitor_SMD` 0402
- Buck inductor, 4.7 µH: `Inductor_SMD:L_1008_2520Metric` (e.g. FTC252010S4R7MBCA, C5832360). Check the value against the AP63205 datasheet.
- 6-pin JST-GH: `Connector_JST:JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal`
- Mounting holes: `MountingHole:MountingHole_3.2mm_M3` (plain, no copper, courtyard trimmed to the 3 mm keep-out)
- RESET/BOOT pad pairs: `Jumper:SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm`

### Adding a part

```
pip install easyeda2kicad
python -m easyeda2kicad --full --lcsc_id=C123456 --output electrical/pcb/network-drone-fc/lib/tar_fc
```

Then change the new footprint's `model` path to `${KIPRJMOD}/lib/tar_fc.3dshapes/<name>.step` so it works on every machine.

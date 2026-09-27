# TAR Team 1 — Hardware

Hardware for the Team 1 swarm mapping project (Texas Aerial Robotics, UT Austin).

Flight controller designed by **Pranav Shivashankar**.

## Network drone flight controller

KiCad 9 project in [`network-drone-fc/`](network-drone-fc/). Open `network-drone-fc.kicad_pro`.

- 4-layer board, 27 × 27 mm, four M2 holes on a 20 × 20 mm pattern so it stacks on a bought 4-in-1 ESC
- Parts on both sides: ESP32 + sensors on top, power + connectors on the bottom (facing the ESC)
- Designed for a 2S battery; input stage tolerates up to 4S
- Resize the outline to match the ESC once it is chosen

### Parts in `lib/tar_fc`

Symbols, footprints and 3D models (STEP) pulled from LCSC/EasyEDA. The project's library tables already point at them.

| Function | Part | LCSC |
|---|---|---|
| MCU, bare chip (8 MB flash in package) | ESP32-S3FN8 | C2913196 |
| MCU crystal, 40 MHz ±10 ppm | Q22FA12800101 (2016) | C255898 |
| MCU module (fallback only, not used) | ESP32-S3-MINI-1U-N8 | C2980299 |
| Flight IMU (SPI) | ICM-42688-P | C1850418 |
| Orientation IMU | BNO085 | C5189642 |
| 32.768 kHz crystal (BNO085) | FC-12M 32.768 kHz 7 pF | C99009 |
| Barometer | BMP581 | C5362283 |
| GPS | u-blox MAX-M10S | C4153167 |
| Antenna connector (ESP32 / GPS) | U.FL-R-SMT-1 | C88374 |
| 5 V buck (3.8–32 V in) | AP63205WU-7 | C2071056 |
| 3.3 V LDO, digital | TLV75733PDBVR | C485517 |
| 3.3 V LDO, sensors (low noise) | TPS7A2033PDBVR | C2862740 |
| Battery TVS | SMAJ15A | C113958 |
| USB 5 V OR-ing diode | B5819W | C8598 |
| USB ESD | USBLC6-2SC6 | C7519 |
| USB-C | USB4105-GF-A | C3020560 |
| ESC connector (8-pin JST-SH) | SM08B-SRSS-TB | C160407 |
| Peripheral port (4-pin JST-GH) | SM04B-GHS-TB | C189895 |

From the stock KiCad libraries (already have 3D models):

- Passives: `Resistor_SMD` / `Capacitor_SMD` 0402
- Buck inductor, 4.7 µH: `Inductor_SMD:L_1008_2520Metric` (e.g. FTC252010S4R7MBCA, C5832360). Check the value against the AP63205 datasheet.
- 6-pin JST-GH: `Connector_JST:JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal`
- Mounting holes: `MountingHole:MountingHole_2.2mm_M2_Pad`

### Adding a part

```
pip install easyeda2kicad
python -m easyeda2kicad --full --lcsc_id=C123456 --output network-drone-fc/lib/tar_fc
```

Then change the new footprint's `model` path to `${KIPRJMOD}/lib/tar_fc.3dshapes/<name>.step` so it works on every machine.

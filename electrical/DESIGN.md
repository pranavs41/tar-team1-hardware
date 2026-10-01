# Network drone flight controller: design document

Designer: Pranav Shivashankar · Texas Aerial Robotics, Team 1 · Rev A (in progress)

This is the plan for the board: what it has to do, what's on it, how power and signals flow, and where everything goes on the PCB. For how each individual circuit works, see [docs/circuits](docs/circuits/README.md).

## 1. What the board does

The flight controller for the network (relay) drones in the swarm. It:

- stabilises and flies the drone (the IMU and barometer feed the ESP32, which drives 4 brushless motors through the ESC)
- carries the Wi-Fi/BLE link that relays mapping data back to the base station
- reads GPS so the drone can reference the RTK ground station for landing
- runs from a 2S battery through a bought 4-in-1 ESC stacked underneath

Charging is handled by a separate board.

## 2. Requirements

| Requirement | Value |
|---|---|
| Components | bare chips only, no modules or breakout boards |
| Battery | 2S LiPo/Li-ion (6.0 to 8.4 V); input survives up to 4S (16.8 V) |
| Board size | 36 × 36 mm, 2 mm corner radius |
| Mounting | four M2 holes on a 20 × 20 mm pattern, centred, to stack on a 20 × 20 ESC |
| Assembly | hot plate only, so all parts on the top side; bottom has test pads only |
| Layers | 4 |
| Programming | USB-C (native ESP32-S3 USB); UART test pads as fallback |
| Antennas | U.FL for Wi-Fi and for GPS |

## 3. Block diagram

```
                 ┌──────────────── ESC connector (JST-SH 8) ────────────────┐
                 │ VBAT   GND   CUR   TLM   M1  M2  M3  M4                    │
                 └──┬───────────────┬─────┬────┬───┬───┬───┬─────────────────┘
                    │               │     │    │   │   │   │
   USB-C ─► ESD ─►──┼── D1 ──┐      │     │    └───┴───┴───┴── DShot ─────┐
                    │        ▼      │     │                               │
   TVS ─────────────┤     +5V rail  │     └── ESC_TELEM (UART) ──────┐    │
   VBAT/11 divider ─┤        │      └── ESC_CUR (ADC1) ───────────┐  │    │
                    ▼        │                                    ▼  ▼    ▼
              AP63205 buck ──┘                              ┌──────────────────┐
                             ├─ TLV75733 ─► +3V3 ─────────► │  ESP32-S3FN8     │◄─ 40 MHz crystal
                             │                              │                  │── π network ─► U.FL (Wi-Fi)
                             └─ TPS7A2033 ─► +3V3_SENS      │  USB D+/D−       │◄─ USB-C
                                   │                        │                  │── 3 LEDs, RESET, BOOT
                                   ▼                        └──┬─────┬─────┬───┘
                         ┌─────────────────────┐   SPI bus     │ I2C │ UART│ UART
                         │ ICM-42688-P (IMU)   │◄──────────────┘     │     │
                         │ BMP581 (barometer)  │◄────────────────────┘     │
                         │ MAX-M10S (GPS) ─► U.FL (GPS antenna)  ◄─────────┘
                         └─────────────────────┘
   Spare ports: JST-GH I2C (ToF etc.), JST-GH UART (companion / telemetry)
   Charging port: JST-GH to the charging board, DOCK_DET (GPIO) and AUX_ADC (ADC1)
```

## 4. Components

### Main chips

| Ref | Part | Job | Package |
|---|---|---|---|
| U1 | ESP32-S3FN8 | MCU, Wi-Fi/BLE, 8 MB flash in package | QFN-56 7 × 7 |
| X1 | 40 MHz ±10 ppm crystal | MCU clock | 2016 |
| U2 | USBLC6-2SC6 | USB ESD protection | SOT-23-6 |
| U3 | AP63205WU | 5 V buck, 2 A | TSOT-23-6 |
| U4 | TLV75733 | 3.3 V LDO for ESP32 (`+3V3`) | SOT-23-5 |
| U5 | TPS7A2033 | low-noise 3.3 V LDO for sensors (`+3V3_SENS`) | SOT-23-5 |
| TBD | ICM-42688-P | gyro and accelerometer (SPI); orientation fusion runs on the ESP32 | LGA-14 2.5 × 3 |
| TBD | BMP581 | barometer (I2C) | LGA-10 2 × 2 |
| TBD | u-blox MAX-M10S | GPS (UART) | LCC 9.7 × 10.1 |

Refs marked TBD are assigned when the sensors box is drawn. LCSC part numbers are in the [repo README](../README.md).

### Connectors and user interface

| Ref | Part | Purpose |
|---|---|---|
| J1 | U.FL | Wi-Fi antenna |
| J2 | USB-C 16-pin | programming, debug, bench power |
| TBD | U.FL | GPS antenna |
| TBD | JST-SH 8-pin | ESC: VBAT, GND, current, telemetry, 4 motor signals |
| TBD | JST-GH 4-pin ×2 | spare I2C port, spare UART port |
| TBD | JST-GH 4-pin | charging board port: GND, DOCK_DET, AUX_ADC, spare |
| SW1, SW2 | tactile switches | RESET, BOOT |
| D2, D3, D4 | 0603 LEDs | red power, green status, yellow status |
| TP1 to TP6 | test pads (bottom) | UART0 TX/RX, VBAT, +5V, +3V3, +3V3_SENS |

## 5. Power

| Rail | Source | Feeds | Budget |
|---|---|---|---|
| `VBAT` | battery via ESC connector | buck, divider, TVS | limited by the battery |
| `+5V` | AP63205 buck (or USB through D1) | both LDOs, spare-port 5 V | 2 A max |
| `+3V3` | TLV75733 | ESP32, LEDs | ~350 mA peak (Wi-Fi TX) |
| `+3V3_SENS` | TPS7A2033 | ICM-42688-P, BMP581, GPS | ~60 mA |

The sensors get their own low-noise rail so radio transmit bursts don't show up as IMU and barometer noise.

## 6. Interfaces

Full pin table: [docs/pin-map.md](docs/pin-map.md).

| Bus | Devices | ESP32 pins |
|---|---|---|
| SPI | ICM-42688-P | GPIO10 to 13 |
| I2C | BMP581, spare I2C port | GPIO33, 34 |
| UART | GPS | GPIO35, 36 |
| UART | spare port | GPIO37, 38 |
| UART RX | ESC telemetry | GPIO17 |
| GPIO in | dock connected (`DOCK_DET`), from the charging board | GPIO18 |
| ADC1 | analog input from the charging board (`AUX_ADC`) | GPIO8 |
| DShot | 4 motors | GPIO4 to 7 |
| ADC1 | battery voltage, ESC current | GPIO1, 2 |
| USB | USB-C | GPIO19, 20 |

## 7. Board layout plan

Top view, 36 × 36 mm. Holes (●) on the 20 × 20 pattern sit 8 mm in from each edge. The ESC is underneath.

```
 ┌────────────────────────────────────────────┐
 │ [GPS U.FL]  GPS          ▲ north   [Wi-Fi  │
 │  MAX-M10S                          U.FL]   │
 │        ●                        ●   π net  │
 │                                            │
 │   BMP581                 ESP32-S3  crystal │
 │   (foam)     ICM-42688-P  (QFN)            │  ← USB-C
 │              (centre)                      │
 │        ●                        ●  LEDs    │
 │  buck + inductor   LDOs    RESET BOOT      │
 │  [JST-GH]   [ESC JST-SH 8]      [JST-GH]   │
 └────────────────────────────────────────────┘
```

Why things go where they do:

| Area | Contents | Reason |
|---|---|---|
| Centre | ICM-42688-P | Least vibration and closest to the centre of rotation; far from the buck |
| Right | ESP32, crystal, Wi-Fi U.FL | Crystal hard against pins 53/54; RF trace to the U.FL short and straight at the board edge |
| Top left | GPS and its U.FL | Opposite corner from the Wi-Fi antenna and away from the buck, whose switching noise desenses GPS |
| Bottom left | buck, LDOs | Next to the ESC connector where VBAT enters; tight switching loop kept away from sensors and RF |
| Bottom edge | ESC and spare-port connectors | Cables drop straight down to the ESC and out the sides |
| Right edge | USB-C, LEDs | Reachable and visible with the stack assembled |
| Left | BMP581 | Out of direct prop wash and away from LED light and buck heat; covered with open-cell foam |
| Bottom side | test pads only | Hot-plate assembly: nothing to solder on the bottom |

Keep-outs: the four mounting holes plus grommet clearance (about 5 mm diameter), and the area under the Wi-Fi and GPS RF traces (no other routing).

### Layer stackup (4 layers)

| Layer | Use |
|---|---|
| L1 (top) | all components, short signal routing, RF traces |
| L2 | solid GND plane, unbroken under RF traces, crystal and IMU |
| L3 | power (`+5V`, `+3V3`, `+3V3_SENS`) and remaining signals |
| L4 (bottom) | test pads, leftover signals, GND fill |

The 50 Ω RF trace width comes from JLCPCB's impedance calculator for the stackup chosen at order time.

## 8. Status

| Stage | State |
|---|---|
| Parts selected, libraries imported | done |
| Schematic: MCU, USB, power | done, ERC clean |
| Schematic: sensors | in progress (ICM-42688-P next) |
| Schematic: connectors | to do |
| Footprints assigned, final ERC | to do |
| PCB layout | to do |
| Order rev A | to do |
| Bring-up | to do ([checklist](docs/bring-up.md)) |

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
   Spare port: JST-GH I2C (ToF etc.); spare UART on test pads
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
| U6 | ICM-42688-P | gyro and accelerometer (SPI); orientation fusion runs on the ESP32 | LGA-14 2.5 × 3 |
| U7 | BMP581 | barometer (I2C) | LGA-10 2 × 2 |
| U8 | u-blox MAX-M10S | GPS (UART) | LCC 9.7 × 10.1 |

LCSC part numbers are in the [repo README](../README.md).

### Connectors and user interface

| Ref | Part | Purpose |
|---|---|---|
| J1 | U.FL | Wi-Fi antenna |
| J2 | USB-C 16-pin | programming, debug, bench power |
| J3 | U.FL | GPS antenna |
| J4 | JST-SH 8-pin | ESC: VBAT, GND, current, telemetry, 4 motor signals |
| J5 | JST-GH 4-pin | spare I2C port |
| J7 | JST-GH 4-pin | charging board port: GND, DOCK_DET, AUX_ADC, spare |
| JP1, JP2 | pad pairs on the bottom | RESET, BOOT (short to GND with tweezers) |
| D2, D3, D4 | 0603 LEDs | red power, green status, yellow status |
| TP1 to TP18 | test pads (bottom) | UART0 TX/RX, the four rails, IMU SPI, I2C, GPS UART, ESC telemetry, spare UART |

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
| UART | spare, on test pads | GPIO37, 38 |
| UART RX | ESC telemetry | GPIO17 |
| GPIO in | dock connected (`DOCK_DET`), from the charging board | GPIO18 |
| ADC1 | analog input from the charging board (`AUX_ADC`) | GPIO8 |
| DShot | 4 motors | GPIO4 to 7 |
| ADC1 | battery voltage, ESC current | GPIO1, 2 |
| USB | USB-C | GPIO19, 20 |

## 7. Board layout

Top view, 36 × 36 mm, 2 mm corner radius. The four M2 holes (plain, no copper) sit on the 20 × 20 pattern, 8 mm in from each edge, with a 3 mm keep-out around each so a 6 mm grommet or standoff fits. The ESC is underneath. All parts are on the top side; only the six test pads are on the bottom. This is the placement as scripted in `electrical/pcb/`; routing is done by hand.

```
 ┌────────────────────────────────────────────┐
 │ [J3 GPS U.FL]  bias-T   U8 GPS   [J7 charge] │  top edge
 │    ●                            ●   LEDs    │
 │ [J5 I2C]  LDOs   U6 IMU   U1 ESP32  U2  USB │  right edge: J2 USB-C
 │   D1       C4/C19        crystal   caps     │
 │ U7 baro  buck: U3 L2 D5 C16 C18     π net   │
 │    ●     divider           ●   [J1 Wi-Fi]   │
 │          [J4 ESC JST-SH 8]                  │  bottom edge
 └────────────────────────────────────────────┘
```

| Area | Contents | Reason |
|---|---|---|
| Centre | U6 ICM-42688-P with its three capacitors and the CS pull-up | Least vibration, closest to the centre of rotation, far from the buck |
| Centre-right | U1 ESP32 (rotated 180° so the RF pin faces the right edge), decoupling in one column beside it, crystal below it | Short paths from every power pin to its capacitor; crystal hard against pins 53/54 |
| Right edge | J2 USB-C, U2 ESD chip and the CC resistors above it, three LEDs with their resistors, J1 Wi-Fi U.FL at the lower right with the π network beside it | Cable and LEDs reachable with the stack assembled; RF trace short and straight to the edge |
| Top edge | U8 GPS at top centre with J3 and the bias-T at the top-left corner, J7 charging-board port at the top right | GPS in the corner opposite the Wi-Fi antenna and away from the buck; the top-right slot is the only edge left for a third port |
| Left edge | J5 I2C port, D1 USB diode above it, the two LDOs beside the IMU, U7 barometer at the lower left | Barometer away from the buck's heat and the LEDs' light |
| Bottom centre | U3 buck, L2, D5 TVS, C16 input and C18 output capacitors, the battery divider column | Right above the ESC connector where VBAT enters, switching loop kept small and away from the sensors and both antennas |
| Bottom edge | J4 ESC connector, centred between the holes | The only connector that must face the ESC |
| Bottom side | TP1 to TP18 test pads and the RESET/BOOT pad pairs | Nothing to solder, so the top stays the only reflow side |

Design rules set in the board: 0.12 mm clearance, 0.2 mm default track, 0.6/0.3 mm vias, 0.3 mm copper-to-edge, 4 copper layers.

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
| Schematic: sensors | done |
| Schematic: connectors | done |
| Footprints assigned, final ERC | done, 0 errors, 0 warnings |
| PCB placement | done, DRC clean apart from silkscreen warnings |
| PCB routing | in progress (by hand) |
| Order rev A | to do |
| Bring-up | to do ([checklist](docs/bring-up.md)) |

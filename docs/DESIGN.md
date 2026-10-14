# Network drone flight controller: design document

Designer: Pranav Shivashankar · Texas Aerial Robotics, Team 1 · Rev A (in progress)

This is the plan for the board: what it has to do, what's on it, how power and signals flow, and where everything goes on the PCB. For how each individual circuit works, see [circuits](circuits/README.md).

## 1. What the board does

The flight controller for the network (relay) drones in the swarm. It:

- stabilises and flies the drone (the IMU and barometer feed the ESP32, which drives 4 brushless motors through the ESC)
- carries the Wi-Fi/BLE link that relays mapping data back to the base station
- reads GPS so the drone can reference the RTK ground station for landing
- runs from a 2S battery through a bought 4-in-1 ESC stacked underneath

Charging is handled by a separate board, described in [charging-board.md](charging-board.md).

## 2. Requirements

| Requirement | Value |
|---|---|
| Components | bare chips only, no modules or breakout boards |
| Battery | 2S LiPo/Li-ion (6.0 to 8.4 V); input survives up to 4S (16.8 V) |
| Board size | 36 wide × 39 tall mm, 2 mm corner radius |
| Mounting | four 3.2 mm (M3) holes on a 20 × 20 mm pattern, matching the bought ESC |
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
   Sensor port: JST-GH, 5 V I2C, for the TF-Luna obstacle sensor
   Radio port: JST-SH top entry, 5 V UART, for the VoCore2 networking module
   Charging port: JST-SH to the charging board: battery, I2C, power good, charge status, charge disable
   Landing sensor port: JST-SH, 5 V I2C, for the downward distance sensor
```

## 4. Components

### Main chips

| Ref | Part | Job | Package |
|---|---|---|---|
| U1 | ESP32-S3FN8 | MCU, Wi-Fi/BLE, 8 MB flash in package | QFN-56 7 × 7 |
| X1 | 40 MHz ±10 ppm crystal | MCU clock | 2016 |
| U2 | USBLC6-2SC6 | USB ESD protection | SOT-23-6 |
| U3 | AP63205WU | 5 V buck, 2 A | TSOT-23-6 |
| U4 | TLV75733 | 3.3 V LDO for ESP32 (`+3V3`) | WSON-6 2 × 2 with thermal pad |
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
| J5 | JST-GH 4-pin | sensor port: 5 V, SCL, SDA, GND (TF-Luna obstacle sensor) |
| J6 | JST-SH 4-pin, top entry | radio port: 5 V, TX, RX, GND (VoCore2 networking module); data lines shared with J4 pins 7 and 8 |
| J7 | JST-SH 7-pin | charging board port: BATT+, GND, SDA, SCL, /PG, STAT, CD |
| J8 | JST-SH 4-pin, top entry | landing sensor port: 5 V, SCL, SDA, GND |
| JP1, JP2 | pad pairs on the bottom | RESET, BOOT (short to GND with tweezers) |
| D2, D3, D4 | 0603 LEDs | red power, green status, yellow status |
| TP1 to TP6, TP13 | test pads (bottom, on vias) | UART0 TX/RX, the four rails, I2C SCL |

## 5. Power

| Rail | Source | Feeds | Budget |
|---|---|---|---|
| `VBAT` | battery via ESC connector | buck, divider, TVS, 100 µF bulk capacitor | limited by the battery |
| `+5V` | AP63205 buck (or USB through D1) | both LDOs, sensor port J5, radio port J6 | 2 A max |
| `+3V3` | TLV75733 | ESP32, LEDs | ~350 mA peak (Wi-Fi TX) |
| `+3V3_SENS` | TPS7A2033 | ICM-42688-P, BMP581, GPS | ~60 mA |

The sensors get their own low-noise rail so radio transmit bursts don't show up as IMU and barometer noise. Measured budget, heat and sag check: [power-budget.md](power-budget.md).

## 6. Interfaces

Full pin table: [pin-map.md](pin-map.md).

| Bus | Devices | ESP32 pins |
|---|---|---|
| SPI | ICM-42688-P | GPIO33, 34, 35, 47 (MISO); interrupt on GPIO48 |
| I2C | BMP581, sensor port J5 (TF-Luna) | GPIO37, 38 |
| UART | GPS | GPIO36 (TX), GPIO18 (RX) |
| UART | radio port J6 (VoCore2), or ESC telemetry on RX | GPIO2 (TX), GPIO10 (RX) |
| GPIO in | charger power good (`CHG_PG`), low when docked | GPIO9 |
| GPIO in | charge status (`CHG_STAT`) | GPIO8 |
| GPIO out | charge disable (`CHG_CD`), high stops charging | GPIO7 |
| DShot | 4 motors | GPIO16, 6, 11, 13 (motors 1 to 4) |
| ADC1 | battery voltage; ESC current when the radio port is not used | GPIO4, 2 |
| USB | USB-C | GPIO19, 20 |

## 7. Board layout

Top view, 36 wide by 39 tall, 2 mm corner radius. The four 3.2 mm M3 holes (plain, no copper) sit on the 20 × 20 pattern, 8 mm in from the left, right and bottom edges and 11 mm from the top. Nothing on the top side comes within 3 mm of a hole centre, so a 6 mm grommet, nut or standoff fits at every hole, and the bottom side has nothing near the holes at all. The extra 3 mm strip along the top exists for one reason: it is the only place the charging port fits without crowding the H2 hole. The ESC is underneath. All parts are on the top side except C35, the bulk capacitor, which sits on the bottom at the lower-left corner outside the ESC's outline; the test pads and the RESET/BOOT pad pairs are on the bottom too. Routing is complete: the critical nets by hand, the rest with a grid router, then straightened and checked (see docs/power-budget.md and the decisions log).

```
 ┌────────────────────────────────────────────┐
 │                                [J7 charge]  │  top strip
 │ [J3 GPS U.FL]  bias-T   U8 GPS                │
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
| Top edge | U8 GPS at top centre with J3 and the bias-T at the top-left corner, J7 charging-board port at the top right, in the 3 mm strip above the hole line, with the landing sensor port J8 below it on the right edge | GPS in the corner opposite the Wi-Fi antenna and away from the buck; the strip lets J7 clear H2 by 5 mm instead of sitting on top of it |
| Left edge | J5 sensor port, D1 USB diode above it, the two LDOs beside the IMU, U7 barometer at the lower left | Barometer away from the buck's heat and the LEDs' light |
| Bottom centre | U3 buck, L2, D5 TVS, C16 input and C18 output capacitors, the battery divider column | Right above the ESC connector where VBAT enters, switching loop kept small and away from the sensors and both antennas |
| Bottom edge | J4 ESC connector, centred between the holes | The only connector that must face the ESC |
| Bottom-right corner | J6 radio port, top entry | The only free spot; no edge has room for another side-entry connector |
| Bottom side | C35 bulk capacitor at the lower-left corner, seven test pads on vias, the RESET/BOOT pad pairs, and the second signal layer | One iron-soldered part; the top stays the only reflow side |

Design rules set in the board: 0.12 mm clearance, 0.2 mm default track, 0.6/0.3 mm vias, 0.3 mm copper-to-edge, 4 copper layers.

### Layer stackup (4 layers)

| Layer | Use |
|---|---|
| L1 (top) | all components, most signal routing, RF traces, `+5V` and `+3V3_SENS`, GND fill |
| L2 | solid GND plane, unbroken under RF traces, crystal and IMU |
| L3 | solid `+3V3` plane; every `+3V3` pad reaches it through a via |
| L4 (bottom) | motor, USB and I2C escapes from the ESP32, test pads, GND fill |

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
| PCB routing | done, 163 vias, every track horizontal, vertical or 45 degrees, DRC 0 errors (silkscreen and five courtyard warnings only) |
| Order rev A | to do |
| Bring-up | to do ([checklist](bring-up.md)) |

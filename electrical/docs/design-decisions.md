# Design decisions

Why the network drone flight controller is built the way it is. Add a row when a decision changes, don't rewrite history.

| Date | Decision | Why |
|---|---|---|
| 2026-09-26 | Bare chips only, no modules or breakout boards | Team rule; we design every support circuit ourselves |
| 2026-09-26 | ESP32-S3FN8 (bare QFN-56) as the MCU | Wi-Fi/BLE for the relay mesh, native USB, 8 MB flash in package; the MINI-1U module stays in `lib/` as a fallback only |
| 2026-09-26 | 2S battery, input stage tolerates up to 4S | 2S is more efficient for hovering relay nodes and lets a plain buck make 5 V (1S would need buck-boost) |
| 2026-09-26 | Bought 20 × 20 4-in-1 ESC, not integrated | ESC power stage is noisy and risky on a first board |
| 2026-09-26 | Board 36 × 36 mm, M2 holes on a 20 × 20 pattern | Everything fits on one side, so the whole board reflows on a hot plate in one pass |
| 2026-09-26 | All parts on the top side; bottom has only test pads | Our only assembly method is a hot plate |
| 2026-09-26 | ICM-42688-P for the rate loop | Fast, low-latency SPI gyro and accelerometer |
| 2026-09-26 | BMP581 barometer | Lowest noise of the options, 2 × 2 mm |
| 2026-09-26 | u-blox MAX-M10S GPS with U.FL antenna | Drones reference an RTK ground station for landing |
| 2026-09-26 | Wi-Fi antenna on U.FL, RF pi network footprints kept | Antenna can mount high for stacking; matching can be tuned later with a VNA |
| 2026-09-26 | USB-C is the only programming port | Native USB flashes and debugs with no extra chip; UART0 test pads are the fallback |
| 2026-09-26 | Charging is a separate board | Out of scope for the FC |
| 2026-09-27 | SMAJ18A TVS instead of SMAJ15A | SMAJ15A breaks down at 16.7 V, below a full 4S pack |
| 2026-09-27 | Separate low-noise `+3V3_SENS` rail for sensors | Keeps ESP32 radio TX current spikes out of the IMU and barometer supply |
| 2026-09-27 | Dropped the BNO085 | Overlaps the ICM-42688-P (both are accel and gyro). Its fused output is too slow for the rate loop, orientation fusion runs fine on the ESP32 as on Betaflight and PX4 boards, and its magnetometer would sit centimetres from motor currents. Saves about $20, a dozen parts and five ESP32 pins. If heading is needed later, add a small I2C magnetometer or use the GPS puck's compass. |
| 2026-09-30 | ESC connector follows the Betaflight 4-in-1 order (GND, VBAT, CUR, TLM, M1 to M4) | Most 20 × 20 ESCs use it; confirm against the ESC before ordering |
| 2026-09-30 | I2C and UART ports use the Dronecode order (VCC, signal, signal, GND) | Off-the-shelf cables fit |
| 2026-09-30 | Charging-board port carries DOCK_DET (GPIO18) and AUX_ADC (GPIO8, ADC1); ESC telemetry moved to GPIO17 | ADC2 is unusable while Wi-Fi runs, so the port needed an ADC1 pin; GPIO17 was freed by dropping the BNO085 |
| 2026-09-30 | Mounting holes are plain 2.2 mm holes with no copper ring | Nothing needs to connect to the screws; copper rings only made clearance to the connectors harder |
| 2026-09-30 | USB diode D1 sits by the I2C port on the left edge, not next to the USB-C | The right edge is full; D1 only carries the 5 V feed, so a longer trace costs nothing |
| 2026-09-30 | RESET and BOOT are pad pairs on the bottom, not pushbuttons | Only needed for recovery; USB resets the chip for normal flashing; frees the top edge |
| 2026-09-30 | 3 mm keep-out around each mounting hole | Room for a 6 mm soft-mount grommet or standoff, per the team review |
| 2026-09-30 | Spare UART port dropped to test pads TP17/TP18 | With the 3 mm keep-out there is one connector slot per edge; GPS, USB-C, ESC and the I2C port take four, the charging port takes the top-right |
| 2026-09-30 | Twelve more bottom-side test pads (SPI, I2C, GPS UART, ESC telemetry) | Every bus can be probed when a chip doesn't answer; they cost nothing on a single-side assembly |


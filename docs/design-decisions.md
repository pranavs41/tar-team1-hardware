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
| 2026-09-26 | ICM-42688-P for the rate loop, BNO085 for orientation | ICM-42688 is a fast, low-latency SPI gyro; BNO085's fusion output is too slow for the rate loop |
| 2026-09-26 | BMP581 barometer | Lowest noise of the options, 2 × 2 mm |
| 2026-09-26 | u-blox MAX-M10S GPS with U.FL antenna | Drones reference an RTK ground station for landing |
| 2026-09-26 | Wi-Fi antenna on U.FL, RF pi network footprints kept | Antenna can mount high for stacking; matching can be tuned later with a VNA |
| 2026-09-26 | USB-C is the only programming port | Native USB flashes and debugs with no extra chip; UART0 test pads are the fallback |
| 2026-09-26 | Charging is a separate board | Out of scope for the FC |

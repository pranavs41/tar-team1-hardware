# How the flight controller works

A walkthrough of every circuit on the network drone flight controller: what each one does, and why it's there. Written while designing the board, for anyone on the team who wants to understand it, review it, or build the next revision.

Read in order. Each page covers one box of the schematic.

| Page | Covers |
|---|---|
| [1. MCU](01-mcu.md) | ESP32-S3 chip, its power pins, reset, boot, crystal, antenna, status LEDs |
| [2. USB](02-usb.md) | USB-C connector, ESD protection, powering from USB |
| [3. Power](03-power.md) | Battery input, surge protection, 5 V buck, the two 3.3 V regulators, battery voltage sensing |
| 4. Sensors | *to be written* |
| 5. Connectors | *to be written* |

## Ideas that show up everywhere

**Decoupling capacitors.** Every chip power pin gets its own capacitor, placed right next to the pin, going to GND. When the chip suddenly draws current, the capacitor supplies it before the voltage can dip. Pins often get two or three values (e.g. 10 µF + 1 µF + 0.1 µF) because each size works best at a different frequency: big ones handle slow, large dips, small ones handle fast noise. Each capacitor goes **directly from the power net to GND** (in parallel), never stacked end to end.

**Pull-up and pull-down resistors.** Hold a pin at a known level when nothing is actively driving it, so noise can't flip it.

**Net labels.** Two wires with the same label name are connected, even across the page. We use them to connect boxes instead of long wires, and to avoid wires crossing pin rows (where an accidental junction dot creates a short).

**Power symbols.** `GND`, `+5V`, `+3V3`, `+3V3_SENS` connect by name everywhere on the sheet. One name per rail, used consistently.

**No-connect flags.** An X on a pin means "left open on purpose", so the rules check stays clean and reviewers know it wasn't forgotten.

**DNP (do not populate).** A footprint that exists on the board but is left empty at assembly, so a part can be added later without a new board revision.

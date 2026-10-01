# How the flight controller works

These pages walk through every circuit on the network drone flight controller: what each part does and why we put it there. I wrote them while designing the board so that anyone on the team can review it, debug it, or build the next revision without having to ask me.

Each page covers one box of the schematic. Read them in order if you're new to board design, since later pages lean on ideas from earlier ones.

| Page | What it covers |
|---|---|
| [1. MCU](01-mcu.md) | The ESP32-S3 and everything it needs to run: power pins, reset, boot, crystal, antenna, status LEDs |
| [2. USB](02-usb.md) | The USB-C port, its protection, and powering the board from a laptop |
| [3. Power](03-power.md) | Getting from the battery to clean 5 V and 3.3 V, plus measuring battery voltage |
| [4. Sensors](04-sensors.md) | The ICM-42688-P IMU, BMP581 barometer and MAX-M10S GPS |
| 5. Connectors | Not written yet |

## A few ideas you'll see on every page

Every chip power pin gets its own decoupling capacitor to GND, placed right next to the pin. When the chip suddenly pulls more current, that capacitor supplies it before the voltage has time to dip. You'll often see two or three sizes on one pin, like 10 µF, 1 µF and 0.1 µF. The big ones cover slow, deep dips and the small ones cover fast noise. Each capacitor connects straight from the power net to GND. If you stack two end to end you've put them in series and most of the capacitance disappears (I did this once on this board and had to fix it).

A pull-up or pull-down resistor holds a pin at a known level when nothing is driving it, so noise can't flip it.

Net labels connect wires by name. Two labels that say `SPI_SCK` are the same wire even if they're on opposite sides of the page. We use them to link the boxes together and to keep wires from crossing rows of chip pins. A wire crossing a pin row is how you get an accidental junction dot, and a junction dot is a short. We found three of those on this schematic.

Power symbols (`GND`, `+5V`, `+3V3`, `+3V3_SENS`) also connect by name. Each rail has exactly one name, used everywhere.

An X on a pin is a no-connect flag. It means we left the pin open on purpose, which keeps KiCad's rules check quiet and tells a reviewer we didn't forget it.

DNP means "do not populate". The footprint is on the board but nothing gets soldered there at assembly. It lets us add a part later without ordering a new board.

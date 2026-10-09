# 2. USB

USB-C is the board's only programming port. Plug in a normal USB-C cable and you can flash firmware, read a serial console and debug over JTAG, all through USB hardware that's built into the ESP32-S3. Older ESP32 boards needed a separate USB to serial chip like a CP2102 or CH340, and this one doesn't.

## The connector (J2)

J2 is a generic 16-pin USB-C connector wired for USB 2.0. USB-C puts every signal on both rows of pins so the cable works either way up.

| Pins | Signal | Connects to |
|---|---|---|
| A6 and B6 | D+ | tied together, then to U2 pin 1 |
| A7 and B7 | D− | tied together, then to U2 pin 3 |
| A4B9, B4A9 | VBUS, 5 V from the laptop | the `VBUS` net |
| A5 | CC1 | R5, 5.1 kΩ to GND |
| B5 | CC2 | R4, 5.1 kΩ to GND |
| A1B12, B1A12, 13, 14 | ground and the metal shell | GND |
| A8, B8 | SBU | no-connect, since USB 2.0 doesn't use them |

The two 5.1 kΩ resistors tell the laptop or charger that a device is plugged in and wants 5 V. Leave them off and most USB-C ports supply nothing at all. CC1 and CC2 each need their own resistor, because the host checks both lines separately to work out which way the cable went in.

We picked a generic connector (LCSC C2765186) at about $0.07 over a name-brand one at $1.03. The ESP32 only does USB 2.0 speeds, and at those speeds the two perform the same.

## ESD protection (U2, USBLC6-2SC6)

The connector is the part people touch, and static discharge from a finger or cable would go straight into the ESP32's USB pins. The USBLC6 has diodes inside that dump those spikes to GND or VBUS first.

The data lines pass straight through it. Pins 1 and 6 are the same line inside the chip, and so are pins 3 and 4. We bring the connector side into pins 1 and 3 and take the ESP32 side out of pins 6 and 4, which also tells whoever lays out the PCB how to route it: the signal should pass over the protection pads on its way in. Pin 5 goes to VBUS so the clamp diodes have a voltage to clamp against.

From U2, the labels `USB_DP` and `USB_DN` carry the lines to ESP32 pin 26 (GPIO20) and pin 25 (GPIO19).

## Running the board from USB (D1, B5819W)

VBUS goes into D1's anode, and its cathode (the side with the stripe) feeds `+5V`. That lets a laptop power the whole board for bench work without a battery. The diode also stops the battery's 5 V from flowing back into the laptop when both are plugged in.

We used a Schottky diode because it only drops about 0.3 to 0.4 V, compared with about 0.7 V for a regular diode. On USB power the 5 V rail sits around 4.6 V, which is still plenty for the 3.3 V regulators.

## If the connector breaks

Solder on a new one. Hot air makes this much easier than an iron because the pins are fine pitch. If USB is completely dead, the UART test pads TP1 and TP2 can still flash the chip.

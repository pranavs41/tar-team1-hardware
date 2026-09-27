# 2. USB

USB-C is the only programming port. Plug a normal USB-C cable into a laptop and you get flashing, a serial console and JTAG debugging, all through the ESP32-S3's built-in USB. Older ESP32s needed a separate USB-to-serial chip (CP2102, CH340); this one doesn't.

## Connector: J2 (generic 16-pin USB-C, USB 2.0)

USB-C has every signal twice so the cable works either way up. On the connector:

| Pins | Signal | Connects to |
|---|---|---|
| A6 + B6 | D+ | tied together → U2 pin 1 |
| A7 + B7 | D− | tied together → U2 pin 3 |
| A4B9, B4A9 | VBUS (5 V from the host) | `VBUS` net |
| A5 | CC1 | R5 5.1 kΩ to GND |
| B5 | CC2 | R4 5.1 kΩ to GND (separate resistor) |
| A1B12, B1A12, 13, 14 | GND and shell | GND |
| A8, B8 | SBU | no-connect (not used for USB 2.0) |

**The two 5.1 kΩ resistors on CC1/CC2** tell the host "I am a device, give me 5 V". Without them most USB-C ports and chargers supply nothing. Each CC pin needs its own resistor because the host checks each one separately to work out which way the cable is plugged in.

We use a generic 16-pin connector (LCSC C2765186, about $0.07) instead of a name-brand one ($1.03). For USB 2.0 speed, which is all the ESP32 does, there is no difference.

## ESD protection: U2 USBLC6-2SC6

Fingers and cables touch the connector pins, and static discharge would go straight into the ESP32's fragile USB pins. The USBLC6 has diodes that dump those spikes to GND or VBUS first.

- The data lines pass straight through it: pins 1 and 6 are the same line internally, as are 3 and 4. The connector side goes into pins 1/3 and the ESP32 side comes out of pins 6/4, which also tells the layout the intended routing (the signal should pass over the protection pads on its way in).
- Pin 5 connects to VBUS so the internal clamp diodes have a reference.
- From U2 to the ESP32, the lines are labelled `USB_DP` → pin 26 (GPIO20) and `USB_DN` → pin 25 (GPIO19).

## Powering from USB: D1 B5819W

`VBUS` → D1 (anode) → `+5V` (cathode, the stripe). This lets USB power the whole board for bench work without a battery, and blocks the battery's 5 V from flowing back into the laptop when both are connected. A Schottky diode drops only ~0.3–0.4 V (a normal diode drops ~0.7 V), so the 5 V rail sits around 4.6 V on USB, which is plenty for the 3.3 V regulators.

## If the connector breaks

Resolder a new one; hot air makes it much easier than an iron. The UART test pads (TP1/TP2) are the fallback for flashing if USB is completely dead.

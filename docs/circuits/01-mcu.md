# 1. MCU: ESP32-S3FN8

The brain of the board. It runs the flight controller, talks to the sensors, drives the ESC, and handles the Wi-Fi/BLE link for the relay mesh.

We use the **bare chip** (7 × 7 mm QFN-56), not a module. A module hides the crystal, flash, RF matching and decoupling inside a metal can; with the bare chip we build each of those ourselves. The reference we follow is Espressif's own schematic for the ESP32-S3-MINI-1U (datasheet Figure 8-2), which is this same chip with a U.FL antenna connector.

"FN8" means 8 MB of flash memory is built into the chip package, so there is no separate flash chip.

## Power pins

The chip has several supply pins because different parts of the silicon need clean power. All connect to `+3V3` except VDD_SPI.

| Pin(s) | Name | Feeds | Capacitors to GND |
|---|---|---|---|
| 2, 3 | VDD3P3 | radio power amplifier | 0.1 µF, then **L1 2.0 nH**, then 10 µF + 1 µF + 0.1 µF |
| 55, 56 | VDDA | analog circuits | 1 µF + 10 nF |
| 46 | VDD3P3_CPU | processor | 0.1 µF |
| 20 | VDD3P3_RTC | low-power domain | 0.1 µF |
| 29 | VDD_SPI | **output**: powers the internal flash | 0.1 µF + 1 µF, **not** connected to +3V3 |
| 57 | exposed pad | GND and heat | — |

**Why L1 (2.0 nH) on VDD3P3.** An inductor's impedance rises with frequency: X = 2π·f·L. At 2.4 GHz, 2 nH is about 30 Ω, while at DC it's nearly zero. So power passes through freely, but radio-frequency energy from the power amplifier can't leak back onto the `+3V3` rail and disturb everything else. Together with the capacitors on each side it forms an LC low-pass filter. It must be rated 500 mA or more (we use Murata LQG15HS2N0B02D, 900 mA, ±0.1 nH) because the full transmit current flows through it.

**Why 10 µF on VDD3P3.** When the radio starts transmitting, its current jumps by hundreds of milliamps in microseconds. The 10 µF supplies that burst so the rail doesn't sag.

## Reset: CHIP_PU (pin 4)

CHIP_PU is "chip power-up": high means run, low means held in reset.

- **R1 10 kΩ to +3V3** holds it high so the chip runs.
- **C11 1 µF to GND** delays startup. At power-on the capacitor is empty, so the pin starts low and rises over about R × C = 10 ms. That keeps the chip in reset until the 3.3 V rail has settled; starting on a half-risen supply can hang it.
- **SW1 RESET to GND** pulls the pin low when pressed.

## Boot mode: GPIO0 (pin 5)

**SW2 BOOT to GND.** No resistor: GPIO0 has an internal pull-up. If GPIO0 is low when the chip comes out of reset, it enters download (flashing) mode. Normally the flashing tool does this automatically over USB; the button is the recovery path when bad firmware crashes USB: hold BOOT, tap RESET, release BOOT.

Keep the wires from these buttons away from the pin rows. An early version had the BOOT wires crossing GPIO1 and the motor lines, and the junction dots shorted them together.

## 40 MHz crystal (pins 53, 54)

The crystal is the chip's clock. Every internal clock, including the 2.4 GHz radio frequency, is derived from it, so it needs ±10 ppm accuracy or the radio drifts off-channel.

- **X1** (Q22FA12800101, 2016 size) between XTAL_P and XTAL_N; its pins 2 and 4 go to GND.
- **C12, C13 15 pF**, one from each side to GND. A crystal oscillates at exactly its rated frequency only when it sees its specified load capacitance CL (10 pF for ours). The two capacitors are effectively in series, plus about 3 pF of stray capacitance from the traces: CL = C/2 + C_stray → 10 = C/2 + 3 → C = 14 pF, nearest standard value 15 pF. Too much makes it run slow, too little fast; these may be tuned on the real board.
- **R2 0 Ω in series with XTAL_P.** Espressif puts a footprint here so a 24 nH inductor can be fitted if the crystal's harmonics interfere with the radio. We start with a 0 Ω jumper, same as Espressif's module.

Layout: the crystal must sit right next to pins 53/54 with short traces and nothing else routed nearby.

## Antenna: LNA_IN (pin 1) → U.FL

- **R3 0 Ω** in series, **C14 and C15 DNP** from each side to GND, then **J1 U.FL** connector (shield pins to GND).
- These three footprints form a **π matching network**. The chip's radio pin is not exactly 50 Ω, but the cable and antenna are; a mismatch reflects power back instead of radiating it. The right values depend on the finished board and are found with a vector network analyzer (VNA), which is why Espressif lists them as TBD.
- We start with 0 Ω straight through and the capacitors empty, which usually works. The empty footprints mean we can tune later without a new board.
- The trace from pin 1 to the U.FL must be a 50 Ω controlled-impedance trace: short, straight, ground plane underneath, ground vias along both sides.
- A U.FL (rather than a PCB antenna) lets the antenna mount high on the drone, which matters for stacking.

## Flash pins 30–35

SPIHD, SPIWP, SPICS0, SPICLK, SPIQ, SPID connect to the internal flash. They must stay unconnected (no-connect flags).

Pins 28 (SPICS1), 36 (SPICLK_N) and 37 (SPICLK_P) have flash-sounding names but are ordinary GPIOs on this chip: GPIO26, GPIO48 and GPIO47.

## Strapping pins

GPIO0, GPIO3, GPIO45 and GPIO46 are read at boot to choose modes. GPIO45 selects the flash voltage and must be low for our 3.3 V flash; its internal pull-down handles that, so it's left floating. GPIO3 and GPIO46 are also left floating. GPIO0 only has the BOOT button.

## Status LEDs

Each LED is source → resistor → LED → GND. Resistor from R = (V_supply − V_f) / I, aiming for about 1.3 mA, which is plenty bright for an indicator.

| LED | Driven by | Resistor | Meaning (suggested) |
|---|---|---|---|
| D2 red | `+3V3` directly | 1 kΩ | power is on |
| D3 green | pin 37 (GPIO47) | 470 Ω | system OK / armed |
| D4 yellow | pin 36 (GPIO48) | 1 kΩ | warning / radio activity |

Green's forward voltage (~2.7 V) is higher than red's or yellow's (~2.0 V), so it gets a smaller resistor for the same current. An ESP32 pin can source about 20 mA, so it drives these directly.

## UART test pads

TP1 on U0TXD (pin 49) and TP2 on U0RXD (pin 50). The chip prints its boot log here even when USB isn't working, and it can be flashed through these pads with a USB-serial adapter. If a board won't show up on USB, these tell you whether the problem is the connector or the chip.

## Signal pins

The remaining GPIOs carry net labels that connect to the sensor and connector boxes. See [pin-map.md](../pin-map.md) for the full table. Two choices worth knowing:

- `VBAT_SENSE` and `ESC_CUR` are on GPIO1/GPIO2 because those are on ADC1. ADC2 is shared with the Wi-Fi radio and gives bad readings while Wi-Fi is on.
- The IMU SPI bus uses GPIO10–13, the chip's native SPI pins, which run fastest.

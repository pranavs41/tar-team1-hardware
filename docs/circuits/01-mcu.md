# 1. MCU: ESP32-S3FN8

The ESP32 runs the flight controller. It reads the sensors, sends motor commands to the ESC, and handles the Wi-Fi and BLE link that the relay mesh depends on.

We're using the bare chip, a 7 × 7 mm QFN with 56 pins. The usual shortcut is an ESP32 module, which is the same chip in a metal can with the crystal, flash, antenna matching and capacitors already inside. Our team rule is bare chips only, so everything the module would have done for us is on this page. The reference I followed is Espressif's own schematic for the ESP32-S3-MINI-1U (Figure 8-2 in its datasheet), which is this exact chip wired to a U.FL connector.

The "FN8" in the part number means 8 MB of flash is built into the chip package, so there's no separate flash chip to add.

## Power pins

The chip has several supply pins because different parts of the silicon want their own clean power. All of them go to `+3V3` except VDD_SPI.

| Pin | Name | What it powers | Capacitors to GND |
|---|---|---|---|
| 2, 3 | VDD3P3 | the radio's power amplifier | 0.1 µF, then L1 (2.0 nH), then 10 µF, 1 µF and 0.1 µF |
| 55, 56 | VDDA | analog circuits | 1 µF and 10 nF |
| 46 | VDD3P3_CPU | the processor | 0.1 µF |
| 20 | VDD3P3_RTC | the low power domain | 0.1 µF |
| 29 | VDD_SPI | this one is an output that powers the internal flash | 0.1 µF and 1 µF, with no connection to +3V3 |
| 57 | exposed pad | ground and heat | none |

KiCad draws pins 3 and 56 hidden underneath pins 2 and 55, so one wire to each spot connects both.

The inductor L1 is there because of the radio. An inductor's impedance goes up with frequency (X = 2π·f·L). At the 2.4 GHz radio frequency, 2 nH works out to about 30 Ω, while at DC it's close to zero. Power passes through without trouble, and radio frequency energy from the amplifier gets blocked from leaking back onto `+3V3`, where it would add noise to everything else. With the capacitors on both sides it makes an LC low pass filter. The whole transmit current flows through it, so it needs to be rated for at least 500 mA. We use a Murata LQG15HS2N0B02D, which is 900 mA and ±0.1 nH.

The 10 µF on VDD3P3 exists for the moment the radio starts transmitting. Current jumps by a few hundred milliamps in microseconds, and that capacitor supplies the burst so the rail doesn't sag.

## Reset (CHIP_PU, pin 4)

CHIP_PU is the chip's power-up pin. High means run, low means hold in reset.

R1 (10 kΩ to +3V3) keeps the pin high so the chip runs. C11 (1 µF to GND) delays startup: when power first arrives the capacitor is empty, so the pin starts low and climbs over roughly R × C = 10 ms. That holds the chip in reset until the 3.3 V rail has settled. An ESP32 that starts on a half-risen supply can hang. JP1 is a pair of pads, one on CHIP_PU and one on GND; shorting them with tweezers pulls the pin low and resets the chip.

## Boot pads (GPIO0, pin 5)

JP2 is a second pad pair, GPIO0 to GND. There's no resistor because GPIO0 has a pull-up inside the chip. If GPIO0 is low when the chip comes out of reset, it starts in download mode for flashing. The flashing tool normally handles this over USB by itself. The pads are for when bad firmware has crashed the USB peripheral: short BOOT, short and release RESET, release BOOT, and it will take new firmware. Pad pairs replaced the two pushbuttons on 2026-09-30 because the buttons took up edge space the connectors needed.

Keep the wires from these two pad pairs away from the row of chip pins. My first version ran the BOOT wires across the GPIO1 and motor lines, and the junction dots where they crossed shorted GPIO0 to GPIO1 and two motor outputs to ground.

## 40 MHz crystal (pins 53 and 54)

The crystal is the chip's clock, and every internal clock comes from it, including the 2.4 GHz radio frequency. It has to be accurate to ±10 ppm or the radio drifts off its channel.

X1 (Q22FA12800101, 2016 size) sits between XTAL_P and XTAL_N, with its pins 2 and 4 grounded. C12 and C13 are 15 pF each, one from each side to GND. A crystal only runs at its rated frequency when it sees a specific load capacitance, called CL, which is 10 pF for ours. The two capacitors act in series, and the traces and pins add roughly 3 pF of stray capacitance, so:

CL = C/2 + C_stray, which gives 10 = C/2 + 3, so C = 14 pF. The nearest standard value is 15 pF.

Too much capacitance makes the crystal run slow and too little makes it run fast, so these may need adjusting once we can measure a real board.

Espressif's reference design leaves a 0 Ω jumper footprint in series with XTAL_P so a 24 nH inductor can go in if the crystal's harmonics interfere with the radio. We dropped it: their own module ships with 0 Ω, and on our board the crystal sits so close to the chip that the extra footprint only lengthened the trace.

On the PCB, the crystal goes right next to pins 53 and 54, with short traces and nothing else routed nearby.

## Antenna (LNA_IN, pin 1, to U.FL)

The radio pin goes through R3 (0 Ω), with C14 and C15 as empty footprints from each side to GND, and then to J1, the U.FL connector. The U.FL's shield pins go to GND.

Those three footprints form a π matching network. The chip's radio pin isn't exactly 50 Ω, while the cable and antenna are, and a mismatch reflects some of the power back into the chip. Finding the right values means measuring the finished board with a vector network analyzer, which is why Espressif marks them TBD. We start with 0 Ω straight through and both capacitors left empty, which usually works well enough. If the range turns out poor, we can solder in tuning parts without a new board.

The trace from pin 1 to the U.FL has to be a 50 Ω controlled impedance trace. Keep it short and straight, with solid ground on the layer below and ground vias along both sides.

We used a U.FL because it lets the antenna mount up high on the drone, which matters when the drones stack in the case. A PCB antenna would sit flat on the board.

## Flash pins (30 to 35)

SPIHD, SPIWP, SPICS0, SPICLK, SPIQ and SPID are wired to the flash inside the package. They stay unconnected, each with a no-connect flag.

Three nearby pins have flash-sounding names but are ordinary GPIOs on this chip: pin 28 (SPICS1) is GPIO26, pin 36 (SPICLK_N) is GPIO48 and pin 37 (SPICLK_P) is GPIO47. We use the last two for the IMU interrupt and SPI MISO.

## Strapping pins

The chip reads GPIO0, GPIO3, GPIO45 and GPIO46 at boot to decide how to start. GPIO45 picks the flash voltage and has to be low for our 3.3 V flash. Its internal pull-down takes care of that, so we leave it floating along with GPIO3 and GPIO46. GPIO0 only has the BOOT pad pair JP2 on it.

## Status LEDs

Each LED is wired as source, resistor, LED, then GND. The resistor comes from R = (V_supply − V_f) / I, where V_f is the LED's forward voltage. I aimed for about 1.3 mA, which is plenty bright for an indicator.

| LED | Driven by | Resistor | Suggested meaning |
|---|---|---|---|
| D2, red | `+3V3` directly | 1 kΩ | power is on |
| D3, green | pin 45 (GPIO40) | 470 Ω | running, or armed when solid |
| D4, yellow | pin 44 (GPIO39) | 1 kΩ | warnings or radio activity |

Green has a higher forward voltage (around 2.7 V) than red or yellow (around 2.0 V), so it gets a smaller resistor to reach the same current. An ESP32 pin can supply about 20 mA, which is far more than these need, so the pins drive the LEDs directly.

## UART test pads

TP1 is on U0TXD (pin 49) and TP2 is on U0RXD (pin 50). The chip prints its boot log on this UART even when USB isn't working, and you can flash it through these pads with a USB serial adapter. If a board doesn't show up on USB, these pads tell you whether the connector or the chip is the problem.

## Signal pins

The rest of the GPIOs have net labels that connect to the sensor and connector boxes. The full table is in [pin-map.md](../pin-map.md). Two of the choices matter for firmware:

`VBAT_SENSE`, `ESC_CUR` and `AUX_ADC` are on GPIO4, GPIO2 and GPIO8 because those pins belong to ADC1. The ESP32's other ADC, ADC2, shares hardware with the Wi-Fi radio and gives bad readings while Wi-Fi is running.

The IMU SPI bus is on GPIO33, 34, 35 and 47, which the chip reaches through its internal routing matrix. The native SPI pins (GPIO10 to 13) would run a little faster, but at the IMU's 8 kHz sample rate the matrix is nowhere near its limit, and those pins were needed as top-layer escapes for the motor signals. The one rule the matrix does not bend: a signal on GPIO0, 3, 45 or 46 would upset the boot straps, so none of ours are there.

# 3. Power

Turns the battery into the clean supply rails every chip needs.

```
Battery (via ESC connector)
  VBAT 6–8.4 V (2S), up to 16.8 V (4S)
   │
   ├── D5 SMAJ18A TVS          surge protection
   ├── R 100k / 10k divider ─► VBAT_SENSE (ESP32 ADC)
   │
   └── U3 AP63205 buck ──► +5V ◄── USB (through D1)
                            │
                            ├── U4 TLV75733 LDO ──► +3V3        ESP32, LEDs
                            └── U5 TPS7A2033 LDO ─► +3V3_SENS   IMUs, barometer, GPS
```

`VBAT` is the raw battery voltage and must never touch an ESP32 pin (they tolerate about 3.6 V). The ESP32 only sees `VBAT_SENSE`, a scaled-down copy.

## Surge protection: D5 SMAJ18A

When the motors brake, the ESC pushes voltage spikes back onto the battery wires. A TVS (transient voltage suppressor) diode sits across the battery and starts conducting when the voltage goes above its breakdown, clamping the spike before it reaches the regulators.

- Cathode (bar) on `VBAT`, anode on GND. It is **unidirectional**: backwards, it conducts all the time and shorts the battery. Use KiCad's `Diode:SMAJ18A` symbol, which marks the cathode; the generic `Device:D_TVS` is the bidirectional kind.
- **Why 18 V and not 15 V.** A TVS starts conducting at its breakdown voltage. The SMAJ15A's is 16.7 V, below a full 4S pack (16.8 V), so on 4S it would conduct constantly and overheat. The SMAJ18A breaks down around 20 V and clamps at about 29 V, still under the buck's 32 V maximum.

## 5 V buck regulator: U3 AP63205

A buck converter steps voltage down efficiently (~90%). An LDO dropping 8.4 V to 5 V would burn the difference as heat (3.4 V × current); on a battery drone, efficiency is flight time.

How it works: the chip switches its SW pin rapidly (about 1 MHz) between VBAT and GND. The inductor and output capacitors smooth that square wave into steady 5 V. The chip measures its own output on FB and adjusts how long it stays on each cycle.

| Part | Value | Why |
|---|---|---|
| C16 | 10 µF **25 V** | Input capacitor. Supplies the buck's sharp current pulses so they don't travel down the battery wires. 25 V rating because it sees battery voltage; ceramic capacitors lose much of their capacitance when run close to their rated voltage. |
| EN (pin 2) → VBAT | — | Enable. Tied high, the regulator runs whenever a battery is connected. |
| C17 BST–SW | 100 nF | Bootstrap capacitor. The chip's high-side switch needs a gate voltage above VIN to turn fully on; this capacitor stores it. The buck won't run without it. |
| L2 | 4.7 µH | The energy-storage element that turns switching into smooth DC. Value from the datasheet's table for 5 V output. |
| C18, C19 | 22 µF 10 V each | Output capacitors. Smooth the ripple and supply current during load jumps. |
| FB (pin 1) → +5V | — | Feedback. The "05" in AP63205 means fixed 5 V output, so FB connects straight to the output with no resistor divider. |

All values are from the AP63205 datasheet, Table 3 and Figure 1.

Layout: the input capacitor, chip, inductor and output capacitors must be packed tightly together. The switching current loop acts like a radio transmitter if it's large, so the buck goes in its own corner, away from the antenna, GPS and IMU.

## 3.3 V regulators: U4 TLV75733 and U5 TPS7A2033

Both are LDOs (low-dropout linear regulators) taking `+5V` down to 3.3 V. Each has 1 µF on the input and 1 µF on the output, EN tied to its input so it's always on, and pin 4 (NC) left unconnected. Dropping 5 V to 3.3 V in an LDO wastes some power, but the currents here are small and an LDO's output is much quieter than a buck's.

**Why two separate 3.3 V rails.** The ESP32's radio draws spiky current, bursts of 300 mA or more when transmitting. On a shared rail those spikes ripple into the sensors' supply and show up as IMU and barometer noise. So:

| Rail | Regulator | Powers |
|---|---|---|
| `+3V3` | TLV75733 (1 A) | ESP32, LEDs |
| `+3V3_SENS` | TPS7A2033 (300 mA, low noise) | ICM-42688-P, BNO085, BMP581, GPS |

## Battery voltage sensing

```
VBAT ── 100k ──┬── 10k ── GND
               ├── 100nF ── GND
               └── VBAT_SENSE → ESP32 pin 6 (GPIO1, ADC1)
```

- The divider outputs VBAT × 10k / (100k + 10k) = **VBAT ÷ 11**: 8.4 V (full 2S) → 0.76 V, 16.8 V (full 4S) → 1.53 V, both safely inside the ADC range. Firmware multiplies the reading by 11.
- **Why 100 kΩ, not smaller.** The divider draws current from the battery constantly, even with the drone off: 8.4 V / 110 kΩ = 76 µA. With 10k + 1k it would be 760 µA, enough to noticeably drain a battery left plugged in for a week in the case.
- **The 100 nF capacitor.** The ADC samples in quick bursts and 100 kΩ can't recharge its input instantly; the capacitor holds a steady voltage for it to read and filters motor noise off the measurement.

## Test points

`VBAT`, `+5V`, `+3V3`, `+3V3_SENS` each get a test pad for probing during bring-up (see [bring-up.md](../bring-up.md)).

## PWR_FLAG

KiCad's rules check wants every power net to have a "source". Our rails come from connector pins or regulator symbols whose pins aren't marked as power outputs, so it complains that they are "not driven". A `PWR_FLAG` symbol on each rail tells it the source is real. Only place one where a real source exists; it silences the check.

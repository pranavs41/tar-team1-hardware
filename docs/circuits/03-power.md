# 3. Power

This box turns the battery into the supply rails that every chip on the board runs from.

```
Battery (through the ESC connector)
  VBAT: 6 to 8.4 V on 2S, up to 16.8 V on 4S
   |
   +-- D5 SMAJ18A TVS          surge protection
   +-- C35 100 uF polymer      bulk capacitor, soaks up ESC noise
   +-- 100k / 10k divider ---> VBAT_SENSE (ESP32 ADC)
   |
   +-- U3 AP63205 buck -----> +5V <--- USB (through D1)
                               |
                               +-- J5 pin 1, J6 pin 1         TF-Luna sensor, VoCore2 radio
                               +-- U4 TLV75733 ----> +3V3        ESP32, LEDs
                               +-- U5 TPS7A2033 ---> +3V3_SENS   IMUs, barometer, GPS
```

`VBAT` is the raw battery voltage and it must never reach an ESP32 pin, since those only tolerate about 3.6 V. The ESP32 sees `VBAT_SENSE`, a scaled-down copy.

## Surge protection (D5, SMAJ18A)

When the motors brake, the ESC pushes voltage spikes back up the battery wires. A TVS (transient voltage suppressor) diode sits across the battery and starts conducting once the voltage passes its breakdown point, which clamps the spike before it reaches the regulators.

The cathode, the side with the bar, goes on `VBAT` and the other side goes to GND. This is a one-direction TVS, and if you put it in backwards it conducts all the time and shorts the battery. Use KiCad's `Diode:SMAJ18A` symbol, which marks the cathode. The generic `Device:D_TVS` symbol is the two-direction kind and doesn't show which side is which.

We first picked the SMAJ15A and changed it. A TVS starts conducting at its breakdown voltage, and the SMAJ15A's is 16.7 V, just under a fully charged 4S pack at 16.8 V. On 4S it would conduct constantly and cook itself. The SMAJ18A breaks down around 20 V and clamps at about 29 V, which is still below the 32 V the buck regulator can take.

## Bulk capacitor (C35, 100 µF 25 V polymer tantalum)

The motors draw current in pulses and throw voltage back onto the battery wires when they brake. The TVS clamps the big spikes, but the everyday ripple needs a capacitor that can take and give back charge quickly, which means a large value with a low ESR (equivalent series resistance). A ceramic cannot reach 100 µF at 25 V in a package this board can carry, and an aluminium electrolytic can is too tall, so C35 is a polymer tantalum: 100 µF, 25 V, 55 mΩ, in a flat D case on the bottom of the board next to the ESC connector. Polymer tantalums do not fail short the way old manganese tantalums did, and 25 V is three times the 2S battery voltage. The 470 µF electrolytic that FPV builds put on the ESC's battery pads is still worth adding there, closer to the source of the noise.

It is polarised. The stripe on the part is the positive end and goes to VBAT; the board's silkscreen marks it. Backwards, a tantalum shorts and burns.

## 5 V buck regulator (U3, AP63205)

A buck converter steps voltage down at about 90% efficiency. A linear regulator dropping 8.4 V to 5 V would turn the difference into heat, 3.4 V times whatever current flows, and on a battery powered drone that lost energy is flight time.

The chip switches its SW pin between VBAT and GND about a million times a second. The inductor and output capacitors smooth that square wave into a steady 5 V, and the chip watches its own output on the FB pin to decide how long to stay on each cycle.

| Part | Value | What it's for |
|---|---|---|
| C16 | 10 µF, 25 V, 0805 | Input capacitor. Supplies the buck's sharp current pulses locally so they don't run down the battery wires. It's rated 25 V because it sees battery voltage, and ceramic capacitors lose a lot of capacitance when run near their rating. It was a 1206 at first, which keeps more of its value under bias. It became an 0805 on 2026-10-14 so the battery track could reach VIN beside it, leaving the EN pin free. At 8.4 V an 0805 keeps roughly 4 µF, which still holds the input ripple to tens of millivolts. The bulk filtering for motor noise is C35 on this board and the 470 µF electrolytic on the ESC's battery pads. |
| R14, R15 on EN, pin 2 | 143 kΩ from VBAT, 34 kΩ to GND | Battery cut-off. EN turns the regulator on above 1.18 V and off below 1.10 V. The chip also feeds the pin 1.5 µA while off and 5.5 µA while on, which widens the gap. Together that turns the board on when the battery rises past about 5.9 V and off when it falls below about 4.9 V. 4.9 V is about 2.5 V per cell, lower than a lithium cell likes, but it stops a pack left plugged in from being drained towards zero. It is set that low so a hard climb on a tired pack, which can briefly pull the voltage well down, does not cut power in the air. The firmware should still land well before it, at about 3.3 V per cell. Equations 1 and 2 of the datasheet give the values. |
| C17, between BST and SW | 100 nF | Bootstrap capacitor. The chip's high side switch needs a gate voltage above VIN to turn fully on, and this capacitor holds that voltage. The buck won't run without it. |
| L2 | 4.7 µH | Stores energy between switching cycles. This is the value the datasheet gives for 5 V out. |
| C18, C19 | 22 µF, 10 V each | Output capacitors. Smooth the ripple and cover sudden load changes. |
| FB, pin 1 | tied to +5V | Feedback. The "05" in AP63205 means it's the fixed 5 V version, so FB connects straight to the output with no resistor divider. |

All of these values come from Table 3 and Figure 1 of the AP63205 datasheet.

On the PCB, the input capacitor, chip, inductor and output capacitors need to be packed close together. The switching current flows around that loop, and a large loop acts like a small radio transmitter. So the buck goes in its own corner, well away from the antennas, the GPS and the IMU.

## 3.3 V regulators (U4, TLV75733 and U5, TPS7A2033)

Both are LDOs (low dropout linear regulators) that take `+5V` down to 3.3 V. Each has 1 µF on its input and 1 µF on its output, its EN pin tied to its input so it's always on, and the unused pins left open. Dropping 5 V to 3.3 V in a linear regulator wastes some power, but the currents here are small, and an LDO's output is much quieter than a buck's.

U4 does the hard work: at the ESP32's average flight current it turns about 0.2 W into heat, and during a radio burst 0.6 W. In the plain SOT-23-5 that heat has to leave through five thin leads, and the package is rated 231 °C/W on a bare test board. U4 is therefore the WSON-6 version of the same chip (TLV75733PDRVR), a 2 × 2 mm package with a metal pad on its belly. The pad is soldered to a GND pad on the board with a via through to the ground plane, which carries the heat into the copper. TI rates it at 100 °C/W on the bare test board, and with the planes under it on this board it should land well under that. The cost is that a package with a belly pad cannot be soldered with an iron; it needs the hot plate or hot air, which the top side gets anyway. U5 stays in the SOT-23-5, it dissipates under 0.05 W.

There are two of them because the ESP32's radio draws current in bursts of 300 mA or more whenever it transmits. If the sensors shared that rail, the bursts would ripple into their supply and show up as noise in the IMU and barometer readings. So each gets its own:

| Rail | Regulator | What it powers |
|---|---|---|
| `+3V3` | TLV75733, 1 A | ESP32 and LEDs |
| `+3V3_SENS` | TPS7A2033, 300 mA, low noise | ICM-42688-P, BMP581 and GPS |

## Battery voltage sensing

```
VBAT --- 100k ---+--- 10k --- GND
                 +--- 100nF --- GND
                 +--- VBAT_SENSE  to ESP32 pin 6 (GPIO1, on ADC1)
```

The divider outputs VBAT × 10k / (100k + 10k), which is VBAT divided by 11. A full 2S pack at 8.4 V reads as 0.76 V and a full 4S pack at 16.8 V reads as 1.53 V, both comfortably inside the ADC's range. Firmware multiplies the reading by 11 to get the battery voltage.

The resistors are large on purpose. The divider pulls current from the battery all the time, even with the drone switched off: 8.4 V across 110 kΩ is 76 µA. With 10k and 1k it would be 760 µA, enough to noticeably drain a battery that sits plugged in inside the case for a week.

The 100 nF capacitor is there because the ADC samples in short bursts and a 100 kΩ source can't refill its input fast enough. The capacitor holds a steady voltage for the ADC to read, and it filters motor noise out of the measurement too.

## Test points

`VBAT`, `+5V`, `+3V3` and `+3V3_SENS` each have a test pad for probing during bring-up. The steps are in [bring-up.md](../bring-up.md).

## PWR_FLAG

KiCad's rules check wants every power net to have a source it recognises. Our rails come from connector pins and regulator symbols whose pins aren't marked as power outputs, so without help it reports them as "not driven". A `PWR_FLAG` symbol on each rail tells KiCad the source is real. It has no effect on the PCB. Only put one on a net that really has a source, because it turns off the check for that net.

# Power budget and stress check

What the board draws, where the heat goes, and whether the copper, the regulators and the connector are sized for it. The numbers come from `tools/power_budget.py`, which you can rerun after changing a part. Datasheet typicals are marked (ds); the rest are stated assumptions.

## First, what does not flow through this board

The motors. A 2S cinewhoop with 1303 motors pulls 10 to 15 A hovering and 40 A or more in a punch-out, but all of that goes from the battery pads on the ESC to the motor drivers on the ESC. The flight controller only takes its own supply through J4 pin 2, a few hundred milliamps. The big currents matter to us in one way only: they sag the battery voltage, and the regulators have to ride that out. That case is checked at the end.

## Loads

| Rail | Consumer | Current | Source |
|---|---|---|---|
| `+3V3` | ESP32-S3, CPU running, radio off | 70 mA | ds, modem-sleep at 240 MHz |
| `+3V3` | ESP32-S3, Wi-Fi connected and listening | ~100 mA | ds, 88 mA RX peak plus CPU |
| `+3V3` | ESP32-S3, Wi-Fi transmit burst | 340 to 355 mA | ds, 802.11b at 21 dBm; 355 is the module spec, used as margin |
| `+3V3` | three LEDs | 4 mA | 1.3 mA each |
| `+3V3_SENS` | MAX-M10S GPS, acquiring | 22 mA | ds |
| `+3V3_SENS` | MAX-M10S GPS, tracking | ~8 mA | ds, 25 mW continuous |
| `+3V3_SENS` | ICM-42688-P, BMP581, I2C pull-ups | ~3 mA | ds |

An active GPS antenna through the bias-T would add 10 to 30 mA to `+3V3_SENS`.

Two off-board devices now take 5 V straight from the buck, through the sensor port J5 and the radio port J6:

| Rail | Consumer | Current | Source |
|---|---|---|---|
| `+5V` | TF-Luna obstacle sensor | 70 mA average, 150 mA peak | ds |
| `+5V` | VoCore2 networking module | 74 mA idle, 230 mA at full speed, about 400 mA for a moment at startup | ds, startup figure from user reports |

## Budget by scenario

| ESP32 state | GPS | `+3V3` | `+3V3_SENS` | `+5V` | battery, 2S | battery, 4S |
|---|---|---|---|---|---|---|
| CPU only | tracking | 74 mA | 13 mA | 87 mA | 65 mA | 34 mA |
| Wi-Fi listening | tracking | 104 mA | 13 mA | 117 mA | 88 mA | 45 mA |
| Wi-Fi listening | acquiring | 104 mA | 25 mA | 129 mA | 97 mA | 50 mA |
| Wi-Fi TX burst | acquiring | 359 mA | 25 mA | 384 mA | 288 mA | 149 mA |

The TX burst lasts milliseconds. A flight with telemetry streaming at a 10 % transmit duty averages 129 mA on `+3V3` and 107 mA from a 2S battery, about 0.8 W. On a 650 mAh pack the flight controller alone would run for six hours; the motors empty the pack in five minutes. The FC's draw is not a flight-time concern.

With the sensor and the radio plugged in, the `+5V` rail carries more:

| Case | `+5V` | from a 2S battery |
|---|---|---|
| flight average, sensor and radio running | 0.44 A | 0.33 A, about 2.4 W |
| everything peaking at once | 0.93 A | 0.70 A |

Every rail is still inside its regulator's rating: the buck is rated 2 A and sees 0.93 A at the very worst, the TLV75733 is rated 1 A and sees 0.36 A, the TPS7A2033 is rated 300 mA and sees 25 mA. The flight controller's share of a 650 mAh pack is still small next to the motors.

## Heat: the one thing to watch

The `+3V3` LDO (U4, TLV75733) drops 5 V to 3.3 V linearly, so it dissipates 1.7 V times the ESP32 current. That is 0.22 W averaged over a flight and 0.61 W during a transmit burst. The first layout had it in a plain SOT-23-5, which TI rates at 231 °C/W on the JEDEC test board and 101 °C/W on their evaluation board with planes. It is now the WSON-6 version with a thermal pad (TLV75733PDRVR), rated 100 °C/W on the JEDEC board (ds); the thermally enhanced SOT-23 (DYD) would have been the drop-in choice at 60 °C/W on an EVM board, but it is on back-order everywhere. The rows below keep the SOT-23 figures as the worst case; the WSON with a via into the ground plane should sit at roughly half of them.

| Condition | Junction rise, JEDEC figure | Junction rise, EVM figure |
|---|---|---|
| flight average, 0.22 W | +51 °C | +22 °C |
| transmit burst held continuously, 0.61 W | +141 °C | +61 °C |

Bursts are too short to heat the package, so the average is what counts. At 45 °C inside the frame on a hot day the junction sits between 67 and 96 °C. The limit is 125 °C and thermal shutdown is near 160 °C, so it holds, but U4 will be the warmest part on the board and the first thing to touch at bring-up. Two ways to buy margin if it ever runs hot: pour the top GND copper right up to U4's tab side (the layout already does), or in a later revision feed the ESP32 straight from a 3.3 V buck (AP63203) and keep the LDO for the sensors only. That would also cut the FC's power by about a quarter, since 28 % of what it draws today becomes heat in U4.

The buck itself loses 0.05 to 0.2 W and the sensor LDO under 0.05 W. Neither warms noticeably.

## Buck inductor

The figures in the next paragraph are for the board alone. With the sensor and radio drawing their peaks at the same moment the load is 0.93 A, and the inductor's peak current becomes 1.09 A on 2S and 1.27 A on 4S. The 1008-size part first listed saturates near 1.1 A, which is no longer enough. Order a 4.7 µH inductor with a saturation current of 2 A or more in the same 1008 (2520) footprint; several exist, and the README names the requirement.

The 4.7 µH inductor sees a ripple of 0.3 A peak to peak on 2S and 0.65 A on 4S, on top of the 0.38 A worst-case load. Peak inductor current is 0.54 A on 2S and 0.71 A on 4S. The 1008-size part listed in the README saturates around 1.1 A, so there is margin on 2S and still some on 4S. Check the saturation rating of the exact inductor ordered; anything under 1 A would be marginal on 4S.

## Copper and connector

The routed board, 1 oz outer copper, IPC-2221 rating at 10 °C rise:

| Net | Narrowest track | Rating | Worst-case current | Drop |
|---|---|---|---|---|
| `VBAT` | 0.3 mm (the stub from C16 into the buck's VIN pins) | 1.0 A | 0.29 A | 6 mV |
| `+5V` | 0.3 mm | 1.0 A | 0.38 A | 26 mV |
| `+3V3` | inner plane | n/a | 0.36 A | negligible |
| `+3V3_SENS` | 0.15 mm (the jumpers on the barometer) | 0.6 A | 25 mA | 4 mV |
| vias, 0.3 mm drill | | ~1 A each | | |

Everything has at least 2.5× margin. The `+5V` net also has a bottom-layer run from the buck's FB pin back to the output; it carries no current, it is a sense line.

J4 is a JST-SH, rated 1 A per contact. VBAT and GND each use one pin. With the sensor and radio fitted they carry 0.33 A on average and 0.70 A when everything peaks together on 2S. That is inside the rating but no longer far inside it, so nothing more should be added to the 5 V rail without giving the board a second VBAT pin.

The radio port's 5 V runs on its own 0.4 mm branch from the buck's output capacitor, 39 mm long with four vias. It is rated for 1.2 A and drops about 20 mV at 0.4 A, so the VoCore2 sees 4.98 V against its 4.5 V minimum. The sensor port's 5 V is a 0.3 mm link 2 mm long.

On USB bench power the Schottky D1 drops 0.35 V, so the LDOs see 4.65 V. The TLV75733 needs 3.43 V at this load, so USB is enough to run the board itself with its own Wi-Fi on, and that 0.38 A worst case is inside a USB port's 0.5 A. With the TF-Luna and the VoCore2 also plugged in the peak is 0.93 A, more than a computer's USB port supplies. On the bench, unplug the VoCore2 or power the board from a battery or a bench supply.

## Battery sag in flight

Model: 2S pack with 30 mΩ internal resistance (a decent 100C 650 mAh pack), last 20 % of charge, hovering at 12 A with two 40 A punch-outs. The battery dips to about 5.4 V at the bottom of a punch-out. The buck's output starts sagging once the input falls below about 5.45 V, so `+5V` touches 4.95 V for a moment and recovers. `+3V3` never moves, because the LDO only needs 3.43 V in. On the numbers, the 3.3 V rail would not drop to the ESP32's 3.0 V minimum until the battery reached 3.4 V, and a 2S pack is finished at 5.0 V. On 4S nothing sags at all.

So the flight controller stays up through the worst of the motor current. The ESC will brown out before the FC does.

## Wi-Fi burst on the 3.3 V rail

A transmit burst steps the ESP32 from about 100 to 355 mA in under a microsecond. The LDO's control loop takes a few microseconds to respond, and in that time the capacitors on the rail supply the difference. With 13 µF on `+3V3` (C4 10 µF plus three 1 µF) the dip is roughly 40 to 100 mV, leaving 3.2 V or better. The ESP32 needs 3.0 V and its brownout detector trips at 2.8 V by default. This is the case that kills many ESP32 boards built with too little capacitance; here the 10 µF Espressif asks for is present.

## What other flight controllers do

Checked against the boards people actually fly: Betaflight-class racing controllers (SpeedyBee F405, the Betaflight F4), Holybro's Pixhawk 6C, and Espressif's own ESP32 design guidance.

- Every one of them uses the same tree as ours: a switching regulator makes 5 V from the battery, then linear regulators make 3.3 V from that. SpeedyBee advertises "MCU and gyro with independent LDO", which is exactly our `+3V3` and `+3V3_SENS` split. Nobody feeds a microcontroller with a radio straight from a buck.
- Pixhawk takes 5 V from an external power module and runs everything from LDOs behind it; its inputs are rated 4.1 to 5.7 V. Our USB path lands at 4.65 V, inside the same window.
- Espressif's guidance for the ESP32-S3 is an LDO of at least 500 mA with 10 µF close to the chip. Ours is 1 A with 10 µF plus three 1 µF.
- Racing controllers' 5 V rails are 1.5 to 3 A because they also power a camera, video transmitter, receiver and GPS. Ours powers nothing external, so 0.4 A is the whole load.

Two things they do that we did not have written down:

1. **A low-ESR bulk capacitor on the battery input.** Every FPV build guide and most ESC manuals call for a 470 µF 35 V electrolytic on the ESC's battery pads. It absorbs the motors' current ripple and the spikes from braking, which otherwise appear as noise on the gyro and as yaw twitch. A 10 mm can does not fit on a 36 mm board, so the board got the biggest low-ESR part that lies flat: C35, a 100 µF 25 V polymer tantalum in a D case (7.3 × 4.3 × 3.1 mm, 55 mΩ) on the bottom side at the lower-left corner, 3.5 mm from the VBAT entry. The 470 µF on the ESC pads is still the recommended first line for the motor noise, and is in the ESC notes and the bring-up checklist.
2. **Input capacitance that survives the battery voltage.** Ceramics lose capacitance under DC bias: an 0805 10 µF 25 V is worth about 5 µF at 8.4 V and 2.5 µF at 16.8 V. C16 is now a 1206 of the same rating, which holds roughly 7 µF at 8.4 V and 4 µF at 16.8 V, and C35 sits behind it. The crystal moved up 0.6 mm to make the room.

## Verdict

The board holds up. No rail, track, via or connector is near its limit, the regulators ride out motor-induced sag, and the radio bursts are covered by the capacitors. The one part that works hard is the `+3V3` LDO, which will run warm; measure it with a thermocouple at bring-up with Wi-Fi streaming. If it is over about 80 °C in the frame even in the WSON package, plan the 3.3 V buck for rev B.

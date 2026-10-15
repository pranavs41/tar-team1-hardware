# Charging board

The board that charges the drone's battery when the drone sits on its dock. It rides on the drone, takes 5 V from the dock contacts, and charges the 2S battery through a BQ25887. Rishab owns this board. This page records the plan, the parts and how it connects to the flight controller, so the two boards are designed to the same pin order.

Nothing on this page is built yet. The part choices come from the team's first parts list and still need checking against the BQ25887 datasheet.

## What it does

```
5 V from the dock contacts
   |
resettable fuse (about 1 A)
   |
TVS diode to ground
   |
LM73100 ideal diode (blocks a reversed dock, stops the battery feeding the contacts,
   and cuts the charger off if the dock voltage goes above about 6 V)
   |
BQ25887 charger: boosts 5 V up to the 2S battery voltage and balances the two cells
   |
2S battery, 1000 mAh ----> ESC (through the XT30 plug)
   |
   +----> flight controller J7 pin 1 (BATT+)
```

The BQ25887 is a boost charger. A 2S battery needs up to 8.4 V, and the dock only supplies 5 V, so the chip steps the voltage up. It also has a wire to the point between the two cells (MID), which lets it keep both cells at the same voltage.

How fast it charges: the input limit set by the 1.2 kΩ resistor is about 0.925 A at 5 V, which is about 4.6 W. After the boost that is roughly 0.5 A into the battery, so a flat 1000 mAh pack takes a little over two hours. A faster charge needs more current from the dock and a higher limit resistor setting.

## Connection to the flight controller

One cable, 7-pin JST-SH (1.0 mm pitch), wired straight through, pin 1 to pin 1. The flight controller's connector is J7, part number SM07B-SRSS-TB. Using the same part on the charging board keeps the cable simple.

| Pin | Signal | Direction | Flight controller side |
|---|---|---|---|
| 1 | BATT+ | to the flight controller | joins VBAT, powers the board. 1 A at most |
| 2 | GND | | ground |
| 3 | SDA | both ways | GPIO37, I2C data |
| 4 | SCL | from the flight controller | GPIO38, I2C clock |
| 5 | /PG | to the flight controller | GPIO9. Low when the charger has good input power |
| 6 | STAT | to the flight controller | GPIO8. Low while charging |
| 7 | CD | from the flight controller | GPIO7. High stops charging |

This is the order in the charging board's own list, with three differences to know about.

**No VBAT_SENSE pin.** The first list had an eighth pin carrying the battery voltage divided by four. The flight controller already measures the battery itself, through its own divider on GPIO4, and BATT+ on pin 1 is that same voltage. A second copy adds nothing, and the ESP32 had no free pin to read it. The 300 kΩ and 100 kΩ resistors and the 100 nF filter capacitor can come off the charging board. The BQ25887 can also report the battery voltage, each cell's voltage and the charge current over I2C.

**No pull-up resistors needed.** The list had 10 kΩ pull-ups on SDA, SCL, /PG and STAT, tied to the flight controller's 3.3 V. There is no 3.3 V pin on the connector. It is not needed: the I2C pull-ups are already on the flight controller (2.2 kΩ), and for /PG and STAT the firmware turns on the ESP32's internal pull-ups. Leave those four resistors off, or leave the pads empty.

**No /INT pin.** It was optional. Firmware polls the charger over I2C instead.

### Rules for this cable

- Pin 1 carries battery voltage, up to 8.4 V. Every other pin is a 3.3 V signal. A wrong-way cable or a solder bridge from pin 1 to pin 2 or pin 3 will do damage, so check the cable with a multimeter before the first power-up.
- Pin 1 is for running the flight controller, which draws 0.8 A at its worst. Charge current, up to 2 A, must go from the charger to the battery on its own wires. If the charger's only path to the battery ran through this cable and the flight controller, the 1 A pins would overheat.
- The battery connects to the ESC through the XT30 plug and to the charging board through its own leads. That makes two paths from battery to flight controller: one through the ESC cable and one through this cable. A small share of the motor current, in the range of a few percent, will take the thinner path. Keep the charging board's battery leads short and thick so that share stays small.
- CD floats when the ESP32 is in reset or has no power. The BQ25887 datasheet says CD is pulled low inside the chip through 900 kΩ, so a floating CD reads as "charging allowed" and no extra resistor is needed.
- The charger's I2C address is 0x6B (BQ25887 datasheet). It does not clash with the barometer (0x46), the distance sensors (0x10 and 0x11) or the compass (0x1C).

## Other connections

| Connection | Wires |
|---|---|
| Dock | 5V_DOCK and GND, from the conductive strips on the propeller guard |
| Battery | B+, MID (the point between the two cells) and B−. A 2S pack's balance plug has exactly these three wires |

## Parts

Prices are rough single-quantity figures, good for budgeting and not checked against a seller the way the flight controller's list was. Check stock and price on the day of ordering. The BQ25887 showed very low stock at DigiKey on 2026-10-11.

| Part | Value or number | Maker (home country) | Qty | Each | Total |
|---|---|---|---|---|---|
| 2S boost charger with balancing | BQ25887RGER, 24-pin 4 × 4 mm QFN | Texas Instruments (US) | 1 | $5.80 | $5.80 |
| Ideal diode with overvoltage cut-off | LM73100RPWR, 10-pin 2 × 2 mm QFN | Texas Instruments (US) | 1 | about $1.60 | $1.60 |
| Overvoltage cut-off divider | 40.2 kΩ and 10 kΩ 1%, 0603 | Yageo (Taiwan) | 2 | $0.10 | $0.20 |
| Power inductor, 1 µH, shielded | DFE252012F-1R0M | Murata (Japan) | 1 | $0.31 | $0.31 |
| Resettable fuse, about 1 A hold, 6 V or more, 1206 | 1206L110TH or similar | Littelfuse (US) | 1 | $0.50 | $0.50 |
| TVS diode, 5 V | SMBJ5.0A | Littelfuse or Diodes Incorporated (US) | 1 | $0.40 | $0.40 |
| ILIM resistor | 1.2 kΩ 1%, 0603 | Yageo (Taiwan) | 1 | $0.10 | $0.10 |
| MID series resistor | 300 Ω 1%, 0603 | Yageo (Taiwan) | 1 | $0.10 | $0.10 |
| CBSET resistor, sets the balancing current | 41.2 Ω 1%, 1 W, 2512 | Yageo or Vishay | 1 | $0.40 | $0.40 |
| Battery thermistor, 10 kΩ NTC | 103AT-2 | Semitec (Japan) | 1 | $1.50 | $1.50 |
| Thermistor bias resistors | 5.23 kΩ and 30.1 kΩ 1%, 0603 (datasheet: 5.24 kΩ and 30.31 kΩ for a 103AT) | Yageo (Taiwan) | 2 | $0.10 | $0.20 |
| VBUS capacitor | 1 µF 25 V X7R, 0603 | Murata | 1 | $0.10 | $0.10 |
| PMID and BAT capacitors | 10 µF 25 V X5R, 0805 (the datasheet asks for a 25 V rating at PMID), TDK C2012X5R1E106K125AB, the same part as the flight controller's C16 | TDK (Japan) | 2 | $0.34 | $0.68 |
| Bootstrap capacitor | 47 nF 16 V X7R | Murata or Samsung | 1 | $0.10 | $0.10 |
| REGN capacitor | 4.7 µF 16 V | Murata or Samsung | 1 | $0.15 | $0.15 |
| Output capacitors | 22 µF 16 V | Murata or Samsung | 2 | $0.45 | $0.90 |
| Flight controller connector, JST-SH 7-pin | SM07B-SRSS-TB | JST (Japan) | 1 | $0.80 | $0.80 |
| Battery connector, 3-pin, to match the pack's balance plug | JST-XH B3B-XH-A | JST (Japan) | 1 | $0.15 | $0.15 |
| Cable to the flight controller, 7-pin JST-SH both ends | | | 1 | $2.00 | $2.00 |
| Bare board, small 2-layer, one of three | | OSH Park (US) | 1 | $1.70 | $1.70 |
| | **Total** | | | | **about $16** |

Dropped from the first list, for the reasons above: four 10 kΩ pull-ups, the optional /INT pull-up, and the VBAT_SENSE divider (300 kΩ, 100 kΩ, 100 nF).

Test points wanted on the board: 5V_DOCK, VBUS, BATT+, MID, GND, SDA, SCL, /PG, STAT, SW.

## Things to check before layout

- [x] **Inductor current rating.** The DFE252012F-1R0M is the inductor TI's own datasheet uses. Peak current here is about 1.6 A: the 0.925 A input limit plus half of a 1.35 A ripple (5 V in, 8.4 V out, 1.5 MHz, 1 µH). Check the exact saturation figure on Murata's page when ordering.
- [x] **Input surge.** The first plan used an LM66100 ideal diode, which is rated only to 6 V, while the 5 V surge diode in front of it clamps near 9 V. It is replaced by the TI LM73100, rated to 28 V. It also survives -15 V, so a drone that lands the wrong way round on the rails is protected, and it cuts its output off within about 1.2 µs if its input rises above a set voltage. That protects the charger, whose input works only up to 6.2 V.

  How to wire the LM73100 (from its datasheet, SNOSDC0A):

  | Pin | Name | Connect to |
  |---|---|---|
  | 1 | EN/UVLO | IN, so it is always enabled |
  | 2 | OVLO | the middle of 40.2 kΩ (to IN) and 10 kΩ (to GND). Cut-off = 1.2 V × (40.2 + 10) / 10 = about 6.0 V, between 5.94 and 6.14 V with part tolerances |
  | 3 | PG | leave unconnected |
  | 4 | PGTH | GND |
  | 5 | IN | dock 5 V, after the fuse and the surge diode |
  | 6 | OUT | the charger's VBUS |
  | 7 | dVdt | leave open for the fastest start, or add a small capacitor to soften the inrush when the contacts touch |
  | 8 | GND | ground |
  | 9 | IMON | GND |
  | 10 | DNC | nothing |
- [x] **Balancing resistor.** 41.2 Ω sets about 100 mA of balancing current (4.2 V divided by 41.2 Ω), a quarter of the chip's 400 mA maximum. It dissipates about 0.43 W, inside the 1 W rating of a 2512 resistor, but it will get warm. Give it copper and keep it away from the battery.
- [ ] **Thermistor.** It only helps if it touches the battery. Decide where it sits and how its wires reach the board.
- [ ] **Charge voltage.** The battery picked is a standard LiPo, 4.2 V per cell, 8.4 V full. Set the charger to that and not to the high-voltage 4.35 V setting.
- [ ] **Exposed contacts.** The dock strips on the propeller guard are bare metal. The LM73100 stops the battery from appearing on them. Confirm that with a meter on the first board.
- [ ] **Which strip is positive**, and what keeps the drone from docking the wrong way round. See the charging concept in [TASKS.md](../TASKS.md).

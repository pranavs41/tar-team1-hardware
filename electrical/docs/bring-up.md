# First power-on checklist

Do these in order on every new board. Stop at the first failure.

1. **Visual:** under a magnifier, check the QFN and LGA edges for bridges, and that the LEDs and diodes face the right way.
2. **No shorts:** with no power, measure resistance from each rail (`VBAT`, `+5V`, `+3V3`, `3V3_SENS`) to GND. Anything under ~100 Ω is a short.
3. **Current-limited power:** bench supply at 7.4 V, current limit 100 mA. Current should stay well under the limit.
4. **Rails:** measure `+5V`, `+3V3`, `3V3_SENS` at their test points. The red LED should be on.
5. **USB:** plug in USB-C; the board should enumerate as "USB JTAG/serial debug unit". If not, hold BOOT, tap RESET, release BOOT and try again.
6. **Flash a blink test:** green and yellow LEDs.
7. **Sensors one at a time:** read the WHO_AM_I / chip ID of the ICM-42688-P and BMP581. LGA joints are hidden, so this is the only proof they soldered.
8. **GPS:** confirm NMEA sentences on `GPS_RX`.
9. **Radio heat:** stream telemetry over Wi-Fi for ten minutes and measure U4 (the `+3V3` LDO) with a thermocouple or an IR gun. Under about 80 °C is fine. Over that, note it for rev B (thermally enhanced package or a 3.3 V buck).
10. **Capacitors:** check C35 on the bottom of the FC has its stripe (positive) toward the VBAT side, and that the 470 µF 35 V electrolytic is soldered on the ESC's battery pads with its stripe on negative. Do not spin motors without the ESC capacitor.
11. **ESC:** with props off, spin each motor with DShot.

Log results for each board serial in `production/<rev>/bringup-log.md`.

# First power-on checklist

Do these in order on every new board. Stop at the first failure.

1. **Visual:** under a magnifier, check the QFN, LGA and WSON (U4) edges for bridges, and that the LEDs, diodes and C35 face the right way.
2. **No shorts:** with no power, measure resistance from each rail (`VBAT`, `+5V`, `+3V3`, `3V3_SENS`) to GND. Anything under ~100 Ω is a short.
3. **Current-limited power:** bench supply at 7.4 V, current limit 100 mA. Current should stay well under the limit.
4. **Rails:** measure `+5V`, `+3V3`, `3V3_SENS` at their test points. The red LED should be on.
5. **USB:** plug in USB-C; the board should enumerate as "USB JTAG/serial debug unit". If not, hold BOOT, tap RESET, release BOOT and try again.
6. **Flash a blink test:** green and yellow LEDs.
7. **Sensors one at a time:** read the WHO_AM_I / chip ID of the ICM-42688-P and BMP581. LGA joints are hidden, so this is the only proof they soldered.
8. **GPS:** confirm NMEA sentences on `GPS_RX`.
9. **Ports, before plugging anything in:** measure 5 V on J5 pin 1 and on J6 pin 1. J5 used to be a 3.3 V port; it is 5 V now, so a 3.3 V-only I2C device must never go there.
10. **Obstacle sensor:** plug the TF-Luna into J5 with its pin 5 tied to ground in the cable, and scan the I2C bus. It answers at address 0x10, next to the barometer.
11. **Radio:** plug the VoCore2 into J6 and watch the 5 V rail on a scope or meter while it boots. It should stay above 4.8 V. Then send bytes both ways over the UART (GPIO2 out, GPIO10 in).
12. **Radio heat:** stream telemetry over Wi-Fi for ten minutes and measure U4 (the `+3V3` LDO) with a thermocouple or an IR gun. Under about 80 °C is fine. Over that, note it for rev B (thermally enhanced package or a 3.3 V buck).
13. **Capacitors:** check C35 on the bottom of the FC has its stripe (positive) toward the VBAT side, and that the 470 µF 35 V electrolytic is soldered on the ESC's battery pads with its stripe on negative. Do not spin motors without the ESC capacitor.
14. **ESC:** with props off, spin each motor with DShot.

Log results for each board serial in `production/<rev>/bringup-log.md`.

## Settings and checks from the datasheet audit (2026-10-14)

Each chip was checked against its datasheet. These are the points the firmware and the first bench test must handle.

**Measure before plugging things in**

- On USB power alone, with no battery, measure the battery line at TP3. The 5 V regulator lets USB power leak backwards into the battery line at about 4 to 4.6 V, so an ESC or charging board plugged in will see it. Expect it and do not run motors on USB.
- Battery cut-off: on the bench supply, raise the voltage slowly from 4 V. The 5 V rail should come up at about 5.9 V. Lower it again and the rail should drop at about 4.9 V. If it never turns on, check R14 and R15 are not swapped.
- Measure the TF-Luna's SDA and SCL with it powered and unplugged from the board. They must not sit above 3.6 V.
- Measure the ESC's current output (its C pad) before ever connecting it. It must stay below 3.6 V.

**Firmware settings**

- Gyro (ICM-42688-P): SPI clock 24 MHz or less. Its interrupt pin starts as open-drain with nothing pulling it up, so either set INT1 to push-pull or turn on GPIO48's internal pull-up. Clear INT_ASYNC_RESET. Write FSYNC_UI_SEL = 0, otherwise a sync flag lands in the lowest bit of the temperature reading.
- Barometer (BMP581): its INT pin is not connected. Set it to push-pull and leave it unused, or leave the interrupt off.
- I2C bus: 100 kHz. Two TF-Lunas share the bus, so give one the address 0x11 once (register 0x22, save with 0x20 = 0x01, then reboot), and run both in trigger mode (register 0x23 = 0x01).
- Charger: the BQ25887 should answer at 0x6B. Its datasheet says 0x6A in one place, so scan the bus once.
- Charger lines: turn on the internal pull-ups on GPIO8 (STAT) and GPIO9 (/PG).
- Crystal: tune the 40 MHz load capacitors with Espressif's RF test tool. If the frequency is high, raise C12 and C13 (keep 12 pF and 18 pF spares).
- Burn the EFUSE_DIS_USB_OTG_DOWNLOAD_MODE fuse once the board is working, so the I2C clock line is not driven low in a USB download mode.


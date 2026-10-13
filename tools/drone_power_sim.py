"""Whole-drone power simulation for the networking drone.

Run:  python tools/drone_power_sim.py

Part 1 checks every supply rail, regulator, track and connector on the flight
controller against its rating, with all the plug-in devices attached.
Part 2 models the motors and propellers from first principles and steps through
a flight second by second, tracking battery voltage and charge used.

Numbers tagged (ds) come from datasheets or seller listings. Numbers tagged
(est) are estimates, and the results that depend on them are only as good as
they are. The propeller coefficients and the frame weight are the big ones.
"""
import math

OK, WATCH, FAIL = "PASS ", "WATCH", "FAIL "
results = []


def check(name, value, limit, unit, watch_at=0.8, note=""):
    """Compare a value to its limit. Over the limit fails, over watch_at of it is flagged."""
    ratio = value / limit
    tag = FAIL if ratio > 1.0 else WATCH if ratio > watch_at else OK
    results.append(tag)
    print("  [%s] %-46s %6.2f %s of %5.2f %s (%3.0f%%) %s" % (tag, name, value, unit, limit, unit, 100 * ratio, note))


# ---------------------------------------------------------------- loads on the flight controller
# +3V3 rail (through U4)
ESP_LISTEN, ESP_TX = 0.100, 0.355            # (ds) ESP32-S3 with Wi-Fi listening, and in a transmit burst
LEDS = 0.0013 * 2 + 0.0028                   # red and yellow at 1.3 mA, yellow-green at about 2.8 mA
# +3V3_SENS rail (through U5)
GPS_TRACK, GPS_ACQ = 0.010, 0.022            # (ds) MAX-M10S
IMU, BARO, PULLUPS = 0.0009, 0.0005, 0.003   # (ds); two 2.2 k pull-ups, worst case both lines low
# straight off +5V, on cables
LUNA_AVG, LUNA_PK = 0.070, 0.150             # (ds) TF-Luna, there are two
VOCORE_AVG, VOCORE_PK = 0.230, 0.400         # (ds) full speed; (est) start-up surge from user reports
COMPASS = 0.003                              # (est) LIS3MDL breakout with its regulator and LED

TX_DUTY = 0.10                               # (est) share of time the ESP32 spends transmitting


def rails(esp, gps, luna, vocore):
    i33 = esp + LEDS
    isens = gps + IMU + BARO + PULLUPS
    i5 = i33 + isens + 2 * luna + vocore + COMPASS
    return i33, isens, i5


avg = rails((1 - TX_DUTY) * ESP_LISTEN + TX_DUTY * ESP_TX, GPS_TRACK, LUNA_AVG, VOCORE_AVG)
peak = rails(ESP_TX, GPS_ACQ, LUNA_PK, VOCORE_PK)


def buck_in(vbat, i5):
    """Battery current the 5 V buck draws. Efficiency read off the AP63205 curves."""
    eff = 0.90 if vbat < 10 else 0.87
    return 5.0 * i5 / eff / vbat, 5.0 * i5 * (1 / eff - 1)


print("=" * 100)
print("PART 1: flight controller rails, with both distance sensors, the VoCore2 and the compass attached")
print("=" * 100)
print("  rail currents       average      everything peaking at once")
for name, a, p in zip(("+3V3", "+3V3_SENS", "+5V"), avg, peak):
    print("  %-12s      %6.3f A      %6.3f A" % (name, a, p))
for v, label in ((8.7, "full, high-voltage charge"), (7.4, "nominal"), (6.6, "nearly empty, 3.3 V per cell")):
    print("  from the battery at %.1f V (%s): %.2f A average, %.2f A peak" % (v, label, buck_in(v, avg[2])[0], buck_in(v, peak[2])[0]))

print("\nRegulators")
check("U3 buck output, peak", peak[2], 2.0, "A", note="AP63205 rated 2 A")
check("U4 3.3 V regulator, peak", peak[0], 1.0, "A", note="TLV75733 rated 1 A")
check("U5 sensor regulator, peak", peak[1], 0.3, "A", note="TPS7A2033 rated 300 mA")

print("\nBuck inductor L2 (4.7 uH at 1.1 MHz, saturates at 2.2 A (ds))")
for vin in (6.6, 8.7, 16.8):
    ripple = (vin - 5.0) * (5.0 / vin) / (1.1e6 * 4.7e-6)
    check("peak inductor current at %.1f V in" % vin, peak[2] + ripple / 2, 2.2, "A")

print("\nHeat (junction temperature with 45 C air inside the frame, limit 125 C)")
TH_U4, TH_U3 = 100.8, 100.0   # (ds) TLV757 on TI's evaluation board; (est) AP63205 order of magnitude
p_u4 = (5.0 - 3.3) * avg[0]
p_u3 = buck_in(7.4, avg[2])[1]
check("U4 junction, flight average (%.2f W)" % p_u4, 45 + p_u4 * TH_U4, 125, "C")
check("U3 junction, flight average (%.2f W)" % p_u3, 45 + p_u3 * TH_U3, 125, "C")
check("U3 junction if every peak were held (%.2f W)" % buck_in(7.4, peak[2])[1], 45 + buck_in(7.4, peak[2])[1] * TH_U3, 125, "C", note="peaks last milliseconds")


def ampacity(width_mm):
    """IPC-2221 outer layer, 1 oz copper, 10 C rise."""
    area_mil2 = (width_mm / 0.0254) * 1.378
    return 0.048 * 10 ** 0.44 * area_mil2 ** 0.725


print("\nTracks (narrowest width measured on the routed board, IPC-2221 rating at 10 C rise)")
ibat_pk, ibat_avg = buck_in(6.6, peak[2])[0], buck_in(6.6, avg[2])[0]
check("VBAT, 0.3 mm, peak at 6.6 V", ibat_pk, ampacity(0.3), "A", note="average is %.2f A" % ibat_avg)
check("+5V trunk, 0.3 mm, peak", peak[2] - peak[0] - peak[1], ampacity(0.3), "A", note="worst case if every off-board load shared one track")
check("+3V3, 0.2 mm stub, peak", peak[0], ampacity(0.2), "A")
check("+3V3_SENS, 0.15 mm, peak", peak[1], ampacity(0.15), "A")

print("\nConnectors (JST-SH and JST-GH contacts are rated 1 A)")
check("J4 pin 2, battery in, peak at 6.6 V", ibat_pk, 1.0, "A", note="average is %.2f A. J7 is not fitted, so J4 carries it all" % ibat_avg)
check("J6 pin 1, 5 V to the VoCore2, start-up surge", VOCORE_PK, 1.0, "A")
check("J5 or J8 pin 1, TF-Luna plus compass, peak", LUNA_PK + COMPASS, 1.0, "A")

print("\nOn USB power only (bench, no battery)")
check("D1 and the VBUS tracks, everything attached, peak", peak[2], 1.0, "A", note="D1 is a 1 A diode")
check("a 500 mA USB port, everything attached, average", avg[2], 0.5, "A", note="unplug the VoCore2 on a weak port")
check("a 500 mA USB port, board alone, peak", rails(ESP_TX, GPS_ACQ, 0, 0)[2], 0.5, "A")

# ---------------------------------------------------------------- propulsion model
print()
print("=" * 100)
print("PART 2: motors, battery and a simulated flight")
print("=" * 100)

MASS = {  # grams
    "flight controller": 8, "ESC": 5.4, "motors x4": 22.4, "propellers x4": 3.0,          # (ds) except the FC (est)
    "battery, 2S 1100 mAh": 62,                                                         # (est) not on the listing
    "VoCore2": 5, "TF-Luna x2": 10, "compass": 1.5, "antennas": 3, "charging board": 6,  # (est)
    "frame with prop guards": 50, "wires, screws, capacitor": 10,                        # (est) until Daniel's CAD gives a figure
}
mass_g = sum(MASS.values())

RHO = 1.225                 # air density, kg/m3
D = 3.0 * 0.0254            # propeller diameter, m
CT, CP = 0.10, 0.045        # (est) static thrust and power coefficients for a 3 inch, 1.8 pitch two-blade prop
KV = 8000.0                 # (ds) rpm per volt
R_M = 0.145                 # (ds) motor winding resistance, ohm
I0 = 0.5                    # (est) no-load current, A
ESC_EFF = 0.93              # (est)
KV_RAD = KV * 2 * math.pi / 60
KT = 1 / KV_RAD             # torque constant, N m per A


def motor_at_thrust(thrust_n):
    """One motor holding a given thrust. Returns electrical power in at the ESC (W) and rev/s."""
    n = math.sqrt(thrust_n / (CT * RHO * D ** 4))
    torque = CP * RHO * n ** 2 * D ** 5 / (2 * math.pi)
    i = torque / KT + I0
    v = i * R_M + 2 * math.pi * n / KV_RAD
    return v * i / ESC_EFF, n


def motor_full_throttle(v_supply):
    """One motor with the full supply voltage across it. Returns current (A), thrust (N), rev/s."""
    lo, hi = 0.0, 2000.0
    for _ in range(60):
        n = (lo + hi) / 2
        i = CP * RHO * n ** 2 * D ** 5 / (2 * math.pi) / KT + I0
        if i * R_M + 2 * math.pi * n / KV_RAD > v_supply: hi = n
        else: lo = n
    return i, CT * RHO * n ** 2 * D ** 4, n


# battery: OVONIC 2S 1100 mAh high-voltage, 60C
CAP_AH = 1.1
R_PACK = 0.045              # (est) both cells, leads and the XT30, ohm


def ocv(soc, full=8.7):
    """Open-circuit voltage of the 2S pack against state of charge (1 = full). Simple curve."""
    pts = [(0.0, 6.4), (0.1, 7.0), (0.2, 7.3), (0.5, 7.6), (0.8, 8.0), (1.0, full)]
    for (s0, v0), (s1, v1) in zip(pts, pts[1:]):
        if soc <= s1: return v0 + (v1 - v0) * (soc - s0) / (s1 - s0)
    return full


print("Weight budget")
for k, v in MASS.items(): print("  %-28s %5.1f g" % (k, v))
print("  %-28s %5.1f g" % ("TOTAL", mass_g))

hover_n = mass_g / 1000 * 9.81 / 4
p_hover, n_hover = motor_at_thrust(hover_n)
i_fc = buck_in(7.4, avg[2])[0]
print("\nHover (each motor lifts %.0f g)" % (mass_g / 4))
print("  propeller speed %.0f rpm, %.1f W per motor, %.1f W for four" % (n_hover * 60, p_hover, 4 * p_hover))
print("  battery current at 7.4 V: %.1f A for the motors + %.2f A for the electronics = %.1f A" % (4 * p_hover / 7.4, i_fc, 4 * p_hover / 7.4 + i_fc))

print("\nFull throttle (battery voltage sags under the load, solved together)")
for soc, label in ((1.0, "full pack"), (0.3, "30% left")):
    v = ocv(soc)
    for _ in range(50):
        i_m, t_m, n_m = motor_full_throttle(v)
        v = ocv(soc) - (4 * i_m / ESC_EFF + i_fc) * R_PACK
    i_tot = 4 * i_m / ESC_EFF + i_fc
    print("  %-10s battery %.2f V under load, %.1f A per motor, %.0f A total, %.0f g thrust per motor, thrust to weight %.1f" %
          (label, v, i_m, i_tot, t_m / 9.81 * 1000, 4 * t_m / 9.81 * 1000 / mass_g))
    if soc == 1.0: full_i, full_im, full_v = i_tot, i_m, v

print("\nPropulsion limits")
check("hover current through the XT30", 4 * p_hover / 7.4 + i_fc, 15.0, "A", note="XT30 rated 15 A continuous")
check("full throttle through the XT30", full_i, 30.0, "A", note="XT30 rated 30 A for short bursts")
check("full throttle from the battery", full_i, 60 * CAP_AH, "A", note="60C times 1.1 Ah")
check("full throttle per ESC channel", full_im, 30.0, "A", note="ESC rated 30 A per motor")
check("full throttle per motor", full_im, 22.5, "A", note="motor rated 22.5 A for 5 s")

# ---------------------------------------------------------------- flight, one second at a time
print("\nSimulated flight, one-second steps, pack charged to 8.7 V")
PHASES = [  # name, seconds, thrust as a multiple of hover
    ("on the pad, VoCore2 starting, GPS acquiring", 30, 0.0),
    ("take-off and climb", 5, 1.5),
    ("cruise to the work area", 60, 1.15),
    ("hover on station", 300, 1.0),
    ("cruise back", 60, 1.15),
    ("descend and land on the rails", 15, 0.85),
]
soc, used_ah, t = 1.0, 0.0, 0
v_min, i_max = 99.0, 0.0
print("  %-46s %6s %7s %7s %7s %8s" % ("phase", "time", "motors", "total", "VBAT", "left"))
for name, secs, mult in PHASES:
    for _ in range(secs):
        p_mot = 4 * motor_at_thrust(hover_n * mult)[0] if mult > 0 else 0.0
        v = ocv(soc)
        for _ in range(20):
            i_e = buck_in(max(v, 5.6), peak[2] if mult == 0 and t < 5 else avg[2])[0]
            i = p_mot / v + i_e
            v = ocv(soc) - i * R_PACK
        used_ah += i / 3600; soc = 1 - used_ah / CAP_AH; t += 1
        v_min, i_max = min(v_min, v), max(i_max, i)
    print("  %-46s %4d s %6.1f A %6.1f A %6.2f V %6.0f %%" % (name, secs, p_mot / v, i, v, 100 * soc))
print("  whole flight: %d min %d s, %.0f mAh used, lowest battery voltage %.2f V, highest current %.1f A" % (t // 60, t % 60, used_ah * 1000, v_min, i_max))

# hover until 20 % is left
soc, used_ah, t = 1.0, 0.0, 0
while soc > 0.20:
    v = ocv(soc)
    for _ in range(20):
        i = 4 * p_hover / v + buck_in(v, avg[2])[0]; v = ocv(soc) - i * R_PACK
    used_ah += i / 3600; soc = 1 - used_ah / CAP_AH; t += 1
print("  hover endurance down to 20%% charge: %d min %d s (battery at %.2f V under load at the end)" % (t // 60, t % 60, v))
check("5 V rail headroom at the end of that hover", 5.45, v, "V", watch_at=0.9, note="the buck needs about 5.45 V in to hold 5 V")

print("\nSensitivity: how the hover figures move if the estimates are off")
for label, m, ct, cp in (("as modelled", 1.0, CT, CP), ("frame 30 g heavier", 1 + 30 / mass_g, CT, CP), ("propellers 25% less efficient", 1.0, CT, CP * 1.25), ("both", 1 + 30 / mass_g, CT, CP * 1.25)):
    CT_, CP_ = CT, CP; CT, CP = ct, cp
    p, _n = motor_at_thrust(hover_n * m); CT, CP = CT_, CP_
    i = 4 * p / 7.4 + i_fc
    print("  %-30s hover %.1f A, about %.1f min to 20%%" % (label, i, CAP_AH * 0.8 / i * 60))

print("\nSummary: %d checks, %d pass, %d to watch, %d fail" % (len(results), results.count(OK), results.count(WATCH), results.count(FAIL)))

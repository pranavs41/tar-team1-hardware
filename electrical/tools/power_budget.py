"""Power budget, thermal and transient model for the network drone FC.
Numbers marked (ds) are datasheet typicals; everything else is stated as an assumption."""
import math
import numpy as np

# ---------------- loads (A) ----------------
ESP = {"cpu only, radio off": 0.070,          # ds: modem-sleep, dual core 240 MHz
       "wifi connected, listening": 0.100,    # ds: RX 88 mA peak, plus CPU
       "wifi TX burst (802.11b 21 dBm)": 0.355}  # ds: 340 mA chip; 355 mA is the module spec, kept as margin
LEDS = 3 * 0.0013
GPS = {"tracking": 0.010, "acquisition": 0.022}   # ds: 22 mA acquisition, ~25 mW continuous tracking
IMU = 0.0009; BARO = 0.0005; PULLUPS = 0.0015
LDO_IQ = 0.00005
BUCK_IQ = 0.000022

def rails(esp, gps, port3v3=0.0):
    i33 = esp + LEDS + port3v3
    isens = gps + IMU + BARO + PULLUPS
    i5 = i33 + isens + 2 * LDO_IQ
    return i33, isens, i5

# ---------------- regulators ----------------
V5, V33 = 5.0, 3.3
THJA_TLV757_DBV = 231.1   # ds: TI JEDEC board, DBV package
THJA_TLV757_4L = 100.8    # ds: TI EVM board (planes under the part), the closer match to our 4-layer board
THJA_AP63205 = 100.0      # TSOT-26, order of magnitude from the Diodes datasheet
def buck_eff(vin, iout):
    # AP63205 curves: ~90% at 7-8 V in, mid-load; a bit less at high input and light load
    e = 0.90 if vin < 10 else 0.87
    if iout < 0.05: e -= 0.08
    return e
def buck(vin, iout):
    pout = V5 * iout; eff = buck_eff(vin, iout); pin = pout / eff
    return pin / vin, pin - pout
def ldo_heat(iout, vin=V5): return (vin - V33) * iout

print("=== Static budget ===")
print("%-34s %-12s %7s %7s %7s | %7s %7s | %7s %7s | %6s %6s"%("ESP32 state","GPS","I_3V3","I_SENS","I_5V","Iin 2S","Iin 4S","P_U4","Tj U4","Tj4L","buck W"))
cases = [("cpu only, radio off","tracking"),("wifi connected, listening","tracking"),("wifi connected, listening","acquisition"),("wifi TX burst (802.11b 21 dBm)","acquisition")]
for e, g in cases:
    i33, isens, i5 = rails(ESP[e], GPS[g])
    iin2, pb2 = buck(7.4, i5); iin4, pb4 = buck(14.8, i5)
    p4 = ldo_heat(i33)
    print("%-34s %-12s %7.3f %7.3f %7.3f | %7.3f %7.3f | %7.3f %7.0f %7.0f | %6.2f"%(e, g, i33, isens, i5, iin2, iin4, p4, 25+p4*THJA_TLV757_DBV, 25+p4*THJA_TLV757_4L, pb2))

# average flight case: telemetry streaming, 10 % TX duty
i_avg = 0.9*ESP["wifi connected, listening"] + 0.1*ESP["wifi TX burst (802.11b 21 dBm)"]
i33, isens, i5 = rails(i_avg, GPS["tracking"])
p4 = ldo_heat(i33)
print("\nFlight average (10%% TX duty): I_3V3 %.3f A, I_5V %.3f A, U4 heat %.2f W -> Tj %+.0f C over ambient (JEDEC) / %+.0f C (4-layer est.)"%(i33, i5, p4, p4*THJA_TLV757_DBV, p4*THJA_TLV757_4L))
print("  at 45 C inside the frame: Tj %.0f C (JEDEC) / %.0f C (4-layer). Limit 125 C, shutdown ~160 C."%(45+p4*THJA_TLV757_DBV, 45+p4*THJA_TLV757_4L))
iin2, pb2 = buck(7.4, i5); print("  battery draw for the FC: %.3f A at 7.4 V (%.2f W), buck loss %.2f W, LDO loss %.2f W -> %.0f%% of the FC's power goes to heat in U4"%(iin2, iin2*7.4, pb2, p4, 100*p4/(iin2*7.4)))

# ---------------- inductor ----------------
print("\n=== Buck inductor (4.7 uH, 1.1 MHz) ===")
for vin in (6.0, 7.4, 8.4, 14.8, 16.8):
    d = V5/vin; dI = (vin - V5)*d/(1.1e6*4.7e-6)
    i33, isens, i5 = rails(ESP["wifi TX burst (802.11b 21 dBm)"], GPS["acquisition"])
    print("  Vin %4.1f V: ripple %.2f A p-p, peak inductor current %.2f A at worst-case load %.2f A"%(vin, dI, i5 + dI/2, i5))
print("  FTC252010S4R7 (1008): Isat ~1.1 A, Irms ~1.0 A (ds, check the exact part ordered)")

# ---------------- copper ----------------
print("\n=== Trace ampacity, IPC-2221 outer layer, 1 oz, 10 C rise ===")
for w in (0.8, 0.5, 0.4, 0.3, 0.2):
    a_mil2 = (w/0.0254) * 1.37
    print("  %.1f mm: %.2f A"%(w, 0.048*(10**0.44)*(a_mil2**0.725)))
print("  0.3 mm drill via, 25 um plating: ~1 A for 10 C rise")

# ---------------- flight transient: pack sag ----------------
print("\n=== Flight profile: pack sag vs the 5 V rail ===")
dt = 0.01; T = 60.0; t = np.arange(0, T, dt)
# throttle: hover 12 A, two punch-outs to 40 A, landing
imot = np.full_like(t, 12.0); imot[(t>20)&(t<23)] = 40; imot[(t>40)&(t<42)] = 40; imot[t<2] = 3
for cells, r_pack, cap_ah, ocv_full, ocv_empty in ((2, 0.030, 0.65, 8.4, 6.6), (4, 0.060, 0.65, 16.8, 13.2)):
    used = np.cumsum(imot)*dt/3600.0
    soc = 1 - used/cap_ah
    ocv = ocv_empty + (ocv_full-ocv_empty)*np.clip(soc, 0, 1)
    # start the sim late in the pack so sag matters: assume 80 % already used
    ocv = ocv_empty + (ocv_full-ocv_empty)*np.clip(0.2 - used/cap_ah, 0, 1)
    vbat = ocv - imot*r_pack
    i5 = rails(i_avg, GPS["tracking"])[2]
    # buck: regulates while vin > 5.0/Dmax + I*R; else tracks vin*Dmax - I*R
    dmax = 0.92; rpath = 0.09 + 0.03
    v5 = np.minimum(V5, vbat*dmax - i5*rpath)
    v33 = np.minimum(V33, v5 - 0.13)   # LDO dropout ~130 mV at this load
    print("  %dS pack (R %.0f mohm, last 20%% of charge): VBAT min %.2f V, +5V min %.2f V, +3V3 min %.2f V -> %s"%(cells, r_pack*1e3, vbat.min(), v5.min(), v33.min(), "OK" if v33.min() > 3.0 else "ESP32 BROWNOUT RISK"))
    if cells == 2:
        # how low can VBAT go before 3.3 V is lost?
        v_sag = (V5 + i5*rpath)/dmax; v_lost = (3.3 + 0.13 + i5*rpath)/dmax; v_brown = (3.0 + 0.13 + i5*rpath)/dmax
        print("    +5V starts sagging below VBAT = %.2f V; +3V3 starts sagging at VBAT = %.2f V; ESP32 minimum (3.0 V) reached at VBAT = %.2f V"%(v_sag, v_lost, v_brown))
        print("    a 2S pack is dead (2.5 V/cell = 5.0 V) long before that, and the ESC drops out first anyway")

# ---------------- Wi-Fi burst on the 3.3 V rail ----------------
print("\n=== Wi-Fi TX burst on +3V3 ===")
C = 10e-6 + 1e-6*3 + 0.1e-6*3    # C4 + C3,C5,C21 + the 0.1 uF ceramics near the chip
esr = 0.010
for tau in (2e-6, 5e-6):
    dI = ESP["wifi TX burst (802.11b 21 dBm)"] - ESP["wifi connected, listening"]
    dip = dI*(tau/C + esr)
    print("  step %.0f mA, LDO loop ~%.0f us, %.1f uF on the rail: dip ~%.0f mV -> %.2f V (ESP32 min 3.0 V, brownout detector default 2.8 V)"%(dI*1e3, tau*1e6, C*1e6, dip*1e3, V33-dip))
print("  Espressif asks for >= 10 uF close to VDD3P3: C4 10 uF is on the rail, plus 1 uF x3.")

# ---------------- connectors, USB ----------------
print("\n=== Connectors ===")
i5w = rails(ESP["wifi TX burst (802.11b 21 dBm)"], GPS["acquisition"])[2]
print("  J4 (JST-SH, 1 A per contact): VBAT pin carries %.2f A worst case on 2S, %.2f A on 4S; GND pin the same."%(buck(7.4, i5w)[0], buck(14.8, i5w)[0]))
print("  USB bench power: +5V load %.2f A worst case through D1 (B5819W, 1 A); 5 V - 0.35 V drop = %.2f V at the LDO inputs; TLV757 needs >= %.2f V -> OK"%(i5w, 5-0.35, 3.3+0.13))
print("  motors never pass through this board: a 40 A punch-out is 40 A in the ESC's battery pads, 0 A in J4 pin 2.")

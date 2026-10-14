"""Per-branch current check on the routed board.

Run with KiCad's Python:
  "C:\\Program Files\\KiCad\\9.0\\bin\\python.exe" tools/current_check.py

For every power branch (a source pad feeding a load pad) it finds the
lowest-resistance path through the real copper, adds that branch's current to
every track and via on the path, then checks each piece against its own total.
Summing a whole net's current onto every segment would be wrong twice over:
branches run in parallel, and no load sits at the end of all of them.

Two currents per branch: the average sets heating (IPC-2221 is a temperature
rise rating), the peak sets voltage drop. Plane layers count as zero resistance.
"""
import math, heapq, collections, pcbnew

PCB = r"C:\dev\tar-team1-hardware\pcb\network-drone-fc\network-drone-fc.kicad_pcb"
RHO = 1.72e-8          # copper, ohm m
T_OUT = 35e-6          # 1 oz outer copper
R_VIA = 0.002          # ohm, 0.3 mm plated hole, 25 um wall, 1.6 mm board
I_VIA = 1.0            # A, rough 10 C rating for one such via

# (net, source ref.pad, load ref.pad, average A, peak A, what it is)
BRANCHES = [
    ("VBAT", "J4.2", "U3.3", 0.44, 0.92, "battery into the 5 V buck, nearly empty 2S pack"),
    ("Net-(U3-SW)", "U3.5", "L2.1", 0.52, 1.30, "buck switch node to the inductor (peak is the inductor ripple top)"),
    ("+5V", "L2.2", "U4.6", 0.13, 0.36, "5 V into the 3.3 V regulator"),
    ("+5V", "L2.2", "U5.1", 0.014, 0.026, "5 V into the sensor regulator"),
    ("+5V", "L2.2", "J6.1", 0.23, 0.40, "5 V out to the VoCore2 (peak is its start-up)"),
    ("+5V", "L2.2", "J5.1", 0.073, 0.153, "5 V out to the forward TF-Luna (and compass)"),
    ("+5V", "L2.2", "J8.1", 0.073, 0.153, "5 V out to the downward TF-Luna (and compass)"),
    ("VBUS", "J2.A4B9", "D1.2", 0.52, 1.09, "USB 5 V into the diode, everything attached (bench only)"),
    ("+3V3_SENS", "U5.5", "U8.8", 0.010, 0.022, "sensor 3.3 V to the GPS"),
    ("+3V3_SENS", "U5.5", "U6.8", 0.001, 0.001, "sensor 3.3 V to the gyro"),
    ("+3V3_SENS", "U5.5", "U7.10", 0.001, 0.001, "sensor 3.3 V to the barometer"),
]


def ampacity(width_mm, k=0.048):
    area_mil2 = (width_mm / 0.0254) * (T_OUT / 25.4e-6)
    return k * 10 ** 0.44 * area_mil2 ** 0.725


b = pcbnew.LoadBoard(PCB)
mm = pcbnew.ToMM
pads = {}
for f in b.GetFootprints():
    for p in f.Pads():
        pads.setdefault("%s.%s" % (f.GetReference(), p.GetNumber()), []).append(p)

report = []
for net, src, dst, i_avg, i_pk, label in BRANCHES:
    # graph: node = (layer, x, y) rounded; plane nodes collapse into one node per layer
    adj = collections.defaultdict(list)
    tracks = [t for t in b.GetTracks() if str(t.GetNetname()) == net]

    def node(layer, p):
        return (layer, round(mm(p.x), 3), round(mm(p.y), 3))

    for t in tracks:
        if t.Type() == pcbnew.PCB_VIA_T:
            a, c = node("F.Cu", t.GetPosition()), node("B.Cu", t.GetPosition())
            e = ("via", R_VIA, I_VIA, t)
        else:
            a, c = node(t.GetLayerName(), t.GetStart()), node(t.GetLayerName(), t.GetEnd())
            w = mm(t.GetWidth())
            r = RHO * (t.GetLength() / 1e9) / (w / 1000 * T_OUT)
            e = ("track", r, ampacity(w), t)
        adj[a].append((c, e)); adj[c].append((a, e))
    # a track end landing partway along another track (a T joint) splits that track
    segs = [t for t in tracks if t.Type() != pcbnew.PCB_VIA_T]
    for n in list(adj):
        if not n[0].endswith(".Cu"): continue
        x, y = n[1], n[2]
        for t in segs:
            if t.GetLayerName() != n[0]: continue
            sx, sy, ex, ey = mm(t.GetStart().x), mm(t.GetStart().y), mm(t.GetEnd().x), mm(t.GetEnd().y)
            L2 = (ex - sx) ** 2 + (ey - sy) ** 2
            if L2 < 1e-9: continue
            u = ((x - sx) * (ex - sx) + (y - sy) * (ey - sy)) / L2
            if not 0.001 < u < 0.999: continue
            if math.hypot(sx + u * (ex - sx) - x, sy + u * (ey - sy) - y) > mm(t.GetWidth()) / 2 + 0.3: continue  # copper overlapping, allowing for a via's radius
            w = mm(t.GetWidth()); rr = RHO * math.sqrt(L2) / 1000 / (w / 1000 * T_OUT)
            for endp, frac in (((n[0], round(sx, 3), round(sy, 3)), u), ((n[0], round(ex, 3), round(ey, 3)), 1 - u)):
                e = ("track", rr * frac, ampacity(w), t); adj[n].append((endp, e)); adj[endp].append((n, e))
    # every pad on this net joins the track ends and vias that land on it, so current can pass through a pad
    for key, plist in pads.items():
        for p in plist:
            if str(p.GetNetname()) != net: continue
            box = p.GetBoundingBox(); box.Inflate(pcbnew.FromMM(0.25))  # a track end can stop short of the pad and still overlap it
            inside = [n for n in list(adj) if n[0].endswith(".Cu") and p.IsOnLayer(b.GetLayerID(n[0])) and box.Contains(pcbnew.VECTOR2I(pcbnew.FromMM(n[1]), pcbnew.FromMM(n[2])))]
            hub = ("pad", key, id(p))
            for n in inside:
                e = ("pad", 0.0, 99.0, p); adj[n].append((hub, e)); adj[hub].append((n, e))
    # copper pours and planes on this net: anything touching the fill joins it at zero resistance
    for z in b.Zones():
        if str(z.GetNetname()) != net: continue
        for lid in z.GetLayerSet().Seq():
            if not z.HasFilledPolysForLayer(lid): continue
            poly = z.GetFilledPolysList(lid); ln = b.GetLayerName(lid); hub = ("zone", ln, id(z))
            for n in list(adj):
                if n[0] == ln and isinstance(n[1], float) and poly.Contains(pcbnew.VECTOR2I(pcbnew.FromMM(n[1]), pcbnew.FromMM(n[2]))):
                    e = ("zone", 0.0, 99.0, z); adj[n].append((hub, e)); adj[hub].append((n, e))
    # pads: join every track end or via that lands on the pad, on the pad's layers
    def pad_nodes(key):
        out = []
        for p in pads[key]:
            box = p.GetBoundingBox(); box.Inflate(pcbnew.FromMM(0.25))  # a track end can stop short of the pad and still overlap it
            for n in list(adj):
                if n[0].endswith(".Cu") and p.IsOnLayer(b.GetLayerID(n[0])) and box.Contains(pcbnew.VECTOR2I(pcbnew.FromMM(n[1]), pcbnew.FromMM(n[2]))):
                    out.append(n)
        return out
    s_nodes, d_nodes = pad_nodes(src), set(pad_nodes(dst))
    # Dijkstra on resistance
    dist = {n: 0.0 for n in s_nodes}; prev = {}; pq = [(0.0, n) for n in s_nodes]; heapq.heapify(pq); end = None
    while pq:
        dcur, n = heapq.heappop(pq)
        if dcur > dist.get(n, 1e9): continue
        if n in d_nodes: end = n; break
        for m, e in adj[n]:
            nd = dcur + e[1]
            if nd < dist.get(m, 1e9): dist[m] = nd; prev[m] = (n, e); heapq.heappush(pq, (nd, m))
    if end is None:
        report.append((net, src, dst, label, None)); continue
    path = []; n = end
    while n in prev: n, e = prev[n]; path.append(e)
    report.append((net, src, dst, label, (dist[end], path, i_avg, i_pk)))

# accumulate each branch's current onto the pieces it uses
load_avg = collections.defaultdict(float); load_pk = collections.defaultdict(float); piece = {}
for net, src, dst, label, res in report:
    if not res: continue
    _, path, ia, ip = res
    for e in path:
        if e[0] not in ("track", "via"): continue
        k = id(e[3]); piece[k] = e; load_avg[k] += ia; load_pk[k] += ip

print("Branches (lowest-resistance path through the routed copper)")
print("  %-11s %-8s -> %-8s %8s %9s %9s  %s" % ("net", "from", "to", "R mohm", "drop pk", "narrowest", "what"))
for net, src, dst, label, res in report:
    if not res: print("  %-11s %-8s -> %-8s  NO PATH FOUND  %s" % (net, src, dst, label)); continue
    r, path, ia, ip = res
    narrow = min((mm(e[3].GetWidth()) for e in path if e[0] == "track"), default=0)
    print("  %-11s %-8s -> %-8s %8.1f %7.1f mV %7.2f mm  %s" % (net, src, dst, r * 1000, r * ip * 1000, narrow, label))

print("\nEvery track and via, against the total current of the branches it carries")
worst = sorted(piece, key=lambda k: -load_avg[k] / piece[k][2])
fails = 0
for k in worst[:12]:
    kind, r, rating, t = piece[k]
    ratio = load_avg[k] / rating
    tag = "FAIL " if ratio > 1 else "WATCH" if ratio > 0.8 else "PASS "
    fails += ratio > 1
    where = "(%.2f, %.2f)" % (mm(t.GetPosition().x), mm(t.GetPosition().y)) if kind == "via" else "%s %.2f mm wide" % (t.GetLayerName(), mm(t.GetWidth()))
    print("  [%s] %-11s %-5s %-22s average %.2f A of %.2f A (%3.0f%%), peak %.2f A" % (tag, str(t.GetNetname()), kind, where, load_avg[k], rating, 100 * ratio, load_pk[k]))
print("\n%d pieces checked, %d over their rating at the average current" % (len(piece), fails))

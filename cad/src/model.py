"""SteamRoot parametric model (build123d), constructable design (STR-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STL to cad/stl (STEP comes from python .kit/cad_check.py --export) and prints the checks
    python cad/src/model.py --check    prints the constructability checks only
    python cad/src/model.py --mass     prints the masses of the parts added for construction

Every component is modelled as it is made or bought, and every component touches the parts that
hold it. build_components() returns them keyed by a short name; build_parts() groups them under the
BOM item names that docs/04-calcs/sizing.py, concept_media.py and product_model.py use.
PRELIMINARY, NOT FOR FABRICATION. The written ruling from the local boiler authority is an open
prerequisite for any build (see docs/06-design-decisions.md).

Axes: X along the trailer (drawbar at -X, steam hoods at +X), Y across (operator side, firebox door,
at -Y), Z up from the ground. Units: millimetres.
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _p in (str(_HERE), str(_HERE.parents[1] / ".kit")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Top-level parameters (mm). Edit these, not the geometry below.
# docs/04-calcs/sizing.py imports this dictionary, so the calculation and the model share one source.
PARAMS = {
    # Trailer (used single-axle garden or utility trailer)
    "deck_l": 2000.0, "deck_w": 1200.0, "deck_t": 80.0, "deck_z": 420.0, "rail_w": 80.0,
    "wheel_r": 230.0, "wheel_w": 120.0, "wheel_gap": 20.0, "axle_x": 150.0, "drawbar_l": 800.0,
    # Feed water tank, 125 L HDPE drum lying across the deck on two saddles
    "tank_r": 250.0, "tank_l": 640.0, "tank_x": -700.0, "tank_volume_l": 125.0,
    "saddle_y": 220.0, "saddle": (400.0, 80.0, 100.0),          # length along X, width along Y, height
    # Pump and alarm box (pump, battery, alarm controller)
    "pbox": (-430.0, -190.0, 340.0, 590.0, 240.0),               # x0, x1, y0, y1, height
    # Firebox skids: 50 x 50 x 3 square tube across the deck, welded under the firebox
    "skid": 50.0, "skid_t": 3.0, "skid_dx": 250.0,
    # Firebox: 3 mm steel shell, 50 mm ceramic fibre lining. Made taller so the door and fire bed sit
    # below the coil (STR-DDR-003, C1); 40 mm lower again with one coil turn fewer (evaporator bank study,
    # STR-CAL-001 v0.4, section 4)
    "fb_l": 700.0, "fb_w": 600.0, "fb_h": 960.0, "fb_x": 250.0,
    "fb_shell_t": 3.0, "fb_lining_t": 50.0,
    "grate_z": 100.0,          # underside of the grate above the inside of the firebox floor
    "grate": (300.0, 20.0),    # cast grate size (square) and thickness
    "door_open": (300.0, 240.0, 130.0),     # opening width, height, bottom above the inside floor
    "door_lap": 20.0,
    "air_open": (160.0, 60.0, 15.0),        # primary (under-grate) air inlet width, height, bottom above the inside floor
    "air2_open": (150.0, 20.0, 330.0),      # secondary (over-fire) air slot in the door: width, height, bottom above the inside floor
    # Monotube coil: 316 stainless, 25.4 mm OD x 1.65 mm wall, above the fire bed
    "coil_mean_d": 420.0, "tube_od": 25.4, "tube_wall": 1.65, "coil_turns": 10, "coil_pitch": 40.0,
    "coil_z0": 400.0,          # underside of the coil above the inside of the firebox floor
    "bracket_deg": (90.0, 210.0, 330.0), "bracket_angle": (40.0, 5.0), "bracket_tip": 25.0,
    "gland_hole": 40.0, "gland_lift": 30.0, "gland_plate": (80.0, 100.0, 6.0), "frame_angle": (25.0, 3.0),
    # Evaporator bank box between the firebox roof and the economizer (decided 2026-10-02, STR-DDR-002 item 1):
    # 2 mm steel walls and top on a 25 x 25 x 3 angle frame bolted down with the roof, 25 mm fibre lining,
    # and a serpentine of 15.88 mm x 1.24 mm 316 stainless tube (5/8 in x 0.049 in) in two layers of five runs
    "bk_h": 170.0, "bk_shell_t": 2.0, "bk_lining_t": 25.0,
    "bk_tube_od": 15.88, "bk_tube_wall": 1.24, "bk_pitch": 95.25, "bk_runs": 5, "bk_layers": 2,
    "bk_y0": -152.4,           # y of the inlet and outlet runs (the same y as the economizer outlet)
    "bk_z1": 45.0, "bk_dz": 60.0,  # bottom layer centre above the roof plate; layer spacing
    "bk_apex": 290.0,          # bend apexes at fb_x +/- this; 47.6 mm centreline bend radius (standard 5/8 in bender)
    # Gas-pass baffles (STR-DEC-001 S1, 2026-10-24, under Amish's standing instruction of 2026-10-23; STEM check S12):
    # the flue gas crosses the bank and the economizer tubes sideways instead of rising slowly past them.
    # The firebox outlet, the bank box outlet and the economizer inlet move to the -Y side, the economizer outlet
    # and the chimney to the +Y side.
    "flue_y_in": -145.0,       # y of the roof plate hole, the bank box top hole and the economizer floor hole
    "flue_y_out": 145.0,       # y of the economizer lid hole, its spigot and the chimney
    "bk_baffle_z": 73.5, "bk_baffle_t": 1.5, "bk_baffle_gap": 73.0,   # 304 stainless; bank baffle centre above the roof plate;
                                                                      # gas turns up through a gap at the +Y lining
    "eco_baffle_z": (98.0, 174.0), "eco_baffle_t": 1.0, "eco_baffle_gap": 58.0,   # 316L stainless (wet, acid end); above the floor;
                                                                                  # gaps at +Y (lower) and -Y (upper)
    # Flue-gas economizer box on top of the bank box (serpentine of 12.7 mm x 1.2 mm stainless tube)
    "eco_l": 520.0, "eco_w": 460.0, "eco_h": 260.0, "eco_tube_od": 12.7, "eco_tube_wall": 1.2, "eco_tube_len": 7300.0,
    "eco_flange": 30.0, "eco_layers": ((212.0, 6), (136.0, 6), (60.0, 5)),   # (tube centre above the box floor, passes)
    "eco_pitch": 76.2,         # run spacing and layer spacing: 38 mm centreline bend radius, a standard hand bender
    # Chimney with spark arrestor cap
    "chimney_d": 150.0, "chimney_top": 3200.0, "cap_h": 120.0, "spigot_h": 60.0,   # outlet raised from 2400 for draft (STR-DEC-001 S3)
    # Steam header (DN50), water-seal pot, vent pipe, diverter, post
    "header_od": 60.3, "header_len": 300.0, "header_z": 1550.0, "header_dx": 130.0,
    "seal_depth": 1000.0,      # dip leg depth plus annulus rise without the overflow; the overflow at the static
                               # water mark removes the rise, so the seal blows at the dip leg depth (STR-CAL-001, section 6)
    "ovf_od": 26.7, "ovf_trap": 350.0, "ovf_x": 1050.0, "ovf_end_z": 80.0,   # seal pot overflow: 3/4 in pipe, loop seal depth,
                                                                                  # down-pipe x (behind the deck), open end height
    "seal_pot_od": 114.3, "dip_od": 42.2, "vent_od": 42.2, "vent_top": 2300.0, "seal_sump": 100.0,
    "relief_d": 70.0, "post": 50.0, "foot": (200.0, 10.0),
    # Steam hose, 25 mm bore, 6 m
    "hose_od": 44.0, "hose_len": 6000.0,
    # Steam hoods (two, used alternately): open-bottom insulated pans
    "hood_l": 1200.0, "hood_w": 1000.0, "hood_h": 250.0, "hood_ins_t": 40.0, "hood_skin_t": 1.0,
    "skirt_depth": 60.0, "skirt_lap": 40.0, "skirt_t": 1.5,
    "handle_tube": (30.0, 2.5), "handle_foot": (100.0, 3.0), "ballast_kg": 40.0,   # steel handle tube; standoff foot plates;
                                                                                     # ballast per hood (four 10 kg weights)
    "hood_gap": 150.0, "hood_offset": 400.0, "n_hoods": 2,
}

Comp = namedtuple("Comp", "name shape bom kind group pieces holes", defaults=(None, None))


def derived(p=PARAMS):
    """Positions that follow from the parameters (mm)."""
    d = {}
    d["deck_top"] = p["deck_z"] + p["deck_t"]
    d["fb_z0"] = d["deck_top"] + p["skid"]
    d["fb_top"] = d["fb_z0"] + p["fb_h"]
    t = p["fb_shell_t"] + p["fb_lining_t"]
    d["t"] = t
    d["F"] = d["fb_z0"] + t                                   # inside floor
    d["ceil"] = d["fb_top"] - p["fb_lining_t"]                  # underside of the roof board
    d["fb_x0"], d["fb_x1"] = p["fb_x"] - p["fb_l"] / 2, p["fb_x"] + p["fb_l"] / 2
    d["fb_y1"] = p["fb_w"] / 2
    d["cz0"] = d["F"] + p["coil_z0"] + p["tube_od"] / 2         # coil centreline, start of the helix
    d["coil_top"] = d["cz0"] + p["coil_pitch"] * p["coil_turns"]
    d["bk_z0"] = d["fb_top"] + p["fb_shell_t"]                # top of the roof plate: the bank box stands on it
    d["bk_top"] = d["bk_z0"] + p["bk_h"]                       # top of the bank box top plate
    d["bk_zb"] = d["bk_z0"] + p["bk_z1"]                       # bottom (outlet) layer centreline
    d["bk_zt"] = d["bk_zb"] + p["bk_dz"]                       # top (inlet) layer centreline
    d["eco_z0"] = d["bk_top"]                                  # underside of the economizer flange, on the bank box top
    d["eco_floor"] = d["eco_z0"] + 6.0
    d["eco_top"] = d["eco_floor"] + p["eco_h"]
    d["lid_top"] = d["eco_top"] + 2.0
    d["hx"] = d["fb_x1"] + p["header_dx"]
    d["hz"] = p["header_z"]
    # water seal: the dip leg is shortened so that, with the water it pushes into the annulus, the
    # header can rise only to the 1 m effective seal head (0.094 bar) before steam bubbles through
    pot_id = p["seal_pot_od"] - 2 * 3.05
    a_dip = math.pi / 4 * (p["dip_od"] - 2 * 3.56) ** 2
    a_ann = math.pi / 4 * (pot_id ** 2 - p["dip_od"] ** 2)
    d["seal_ratio"] = a_dip / a_ann
    d["dip"] = p["seal_depth"] / (1 + d["seal_ratio"])          # dip leg depth below the static water line
    d["rise"] = d["dip"] * d["seal_ratio"]                      # annulus rise when the seal blows
    d["pot_bot"] = d["deck_top"] + p["foot"][1]
    d["dip_end"] = d["pot_bot"] + p["seal_sump"]
    d["water_line"] = d["dip_end"] + d["dip"]
    d["pot_top"] = d["water_line"] + d["rise"] + 100.0          # 100 mm splash room above the highest level
    d["pot_y"] = -p["header_len"] / 2 - p["seal_pot_od"] / 2 - 10
    d["div_y"] = p["header_len"] / 2 + 15 + 45
    d["vent_line_z"] = d["pot_top"] + 110.0
    d["ovf_z"] = d["water_line"] + (p["ovf_od"] - 2 * 2.87) / 2   # overflow branch centre: its invert is the static water mark
    d["hood_x0"] = p["deck_l"] / 2 + p["hood_offset"]
    d["hood_cx"] = [d["hood_x0"] + p["hood_l"] / 2 + i * (p["hood_l"] + p["hood_gap"]) for i in range(int(p["n_hoods"]))]
    d["hood_inlet_x"] = [c - p["hood_l"] / 2 + 150 for c in d["hood_cx"]]
    d["tank_z"] = d["deck_top"] + p["tank_r"] + 20
    return d


# ------------------------------------------------------------------ geometry helpers
def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z0, r, h):
    b = _b3d()
    return b.Pos(x, y, z0 + h / 2) * b.Cylinder(r, h)


def ycyl(x, y0, z, r, h):
    b = _b3d()
    return b.Pos(x, y0 + h / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def xcyl(x0, y, z, r, h):
    b = _b3d()
    return b.Pos(x0 + h / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


def hexprism(axis, x, y, z, af, h):
    """Hexagon across flats af, length h along axis ('x', 'y' or 'z'), starting at (x, y, z)."""
    b = _b3d()
    hx_ = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h)
    if axis == "z":
        return b.Pos(x, y, z) * hx_
    if axis == "y":
        return b.Pos(x, y, z) * b.Rot(-90, 0, 0) * hx_
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * hx_


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def group(shapes):
    """Several solids as one compound, without a boolean (fixings)."""
    b = _b3d()
    return b.Compound(children=list(shapes))


def _tube_along(points, od, wall=None):
    """Round tube through a polyline of (x, y, z) points (square joints with a ball at each corner); with a wall
    thickness, hollow and open at both ends."""
    if wall:
        out = _tube_along(points, od)
        p0, p1 = points[0], points[-1]
        q0, q1 = points[1], points[-2]
        ext = []
        for a_, c_ in ((p0, q0), (p1, q1)):
            d_ = [a_[i] - c_[i] for i in range(3)]
            n_ = math.sqrt(sum(x * x for x in d_)) or 1.0
            ext.append(tuple(a_[i] + d_[i] / n_ * 2.0 for i in range(3)))
        return out - _tube_along([ext[0]] + list(points[1:-1]) + [ext[1]], od - 2 * wall)
    from build123d import Cylinder, Vector, Sphere, Pos, Plane
    pts = [points[0]]
    for q in points[1:]:
        if math.dist(q, pts[-1]) > 1e-6:
            pts.append(q)
    points = pts
    out = None
    for i, (a, b) in enumerate(zip(points[:-1], points[1:])):
        a, b = Vector(*a), Vector(*b)
        d = b - a
        pl = Plane(origin=(a + b) * 0.5, z_dir=d.normalized())
        seg = pl * Cylinder(od / 2, d.length)
        out = seg if out is None else out + seg
        if i < len(points) - 2:
            out = out + Pos(*b) * Sphere(od / 2)
    return out


def bolt_z(x, y, z_top, z_bot, d, head_up=True):
    """Bolt along Z through a stack from z_bot to z_top: shank, hex head on one side, nut on the other."""
    af = {6: 10, 8: 13, 10: 16, 12: 18}[int(d)]
    hh = 0.7 * d
    shank = zcyl(x, y, z_bot - 0.8 * d - 2, d / 2, z_top - z_bot + 1.5 * d + 4)
    head = hexprism("z", x, y, z_top if head_up else z_bot - hh, af, hh)
    nut = hexprism("z", x, y, z_bot - 0.8 * d if head_up else z_top, af, 0.8 * d)
    return [shank, head, nut]


def stud_z(x, y, z_bot, z_top, d):
    """Stud welded on a plate at z_bot, through the parts above it to z_top, nut on top."""
    af = {6: 10, 8: 13, 10: 16, 12: 18}[int(d)]
    return [zcyl(x, y, z_bot, d / 2, z_top - z_bot + 1.2 * d), hexprism("z", x, y, z_top, af, 0.8 * d)]


def bolt_y(x, z, y_a, y_b, d):
    """Bolt along Y through a stack from y_a to y_b (y_a < y_b): head at y_a, nut at y_b."""
    af = {6: 10, 8: 13, 10: 16, 12: 18}[int(d)]
    return [ycyl(x, y_a - 0.7 * d, z, d / 2, y_b - y_a + 1.5 * d + 2),
            hexprism("y", x, y_a - 0.7 * d, z, af, 0.7 * d), hexprism("y", x, y_b, z, af, 0.8 * d)]


def bolt_x(y, z, x_a, x_b, d):
    af = {6: 10, 8: 13, 10: 16, 12: 18}[int(d)]
    return [xcyl(x_a - 0.7 * d, y, z, d / 2, x_b - x_a + 1.5 * d + 2),
            hexprism("x", x_a - 0.7 * d, y, z, af, 0.7 * d), hexprism("x", x_b, y, z, af, 0.8 * d)]


def angle_y(x, y0, y1, z_top, leg, t, hang_x=+1):
    """Equal angle running along Y from y0 to y1: horizontal leg on top (top face at z_top), vertical
    leg hanging down at the +X (hang_x=+1) or -X edge."""
    h = bx(x - leg / 2, x + leg / 2, y0, y1, z_top - t, z_top)
    xe = x + hang_x * (leg / 2 - t / 2)
    v = bx(xe - t / 2, xe + t / 2, y0, y1, z_top - leg, z_top - t)
    return h + v


def angle_x(y, x0, x1, z_top, leg, t, hang_y=+1):
    h = bx(x0, x1, y - leg / 2, y + leg / 2, z_top - t, z_top)
    ye = y + hang_y * (leg / 2 - t / 2)
    v = bx(x0, x1, ye - t / 2, ye + t / 2, z_top - leg, z_top - t)
    return h + v


def rhs_y(x, y0, y1, z0, s, t):
    """Square hollow section along Y."""
    return bx(x - s / 2, x + s / 2, y0, y1, z0, z0 + s) - bx(x - s / 2 + t, x + s / 2 - t, y0 - 1, y1 + 1, z0 + t, z0 + s - t)


def rhs_z(x, y, z0, z1, s, t):
    return bx(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z0, z1) - bx(x - s / 2 + t, x + s / 2 - t, y - s / 2 + t, y + s / 2 - t, z0 - 1, z1 + 1)


def helix_point(theta_deg, p=PARAMS):
    D = derived(p)
    th = math.radians(theta_deg)
    r = p["coil_mean_d"] / 2
    return (p["fb_x"] + r * math.cos(th), r * math.sin(th), D["cz0"] + p["coil_pitch"] * theta_deg / 360.0)


def eco_bank_points(p=PARAMS):
    """Centreline of the economizer serpentine, inlet (top layer, -X end) to outlet (bottom layer, +X end)."""
    D = derived(p)
    x0, x1 = p["fb_x"] - 193.0, p["fb_x"] + 193.0           # bend apexes; 316 mm straight between R35 bends
    pts = []
    for li, (zrel, n) in enumerate(p["eco_layers"]):
        z = D["eco_floor"] + zrel
        yy = (n - 1) * p["eco_pitch"] / 2                     # runs centred across the box
        ys = [yy - k * p["eco_pitch"] for k in range(n)]
        if li == 1:
            ys = ys[::-1]
        for k, y in enumerate(ys):
            a, c = (x0, x1) if k % 2 == 0 else (x1, x0)
            if pts and abs(pts[-1][2] - z) > 1e-6:
                pts.append((pts[-1][0], pts[-1][1], z))       # riser between layers at the -X end
            pts.append((a, y, z))
            pts.append((c, y, z))
    return pts


def bank_points(p=PARAMS):
    """Centreline of the evaporator bank, inlet (top layer, +X wall) to outlet (bottom layer, +X wall)."""
    D = derived(p)
    fx = p["fb_x"]
    xw = fx + p["fb_l"] / 2 + 15.0                          # tails end 15 mm outside the +X wall
    a0, a1 = fx + p["bk_apex"], fx - p["bk_apex"]
    ys = [p["bk_y0"] + k * p["bk_pitch"] for k in range(int(p["bk_runs"]))]
    pts = []
    for li in range(int(p["bk_layers"])):
        z = D["bk_zt"] - li * p["bk_dz"]
        yl = ys if li % 2 == 0 else ys[::-1]
        start_plus = (li % 2 == 0)
        for k, y in enumerate(yl):
            plus_first = (k % 2 == 0) == start_plus
            a, c = (a0, a1) if plus_first else (a1, a0)
            if pts and abs(pts[-1][2] - z) > 1e-6:
                pts.append((pts[-1][0], pts[-1][1], z))       # riser between layers at the -X end
            pts.append((a, y, z))
            pts.append((c, y, z))
    pts[0] = (xw, pts[0][1], pts[0][2])
    pts[-1] = (xw, pts[-1][1], pts[-1][2])
    return pts


def bank_length(p=PARAMS):
    """Tube length of the bank (m): centreline with each square corner replaced by its bend."""
    pts = bank_points(p)
    L = sum(math.dist(a, c) for a, c in zip(pts[:-1], pts[1:]))
    R = 47.6
    n_bends = 2 * (int(p["bk_runs"]) - 1) * int(p["bk_layers"]) + 2 * (int(p["bk_layers"]) - 1)
    return (L - n_bends * (2 - math.pi / 2) * R) / 1000


def eco_ends(p=PARAMS):
    pts = eco_bank_points(p)
    return pts[0], pts[-1]


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component of option A keyed by a short name: Comp(name, shape, bom, kind, group, pieces, holes).
    'pieces' lists each made or bought piece (or each bolt, washer and nut of a fixing group) as
    (name, shape[, material]); 'shape' is their compound. Kit 1.9 (D3): real stock, ISO fasteners in
    clearance holes, weld beads (key 'welds') and the gas-pass baffles of STR-DEC-001 S1."""
    b = _b3d()
    import str_parts as sp
    import cad_parts as cpk
    D = derived(p)
    C = {}
    W = []                                                    # weld beads: (name, shape, bom, group)

    def add(key, name, items, bom, kind, group_, holes=None):
        if isinstance(items, list):
            pieces = [tuple(q) for q in items]
            shape = b.Compound(children=[q[1] for q in pieces])
        else:
            pieces = [(name, items)]
            shape = items
        C[key] = Comp(name, shape, bom, kind, group_, pieces, list(holes or getattr(items, "holes", [])))

    def weld(name, bom, group_, *a):
        W.append((name, sp.weld(*a), bom, group_))

    def ring(name, bom, group_, *a):
        W.append((name, sp.ring_weld(*a), bom, group_))

    def around(name, bom, group_, x0, x1, y0, y1, z, leg, up=True):
        """Four fillet beads round the foot of a rectangular section x0..x1, y0..y1 standing on (up) or hanging
        from (not up) a face at z, each shortened by one leg at both ends so the corners do not overlap."""
        v = (0, 0, 1) if up else (0, 0, -1)
        for (ax, ay, al, d, u) in ((x0 + leg, y0, x1 - x0 - 2 * leg, (1, 0, 0), (0, -1, 0)),
                                   (x0 + leg, y1, x1 - x0 - 2 * leg, (1, 0, 0), (0, 1, 0)),
                                   (x0, y0 + leg, y1 - y0 - 2 * leg, (0, 1, 0), (-1, 0, 0)),
                                   (x1, y0 + leg, y1 - y0 - 2 * leg, (0, 1, 0), (1, 0, 0))):
            W.append((name, sp.weld((ax, ay, z), d, al, leg, u, v), bom, group_))

    T = D["deck_top"]
    x0d = -p["deck_l"] / 2
    rw = p["rail_w"]

    # 1 trailer (bought used): perimeter rails and deck skin, drawbar with coupling, jockey jack, axle with hangers
    dl2, dw2, dz = p["deck_l"] / 2, p["deck_w"] / 2, p["deck_z"]
    rt = 4.0                                                   # rail wall: 80 x 70 x 4 RHS perimeter frame
    frame = bx(-dl2, dl2, -dw2, dw2, dz, T - 10) - bx(-dl2 + rw, dl2 - rw, -dw2 + rw, dw2 - rw, dz - 1, T)
    frame -= (bx(-dl2 + rt, dl2 - rt, -dw2 + rt, dw2 - rt, dz + rt, T - 10 - rt) - bx(-dl2 + rw - rt, dl2 - rw + rt, -dw2 + rw - rt, dw2 - rw + rt, dz, T))
    deck = bx(-dl2, dl2, -dw2, dw2, T - 10, T)                 # 10 mm exterior plywood deck
    drawbar = bx(x0d - p["drawbar_l"], x0d, -40, 40, dz, dz + 80) - bx(x0d - p["drawbar_l"] - 1, x0d + 1, -36, 36, dz + 4, dz + 76)
    coupling = bx(x0d - p["drawbar_l"] - 120, x0d - p["drawbar_l"], -50, 50, dz + 10, dz + 70)
    jack = zcyl(x0d - p["drawbar_l"] + 150, 0, 0, 30, dz) - zcyl(x0d - p["drawbar_l"] + 150, 0, -1, 25, dz + 2)
    axle = ycyl(p["axle_x"], -dw2 - p["wheel_gap"], p["wheel_r"], 30, p["deck_w"] + 2 * p["wheel_gap"])
    axle -= ycyl(p["axle_x"], -dw2 - p["wheel_gap"] - 1, p["wheel_r"], 25, p["deck_w"] + 2 * p["wheel_gap"] + 2)
    hang = [bx(p["axle_x"] - 40, p["axle_x"] + 40, -dw2 + 10, -dw2 + 70, p["wheel_r"], dz),
            bx(p["axle_x"] - 40, p["axle_x"] + 40, dw2 - 70, dw2 - 10, p["wheel_r"], dz)]
    hang = [h - ycyl(p["axle_x"], -dw2 - p["wheel_gap"], p["wheel_r"], 30, p["deck_w"] + 2 * p["wheel_gap"]) for h in hang]
    add("trailer", "Trailer frame and drawbar", [("Trailer frame, 80 x 70 x 4 RHS rails", frame), ("Trailer deck, 10 mm plywood", deck, "plywood"),
        ("Trailer drawbar, 80 x 80 x 4 RHS", drawbar),
        ("Trailer coupling", coupling), ("Jockey jack", jack), ("Trailer axle", axle),
        ("Spring hanger, left", hang[0]), ("Spring hanger, right", hang[1])], 1, "bought", "Trailer frame and drawbar")
    wy = p["deck_w"] / 2 + p["wheel_gap"]
    add("wheels", "Wheels", [("Wheel and tyre, right", ycyl(p["axle_x"], wy, p["wheel_r"], p["wheel_r"], p["wheel_w"]), "epdm"),
        ("Wheel and tyre, left", ycyl(p["axle_x"], -wy - p["wheel_w"], p["wheel_r"], p["wheel_r"], p["wheel_w"]), "epdm")],
        2, "bought", "Wheels")

    # 17 firebox skids (50 x 50 x 3 SHS) across the deck, bolted through the deck into the side rails
    s, st = p["skid"], p["skid_t"]
    skx = [p["fb_x"] - p["skid_dx"], p["fb_x"] + p["skid_dx"]]
    add("skids", "Firebox skids (2)", [(f"Firebox skid {i + 1}, 50 x 50 x 3 SHS", rhs_y(x, -p["deck_w"] / 2, p["deck_w"] / 2, T, s, st))
                                       for i, x in enumerate(skx)], 17, "made", "Firebox skids")
    ry = p["deck_w"] / 2 - rw / 2
    fx_ = sp.Fix()
    for x in skx:
        for y in (-ry, ry):
            fx_ += sp.bolt(12, T + s - p["deck_z"], (x, y, T + s), "-z")
    add("skid_bolts", "M12 skid bolts (4)", fx_, 21, "fixing", None)

    # 5 firebox shell (3 mm steel) with its openings, and the fibre lining inside it
    t, sh = D["t"], p["fb_shell_t"]
    L, Wd, H = p["fb_l"], p["fb_w"], p["fb_h"]
    fx, z0, F = p["fb_x"], D["fb_z0"], D["F"]
    zc = z0 + H / 2
    dw, dh, db = p["door_open"]
    aw, ah, ab = p["air_open"]
    door_cut = bx(fx - dw / 2, fx + dw / 2, -Wd / 2 - 1, -Wd / 2 + t + 1, F + db, F + db + dh)
    air_cut = bx(fx - aw / 2, fx + aw / 2, -Wd / 2 - 1, -Wd / 2 + t + 1, F + ab, F + ab + ah)
    glands_z = [D["cz0"], D["coil_top"]]
    gh, lift = p["gland_hole"], p["gland_lift"]
    # slots, not holes: the coil goes in from the top, 30 mm high, and its tails slide out through these
    gland_cut = fuse([bx(D["fb_x1"] - t - 1, D["fb_x1"] + 1, -gh / 2, gh / 2, z - gh / 2, z + gh / 2 + lift) for z in glands_z])
    cuts = door_cut + air_cut + gland_cut
    top = D["fb_top"]
    yi = p["flue_y_in"]
    shell = box(fx, 0, zc, L, Wd, H) - bx(fx - L / 2 + sh, fx + L / 2 - sh, -Wd / 2 + sh, Wd / 2 - sh, z0 + sh, top + 1)
    shell -= cuts
    fa, ft = p["frame_angle"]                         # 25 x 25 x 3 angle frame round the top, for the roof bolts
    frame_h = bx(fx - L / 2 - fa, fx + L / 2 + fa, -Wd / 2 - fa, Wd / 2 + fa, top - ft, top) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, top - ft - 1, top + 1)
    frame_v = bx(fx - L / 2 - ft, fx + L / 2 + ft, -Wd / 2 - ft, Wd / 2 + ft, top - fa, top - ft) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, top - fa - 1, top)
    add("shell", "Firebox shell", [("Firebox shell, 3 mm steel, welded box", shell),
                                   ("Firebox roof frame, 25 x 25 x 3 angle, mitred ring", frame_h + frame_v)], 5, "made", "Firebox, fiber lined")
    for (ax, ay, al, d, u) in ((fx - L / 2, -Wd / 2 - 0.0, L, (1, 0, 0), (0, -1, 0)), (fx - L / 2, Wd / 2, L, (1, 0, 0), (0, 1, 0)),
                               (fx - L / 2, -Wd / 2, Wd, (0, 1, 0), (-1, 0, 0)), (fx + L / 2, -Wd / 2, Wd, (0, 1, 0), (1, 0, 0))):
        if d == (1, 0, 0):
            for xa, xb in ((fx - L / 2 + 4, fx - 180), (fx - 120, fx + 120), (fx + 180, fx + L / 2 - 4)):   # stitch welds between the bolts
                weld("Weld, roof frame to shell (stitch)", 5, "Firebox, fiber lined", (xa, ay, top - fa), d, xb - xa, 3, u, (0, 0, -1))
        else:
            for ya, yb in ((-Wd / 2 + 4, -90), (-50, 50), (90, Wd / 2 - 4)):
                weld("Weld, roof frame to shell (stitch)", 5, "Firebox, fiber lined", (ax, ya, top - fa), d, yb - ya, 3, u, (0, 0, -1))
    roof = bx(fx - L / 2 - fa, fx + L / 2 + fa, -Wd / 2 - fa, Wd / 2 + fa, top, top + sh) - zcyl(fx, yi, top - 1, p["chimney_d"] / 2, sh + 2)
    add("roof", "Firebox roof", [("Firebox roof plate, 3 mm, flue opening at the -Y side", roof)], 5, "made", "Firebox, fiber lined")
    rfix = sp.Fix()
    xs_r = [fx - L / 2 - fa / 2 + i * (L + fa) / 4 for i in range(5)]
    ys_r = [-Wd / 2 - fa / 2 + i * (Wd + fa) / 3 for i in range(4)]
    for xr in xs_r:
        for yr in (-Wd / 2 - fa / 2, Wd / 2 + fa / 2):
            rfix += sp.bolt(8, sh + 2 * ft, (xr, yr, top + sh + ft), "-z")
    for yr in ys_r[1:-1]:
        for xr in (fx - L / 2 - fa / 2, fx + L / 2 + fa / 2):
            rfix += sp.bolt(8, sh + 2 * ft, (xr, yr, top + sh + ft), "-z")
    add("roof_bolts", "M8 roof bolts (14), through the bank box frame, roof and shell frame", rfix, 21, "fixing", None)

    # 18 coil brackets: 40 x 40 x 5 stainless angle, welded to the inside of the shell, through slots
    #    in the lining; each carries the lowest turn of the coil
    leg, bt = p["bracket_angle"]
    tip = p["bracket_tip"]
    brk = []
    for deg in p["bracket_deg"]:
        xh, yh, _ = helix_point(deg, p)
        # the coil slopes 40 mm a turn: set the bracket top under the tube where it crosses the
        # downhill edge of the bracket, so the tube rests on that edge and does not cut into it
        c = abs(math.cos(math.radians(deg)))
        half = leg / 2 / (1.0 if c < 0.01 else c) if abs(math.sin(math.radians(deg))) < 0.99 else leg / 2
        dth = math.degrees(half / (p["coil_mean_d"] / 2))
        ztop = helix_point(deg - dth, p)[2] - p["tube_od"] / 2
        if abs(math.sin(math.radians(deg))) > 0.99:          # on the +Y or -Y wall, runs along Y
            sgn = 1 if math.sin(math.radians(deg)) > 0 else -1
            y_in = sgn * (Wd / 2 - sh)
            brk.append(angle_y(xh, min(y_in, yh - sgn * tip), max(y_in, yh - sgn * tip), ztop, leg, bt, hang_x=+1))
            weld("Weld, coil bracket to shell", 18, "Firebox, fiber lined", (xh - leg / 2 + 3, y_in, ztop), (1, 0, 0), leg - 6, 3, (0, -sgn, 0), (0, 0, 1))
        else:                                                 # on the +X or -X wall, runs along X
            sgn = 1 if math.cos(math.radians(deg)) > 0 else -1
            x_in = fx + sgn * (L / 2 - sh)
            brk.append(angle_x(yh, min(x_in, xh - sgn * tip), max(x_in, xh - sgn * tip), ztop, leg, bt, hang_y=-1))
            weld("Weld, coil bracket to shell", 18, "Firebox, fiber lined", (x_in, yh - leg / 2 + 3, ztop), (0, 1, 0), leg - 6, 3, (-sgn, 0, 0), (0, 0, 1))
    add("brackets", "Coil brackets (3)", [(f"Coil bracket {i + 1}, 40 x 40 x 5 stainless angle", q, "stainless") for i, q in enumerate(brk)],
        18, "made", "Firebox, fiber lined")

    lt = p["fb_lining_t"]
    lining = bx(fx - L / 2 + sh, fx + L / 2 - sh, -Wd / 2 + sh, Wd / 2 - sh, z0 + sh, top) - bx(fx - L / 2 + t, fx + L / 2 - t, -Wd / 2 + t, Wd / 2 - t, F, top + 1)
    lining -= cuts
    for bk in brk:                                           # slots cut 5 mm round each bracket and its weld
        bb = bk.bounding_box()
        lining -= bx(bb.min.X - 5, bb.max.X + 5, bb.min.Y - 5, bb.max.Y + 5, bb.min.Z - 5, bb.max.Z + 5)
    add("lining", "Ceramic fibre lining", [("Ceramic fibre lining, 50 mm, walls and floor", lining, "insulated_white")], 5, "bought", "Firebox, fiber lined")
    board = bx(fx - L / 2 + t, fx + L / 2 - t, -Wd / 2 + t, Wd / 2 - t, top - lt, top) - zcyl(fx, yi, top - lt - 1, p["chimney_d"] / 2, lt + 2)
    add("board", "Roof board", [("Ceramic fibre roof board, 50 mm", board, "insulated_white")], 5, "bought", "Firebox, fiber lined")

    # 18 grate stand (25 mm square tube ring on four legs with foot pads) and 5 cast grate
    gs, gt = p["grate"]
    gz = F + p["grate_z"]
    ringp = bx(fx - gs / 2, fx + gs / 2, -gs / 2, gs / 2, gz - 25, gz) - bx(fx - gs / 2 + 25, fx + gs / 2 - 25, -gs / 2 + 25, gs / 2 - 25, gz - 26, gz + 1)
    ringp -= bx(fx - gs / 2 + 2, fx + gs / 2 - 2, -gs / 2 + 2, gs / 2 - 2, gz - 23, gz - 2) - bx(fx - gs / 2 + 23, fx + gs / 2 - 23, -gs / 2 + 23, gs / 2 - 23, gz - 24, gz - 1)
    spieces = [("Grate stand ring, 25 x 25 x 2 SHS", ringp)]
    k = 0
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            k += 1
            cx_, cy_ = fx + sx_ * (gs / 2 - 12.5), sy_ * (gs / 2 - 12.5)
            spieces.append((f"Grate stand leg {k}, 25 x 25 x 2 SHS", rhs_z(cx_, cy_, F + 5, gz - 25, 25, 2)))
            spieces.append((f"Grate stand foot pad {k}, 60 x 60 x 5", bx(cx_ - 30, cx_ + 30, cy_ - 30, cy_ + 30, F, F + 5)))
            around("Weld, grate stand leg to pad", 18, "Firebox, fiber lined", cx_ - 12.5, cx_ + 12.5, cy_ - 12.5, cy_ + 12.5, F + 5, 3)
    add("stand", "Grate stand", spieces, 18, "made", "Firebox, fiber lined")
    grate = bx(fx - gs / 2, fx + gs / 2, -gs / 2, gs / 2, gz, gz + gt)
    for i in range(-5, 6):
        grate -= bx(fx + i * 25 - 6, fx + i * 25 + 6, -gs / 2 + 25, gs / 2 - 25, gz - 1, gz + gt + 1)
    add("grate", "Cast grate", [("Cast iron grate, 300 x 300", grate, "mild_steel")], 5, "bought", "Firebox, fiber lined")

    # 5 door: 3 mm plate lapping the opening by 20 mm, with a 46 mm fibre board plug; handle; hinges; latch
    lap = p["door_lap"]
    yd = -Wd / 2
    dz0, dz1 = F + db - lap, F + db + dh + lap
    dx0, dx1 = fx - dw / 2 - lap, fx + dw / 2 + lap
    s2w, s2h, s2b = p["air2_open"]
    s2z0, s2z1 = F + s2b, F + s2b + s2h
    dplate = bx(dx0, dx1, yd - 3, yd, dz0, dz1) - bx(fx - s2w / 2, fx + s2w / 2, yd - 4, yd + 1, s2z0, s2z1)
    plug = bx(fx - dw / 2 + 4, fx + dw / 2 - 4, yd, yd + t - 4, F + db + 4, F + db + dh - 4) - bx(fx - s2w / 2, fx + s2w / 2, yd - 1, yd + t, s2z0, s2z1)
    zm_ = (dz0 + dz1) / 2
    hbar = bx(fx - 60, fx + 60, yd - 3 - 30, yd - 3 - 20, zm_ - 8, zm_ + 8)
    hst = [bx(fx + sx_ * 60 - 8, fx + sx_ * 60 + 8, yd - 23, yd - 3, zm_ - 8, zm_ + 8) for sx_ in (-1, 1)]
    add("door", "Firebox door", [("Firebox door plate, 3 mm", dplate), ("Door plug, ceramic fibre board", plug, "insulated_white"),
                                 ("Door handle bar, 16 x 10 flat", hbar), ("Door handle standoff, left", hst[0]),
                                 ("Door handle standoff, right", hst[1])], 5, "made", "Firebox, fiber lined")
    for sx_ in (-1, 1):
        for zz, vv in ((zm_ + 8, 1), (zm_ - 8, -1)):
            weld("Weld, door handle standoff to plate", 5, "Firebox, fiber lined", (fx + sx_ * 60 - 8 + 2, yd - 3, zz), (1, 0, 0), 12, 2.5, (0, 0, vv), (0, -1, 0))
    q0, q1 = s2z0 - 15, s2z1 + 15
    dslide2 = bx(fx - s2w / 2 - 20, fx + s2w / 2 + 20, yd - 6, yd - 3, q0, q1)
    knob2 = ycyl(fx - s2w / 2 - 5, yd - 22, (q0 + q1) / 2, 8, 16)
    add("damper2", "Secondary air damper slide", [("Secondary air damper slide, 3 mm", dslide2), ("Secondary damper knob", knob2, "matte_black")],
        5, "made", "Firebox, fiber lined")
    g2 = []
    for zg, sgn in ((q1, 1), (q0, -1)):
        gz0, gz1 = (zg, zg + 6) if sgn > 0 else (zg - 6, zg)
        g = bx(fx - s2w / 2 - 50, fx + s2w / 2 + 50, yd - 6, yd - 3, gz0, gz1)
        g += bx(fx - s2w / 2 - 50, fx + s2w / 2 + 50, yd - 9, yd - 6, gz0, gz1)
        g += bx(fx - s2w / 2 - 50, fx + s2w / 2 + 50, yd - 9, yd - 6, (gz0 - 6 if sgn > 0 else gz1), (gz0 if sgn > 0 else gz1 + 6))
        g2.append(g)
        ze = gz1 if sgn > 0 else gz0
        weld("Weld, secondary damper guide to door", 5, "Firebox, fiber lined", (fx - s2w / 2 - 46, yd - 3, ze), (1, 0, 0), s2w + 92, 2.5, (0, 0, sgn), (0, -1, 0))
    add("guides2", "Secondary damper guides (2)", [("Secondary damper guide, upper", g2[0]), ("Secondary damper guide, lower", g2[1])], 5, "made", "Firebox, fiber lined")
    hinges = []
    for zh_ in (dz0 + 40, dz1 - 40):
        hg = zcyl(dx1 + 10, yd - 9, zh_ - 30, 8, 60)                       # knuckle on its pin
        hg += bx(dx1 - 15, dx1 + 4, yd - 6, yd - 3, zh_ - 30, zh_ + 30)       # leaf welded to the door
        hg += bx(dx1 + 16, dx1 + 40, yd - 3, yd, zh_ - 30, zh_ + 30)          # leaf welded to the shell
        hg += bx(dx1 + 2, dx1 + 18, yd - 6, yd - 3, zh_ - 30, zh_ + 30)
        hinges.append(hg)
        weld("Weld, hinge leaf to door", 5, "Firebox, fiber lined", (dx1 - 15, yd - 3, zh_ - 27), (0, 0, 1), 54, 2.5, (-1, 0, 0), (0, -1, 0))
        weld("Weld, hinge leaf to shell", 5, "Firebox, fiber lined", (dx1 + 40, yd, zh_ - 27), (0, 0, 1), 54, 2.5, (1, 0, 0), (0, -1, 0))
    add("hinges", "Door hinges (2)", [("Weld-on door hinge, upper", hinges[1], "zinc_plated"), ("Weld-on door hinge, lower", hinges[0], "zinc_plated")],
        5, "bought", "Firebox, fiber lined")
    zl = zm_
    keeper = bx(dx0 - 30, dx0 - 6, yd - 20, yd, zl + 10, zl + 30)          # keeper welded to the shell
    lbar = bx(dx0 - 30, dx0 + 40, yd - 26, yd - 20, zl + 10, zl + 30)      # turn latch bar over the door edge
    boss = bx(dx0 + 20, dx0 + 40, yd - 20, yd - 3, zl + 10, zl + 30)       # latch boss on the door
    add("latch", "Door latch", [("Door latch keeper", keeper, "zinc_plated"), ("Door turn latch bar", lbar, "zinc_plated"),
                                ("Door latch boss", boss, "zinc_plated")], 5, "bought", "Firebox, fiber lined")

    # 5 primary air damper: 3 mm slide plate in two guides below the door
    az0, az1 = F + ab, F + ab + ah
    pz0, pz1 = az0 - 20, az1 + 20
    dslide = bx(fx - aw / 2 - 30, fx + aw / 2 + 30, yd - 6, yd - 3, pz0, pz1)
    knob = ycyl(fx - aw / 2 - 10, yd - 26, (pz0 + pz1) / 2, 10, 20)
    add("damper", "Primary air damper slide", [("Primary air damper slide, 3 mm", dslide), ("Primary damper knob", knob, "matte_black")],
        5, "made", "Firebox, fiber lined")
    guides = []
    for zg, sgn in ((pz1, 1), (pz0, -1)):
        g = bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 3, yd, zg if sgn > 0 else zg - 6, zg + 6 if sgn > 0 else zg)
        g += bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 9, yd - 3, zg if sgn > 0 else zg - 6, zg + 6 if sgn > 0 else zg)
        g += bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 9, yd - 6, (zg - 6 if sgn > 0 else zg), (zg if sgn > 0 else zg + 6))
        guides.append(g)
        ze = zg + 6 if sgn > 0 else zg - 6
        weld("Weld, damper guide to shell", 5, "Firebox, fiber lined", (fx - aw / 2 - 56, yd, ze), (1, 0, 0), aw + 112, 2.5, (0, 0, sgn), (0, -1, 0))
    add("guides", "Damper guides (2)", [("Primary damper guide, upper", guides[0]), ("Primary damper guide, lower", guides[1])], 5, "made", "Firebox, fiber lined")

    # 6 monotube coil: helix above the fire bed, tails out through the +X wall
    r = p["coil_mean_d"] / 2
    height = p["coil_pitch"] * p["coil_turns"]
    path = b.Pos(fx, 0, D["cz0"]) * b.Helix(pitch=p["coil_pitch"], height=height, radius=r)
    prof = b.Plane(origin=path @ 0, z_dir=path % 0) * (b.Circle(p["tube_od"] / 2) - b.Circle(p["tube_od"] / 2 - p["tube_wall"]))
    helix = b.sweep(prof, path, is_frenet=True)
    x_out = D["fb_x1"]
    hx, hz = D["hx"], D["hz"]
    tail_end = x_out + 10                          # tails stop 10 mm outside the wall so the coil can go in
    tails = [_tube_along([(fx + r, 0, z_), (tail_end, 0, z_)], p["tube_od"], p["tube_wall"]) for z_ in (D["coil_top"], D["cz0"])]
    # one part of three solids: a boolean union of the hollow helix and its hollow tails drops the helix (OCC), so
    # the tails are kept as separate solids butted to the helix ends
    add("coil", "Monotube steam coil", [("Monotube steam coil, 316 stainless 25.4 x 1.65, 10 turns", b.Compound(children=[helix] + tails), "stainless")],
        6, "made", "Monotube steam coil")
    union_o = hexprism("x", tail_end, 0, D["coil_top"], 36, 25)               # compression union
    opipe = _tube_along([(tail_end + 25, 0, D["coil_top"]), (x_out + 60, 0, D["coil_top"]), (x_out + 60, 0, hz),
                         (hx - p["header_od"] / 2, 0, hz)], p["tube_od"], p["tube_wall"])
    add("outlet", "Coil outlet pipe and union", [("Coil outlet union, 25.4 mm compression", union_o, "stainless"),
                                                 ("Coil outlet pipe, 316 stainless 25.4 mm", opipe, "stainless")], 6, "made", "Monotube steam coil")

    # 18 tube gland plates on the outside of the +X wall, with their M6 weld studs
    gpw, gph, gpt = p["gland_plate"]
    gl, gfix = [], sp.Fix()
    for z in glands_z:
        zm = z + lift / 2
        g = bx(x_out, x_out + gpt, -gpw / 2, gpw / 2, zm - gph / 2, zm + gph / 2) - xcyl(x_out - 1, 0, z, p["tube_od"] / 2 + 0.3, gpt + 2)
        gl.append(g)
        for dy in (-28, 28):
            for dz in (-38, 38):
                gfix += sp.stud(6, (x_out, dy, zm + dz), "+x", gpt)
    add("glands", "Tube gland plates (2)", [("Tube gland plate, lower", gl[0]), ("Tube gland plate, upper", gl[1])], 18, "made", "Firebox, fiber lined")
    add("gland_studs", "M6 gland studs and nuts (8)", gfix, 21, "fixing", None)

    # 22 evaporator bank box on the roof plate: 2 mm walls and top on a 25 x 25 x 3 angle frame that the
    #    roof bolts clamp down, 25 mm fibre lining, a slot in the +X wall for the two tails (open at the
    #    bottom so the box lowers over the bank) closed by a cover plate, the bank on support bars, and the
    #    gas-pass baffle between the two layers (STR-DEC-001 S1)
    e_in, e_out = eco_ends(p)
    bt_, blt = p["bk_shell_t"], p["bk_lining_t"]
    bz0, btop = D["bk_z0"], D["bk_top"]
    bpts = bank_points(p)
    bod = p["bk_tube_od"]
    br = bod / 2
    xw = fx + L / 2
    slot = bx(xw - bt_ - blt - 1, xw + ft + 1, p["bk_y0"] - br - 1, p["bk_y0"] + br + 1, bz0 - 1, D["bk_zt"] + br + 1)
    walls = bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, bz0, btop) - bx(fx - L / 2 + bt_, fx + L / 2 - bt_, -Wd / 2 + bt_, Wd / 2 - bt_, bz0 - 1, btop - bt_)
    walls -= zcyl(fx, yi, btop - bt_ - 1, p["chimney_d"] / 2, bt_ + 2)
    bframe = bx(fx - L / 2 - fa, fx + L / 2 + fa, -Wd / 2 - fa, Wd / 2 + fa, bz0, bz0 + ft) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, bz0 - 1, bz0 + ft + 1)
    bframe += bx(fx - L / 2 - ft, fx + L / 2 + ft, -Wd / 2 - ft, Wd / 2 + ft, bz0 + ft, bz0 + fa) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, bz0, bz0 + fa + 1)
    add("bk_box", "Evaporator bank box", [("Evaporator bank box, 2 mm steel, welded", walls - slot),
                                          ("Bank box frame, 25 x 25 x 3 angle, mitred ring", bframe - slot)], 22, "made", "Evaporator bank")
    for (ax, ay, al, d, u) in ((fx - L / 2, -Wd / 2, L, (1, 0, 0), (0, -1, 0)), (fx - L / 2, Wd / 2, L, (1, 0, 0), (0, 1, 0)),
                               (fx - L / 2, -Wd / 2, Wd, (0, 1, 0), (-1, 0, 0)), (fx + L / 2, -Wd / 2, Wd, (0, 1, 0), (1, 0, 0))):
        if d == (1, 0, 0):
            for xa, xb in ((fx - L / 2 + 4, fx - 180), (fx - 120, fx + 120), (fx + 180, fx + L / 2 - 4)):
                weld("Weld, bank box frame to wall (stitch)", 22, "Evaporator bank", (xa, ay, bz0 + fa), d, xb - xa, 3, u, (0, 0, 1))
        else:
            spans = ((-Wd / 2 + 4, -90), (-50, 50), (90, Wd / 2 - 4))
            if ax > fx:     # the +X wall: keep clear of the tail slot and its cover
                spans = ((-Wd / 2 + 4, p["bk_y0"] - 40), (p["bk_y0"] + 40, 50), (90, Wd / 2 - 4))
            for ya, yb in spans:
                weld("Weld, bank box frame to wall (stitch)", 22, "Evaporator bank", (ax, ya, bz0 + fa), d, yb - ya, 3, u, (0, 0, 1))
    blin = bx(fx - L / 2 + bt_, fx + L / 2 - bt_, -Wd / 2 + bt_, Wd / 2 - bt_, bz0, btop - bt_) - bx(fx - L / 2 + bt_ + blt, fx + L / 2 - bt_ - blt, -Wd / 2 + bt_ + blt, Wd / 2 - bt_ - blt, bz0 - 1, btop - bt_ - blt)
    blin -= zcyl(fx, yi, btop - bt_ - blt - 1, p["chimney_d"] / 2, blt + 2)
    blin -= slot
    add("bk_lining", "Bank box lining", [("Bank box lining, 25 mm ceramic fibre", blin, "insulated_white")], 22, "bought", "Evaporator bank")
    add("bk_bank", "Evaporator bank tube", [("Evaporator bank, 316 stainless 15.88 x 1.24 serpentine", _tube_along(bpts, bod, p["bk_tube_wall"]), "stainless")],
        22, "made", "Evaporator bank")
    iy0, iy1 = -Wd / 2 + bt_ + blt, Wd / 2 - bt_ - blt
    ix0, ix1 = fx - L / 2 + bt_ + blt, fx + L / 2 - bt_ - blt
    zb_lo = bz0 + p["bk_baffle_z"] - p["bk_baffle_t"] / 2
    zb_hi = bz0 + p["bk_baffle_z"] + p["bk_baffle_t"] / 2
    sups = []
    for k, dx in enumerate((-150, 150)):
        sups.append((f"Bank support bar {k + 1}, 6 mm flat", bx(fx + dx - 3, fx + dx + 3, iy0, iy1, bz0, D["bk_zb"] - br)))       # on the roof plate
        sups.append((f"Bank spacer, lower {k + 1}, 6 mm flat", bx(fx + dx - 3, fx + dx + 3, iy0, iy1, D["bk_zb"] + br, zb_lo)))  # under the baffle
        sups.append((f"Bank spacer, upper {k + 1}, 6 mm flat", bx(fx + dx - 3, fx + dx + 3, iy0, iy1, zb_hi, D["bk_zt"] - br)))  # over the baffle
    add("bk_sups", "Bank support bars (2) and spacers (4)", sups, 22, "made", "Evaporator bank")
    import cad_parts as _cp
    baffle = b.Pos((ix0 + ix1) / 2, (iy0 + 1 + iy1 - p["bk_baffle_gap"]) / 2, zb_lo) * _cp.sheet(ix1 - ix0 - 2, iy1 - p["bk_baffle_gap"] - iy0 - 1, p["bk_baffle_t"], r_corner=5)
    add("bk_baffle", "Bank gas-pass baffle", [("Bank gas-pass baffle, 1.5 mm 304 stainless", baffle, "stainless")], 22, "made", "Evaporator bank")
    # cover: a 3 mm plate on the wall above the frame, cranked out over the frame leg below
    cov = bx(xw, xw + 3, p["bk_y0"] - 30, p["bk_y0"] + 30, bz0 + fa, D["bk_zt"] + 30)
    cov += bx(xw + ft, xw + ft + 3, p["bk_y0"] - 30, p["bk_y0"] + 30, bz0 + ft, bz0 + fa + 8)
    for z_ in (D["bk_zb"], D["bk_zt"]):
        cov -= xcyl(xw - 1, p["bk_y0"], z_, br + 0.3, 5)
    add("bk_cover", "Bank tail slot cover", [("Bank tail slot cover, 3 mm", cov)], 22, "made", "Evaporator bank")
    covfix = sp.Fix()
    covfix += sp.screw(5, ft + 3 + bt_ - 0.5, (xw + ft + 3, p["bk_y0"] + 20, bz0 + 14), "-x")
    covfix += sp.screw(5, 3 + bt_ - 0.5, (xw + 3, p["bk_y0"] + 20, D["bk_zt"] + 20), "-x")
    add("bk_cover_screws", "M5 cover screws (2)", covfix, 21, "fixing", None)
    # unions on the two tails (5/8 to 1/2 in reducing), the economizer to bank link, and the jumper to the coil
    ux0 = bpts[0][0]
    unions = [hexprism("x", ux0, p["bk_y0"], z_, 30, 25) for z_ in (D["bk_zt"], D["bk_zb"])]
    ux1 = ux0 + 25
    lx = fx + L / 2 + 70
    link = _tube_along([(p["fb_x"] + p["eco_l"] / 2 + 20, e_out[1], e_out[2]), (lx, e_out[1], e_out[2]), (lx, e_out[1], D["bk_zt"]),
                        (ux1, e_out[1], D["bk_zt"])], p["eco_tube_od"], p["eco_tube_wall"])
    add("bk_link", "Economizer to bank link and unions", [("Economizer to bank link, 316 stainless 12.7 mm", link, "stainless"),
        ("Bank inlet reducing union, 5/8 to 1/2 in", unions[0], "stainless"), ("Bank outlet reducing union, 5/8 to 1/2 in", unions[1], "stainless")],
        19, "bought", "Feed lines")

    # 19 coil inlet jumper (12.7 mm stainless) from the coil inlet reducer up to the bank outlet union
    jx = x_out + 50
    red_u = hexprism("x", x_out + 10, 0, D["cz0"], 36, 25)
    red_r = xcyl(x_out + 35, 0, D["cz0"], 12.0, 15)
    jumper = _tube_along([(jx, 0, D["cz0"]), (jx, p["bk_y0"], D["cz0"]), (jx, p["bk_y0"], D["bk_zb"]),
                          (ux1, p["bk_y0"], D["bk_zb"])], p["eco_tube_od"], p["eco_tube_wall"]) - red_r
    add("jumper", "Coil inlet jumper and reducer", [("Coil inlet union, 25.4 mm compression", red_u, "stainless"),
        ("Coil inlet reducer, 25.4 to 12.7 mm", red_r, "stainless"), ("Coil inlet jumper, 316 stainless 12.7 mm", jumper, "stainless")],
        19, "bought", "Feed lines")

    # 7 economizer: 2 mm steel box with a bolting flange on the bank box, bolted lid with the chimney spigot
    #   at the +Y side, the stainless serpentine inside on two support bars, two gas-pass baffles on ledges
    #   (STR-DEC-001 S1) and a condensate drain
    el, ew, eh = p["eco_l"], p["eco_w"], p["eco_h"]
    ef = p["eco_flange"]
    yo = p["flue_y_out"]
    ez0, ezf, ezt = D["eco_z0"], D["eco_floor"], D["eco_top"]
    ebox = bx(fx - el / 2 - ef, fx + el / 2 + ef, -ew / 2 - ef, ew / 2 + ef, ez0, ezf)              # flange plate
    ebox += bx(fx - el / 2, fx + el / 2, -ew / 2, ew / 2, ezf, ezt) - bx(fx - el / 2 + 2, fx + el / 2 - 2, -ew / 2 + 2, ew / 2 - 2, ezf - 1, ezt + 1)
    ebox += bx(fx - el / 2 - 25, fx + el / 2 + 25, -ew / 2 - 25, ew / 2 + 25, ezt - 3, ezt) - bx(fx - el / 2 + 2, fx + el / 2 - 2, -ew / 2 + 2, ew / 2 - 2, ezt - 4, ezt + 1)
    ebox -= zcyl(fx, yi, ez0 - 1, p["chimney_d"] / 2, 8)
    for (x_, y_, z_) in (e_in, e_out):
        ebox -= xcyl(fx - el / 2 - 1 if x_ < fx else fx + el / 2 - 3, y_, z_, p["eco_tube_od"] / 2 + 0.3, 5)
    drain_z = ezf + 14
    ebox -= xcyl(fx - el / 2 - 1, 150, drain_z, 6, 5)
    drain = xcyl(fx - el / 2 - 50, 150, drain_z, 10, 50) - xcyl(fx - el / 2 - 51, 150, drain_z, 6, 52)
    bars = [bx(fx + dx - 1.5, fx + dx + 1.5, -ew / 2 + 2, ew / 2 - 2, e_out[2] - p["eco_tube_od"] / 2 - 25, e_out[2] - p["eco_tube_od"] / 2)
            for dx in (-120, 120)]
    et_ = p["eco_baffle_t"]
    gap_e = p["eco_baffle_gap"]
    ey0, ey1 = -ew / 2 + 2, ew / 2 - 2
    ex0, ex1 = fx - el / 2 + 2, fx + el / 2 - 2
    eb, ledges = [], []
    for i, zr in enumerate(p["eco_baffle_z"]):
        zlo = ezf + zr - et_ / 2
        ya, yb = (ey0 + 1, ey1 - gap_e) if i == 0 else (ey0 + gap_e, ey1 - 1)
        # the bank is one bent serpentine: both baffles slide in between its layers on the bench and go into the box
        # with it, so the lower baffle is 11 mm shorter at each end to pass the narrow upper ledges, and lands on
        # wide lower ledges that also close its end gaps
        bl = ex1 - ex0 - (22 if i == 0 else 2)
        lw = 25.0 if i == 0 else 10.0
        eb.append((f"Economizer gas-pass baffle {i + 1}, 1 mm 316L stainless", b.Pos((ex0 + ex1) / 2, (ya + yb) / 2, zlo) * cpk.sheet(bl, yb - ya, et_, r_corner=5), "stainless"))
        for side, xe in ((-1, ex0), (1, ex1)):
            xl0, xl1 = (xe, xe + lw) if side < 0 else (xe - lw, xe)
            ledges.append((f"Economizer baffle ledge {i + 1}{'L' if side < 0 else 'R'}, {lw:.0f} x 3 flat", bx(xl0, xl1, ya + 5, yb - 5, zlo - 3, zlo)))
            xr_ = xl1 if side < 0 else xl0
            weld("Weld, baffle ledge to economizer wall", 7, "Flue-gas economizer", (xe, ya + 8, zlo - 3), (0, 1, 0), yb - ya - 16, 2.5,
                 (0, 0, -1), (-side, 0, 0))
    add("eco_box", "Economizer box", [("Economizer box, 2 mm steel with bolting flange, welded", ebox),
        ("Economizer tube support bar, left", bars[0]), ("Economizer tube support bar, right", bars[1]),
        ("Economizer condensate drain nipple", drain, "stainless")] + ledges + eb, 7, "made", "Flue-gas economizer")
    lid = bx(fx - el / 2 - 25, fx + el / 2 + 25, -ew / 2 - 25, ew / 2 + 25, ezt, ezt + 2) - zcyl(fx, yo, ezt - 1, p["chimney_d"] / 2 - 1, 4)
    spig = zcyl(fx, yo, ezt, p["chimney_d"] / 2 - 1, p["spigot_h"] + 2) - zcyl(fx, yo, ezt - 1, p["chimney_d"] / 2 - 2.5, p["spigot_h"] + 4)
    add("eco_lid", "Economizer lid and spigot", [("Economizer lid, 2 mm", lid), ("Chimney spigot, through the lid", spig, "stainless")],
        7, "made", "Flue-gas economizer")
    ring("Weld, spigot to lid (underside)", 7, "Flue-gas economizer", (fx, yo, ezt), "-z", p["chimney_d"] / 2 - 1, 3)
    bank_pts = [(fx - el / 2 - 20, e_in[1], e_in[2])] + eco_bank_points(p) + [(fx + el / 2 + 20, e_out[1], e_out[2])]
    add("eco_bank", "Economizer tube bank", [("Economizer tube bank, 316 stainless 12.7 x 1.2 serpentine", _tube_along(bank_pts, p["eco_tube_od"], p["eco_tube_wall"]), "stainless")],
        7, "made", "Flue-gas economizer")
    efix = sp.Fix()
    for i in range(4):
        xb = fx - el / 2 - ef / 2 + i * (el + ef) / 3
        for yb in (-ew / 2 - ef / 2, ew / 2 + ef / 2):
            efix += sp.stud(8, (xb, yb, ez0), "+z", ezf - ez0)
    for yb in (-ew / 2 / 3, ew / 2 / 3):
        for xb in (fx - el / 2 - ef / 2, fx + el / 2 + ef / 2):
            efix += sp.stud(8, (xb, yb, ez0), "+z", ezf - ez0)
    add("eco_bolts", "M8 economizer flange studs and nuts (12)", efix, 21, "fixing", None)
    lfix = sp.Fix()
    for i in range(4):
        xb = fx - el / 2 - 12 + i * (el + 24) / 3
        for yb in (-ew / 2 - 12, ew / 2 + 12):
            lfix += sp.bolt(6, 5, (xb, yb, ezt + 2), "-z")
    add("lid_bolts", "M6 lid bolts (8)", lfix, 21, "fixing", None)

    # 8 chimney (150 mm single-wall stainless) over the spigot at the +Y side, spark arrestor cap on top
    ch0 = ezt + 2
    cap0 = p["chimney_top"] - p["cap_h"]
    ri = p["chimney_d"] / 2 - 1                   # chimney bore = spigot outside diameter, a slide fit
    chim = zcyl(fx, yo, ch0, ri + 0.8, cap0 + 50 - ch0) - zcyl(fx, yo, ch0 - 1, ri, cap0 + 52 - ch0)
    capc = zcyl(fx, yo, cap0, ri + 4.0, 50) - zcyl(fx, yo, cap0 - 1, ri + 0.8, 52)
    capm = zcyl(fx, yo, cap0 + 50, p["chimney_d"] / 2 + 45, p["cap_h"] - 50) - zcyl(fx, yo, cap0 + 49, p["chimney_d"] / 2 + 42, p["cap_h"] - 52)
    add("chimney", "Chimney", [("Chimney, 150 mm single-wall stainless", chim, "stainless")], 8, "bought", "Chimney and spark arrestor")
    add("cap", "Spark arrestor cap", [("Spark arrestor cap collar", capc, "stainless"), ("Spark arrestor cage, 6 mm mesh, with rain cap", capm, "stainless")],
        8, "bought", "Chimney and spark arrestor")

    # 17 header post (50 mm square tube on a foot plate) and 9 header with its connections
    po = p["post"]
    fpw, fpt = p["foot"]
    pfoot = bx(hx - 75, hx + 75, -75, 75, T, T + fpt)
    ptube = rhs_z(hx, 0, T + fpt, hz - p["header_od"] / 2 - 6, po, 3)
    psad = bx(hx - 40, hx + 40, -30, 30, hz - p["header_od"] / 2 - 6, hz - p["header_od"] / 2)
    add("post", "Header post", [("Header post foot plate, 150 x 150 x 10", pfoot), ("Header post, 50 x 50 x 3 SHS", ptube),
                                ("Header saddle plate, 80 x 60 x 6", psad)], 17, "made", "Steam header and water-seal vent")
    around("Weld, header post to foot plate", 17, "Steam header and water-seal vent", hx - po / 2, hx + po / 2, -po / 2, po / 2, T + fpt, 4)
    around("Weld, header post to saddle plate", 17, "Steam header and water-seal vent", hx - po / 2, hx + po / 2, -po / 2, po / 2,
           hz - p["header_od"] / 2 - 6, 2.5, up=False)
    pfix = sp.Fix()
    for dx in (-50, 50):
        for dy in (-50, 50):
            pfix += sp.bolt(10, fpt + 10, (hx + dx, dy, T + fpt), "-z")
    for k, dy in enumerate((-20, 20)):                       # U-bolt over the header through the saddle plate, two nuts
        ub = b.Pos(hx, dy, hz) * b.Rot(90, 0, 0) * (b.Cylinder(p["header_od"] / 2 + 6, 8) - b.Cylinder(p["header_od"] / 2, 9)) & bx(hx - 50, hx + 50, dy - 5, dy + 5, hz, hz + 50)
        for sx_ in (-1, 1):
            ub = ub + zcyl(hx + sx_ * (p["header_od"] / 2 + 3), dy, hz - p["header_od"] / 2 - 16, 3, p["header_od"] / 2 + 16)
        pfix.append((f"M6 U-bolt for 60 mm pipe {k + 1}, zinc plated", ub))
        for sx_ in (-1, 1):
            xx = hx + sx_ * (p["header_od"] / 2 + 3)
            zs_ = hz - p["header_od"] / 2 - 6
            pfix.append(("M6 washer (ISO 7089)", b.Pos(xx, dy, zs_) * b.Rot(180, 0, 0) * cpk.washer(6)))
            pfix.append(("M6 hex nut (ISO 4032)", b.Pos(xx, dy, zs_ - 1.6) * b.Rot(180, 0, 0) * cpk.hex_nut(6)))
            pfix.holes.append(zcyl(xx, dy, zs_ - 1, 3.3, 8))
    add("post_bolts", "M10 post bolts and header U-bolts", pfix, 21, "fixing", None)

    hl_ = p["header_len"]
    header = ycyl(hx, -hl_ / 2, hz, p["header_od"] / 2, hl_) - ycyl(hx, -hl_ / 2 - 1, hz, p["header_od"] / 2 - 3.9, hl_ + 2)
    header += ycyl(hx, -hl_ / 2, hz, p["header_od"] / 2, 4) + ycyl(hx, hl_ / 2 - 4, hz, p["header_od"] / 2, 4)    # welded end caps
    gauge = zcyl(hx, -70, hz, 7, p["header_od"] / 2 + 60) + ycyl(hx, -70 - 25, hz + p["header_od"] / 2 + 90, 25, 20)
    gauge += zcyl(hx, -70, hz + p["header_od"] / 2 + 55, 8, 15)
    header -= zcyl(hx, -70, hz, 7, p["header_od"])                           # tapped boss hole for the gauge siphon
    add("header", "Steam header and gauge", [("Steam header, DN50 stainless pipe with end caps", header, "stainless"),
                                             ("Steam gauge, 0 to 1 bar, with siphon", gauge, "brass")], 9, "made", "Steam header and water-seal vent")

    # 9 water-seal pot on its foot plate: dip leg inside, vent pipe from the top, link from the header
    py = D["pot_y"]
    pr = p["seal_pot_od"] / 2
    pot = zcyl(hx, py, D["pot_bot"], pr, D["pot_top"] - D["pot_bot"]) - zcyl(hx, py, D["pot_bot"] + 6, pr - 3.05, D["pot_top"] - D["pot_bot"] - 12)
    pfp = bx(hx - fpw / 2, hx + fpw / 2, py - fpw / 2, py + fpw / 2, T, T + fpt)
    dip_y = py + (pr - 3.05 - p["dip_od"] / 2 - 1)
    dip = zcyl(hx, dip_y, D["dip_end"], p["dip_od"] / 2, hz - D["dip_end"]) - zcyl(hx, dip_y, D["dip_end"] - 1, p["dip_od"] / 2 - 3.56, hz - D["dip_end"] - 20)
    plink = ycyl(hx, dip_y, hz, p["dip_od"] / 2, -hl_ / 2 - dip_y)
    dip = dip + plink                                                    # dip leg and header link: one welded pipe
    pot -= ycyl(hx, dip_y, hz, p["dip_od"] / 2, -hl_ / 2 - dip_y)         # the link passes out through the pot wall
    pot -= zcyl(hx, py, D["pot_top"] - 7, p["vent_od"] / 2 - 3.56, 8)     # vent opening in the top cap
    vent = zcyl(hx, py, D["pot_top"], p["vent_od"] / 2, p["vent_top"] - D["pot_top"]) - zcyl(hx, py, D["pot_top"] - 1, p["vent_od"] / 2 - 3.56, p["vent_top"] - D["pot_top"] + 2)
    ys_ = py - pr - 12                                                   # level sight tube on the operator side
    sight = zcyl(hx, ys_, D["dip_end"] + 50, 6, D["water_line"] + D["rise"] - D["dip_end"]) \
        + ycyl(hx, ys_, D["dip_end"] + 65, 5, 12) + ycyl(hx, ys_, D["water_line"] + D["rise"] + 35, 5, 12)
    drainv = xcyl(hx + pr, py, D["pot_bot"] + 40, 10, 50)
    add("pot", "Water-seal pot, dip leg and vent", [("Water-seal pot, 114.3 mm pipe with caps", pot), ("Seal pot foot plate, 200 x 200 x 10", pfp),
        ("Dip leg with header link, 42.2 mm stainless pipe", dip, "stainless"),
        ("Vent pipe, DN32, to 2.3 m", vent, "galvanised"), ("Seal pot level sight tube", sight, "polycarbonate"),
        ("Seal pot drain valve", drainv, "brass")], 9, "made", "Steam header and water-seal vent")
    ring("Weld, seal pot to foot plate", 9, "Steam header and water-seal vent", (hx, py, T + fpt), "+z", pr, 5)
    potfix = sp.Fix()
    for dx in (-80, 80):
        for dy in (-80, 80):
            potfix += sp.bolt(10, fpt + 10, (hx + dx, py + dy, T + fpt), "-z")
    add("pot_bolts", "M10 pot foot bolts (4)", potfix, 21, "fixing", None)
    # stay from the post to the pot, a clamp band round the pot
    zs = T + 600
    sbar = bx(hx - 20, hx + 20, py + pr + 3, -po / 2, zs - 3, zs + 3)
    sband = zcyl(hx, py, zs - 20, pr + 3, 40) - zcyl(hx, py, zs - 21, pr, 42)
    add("stay", "Pot stay and clamp band", [("Pot stay, 40 x 6 flat", sbar), ("Pot clamp band", sband)], 17, "made", "Steam header and water-seal vent")
    for zz, vv in ((zs + 3, 1), (zs - 3, -1)):
        weld("Weld, pot stay to post", 17, "Steam header and water-seal vent", (hx - 17, -po / 2, zz), (1, 0, 0), 34, 3, (0, 0, vv), (0, -1, 0))

    # 9 seal pot overflow (decided 2026-10-02): 3/4 in pipe from a half coupling at the static water mark,
    #   a 350 mm loop seal so vent back pressure cannot blow steam out of it, then across to the trailer
    #   centreline behind the deck and down to 80 mm above the ground, away from the operator's side
    oz = D["ovf_z"]
    od_ = p["ovf_od"]
    x1o = hx + pr + 60
    crown = oz - 100
    ubot = crown - p["ovf_trap"]
    xo = p["ovf_x"]
    ovf = _tube_along([(hx + pr, py, oz), (x1o, py, oz), (x1o, py, ubot), (x1o + 70, py, ubot), (x1o + 70, py, crown),
                       (xo, py, crown), (xo, 0, crown), (xo, 0, p["ovf_end_z"])], od_, 2.87)
    plug_ = zcyl(x1o + 35, py, ubot - od_ / 2 - 12, 9, 12)                        # trap drain plug under the U
    add("overflow", "Seal pot overflow with loop seal", [("Seal pot overflow, 3/4 in galvanized pipe with loop seal", ovf, "galvanised"),
                                                         ("Loop seal drain plug, 3/4 in", plug_, "brass")], 9, "bought", "Steam header and water-seal vent")
    tstay = bx(hx + pr + 3, x1o - od_ / 2, py - 20, py + 20, zs - 3, zs + 3)       # from the pot clamp band to the down-leg
    add("ovf_stay", "Overflow trap stay", [("Overflow trap stay, 40 x 6 flat", tstay)], 17, "made", "Steam header and water-seal vent")
    x_end = p["deck_l"] / 2
    zc_ = p["deck_z"] + p["deck_t"] / 2
    clip = bx(x_end, x_end + 6, -40, 40, zc_ - 30, zc_ + 30)                       # foot plate on the rear rail end
    clip += bx(x_end + 6, xo - od_ / 2 - 3, -15, 15, zc_ - 3, zc_ + 3)              # arm
    clip += zcyl(xo, 0, zc_ - 20, od_ / 2 + 3, 40) - zcyl(xo, 0, zc_ - 21, od_ / 2, 42)   # clamp band
    add("ovf_clip", "Overflow rear clip", [("Overflow rear clip, welded", clip)], 17, "made", "Steam header and water-seal vent")
    ofix = sp.Fix()
    for dy in (-25, 25):
        ofix += sp.bolt(8, p["rail_w"] + 6, (x_end - p["rail_w"], dy, zc_), "+x")
    add("ovf_bolts", "M8 overflow clip bolts (2)", ofix, 21, "fixing", None)

    # 9 diverter at the +Y end of the header: hose coupling to +X, vent line up and over to the vent
    dy_ = D["div_y"]
    nip = ycyl(hx, hl_ / 2, hz, 13.35, 15)
    div = box(hx, dy_, hz, 70, 90, 70) + nip
    div += zcyl(hx, dy_, hz + 35, 6, 40) + bx(hx - 6, hx + 90, dy_ - 6, dy_ + 6, hz + 75, hz + 85)      # lever
    coupling = xcyl(hx + 35, dy_, hz, 22, 40)
    add("diverter", "Three-way diverter and hose coupling", [("Three-way diverter valve, no closed position", div, "brass"),
                                                             ("Steam hose quick coupling", coupling, "brass")], 9, "bought", "Steam header and water-seal vent")
    vz = D["vent_line_z"]
    vline = _tube_along([(hx, dy_ + 45, hz), (hx, dy_ + 75, hz), (hx, dy_ + 75, vz), (hx, py + p["vent_od"] / 2, vz)], 33.4, 3.38)
    add("vent_line", "Diverter vent line", [("Diverter vent line, 1 in steel pipe", vline, "galvanised")], 20, "bought", "Steam header and water-seal vent")

    # 10 relief valve on the header top, discharge pipe to 2.3 m, stay to the vent pipe
    rvy = 60.0
    rv0 = hz + p["header_od"] / 2
    relief = zcyl(hx, rvy, rv0, 13.35, 20) + zcyl(hx, rvy, rv0 + 20, p["relief_d"] / 2, 100) + zcyl(hx, rvy, rv0 + 120, 20, 60)
    relief += bx(hx + 30, hx + 60, rvy - 4, rvy + 4, rv0 + 150, rv0 + 158)                             # test lever
    dis_x = hx + 80
    disch = _tube_along([(hx + p["relief_d"] / 2, rvy, rv0 + 70), (dis_x, rvy, rv0 + 70), (dis_x, rvy, p["vent_top"])], 26.7, 2.87)
    zst = p["vent_top"] - 100
    ux, uy = hx - dis_x, py - rvy
    un = math.hypot(ux, uy)
    ux, uy = ux / un, uy / un
    dstay = _tube_along([(dis_x, rvy, zst), (hx - ux * p["vent_od"] / 2, py - uy * p["vent_od"] / 2, zst)], 12.0)
    dstay = dstay - zcyl(dis_x, rvy, zst - 20, 26.7 / 2, 40)                 # welded to the side of the discharge pipe
    add("relief", "Certified relief valve", [("Certified steam safety valve, 3/4 in, 15 psi", relief, "brass")], 10, "bought", "Certified relief valve")
    add("discharge", "Relief discharge pipe and stay", [("Relief discharge pipe, 3/4 in, to 2.3 m", disch, "galvanised"),
                                                        ("Discharge stay, 12 mm round bar", dstay)], 20, "bought", "Certified relief valve")

    # 11 steam hose, diverter coupling to the first hood (routing is indicative; the hose is flexible)
    hcx = D["hood_inlet_x"][0]
    hood_top_cpl = p["hood_h"] + 3 + 80
    c0 = hx + 75
    hose = _tube_along([(c0, dy_, hz), (c0 + 200, dy_, hz), (c0 + 330, dy_, hz - 250), (c0 + 330, dy_, 650),
                        (hcx, 0, 650), (hcx, 0, hood_top_cpl)], p["hose_od"], 9.5)
    add("hose", "Steam hose", [("Steam hose, EPDM 25 mm bore, 6 m", hose, "epdm")], 11, "bought", "Steam hose")

    # 12 steam hoods: double-skin insulated shell, galvanised skirt, perforated manifold, handles for ballast
    hood_parts(p, D, add, weld, around)

    # 3 feed tank on two saddles with two ratchet straps
    tx, tr, tl = p["tank_x"], p["tank_r"], p["tank_l"]
    tz = D["tank_z"]
    tank = ycyl(tx, -tl / 2, tz, tr, tl) - ycyl(tx, -tl / 2 + 5, tz, tr - 5, tl - 10)
    tank += ycyl(tx, tl / 2, tz - tr + 60, 15, 40)                           # outlet bulkhead and strainer
    tank += zcyl(tx + 120, 0, tz + tr - 20, 40, 40)                          # filler cap
    add("tank", "Feed water drum", [("Feed water drum, 125 L HDPE", tank, "hdpe_natural")], 3, "bought", "Feed water tank, 125 L")
    sl, swd, sht = p["saddle"]
    sad = []
    sfix = sp.Fix()
    for k, sy_ in enumerate((-p["saddle_y"], p["saddle_y"])):
        sd = bx(tx - sl / 2, tx + sl / 2, sy_ - swd / 2, sy_ + swd / 2, T, T + sht) - ycyl(tx, sy_ - swd, tz, tr, 2 * swd)
        for dx in (-sl / 2 + 25, sl / 2 - 25):
            sd -= zcyl(tx + dx, sy_, T + 30, 13, sht)                            # counterbore for the bolt head
            sfix += sp.bolt(10, 40, (tx + dx, sy_, T + 30), "-z")
        sad.append((f"Drum saddle {k + 1}, hardwood, two layers", sd, "hardwood"))
    add("saddles", "Drum saddles (2)", sad, 17, "made", "Feed water tank, 125 L")
    straps = []
    for k, sy_ in enumerate((-p["saddle_y"] - 70, p["saddle_y"] + 70)):
        ring_ = ycyl(tx, sy_ - 12.5, tz, tr + 2, 25) - ycyl(tx, sy_ - 13, tz, tr, 26)
        ring_ = ring_ & bx(tx - tr - 5, tx + tr + 5, sy_ - 15, sy_ + 15, tz, tz + tr + 5)
        for sx_ in (-1, 1):
            ring_ += bx(tx + sx_ * (tr + 1) - 1, tx + sx_ * (tr + 1) + 1, sy_ - 12.5, sy_ + 12.5, T + 10, tz)
        straps.append((f"Ratchet strap {k + 1}, 25 mm", ring_, "canvas"))
        for sx_ in (-1, 1):
            straps.append(("Deck lashing point", bx(tx + sx_ * (tr + 1) - 15, tx + sx_ * (tr + 1) + 15, sy_ - 20, sy_ + 20, T, T + 10), "zinc_plated"))
    add("straps", "Ratchet straps (2)", straps, 21, "bought", "Feed water tank, 125 L")
    add("saddle_bolts", "M10 saddle bolts (4)", sfix, 21, "fixing", None)

    # 4, 13, 16 pump and alarm box (pump, needle valve, flow meter, battery, alarm controller)
    bx0, bx1, by0, by1, bh = p["pbox"]
    pbox = bx(bx0, bx1, by0, by1, T, T + bh)
    ind = zcyl(bx0 + 40, by1 - 40, T + bh, 8, 10) + zcyl(bx0 + 80, by1 - 40, T + bh, 8, 10)
    add("pbox", "Pump and alarm box", [("Pump and alarm enclosure, IP65", pbox, "matte_black"), ("Alarm indicator lamps", ind, "safety_red")],
        4, "bought", "Feed pump")

    # 19 feed lines: suction hose from the drum, 12.7 mm stainless line to the economizer inlet with two clips
    suction = _tube_along([(tx, tl / 2 + 40, tz - tr + 60), (tx, (by0 + by1) / 2, tz - tr + 60), (bx0, (by0 + by1) / 2, tz - tr + 60)], 16.0)
    xf = D["fb_x0"] - 40
    yfl = (by0 + by1) / 2
    feed = _tube_along([((bx0 + bx1) / 2, yfl, T + bh), ((bx0 + bx1) / 2, yfl, T + bh + 80), (xf, yfl, T + bh + 80),
                        (xf, e_in[1], T + bh + 80), (xf, e_in[1], e_in[2]), (fx - el / 2 - 20, e_in[1], e_in[2])], p["eco_tube_od"], p["eco_tube_wall"])
    clips = []
    for k, zc2 in enumerate((D["fb_z0"] + 400, D["fb_z0"] + 850)):
        clips.append((f"Feed line clip {k + 1}", bx(xf + p["eco_tube_od"] / 2, D["fb_x0"], e_in[1] - 10, e_in[1] + 10, zc2 - 10, zc2 + 10)))
    add("feed", "Feed lines", [("Suction hose, 16 mm reinforced", suction, "epdm"), ("Feed line, 316 stainless 12.7 mm", feed, "stainless")],
        19, "bought", "Feed lines")
    add("clips", "Feed line clips (2)", clips, 19, "made", "Feed lines")

    # drill the clearance holes: each part loses the holes of the fixings that pass through it
    for k_, f_ in (("skids", "skid_bolts"), ("trailer", "skid_bolts"), ("shell", "roof_bolts"), ("roof", "roof_bolts"), ("bk_box", "roof_bolts"),
                   ("eco_box", "eco_bolts"), ("bk_box", "bk_cover_screws"), ("bk_cover", "bk_cover_screws"),
                   ("eco_box", "lid_bolts"), ("eco_lid", "lid_bolts"), ("post", "post_bolts"), ("trailer", "post_bolts"),
                   ("trailer", "ovf_bolts"), ("ovf_clip", "ovf_bolts"), ("pot", "pot_bolts"), ("trailer", "pot_bolts"),
                   ("glands", "gland_studs"), ("saddles", "saddle_bolts"), ("trailer", "saddle_bolts")) + tuple(
                       (f"handles{n}", f"hood_bolts{n}") for n in range(1, int(p["n_hoods"]) + 1)) + tuple(
                       (f"hood{n}", f"hood_bolts{n}") for n in range(1, int(p["n_hoods"]) + 1)):
        drill(C, k_, f_)
    C["welds"] = Comp("Weld beads", b.Compound(children=[w[1] for w in W]), None, "weld", None, [(w[0], w[1], "mild_steel", w[2], w[3]) for w in W], [])
    return C


def drill(C, key, fix_key):
    """Subtract the holes of C[fix_key] from every piece of C[key] whose bounding box they touch."""
    b = _b3d()
    holes = C[fix_key].holes
    if not holes:
        return
    hb = [(h, h.bounding_box()) for h in holes]
    out = []
    for q in C[key].pieces:
        shp = q[1]
        bb = shp.bounding_box()
        for h, hbb in hb:
            if not (hbb.max.X < bb.min.X or bb.max.X < hbb.min.X or hbb.max.Y < bb.min.Y or bb.max.Y < hbb.min.Y
                    or hbb.max.Z < bb.min.Z or bb.max.Z < hbb.min.Z):
                shp = shp - h
        out.append((q[0], shp) + tuple(q[2:]))
    c = C[key]
    C[key] = c._replace(pieces=out, shape=b.Compound(children=[q[1] for q in out]))


def hood_parts(p, D, add, weld, around, cx_list=None, tag=""):
    """Steam hoods (BOM 12): shell, galvanised skirt, perforated manifold with its inlet, and handles of
    30 x 30 x 2.5 SHS on SHS standoffs welded to 100 x 100 x 3 foot plates, each through-bolted with two M6
    bolts to a backing plate inside the hood wall (handles sized for 40 kg of ballast, decided 2026-10-02)."""
    import str_parts as sp
    hl, hw, hh, ins = p["hood_l"], p["hood_w"], p["hood_h"], p["hood_ins_t"]
    cxs = cx_list or D["hood_cx"]
    for i, cx in enumerate(cxs):
        n = i + 1
        ix = cx - hl / 2 + 150
        sk_ = p["hood_skin_t"]
        outer = box(cx, 0, hh / 2, hl, hw, hh)
        o_in = box(cx, 0, (hh - sk_) / 2 - 0.5, hl - 2 * sk_, hw - 2 * sk_, hh - sk_ + 1)
        w_in = box(cx, 0, (hh - ins + sk_) / 2 - 0.5, hl - 2 * ins + 2 * sk_, hw - 2 * ins + 2 * sk_, hh - ins + sk_ + 1)
        i_in = box(cx, 0, (hh - ins) / 2 - 0.5, hl - 2 * ins, hw - 2 * ins, hh - ins + 1)
        hole = zcyl(ix, 0, hh - ins - 1, 15.3, ins + 2)
        # hardwood blocks glued inside the outer pan under each handle foot plate and at the inlet, with a 3 mm
        # aluminium backing plate between each handle block and the inner pan (STR-BLD-001, section 3.20)
        hfp_ = p["handle_foot"][0]
        blocks = []
        for sy_ in (1, -1):
            for sx_ in (-400, 400):
                y0b, y1b = sorted((sy_ * (hw / 2 - sk_), sy_ * (hw / 2 - ins + sk_ + 3)))
                blocks.append(bx(cx + sx_ - hfp_ / 2, cx + sx_ + hfp_ / 2, y0b, y1b, hh - 60 - hfp_ / 2, hh - 60 + hfp_ / 2))
        blocks.append(bx(ix - 50, ix + 50, -50, 50, hh - ins + sk_, hh - sk_) - hole)
        wool = o_in - w_in - hole
        for blk in blocks:
            wool = wool - blk
        for sy_ in (1, -1):              # pockets for the backing plates behind the handle blocks
            for sx_ in (-400, 400):
                y0b, y1b = sorted((sy_ * (hw / 2 - ins + sk_), sy_ * (hw / 2 - ins + sk_ + 3)))
                wool = wool - bx(cx + sx_ - hfp_ / 2, cx + sx_ + hfp_ / 2, y0b, y1b, hh - 60 - hfp_ / 2, hh - 60 + hfp_ / 2)
        add(f"hood{n}", f"Hood {n} shell", [(f"Hood {n} outer skin, 1 mm aluminium", outer - o_in - hole, "aluminium"),
            (f"Hood {n} insulation, 40 mm mineral wool", wool, "insulated_white"),
            (f"Hood {n} inner skin, 1 mm aluminium", w_in - i_in - hole, "aluminium")]
            + [(f"Hood {n} hardwood block {k + 1}", blk, "hardwood") for k, blk in enumerate(blocks)], 12, "made", "Steam hoods (2)")
        sk, lp, skt = p["skirt_depth"], p["skirt_lap"], p["skirt_t"]
        skirt = box(cx, 0, (lp - sk) / 2, hl + 2 * skt, hw + 2 * skt, sk + lp) - box(cx, 0, (lp - sk) / 2, hl, hw, sk + lp + 2)
        add(f"skirt{n}", f"Hood {n} skirt", [(f"Hood {n} soil skirt, 1.5 mm galvanized", skirt, "galvanised")], 12, "made", "Steam hoods (2)")
        mz = hh - ins - 15 - 15
        man = xcyl(cx - (hl - 2 * ins - 80) / 2, 0, mz, 15, hl - 2 * ins - 80) - xcyl(cx - (hl - 2 * ins - 80) / 2 - 1, 0, mz, 12.5, hl - 2 * ins - 78)
        riser = zcyl(ix, 0, mz, 15, hh - mz)
        hangs = [bx(cx + dxh - 10, cx + dxh + 10, -2, 2, mz + 14.9, hh - ins) for dxh in (-300, 300)]
        fl = zcyl(ix, 0, hh, 35, 3) - zcyl(ix, 0, hh - 1, 15, 5)
        cpl = zcyl(ix, 0, hh + 3, 20, 80)
        add(f"manifold{n}", f"Hood {n} manifold and inlet", [(f"Hood {n} perforated manifold, 30 mm stainless", man - riser, "stainless"),
            (f"Hood {n} inlet riser", riser, "stainless"), (f"Hood {n} manifold hanger strap 1", hangs[0], "stainless"),
            (f"Hood {n} manifold hanger strap 2", hangs[1], "stainless"), (f"Hood {n} inlet flange", fl, "stainless"),
            (f"Hood {n} hose coupling", cpl, "brass")], 12, "made", "Steam hoods (2)")
        hts, htt = p["handle_tube"]
        hfp, hft = p["handle_foot"]
        hd = []
        fix = sp.Fix()
        for sy_ in (1, -1):
            yb = sy_ * (hw / 2 + 60)
            hd.append((f"Hood {n} handle bar, 30 x 30 x 2.5 SHS", box(cx, yb, hh - 60, 900, hts, hts) - box(cx, yb, hh - 60, 902, hts - 2 * htt, hts - 2 * htt)))
            for sx_ in (-400, 400):
                y0_, y1_ = sorted((sy_ * (hw / 2 + hft), sy_ * (hw / 2 + 60 - hts / 2)))
                so = bx(cx + sx_ - 15, cx + sx_ + 15, y0_, y1_, hh - 75, hh - 45) - bx(cx + sx_ - 12.5, cx + sx_ + 12.5, y0_ - 1, y1_ + 1, hh - 72.5, hh - 47.5)
                hd.append((f"Hood {n} handle standoff, 30 x 30 x 2.5 SHS", so))
                f0, f1 = sorted((sy_ * hw / 2, sy_ * (hw / 2 + hft)))
                hd.append((f"Hood {n} handle foot plate, 100 x 100 x 3", bx(cx + sx_ - hfp / 2, cx + sx_ + hfp / 2, f0, f1, hh - 60 - hfp / 2, hh - 60 + hfp / 2)))
                b0, b1 = sorted((sy_ * (hw / 2 - ins + 1), sy_ * (hw / 2 - ins + 4)))       # inside the wall, on the inner pan
                hd.append((f"Hood {n} handle backing plate, 100 x 68 x 3 aluminium", bx(cx + sx_ - hfp / 2, cx + sx_ + hfp / 2, b0, b1, hh - 60 - hfp / 2, hh - ins - 2), "aluminium"))
                for dx_ in (-35, 35):
                    fix += sp.bolt(6, hft + ins, (cx + sx_ + dx_, sy_ * (hw / 2 + hft), hh - 60), "-y" if sy_ > 0 else "+y")
                yf = sy_ * (hw / 2 + hft)
                yo_ = sy_ * (hw / 2 + 60 - hts / 2)
                for xx, uu in ((cx + sx_ + 15, 1), (cx + sx_ - 15, -1)):
                    weld(f"Weld, hood {n} handle standoff to foot plate", 12, "Steam hoods (2)", (xx, yf, hh - 72), (0, 0, 1), 24, 3, (uu, 0, 0), (0, sy_, 0))
                    weld(f"Weld, hood {n} handle standoff to bar", 12, "Steam hoods (2)", (xx, yo_, hh - 72), (0, 0, 1), 24, 3, (uu, 0, 0), (0, -sy_, 0))
        add(f"handles{n}", f"Hood {n} handles", hd, 12, "made", "Steam hoods (2)")
        add(f"hood_bolts{n}", f"M6 hood {n} handle bolts (8)", fix, 21, "fixing", None)


def coil_display(p=PARAMS, per_turn=24):
    """The coil as straight pieces (per_turn a turn) in one compound, for pictures: the swept helix
    takes minutes to tessellate. Same centreline, tube size and tails as the model."""
    b = _b3d()
    D = derived(p)
    r = p["coil_mean_d"] / 2
    n = int(p["coil_turns"] * per_turn)
    pts = [helix_point(360.0 * i / per_turn, p) for i in range(n + 1)]
    kids = []
    for a_, c_ in zip(pts[:-1], pts[1:]):
        va, vc = b.Vector(*a_), b.Vector(*c_)
        d = vc - va
        kids.append(b.Plane(origin=(va + vc) * 0.5, z_dir=d.normalized()) * b.Cylinder(p["tube_od"] / 2, d.length))
        kids.append(b.Pos(*c_) * b.Sphere(p["tube_od"] / 2))
    x_out = D["fb_x1"]
    for z in (D["cz0"], D["coil_top"]):
        kids.append(xcyl(p["fb_x"] + r, 0, z, p["tube_od"] / 2, x_out + 10 - p["fb_x"] - r))
    return b.Compound(children=kids)


GROUP_ORDER = ["Trailer frame and drawbar", "Wheels", "Firebox skids", "Feed water tank, 125 L", "Feed pump", "Feed lines",
               "Firebox, fiber lined", "Monotube steam coil", "Evaporator bank", "Flue-gas economizer", "Chimney and spark arrestor",
               "Steam header and water-seal vent", "Certified relief valve", "Steam hose", "Steam hoods (2)"]


def build_parts(p=PARAMS):
    """{BOM item name: solid} for the main items, in GROUP_ORDER. Fixings are left out."""
    C = build_components(p)
    out = {}
    for g in GROUP_ORDER:
        shapes = [c.shape for c in C.values() if c.group == g]
        if shapes:
            out[g] = _b3d().Compound(children=shapes)
    return out


def build(p=PARAMS):
    """Whole assembly as one compound, fixings included."""
    from build123d import Compound
    return Compound(children=[c.shape for c in build_components(p).values()])


MAIN_PARTS = {  # file stem: component keys, for individual exports
    "steamroot-firebox": ["skids", "shell", "roof", "board", "lining", "brackets", "stand", "grate", "door", "hinges", "latch", "damper", "guides", "damper2", "guides2", "glands"],
    "steamroot-bank": ["bk_box", "bk_lining", "bk_bank", "bk_sups", "bk_cover", "bk_link"],
    "steamroot-coil": ["coil", "outlet"],
    "steamroot-header": ["post", "header", "pot", "stay", "diverter", "vent_line", "relief", "discharge", "overflow", "ovf_stay", "ovf_clip"],
    "steamroot-hood": ["hood1", "skirt1", "manifold1", "handles1"],
}


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    """Overlap volume, solid by solid (a compound whose own solids overlap, like the coil and its tails, gives a
    false result when intersected as a whole)."""
    try:
        tot = 0.0
        for sa in (a.solids() or [a]):
            s = sa & b_
            tot += s.volume if s is not None else 0.0
        return tot
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch without overlapping, or stay apart by a minimum clearance (mm).
    Returns (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect, tol=0.2):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1.0 and (gp < tol if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    chk("Wheels on the axle", S("wheels"), S("trailer"), "touch")
    chk("Skids on the deck", S("skids"), S("trailer"), "touch")
    chk("Firebox shell on the skids", S("shell"), S("skids"), "touch")
    chk("Roof on the shell frame", S("roof"), S("shell"), "touch")
    chk("Roof board under the roof", S("board"), S("roof"), "touch")
    chk("Roof board inside the wall lining", S("board"), S("lining"), "touch")
    chk("Coil clear of the roof board", S("coil"), S("board"), 20.0)
    # assembly order: the coil goes in from the top with the roof off, held 30 mm high and 66 mm toward
    # the back wall so its tail ends clear the lining, then slides forward so the tails pass out through
    # the slots, then drops 30 mm onto the brackets
    D_ = derived(p)
    shift = 10 + D_["t"] + 6
    lifted = C["coil"].shape.moved(_b3d().Location((-shift, 0, p["gland_lift"])))
    chk("Coil going in (high, held back): clear of the lining", lifted, S("lining"), 2.0)
    chk("Coil going in (high, held back): clear of the brackets", lifted, S("brackets"), 2.0)
    slid = C["coil"].shape.moved(_b3d().Location((0, 0, p["gland_lift"] - 1)))
    chk("Coil slid forward, still high: tails clear in the slots", slid, S("shell") + S("lining"), 2.0)
    chk("Coil slid forward, still high: clear of the brackets", slid, S("brackets"), 0.5)
    chk("Outlet union on the upper coil tail", S("outlet"), S("coil"), "touch")
    chk("Outlet union clear of the gland plate", S("outlet"), S("glands"), 3.0)
    chk("Gland plates clear of the roof frame", S("glands"), S("roof"), 3.0)
    chk("Lining inside the shell", S("lining"), S("shell"), "touch")
    chk("Coil brackets on the shell", S("brackets"), S("shell"), "touch")
    chk("Coil brackets through the lining slots", S("brackets"), S("lining"), 0.9)
    chk("Grate stand on the floor lining", S("stand"), S("lining"), "touch")
    chk("Grate on the grate stand", S("grate"), S("stand"), "touch")
    chk("Grate stand clear of the shell", S("stand"), S("shell"), 20.0)
    chk("Coil on its brackets", S("coil"), S("brackets"), "touch", tol=0.3)
    chk("Coil clear of the lining (7 mm round the tails in the gland holes)", S("coil"), S("lining"), 5.0)
    chk("Coil clear of the shell (through the gland holes)", S("coil"), S("shell"), 2.0)
    chk("Coil clear of the grate (fire space)", S("coil"), S("grate"), 250.0)
    chk("Coil clear of the door plug", S("coil"), S("door"), 25.0)
    chk("Gland plates on the shell", S("glands"), S("shell"), "touch")
    chk("Gland plates round the coil tails (sliding fit)", S("glands"), S("coil"), 0.25)
    chk("Door on the shell", S("door"), S("shell"), "touch")
    chk("Door plug clear of the lining", S("door"), S("lining"), 3.0)
    chk("Hinges on the door and shell", S("hinges"), S("door"), "touch")
    chk("Hinges on the shell", S("hinges"), S("shell"), "touch")
    chk("Latch on the shell and door", S("latch"), S("shell"), "touch")
    chk("Damper guides on the shell", S("guides"), S("shell"), "touch")
    chk("Damper slide in its guides", S("damper"), S("guides"), "touch")
    chk("Damper guides clear of the door", S("guides"), S("door"), 3.0)
    chk("Secondary damper guides on the door", S("guides2"), S("door"), "touch")
    chk("Secondary damper slide in its guides", S("damper2"), S("guides2"), "touch")
    chk("Secondary damper slide on the door", S("damper2"), S("door"), "touch")
    chk("Secondary damper clear of the door handle and latch", S("damper2") + S("guides2"), S("latch") + S("hinges"), 10.0)
    chk("Secondary damper clear of the shell (door swings)", S("damper2") + S("guides2"), S("shell"), 3.0)
    chk("Bank box frame on the roof", S("bk_box"), S("roof"), "touch")
    chk("Bank box clear of the roof bolts (drilled)", S("bk_box"), S("roof_bolts"), "touch")
    chk("Bank box lining inside the box", S("bk_lining"), S("bk_box"), "touch")
    chk("Bank support bars on the roof plate", S("bk_sups"), S("roof"), "touch")
    chk("Bank on its support bars", S("bk_bank"), S("bk_sups"), "touch")
    chk("Bank clear of the box lining (1 mm round the tails in the slot)", S("bk_bank"), S("bk_lining"), 0.9)
    chk("Bank tails clear in the wall slot", S("bk_bank"), S("bk_box"), 0.9)
    chk("Bank tails through the slot cover (sliding fit)", S("bk_bank"), S("bk_cover"), 0.25)
    chk("Slot cover on the bank box", S("bk_cover"), S("bk_box"), "touch")
    chk("Bank clear of the roof (gas space)", S("bk_bank"), S("roof"), 25.0)
    chk("Link and unions on the bank tails", S("bk_link"), S("bk_bank"), "touch")
    chk("Link on the economizer outlet", S("bk_link"), S("eco_bank"), "touch")
    chk("Link clear of the bank box", S("bk_link"), S("bk_box") + S("bk_cover_screws"), 5.0)
    chk("Link clear of the seal pot and vent", S("bk_link"), S("pot"), 20.0)
    chk("Link clear of the header and gauge", S("bk_link"), S("header"), 20.0)
    chk("Jumper on the bank outlet union", S("jumper"), S("bk_link"), "touch")
    chk("Jumper clear of the bank box frame", S("jumper"), S("bk_box") + S("roof_bolts"), 8.0)
    chk("Economizer flange on the bank box", S("eco_box"), S("bk_box"), "touch")
    chk("Economizer flange clear of the roof bolts", S("eco_box"), S("roof_bolts"), 3.0)
    chk("Economizer lid on the box", S("eco_lid"), S("eco_box"), "touch")
    chk("Tube bank on its support bars", S("eco_bank"), S("eco_box"), "touch")
    chk("Tube bank clear of the lid", S("eco_bank"), S("eco_lid"), 20.0)
    chk("Chimney over the spigot", S("chimney"), S("eco_lid"), "touch")
    chk("Spark arrestor cap on the chimney", S("cap"), S("chimney"), "touch")
    chk("Jumper on the coil inlet tail", S("jumper"), S("coil"), "touch")
    chk("Jumper union clear of the shell (spanner room)", S("jumper"), S("shell"), 8.0)
    chk("Jumper union clear of the gland plate", S("jumper"), S("glands") + S("gland_studs"), 3.0)
    chk("Coil outlet into the header", S("outlet"), S("header"), "touch")
    chk("Coil outlet clear of the post", S("outlet"), S("post"), 10.0)
    chk("Coil outlet clear of the jumper", S("outlet"), S("jumper"), 20.0)
    chk("Header post on the deck", S("post"), S("trailer"), "touch")
    chk("Header on the post saddle", S("header"), S("post"), "touch")
    chk("Pot foot plate on the deck", S("pot"), S("trailer"), "touch")
    chk("Pot link into the header", S("pot"), S("header"), "touch")
    chk("Pot stay on the post", S("stay"), S("post"), "touch")
    chk("Pot stay round the pot", S("stay"), S("pot"), "touch")
    chk("Diverter on the header", S("diverter"), S("header"), "touch")
    chk("Vent line from the diverter", S("vent_line"), S("diverter"), "touch")
    chk("Vent line into the vent pipe", S("vent_line"), S("pot"), "touch")
    chk("Vent line clear of the relief valve", S("vent_line"), S("relief"), 10.0)
    chk("Relief valve on the header", S("relief"), S("header"), "touch")
    chk("Discharge pipe on the relief valve", S("discharge"), S("relief"), "touch")
    chk("Discharge stay on the vent pipe", S("discharge"), S("pot"), "touch")
    chk("Discharge pipe clear of the vent line", S("discharge"), S("vent_line"), 10.0)
    chk("Discharge pipe clear of the diverter", S("discharge"), S("diverter"), 10.0)
    chk("Pot clear of the jumper", S("pot"), S("jumper"), 20.0)
    chk("Pot clear of the firebox", S("pot"), S("shell"), 20.0)
    chk("Post clear of the firebox", S("post"), S("shell") + S("glands"), 20.0)
    chk("Chimney clear of the vent and discharge", S("chimney") + S("cap"), S("pot") + S("discharge"), 100.0)
    chk("Hose on the diverter coupling", S("hose"), S("diverter"), "touch")
    chk("Hose on the hood 1 coupling", S("hose"), S("manifold1"), "touch")
    chk("Hose clear of the trailer", S("hose"), S("trailer"), 30.0)
    chk("Hose clear of the discharge pipe", S("hose"), S("discharge"), 20.0)
    chk("Overflow branch on the seal pot", S("overflow"), S("pot"), "touch")
    chk("Overflow trap stay on the pot clamp band", S("ovf_stay"), S("stay"), "touch")
    chk("Overflow trap stay on the down-leg", S("ovf_stay"), S("overflow"), "touch")
    chk("Overflow rear clip on the trailer rail", S("ovf_clip"), S("trailer"), "touch")
    chk("Overflow in its rear clip", S("ovf_clip"), S("overflow"), "touch")
    chk("Overflow clear of the trailer deck", S("overflow"), S("trailer"), 20.0)
    chk("Overflow clear of the header post and pot drain", S("overflow"), S("post") + S("stay"), 20.0)
    chk("Overflow clear of the hose", S("overflow"), S("hose"), 50.0)
    chk("Overflow clear of the relief discharge and vent line", S("overflow"), S("discharge") + S("vent_line") + S("diverter"), 20.0)
    for n in (1, 2):
        chk(f"Hood {n} skirt round the shell", S(f"skirt{n}"), S(f"hood{n}"), "touch")
        chk(f"Hood {n} manifold hung from the inner skin", S(f"manifold{n}"), S(f"hood{n}"), "touch")
        chk(f"Hood {n} handles on the shell", S(f"handles{n}"), S(f"hood{n}"), "touch")
        chk(f"Hood {n} handles clear of the skirt", S(f"handles{n}"), S(f"skirt{n}"), 20.0)
    chk("Drum on its saddles", S("tank"), S("saddles"), "touch")
    chk("Saddles on the deck", S("saddles"), S("trailer"), "touch")
    chk("Straps over the drum", S("straps"), S("tank"), "touch")
    chk("Straps clear of the saddles", S("straps"), S("saddles"), 5.0)
    chk("Pump box on the deck", S("pbox"), S("trailer"), "touch")
    chk("Pump box clear of the drum", S("pbox"), S("tank"), 10.0)
    chk("Suction hose on the drum outlet", S("feed"), S("tank"), "touch")
    chk("Feed line on the pump box", S("feed"), S("pbox"), "touch")
    chk("Feed line on the economizer inlet", S("feed"), S("eco_bank"), "touch")
    chk("Feed line clips on the shell", S("clips"), S("shell"), "touch")
    chk("Feed line in its clips", S("clips"), S("feed"), "touch")
    chk("Feed line clear of the economizer flange", S("feed"), S("eco_box"), 3.0)
    chk("Feed line clear of the bank box frame", S("feed"), S("bk_box") + S("roof_bolts"), 3.0)
    chk("Skids clear of the drum saddles and pump box", S("skids"), S("saddles") + S("pbox"), 50.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:58s} overlap {v:9.2f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


DENSITY = {"steel": 7.85e-6, "stainless": 8.0e-6}     # kg/mm3


def construction_masses(p=PARAMS):
    """Masses (kg) of the parts added for construction, for STR-CAL-001 (python model.py --mass)."""
    C = build_components(p)
    st, ss = DENSITY["steel"], DENSITY["stainless"]
    m = {
        "Firebox skids": C["skids"].shape.volume * st,
        "Header post and foot plate": C["post"].shape.volume * st,
        "Pot stay and pot foot plate": C["stay"].shape.volume * st + p["foot"][0] ** 2 * p["foot"][1] * st,
        "Drum saddles (hardwood)": C["saddles"].shape.volume * 0.7e-6,
        "Coil brackets": C["brackets"].shape.volume * ss,
        "Grate stand": C["stand"].shape.volume * st,
        "Gland plates": C["glands"].shape.volume * st,
        "Damper guides and slide": (C["guides"].shape.volume + C["damper"].shape.volume) * st,
        "Feed lines, jumper and clips": (C["feed"].shape.volume * 0.35 + C["jumper"].shape.volume * 0.35 + C["clips"].shape.volume) * ss,
        "Vent line and relief discharge": (C["vent_line"].shape.volume + C["discharge"].shape.volume) * 0.3 * st,
        "Secondary air damper and guides": (C["guides2"].shape.volume + C["damper2"].shape.volume) * st,
        "Seal pot overflow, trap stay and clip": (C["overflow"].shape.volume * 0.38 + C["ovf_stay"].shape.volume + C["ovf_clip"].shape.volume) * st,
    }
    return m


def bank_masses(p=PARAMS):
    """Masses (kg) of the evaporator bank parts, for STR-CAL-001 (python model.py --mass)."""
    C = build_components(p)
    st, ss = DENSITY["steel"], DENSITY["stainless"]
    od, w = p["bk_tube_od"], p["bk_tube_wall"]
    m = {
        "Bank box, frame and cover": (C["bk_box"].shape.volume + C["bk_cover"].shape.volume) * st,
        "Bank box lining (128 kg/m3)": C["bk_lining"].shape.volume * 0.128e-6,
        "Bank tube": math.pi / 4 * (od ** 2 - (od - 2 * w) ** 2) * bank_length(p) * 1000 * ss,
        "Bank supports": C["bk_sups"].shape.volume * st,
        "Link and unions": C["bk_link"].shape.volume * 0.4 * ss,
    }
    return m



# ------------------------------------------------------------------ kit 1.9 interface (STANDARDS section 24)
TITLE = "SteamRoot"
OPTIONS = {"A": "Monotube coil generator (current design)", "B": "Vented fire-tube kettle"}
PRINCIPLES = {
    "A": "A pump pushes water once through an economizer, an evaporator bank and a 25.4 mm stainless coil above a "
         "wood fire; steam leaves at near atmospheric pressure past a water-seal vent with 7.3 L of water heated.",
    "B": "A wood fire under a vented steel kettle boils a 70 L pool of water round seven vertical fire tubes; a "
         "float switch tops it up and the same water-seal vent holds it near atmospheric pressure.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 22, "az": -55, "scale": "person", "ground_z": 0} for k in OPTIONS}
# Pairs that share volume on purpose (substring pairs, as cad_check.py reads them): none so far; every hole is drilled
ALLOWED_CONTACTS = []

# default material by component key (cad_parts.MATERIALS); pieces may name their own
A_MAT = {
    "trailer": "galvanised", "skids": "painted_steel", "shell": "mild_steel", "roof": "mild_steel", "door": "mild_steel",
    "damper": "mild_steel", "damper2": "mild_steel", "guides": "mild_steel", "guides2": "mild_steel", "stand": "mild_steel",
    "glands": "mild_steel", "bk_box": "mild_steel", "bk_sups": "mild_steel", "bk_cover": "mild_steel", "eco_box": "mild_steel",
    "eco_lid": "mild_steel", "post": "painted_steel", "stay": "painted_steel", "ovf_stay": "painted_steel",
    "ovf_clip": "painted_steel", "pot": "painted_steel", "clips": "stainless", "discharge": "galvanised",
}
EXPLODE = {"Trailer frame and drawbar": (0, 0, -380), "Wheels": (0, 0, -760), "Firebox skids": (0, 0, -150),
           "Feed water tank, 125 L": (-350, 0, 250), "Feed pump": (-200, 500, 150), "Feed lines": (-350, 0, 450),
           "Firebox, fiber lined": (0, -700, 0), "Monotube steam coil": (0, 0, 0), "Evaporator bank": (0, 0, 450),
           "Flue-gas economizer": (0, 0, 900), "Chimney and spark arrestor": (0, 0, 1500),
           "Steam header and water-seal vent": (450, -500, 350), "Certified relief valve": (450, 450, 650),
           "Steam hose": (650, 0, 250), "Steam hoods (2)": (1000, 0, 0)}
_PARTS = {}


def _is_bare(shape):
    """As .kit/cad_check.py: an untouched box or a plain three-face solid."""
    try:
        f = shape.faces()
        return len(f) == 3 or (len(f) == 6 and all(str(x.geom_type).endswith("PLANE") for x in f))
    except Exception:
        return False


def _part(name, shape, material, kind, bom, group, key):
    import cad_parts as cp
    import build123d as bd
    if kind in ("made", "bought") and _is_bare(shape):
        shape = cp.break_edges(shape, 1.0)                    # the edge break a cut, sawn or moulded part has
    if isinstance(shape, bd.Compound):
        sols = shape.solids()
        # one solid: use it; several (possibly nested compounds): a flat compound of fresh solids, which STEP can write
        shape = sols[0] if len(sols) == 1 else bd.Compound(children=[bd.Solid(x.wrapped) for x in sols])
    if isinstance(shape, bd.Solid):
        shape = bd.Solid(shape.wrapped)                       # a fresh wrapper writes to STEP on its own (build123d 0.13)
    q = cp.part(name, shape, material, kind=kind, bom=bom, group=group or "shell", explode=EXPLODE.get(group, (0, 0, 0)))
    q["key_src"] = key
    return q


def parts_from(C, skip=()):
    """cad_parts.part() dicts for every piece of a build_components()-style dictionary."""
    out = []
    for key, c in C.items():
        if key in skip:
            continue
        if c.kind == "weld":
            for nm, sh, mat, bom, grp in c.pieces:
                out.append(_part(nm, sh, mat, "weld", bom, grp, key))
            continue
        kind = "fastener" if c.kind == "fixing" else c.kind
        for q in c.pieces:
            mat = q[2] if len(q) > 2 else ("zinc_plated" if kind == "fastener" else A_MAT.get(key, "mild_steel"))
            out.append(_part(q[0], q[1], mat, kind, c.bom, c.group, key))
    return out


def components(option=CHOSEN):
    """Kit 1.9: every part of one concept option as cad_parts.part() dicts (working position, hood 1 on the bed)."""
    if option in _PARTS:
        return list(_PARTS[option])
    if option == "A":
        out = parts_from(build_components())
    elif option == "B":
        import str_option_b
        out = str_option_b.components()
    else:
        raise KeyError(option)
    _PARTS[option] = out
    return list(out)


def baffle_masses():
    """Masses (kg) of the gas-pass baffles, their ledges and the split spacers (STR-DEC-001 S1), from the kit 1.9 parts."""
    import cad_parts as cp
    return {q["name"]: cp.mass_kg(q) for q in components("A")
            if q["kind"] in ("made", "bought") and ("baffle" in q["name"].lower() or "ledge" in q["name"].lower())}


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    if "--mass" in sys.argv:
        for m in (construction_masses(), bank_masses(), baffle_masses()):
            for k, v in m.items():
                print(f"  {k:38s} {v:6.1f} kg")
            print(f"  {'total':38s} {sum(m.values()):6.1f} kg")
        sys.exit(0)
    from build123d import export_stl, Compound
    root = Path(__file__).resolve().parents[1]
    (root / "stl").mkdir(exist_ok=True)
    C = build_components()
    stl_tol = dict(tolerance=0.15, angular_tolerance=0.2)      # 0.15 mm chord (STANDARDS section 24)
    for stem, keys in MAIN_PARTS.items():
        c = Compound(children=[s_ for k in keys for s_ in C[k].shape.solids()])
        export_stl(c, str(root / "stl" / f"{stem}.stl"), **stl_tol)
    asm = Compound(children=[s_ for k, c in C.items() if c.kind in ("made", "bought") for s_ in c.shape.solids()])
    export_stl(asm, str(root / "stl" / "steamroot.stl"), **stl_tol)
    bb = asm.bounding_box()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm "
          f"(x {bb.min.X:.0f} to {bb.max.X:.0f}, y {bb.min.Y:.0f} to {bb.max.Y:.0f}, z {bb.min.Z:.0f} to {bb.max.Z:.0f})")
    print("STL written to cad/stl/ (made and bought parts; fasteners and welds are in the STEP assemblies from cad_check.py --export)")
    print_checks()

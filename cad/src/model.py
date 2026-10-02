"""SteamRoot parametric model (build123d), constructable design (STR-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL to cad/step and cad/stl and prints the checks
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
    # below the coil (STR-DDR-003, C1)
    "fb_l": 700.0, "fb_w": 600.0, "fb_h": 1000.0, "fb_x": 250.0,
    "fb_shell_t": 3.0, "fb_lining_t": 50.0,
    "grate_z": 100.0,          # underside of the grate above the inside of the firebox floor
    "grate": (300.0, 20.0),    # cast grate size (square) and thickness
    "door_open": (300.0, 240.0, 130.0),     # opening width, height, bottom above the inside floor
    "door_lap": 20.0,
    "air_open": (160.0, 60.0, 15.0),        # air inlet width, height, bottom above the inside floor
    # Monotube coil: 316 stainless, 25.4 mm OD x 1.65 mm wall, above the fire bed
    "coil_mean_d": 420.0, "tube_od": 25.4, "tube_wall": 1.65, "coil_turns": 11, "coil_pitch": 40.0,
    "coil_z0": 400.0,          # underside of the coil above the inside of the firebox floor
    "bracket_deg": (90.0, 210.0, 330.0), "bracket_angle": (40.0, 5.0), "bracket_tip": 25.0,
    "gland_hole": 40.0, "gland_lift": 30.0, "gland_plate": (80.0, 100.0, 6.0), "frame_angle": (25.0, 3.0),
    # Flue-gas economizer box on top of the firebox (serpentine of 12.7 mm x 1.2 mm stainless tube)
    "eco_l": 520.0, "eco_w": 460.0, "eco_h": 260.0, "eco_tube_od": 12.7, "eco_tube_wall": 1.2, "eco_tube_len": 7300.0,
    "eco_flange": 30.0, "eco_layers": ((212.0, 6), (136.0, 6), (60.0, 5)),   # (tube centre above the box floor, passes)
    "eco_pitch": 76.2,         # run spacing and layer spacing: 38 mm centreline bend radius, a standard hand bender
    # Chimney with spark arrestor cap
    "chimney_d": 150.0, "chimney_top": 2400.0, "cap_h": 120.0, "spigot_h": 60.0,
    # Steam header (DN50), water-seal pot, vent pipe, diverter, post
    "header_od": 60.3, "header_len": 300.0, "header_z": 1550.0, "header_dx": 130.0,
    "seal_depth": 1000.0,      # effective seal head (0.094 bar); the dip leg is shorter, see derived()
    "seal_pot_od": 114.3, "dip_od": 42.2, "vent_od": 42.2, "vent_top": 2300.0, "seal_sump": 100.0,
    "relief_d": 70.0, "post": 50.0, "foot": (200.0, 10.0),
    # Steam hose, 25 mm bore, 6 m
    "hose_od": 44.0, "hose_len": 6000.0,
    # Steam hoods (two, used alternately): open-bottom insulated pans
    "hood_l": 1200.0, "hood_w": 1000.0, "hood_h": 250.0, "hood_ins_t": 40.0, "hood_skin_t": 1.0,
    "skirt_depth": 60.0, "skirt_lap": 40.0, "skirt_t": 1.5,
    "hood_gap": 150.0, "hood_offset": 400.0, "n_hoods": 2,
}

Comp = namedtuple("Comp", "name shape bom kind group")


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
    d["eco_z0"] = d["fb_top"] + p["fb_shell_t"]               # underside of the economizer flange, on the roof plate
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


def _tube_along(points, od):
    """Round tube through a polyline of (x, y, z) points (square joints with a ball at each corner)."""
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


def eco_ends(p=PARAMS):
    pts = eco_bank_points(p)
    return pts[0], pts[-1]


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    b = _b3d()
    D = derived(p)
    C = {}

    def add(key, name, shape, bom, kind, group_):
        C[key] = Comp(name, shape, bom, kind, group_)

    T = D["deck_top"]
    x0d = -p["deck_l"] / 2
    rw = p["rail_w"]

    # 1 trailer: perimeter rails, deck skin, drawbar with coupling and jack, axle
    frame = bx(-p["deck_l"] / 2, p["deck_l"] / 2, -p["deck_w"] / 2, p["deck_w"] / 2, p["deck_z"], T)
    frame -= bx(-p["deck_l"] / 2 + rw, p["deck_l"] / 2 - rw, -p["deck_w"] / 2 + rw, p["deck_w"] / 2 - rw, p["deck_z"] - 1, T - 10)
    drawbar = bx(x0d - p["drawbar_l"], x0d, -40, 40, p["deck_z"], p["deck_z"] + 80)
    drawbar += bx(x0d - p["drawbar_l"] - 120, x0d - p["drawbar_l"], -50, 50, p["deck_z"] + 10, p["deck_z"] + 70)
    jack = zcyl(x0d - p["drawbar_l"] + 150, 0, 0, 30, p["deck_z"])
    axle = ycyl(p["axle_x"], -p["deck_w"] / 2 - p["wheel_gap"], p["wheel_r"], 30, p["deck_w"] + 2 * p["wheel_gap"])
    axle += bx(p["axle_x"] - 40, p["axle_x"] + 40, -p["deck_w"] / 2 + 10, -p["deck_w"] / 2 + 70, p["wheel_r"], p["deck_z"])
    axle += bx(p["axle_x"] - 40, p["axle_x"] + 40, p["deck_w"] / 2 - 70, p["deck_w"] / 2 - 10, p["wheel_r"], p["deck_z"])
    add("trailer", "Trailer frame and drawbar", frame + drawbar + jack + axle, 1, "bought", "Trailer frame and drawbar")
    wy = p["deck_w"] / 2 + p["wheel_gap"]
    add("wheels", "Wheels", ycyl(p["axle_x"], wy, p["wheel_r"], p["wheel_r"], p["wheel_w"])
        + ycyl(p["axle_x"], -wy - p["wheel_w"], p["wheel_r"], p["wheel_r"], p["wheel_w"]), 2, "bought", "Wheels")

    # 17 firebox skids, across the deck, ends bolted through the deck into the side rails
    s, st = p["skid"], p["skid_t"]
    skx = [p["fb_x"] - p["skid_dx"], p["fb_x"] + p["skid_dx"]]
    add("skids", "Firebox skids (2)", fuse([rhs_y(x, -p["deck_w"] / 2, p["deck_w"] / 2, T, s, st) for x in skx]), 17, "made", "Firebox skids")
    ry = p["deck_w"] / 2 - rw / 2
    add("skid_bolts", "M12 skid bolts (4)", group([q for x in skx for y in (-ry, ry) for q in bolt_z(x, y, T + s, p["deck_z"], 12)]), 21, "fixing", None)

    # 5 firebox shell (3 mm steel) with its openings, and the fibre lining inside it
    t, sh = D["t"], p["fb_shell_t"]
    L, W, H = p["fb_l"], p["fb_w"], p["fb_h"]
    fx, z0, F = p["fb_x"], D["fb_z0"], D["F"]
    zc = z0 + H / 2
    dw, dh, db = p["door_open"]
    aw, ah, ab = p["air_open"]
    door_cut = bx(fx - dw / 2, fx + dw / 2, -W / 2 - 1, -W / 2 + t + 1, F + db, F + db + dh)
    air_cut = bx(fx - aw / 2, fx + aw / 2, -W / 2 - 1, -W / 2 + t + 1, F + ab, F + ab + ah)
    glands_z = [D["cz0"], D["coil_top"]]
    gh, lift = p["gland_hole"], p["gland_lift"]
    # slots, not holes: the coil goes in from the top, 30 mm high, and its tails slide out through these
    gland_cut = fuse([bx(D["fb_x1"] - t - 1, D["fb_x1"] + 1, -gh / 2, gh / 2, z - gh / 2, z + gh / 2 + lift) for z in glands_z])
    cuts = door_cut + air_cut + gland_cut
    top = D["fb_top"]
    shell = box(fx, 0, zc, L, W, H) - bx(fx - L / 2 + sh, fx + L / 2 - sh, -W / 2 + sh, W / 2 - sh, z0 + sh, top + 1)
    shell -= cuts
    fa, ft = p["frame_angle"]                         # 25 x 25 x 3 angle frame round the top, for the roof bolts
    frame_h = bx(fx - L / 2 - fa, fx + L / 2 + fa, -W / 2 - fa, W / 2 + fa, top - ft, top) - bx(fx - L / 2, fx + L / 2, -W / 2, W / 2, top - ft - 1, top + 1)
    frame_v = bx(fx - L / 2 - ft, fx + L / 2 + ft, -W / 2 - ft, W / 2 + ft, top - fa, top - ft) - bx(fx - L / 2, fx + L / 2, -W / 2, W / 2, top - fa - 1, top)
    add("shell", "Firebox shell", shell + frame_h + frame_v, 5, "made", "Firebox, fiber lined")
    roof = bx(fx - L / 2 - fa, fx + L / 2 + fa, -W / 2 - fa, W / 2 + fa, top, top + sh) - zcyl(fx, 0, top - 1, p["chimney_d"] / 2, sh + 2)
    add("roof", "Firebox roof", roof, 5, "made", "Firebox, fiber lined")
    rfix = []
    xs_r = [fx - L / 2 - fa / 2 + i * (L + fa) / 4 for i in range(5)]
    ys_r = [-W / 2 - fa / 2 + i * (W + fa) / 3 for i in range(4)]
    for xr in xs_r:
        for yr in (-W / 2 - fa / 2, W / 2 + fa / 2):
            rfix += bolt_z(xr, yr, top + sh, top - ft, 8)
    for yr in ys_r[1:-1]:
        for xr in (fx - L / 2 - fa / 2, fx + L / 2 + fa / 2):
            rfix += bolt_z(xr, yr, top + sh, top - ft, 8)
    add("roof_bolts", "M8 roof bolts (14)", group(rfix), 21, "fixing", None)

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
            y_in = sgn * (W / 2 - sh)
            brk.append(angle_y(xh, min(y_in, yh - sgn * tip), max(y_in, yh - sgn * tip), ztop, leg, bt, hang_x=+1))
        else:                                                 # on the +X or -X wall, runs along X
            sgn = 1 if math.cos(math.radians(deg)) > 0 else -1
            x_in = fx + sgn * (L / 2 - sh)
            brk.append(angle_x(yh, min(x_in, xh - sgn * tip), max(x_in, xh - sgn * tip), ztop, leg, bt, hang_y=-1))
    add("brackets", "Coil brackets (3)", fuse(brk), 18, "made", "Firebox, fiber lined")

    lt = p["fb_lining_t"]
    lining = bx(fx - L / 2 + sh, fx + L / 2 - sh, -W / 2 + sh, W / 2 - sh, z0 + sh, top) - bx(fx - L / 2 + t, fx + L / 2 - t, -W / 2 + t, W / 2 - t, F, top + 1)
    lining -= cuts
    for bk in brk:
        bb = bk.bounding_box()
        lining -= bx(bb.min.X - 1, bb.max.X + 1, bb.min.Y - 1, bb.max.Y + 1, bb.min.Z - 1, bb.max.Z + 1)
    add("lining", "Ceramic fibre lining", lining, 5, "bought", "Firebox, fiber lined")
    board = bx(fx - L / 2 + t, fx + L / 2 - t, -W / 2 + t, W / 2 - t, top - lt, top) - zcyl(fx, 0, top - lt - 1, p["chimney_d"] / 2, lt + 2)
    add("board", "Roof board", board, 5, "bought", "Firebox, fiber lined")

    # 18 grate stand (25 mm square tube ring on four legs with foot pads) and 5 cast grate
    gs, gt = p["grate"]
    gz = F + p["grate_z"]
    ring = bx(fx - gs / 2, fx + gs / 2, -gs / 2, gs / 2, gz - 25, gz) - bx(fx - gs / 2 + 25, fx + gs / 2 - 25, -gs / 2 + 25, gs / 2 - 25, gz - 26, gz + 1)
    legs = []
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            cx_, cy_ = fx + sx_ * (gs / 2 - 12.5), sy_ * (gs / 2 - 12.5)
            legs.append(bx(cx_ - 12.5, cx_ + 12.5, cy_ - 12.5, cy_ + 12.5, F + 5, gz - 25))
            legs.append(bx(cx_ - 30, cx_ + 30, cy_ - 30, cy_ + 30, F, F + 5))
    add("stand", "Grate stand", fuse([ring] + legs), 18, "made", "Firebox, fiber lined")
    grate = bx(fx - gs / 2, fx + gs / 2, -gs / 2, gs / 2, gz, gz + gt)
    for i in range(-5, 6):
        grate -= bx(fx + i * 25 - 6, fx + i * 25 + 6, -gs / 2 + 25, gs / 2 - 25, gz - 1, gz + gt + 1)
    add("grate", "Cast grate", grate, 5, "bought", "Firebox, fiber lined")

    # 5 door: 3 mm plate lapping the opening by 20 mm, with a 46 mm fibre board plug; hinges; latch
    lap = p["door_lap"]
    yd = -W / 2
    dz0, dz1 = F + db - lap, F + db + dh + lap
    dx0, dx1 = fx - dw / 2 - lap, fx + dw / 2 + lap
    door = bx(dx0, dx1, yd - 3, yd, dz0, dz1)
    door += bx(fx - dw / 2 + 4, fx + dw / 2 - 4, yd, yd + t - 4, F + db + 4, F + db + dh - 4)     # board plug
    door += bx(fx - 60, fx + 60, yd - 3 - 30, yd - 3 - 20, (dz0 + dz1) / 2 - 8, (dz0 + dz1) / 2 + 8)   # handle bar
    door += fuse([bx(fx + sx_ * 60 - 8, fx + sx_ * 60 + 8, yd - 23, yd - 3, (dz0 + dz1) / 2 - 8, (dz0 + dz1) / 2 + 8) for sx_ in (-1, 1)])
    add("door", "Firebox door", door, 5, "made", "Firebox, fiber lined")
    hinges = []
    for zh_ in (dz0 + 40, dz1 - 40):
        hinges.append(zcyl(dx1 + 10, yd - 9, zh_ - 30, 8, 60))                   # knuckle on its pin
        hinges.append(bx(dx1 - 15, dx1 + 4, yd - 6, yd - 3, zh_ - 30, zh_ + 30))  # leaf welded to the door
        hinges.append(bx(dx1 + 16, dx1 + 40, yd - 3, yd, zh_ - 30, zh_ + 30))   # leaf welded to the shell
        hinges.append(bx(dx1 + 2, dx1 + 18, yd - 6, yd - 3, zh_ - 30, zh_ + 30))
    add("hinges", "Door hinges (2)", fuse(hinges), 5, "bought", "Firebox, fiber lined")
    zl = (dz0 + dz1) / 2
    latch = bx(dx0 - 30, dx0 - 6, yd - 20, yd, zl + 10, zl + 30)          # keeper welded to the shell
    latch += bx(dx0 - 30, dx0 + 40, yd - 26, yd - 20, zl + 10, zl + 30)   # turn latch bar over the door edge
    latch += bx(dx0 + 20, dx0 + 40, yd - 20, yd - 3, zl + 10, zl + 30)    # latch boss on the door
    add("latch", "Door latch", latch, 5, "bought", "Firebox, fiber lined")

    # 5 air damper: 3 mm slide plate in two guides below the door
    az0, az1 = F + ab, F + ab + ah
    pz0, pz1 = az0 - 20, az1 + 20
    damper = bx(fx - aw / 2 - 30, fx + aw / 2 + 30, yd - 6, yd - 3, pz0, pz1)
    damper += ycyl(fx - aw / 2 - 10, yd - 26, (pz0 + pz1) / 2, 10, 20)       # knob
    add("damper", "Air damper slide", damper, 5, "made", "Firebox, fiber lined")
    guides = []
    for zg, sgn in ((pz1, 1), (pz0, -1)):
        g = bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 3, yd, zg if sgn > 0 else zg - 6, zg + 6 if sgn > 0 else zg)
        g += bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 9, yd - 3, zg if sgn > 0 else zg - 6, zg + 6 if sgn > 0 else zg)
        g += bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 9, yd - 6, (zg - 6 if sgn > 0 else zg), (zg if sgn > 0 else zg + 6))
        guides.append(g)
    add("guides", "Damper guides (2)", fuse(guides), 5, "made", "Firebox, fiber lined")

    # 6 monotube coil: helix above the fire bed, tails out through the +X wall
    r = p["coil_mean_d"] / 2
    height = p["coil_pitch"] * p["coil_turns"]
    path = b.Pos(fx, 0, D["cz0"]) * b.Helix(pitch=p["coil_pitch"], height=height, radius=r)
    prof = b.Plane(origin=path @ 0, z_dir=path % 0) * b.Circle(p["tube_od"] / 2)
    helix = b.sweep(prof, path, is_frenet=True)
    x_out = D["fb_x1"]
    hx, hz = D["hx"], D["hz"]
    tail_end = x_out + 10                          # tails stop 10 mm outside the wall so the coil can go in
    tails = _tube_along([(fx + r, 0, D["coil_top"]), (tail_end, 0, D["coil_top"])], p["tube_od"])
    tails += _tube_along([(fx + r, 0, D["cz0"]), (tail_end, 0, D["cz0"])], p["tube_od"])
    add("coil", "Monotube steam coil", helix + tails, 6, "made", "Monotube steam coil")
    outlet = hexprism("x", tail_end, 0, D["coil_top"], 36, 25)                  # compression union
    outlet += _tube_along([(tail_end + 25, 0, D["coil_top"]), (x_out + 60, 0, D["coil_top"]), (x_out + 60, 0, hz),
                           (hx - p["header_od"] / 2, 0, hz)], p["tube_od"])
    add("outlet", "Coil outlet pipe and union", outlet, 6, "made", "Monotube steam coil")

    # 18 tube gland plates on the outside of the +X wall, with their M6 studs
    gpw, gph, gpt = p["gland_plate"]
    gl, gfix = [], []
    for z in glands_z:
        zm = z + lift / 2
        g = bx(x_out, x_out + gpt, -gpw / 2, gpw / 2, zm - gph / 2, zm + gph / 2) - xcyl(x_out - 1, 0, z, p["tube_od"] / 2 + 0.3, gpt + 2)
        gl.append(g)
        for dy in (-28, 28):
            for dz in (-38, 38):
                gfix += [xcyl(x_out - 3, dy, zm + dz, 3, gpt + 10), hexprism("x", x_out + gpt, dy, zm + dz, 10, 5)]
    add("glands", "Tube gland plates (2)", fuse(gl), 18, "made", "Firebox, fiber lined")
    add("gland_studs", "M6 gland studs and nuts (8)", group(gfix), 21, "fixing", None)

    # 19 coil inlet jumper (12.7 mm stainless) from the coil inlet reducer up to the economizer outlet
    e_in, e_out = eco_ends(p)
    jx = x_out + 50
    red = hexprism("x", x_out + 10, 0, D["cz0"], 36, 25) + xcyl(x_out + 35, 0, D["cz0"], 12.0, 15)   # union and reducer
    jumper = _tube_along([(jx, 0, D["cz0"]), (jx, e_out[1], D["cz0"]), (jx, e_out[1], e_out[2]),
                          (p["fb_x"] + p["eco_l"] / 2 + 20, e_out[1], e_out[2])], p["eco_tube_od"])
    add("jumper", "Coil inlet jumper and reducer", red + jumper, 19, "bought", "Feed lines")

    # 7 economizer: 2 mm steel box with a bolting flange on the roof, bolted lid with the chimney
    #   spigot, the stainless serpentine inside on two support bars, and a condensate drain
    el, ew, eh = p["eco_l"], p["eco_w"], p["eco_h"]
    ef = p["eco_flange"]
    ez0, ezf, ezt = D["eco_z0"], D["eco_floor"], D["eco_top"]
    ebox = bx(fx - el / 2 - ef, fx + el / 2 + ef, -ew / 2 - ef, ew / 2 + ef, ez0, ezf)              # flange plate
    ebox += bx(fx - el / 2, fx + el / 2, -ew / 2, ew / 2, ezf, ezt) - bx(fx - el / 2 + 2, fx + el / 2 - 2, -ew / 2 + 2, ew / 2 - 2, ezf - 1, ezt + 1)
    ebox += bx(fx - el / 2 - 25, fx + el / 2 + 25, -ew / 2 - 25, ew / 2 + 25, ezt - 3, ezt) - bx(fx - el / 2 + 2, fx + el / 2 - 2, -ew / 2 + 2, ew / 2 - 2, ezt - 4, ezt + 1)
    ebox -= zcyl(fx, 0, ez0 - 1, p["chimney_d"] / 2, 8)
    for (x_, y_, z_) in (e_in, e_out):
        ebox -= xcyl(fx - el / 2 - 1 if x_ < fx else fx + el / 2 - 3, y_, z_, p["eco_tube_od"] / 2 + 0.3, 5)
    drain_z = ezf + 14
    ebox -= xcyl(fx - el / 2 - 1, 150, drain_z, 6, 5)
    drain = xcyl(fx - el / 2 - 50, 150, drain_z, 10, 50) - xcyl(fx - el / 2 - 51, 150, drain_z, 6, 52)
    bars = fuse([bx(fx + dx - 1.5, fx + dx + 1.5, -ew / 2 + 2, ew / 2 - 2, e_out[2] - p["eco_tube_od"] / 2 - 25, e_out[2] - p["eco_tube_od"] / 2)
                 for dx in (-120, 120)])
    add("eco_box", "Economizer box", ebox + bars + drain, 7, "made", "Flue-gas economizer")
    lid = bx(fx - el / 2 - 25, fx + el / 2 + 25, -ew / 2 - 25, ew / 2 + 25, ezt, ezt + 2) - zcyl(fx, 0, ezt - 1, p["chimney_d"] / 2 - 1, 4)
    spig = zcyl(fx, 0, ezt + 2, p["chimney_d"] / 2 - 1, p["spigot_h"]) - zcyl(fx, 0, ezt + 1, p["chimney_d"] / 2 - 2.5, p["spigot_h"] + 2)
    add("eco_lid", "Economizer lid and spigot", lid + spig, 7, "made", "Flue-gas economizer")
    bank_pts = [(fx - el / 2 - 20, e_in[1], e_in[2])] + eco_bank_points(p) + [(fx + el / 2 + 20, e_out[1], e_out[2])]
    add("eco_bank", "Economizer tube bank", _tube_along(bank_pts, p["eco_tube_od"]), 7, "made", "Flue-gas economizer")
    efix = []
    for i in range(4):
        xb = fx - el / 2 - ef / 2 + i * (el + ef) / 3
        for yb in (-ew / 2 - ef / 2, ew / 2 + ef / 2):
            efix += stud_z(xb, yb, ez0, ezf, 8)
    for yb in (-ew / 2 / 3, ew / 2 / 3):
        for xb in (fx - el / 2 - ef / 2, fx + el / 2 + ef / 2):
            efix += stud_z(xb, yb, ez0, ezf, 8)
    add("eco_bolts", "M8 economizer flange studs and nuts (12)", group(efix), 21, "fixing", None)
    lfix = []
    for i in range(4):
        xb = fx - el / 2 - 12 + i * (el + 24) / 3
        for yb in (-ew / 2 - 12, ew / 2 + 12):
            lfix += bolt_z(xb, yb, ezt + 2, ezt - 3, 6)
    add("lid_bolts", "M6 lid bolts (8)", group(lfix), 21, "fixing", None)

    # 8 chimney (150 mm single-wall stainless) over the spigot, spark arrestor cap on top
    ch0 = ezt + 2
    cap0 = p["chimney_top"] - p["cap_h"]
    ri = p["chimney_d"] / 2 - 1                   # chimney bore = spigot outside diameter, a slide fit
    chim = zcyl(fx, 0, ch0, ri + 0.8, cap0 + 50 - ch0) - zcyl(fx, 0, ch0 - 1, ri, cap0 + 52 - ch0)
    cap = zcyl(fx, 0, cap0, ri + 4.0, 50) - zcyl(fx, 0, cap0 - 1, ri + 0.8, 52)
    cap += zcyl(fx, 0, cap0 + 50, p["chimney_d"] / 2 + 45, p["cap_h"] - 50) - zcyl(fx, 0, cap0 + 49, p["chimney_d"] / 2 + 42, p["cap_h"] - 52)
    add("chimney", "Chimney", chim, 8, "bought", "Chimney and spark arrestor")
    add("cap", "Spark arrestor cap", cap, 8, "bought", "Chimney and spark arrestor")

    # 17 header post (50 mm square tube on a foot plate) and 9 header with its connections
    po = p["post"]
    fpw, fpt = p["foot"]
    post = bx(hx - 75, hx + 75, -75, 75, T, T + fpt)
    post += rhs_z(hx, 0, T + fpt, hz - p["header_od"] / 2 - 6, po, 3)
    post += bx(hx - 40, hx + 40, -30, 30, hz - p["header_od"] / 2 - 6, hz - p["header_od"] / 2)      # saddle plate
    add("post", "Header post", post, 17, "made", "Steam header and water-seal vent")
    pfix = []
    for dx in (-50, 50):
        for dy in (-50, 50):
            pfix += bolt_z(hx + dx, dy, T + fpt, T - 10, 10)
    ub = []
    for dy in (-20, 20):                                 # U-bolt over the header into the saddle plate
        ub.append(b.Pos(hx, dy, hz) * b.Rot(90, 0, 0) * (b.Cylinder(p["header_od"] / 2 + 6, 8) - b.Cylinder(p["header_od"] / 2, 9)) & bx(hx - 50, hx + 50, dy - 5, dy + 5, hz, hz + 50))
        for sx_ in (-1, 1):
            ub.append(zcyl(hx + sx_ * (p["header_od"] / 2 + 3), dy, hz - p["header_od"] / 2 - 16, 3, p["header_od"] / 2 + 16))
    add("post_bolts", "M10 post bolts and header U-bolts", group(pfix + ub), 21, "fixing", None)

    hl_ = p["header_len"]
    header = ycyl(hx, -hl_ / 2, hz, p["header_od"] / 2, hl_)
    gauge = zcyl(hx, -70, hz, 7, p["header_od"] / 2 + 60) + ycyl(hx, -70 - 25, hz + p["header_od"] / 2 + 90, 25, 20)
    gauge += zcyl(hx, -70, hz + p["header_od"] / 2 + 55, 8, 15)
    add("header", "Steam header and gauge", header + gauge, 9, "made", "Steam header and water-seal vent")

    # 9 water-seal pot on its foot plate: dip leg inside, vent pipe from the top, link from the header
    py = D["pot_y"]
    pr = p["seal_pot_od"] / 2
    pot = zcyl(hx, py, D["pot_bot"], pr, D["pot_top"] - D["pot_bot"]) - zcyl(hx, py, D["pot_bot"] + 6, pr - 3.05, D["pot_top"] - D["pot_bot"] - 12)
    pot += bx(hx - fpw / 2, hx + fpw / 2, py - fpw / 2, py + fpw / 2, T, T + fpt)
    dip_y = py + (pr - 3.05 - p["dip_od"] / 2 - 1)
    dip = zcyl(hx, dip_y, D["dip_end"], p["dip_od"] / 2, hz - D["dip_end"]) - zcyl(hx, dip_y, D["dip_end"] - 1, p["dip_od"] / 2 - 3.56, hz - D["dip_end"] - 20)
    link = ycyl(hx, dip_y, hz, p["dip_od"] / 2, -hl_ / 2 - dip_y)
    vent = zcyl(hx, py, D["pot_top"], p["vent_od"] / 2, p["vent_top"] - D["pot_top"])
    ys_ = py - pr - 12                                                   # level sight tube on the operator side
    sight = zcyl(hx, ys_, D["dip_end"] + 50, 6, D["water_line"] + D["rise"] - D["dip_end"]) \
        + ycyl(hx, ys_, D["dip_end"] + 65, 5, 13) + ycyl(hx, ys_, D["water_line"] + D["rise"] + 35, 5, 13)
    drainv = xcyl(hx + pr - 1, py, D["pot_bot"] + 40, 10, 50)
    add("pot", "Water-seal pot, dip leg and vent", pot + dip + link + vent + sight + drainv, 9, "made", "Steam header and water-seal vent")
    potfix = []
    for dx in (-80, 80):
        for dy in (-80, 80):
            potfix += bolt_z(hx + dx, py + dy, T + fpt, T - 10, 10)
    add("pot_bolts", "M10 pot foot bolts (4)", group(potfix), 21, "fixing", None)
    # stay from the post to the pot, a clamp band round the pot
    zs = T + 600
    stay = bx(hx - 20, hx + 20, py + pr + 3, -po / 2, zs - 3, zs + 3)
    stay += zcyl(hx, py, zs - 20, pr + 3, 40) - zcyl(hx, py, zs - 21, pr, 42)
    add("stay", "Pot stay and clamp band", stay, 17, "made", "Steam header and water-seal vent")

    # 9 diverter at the +Y end of the header: hose coupling to +X, vent line up and over to the vent
    dy_ = D["div_y"]
    nip = ycyl(hx, hl_ / 2, hz, 13.35, 15)
    div = box(hx, dy_, hz, 70, 90, 70) + nip
    div += zcyl(hx, dy_, hz + 35, 6, 40) + bx(hx - 6, hx + 90, dy_ - 6, dy_ + 6, hz + 75, hz + 85)      # lever
    coupling = xcyl(hx + 35, dy_, hz, 22, 40)
    add("diverter", "Three-way diverter and hose coupling", div + coupling, 9, "bought", "Steam header and water-seal vent")
    vz = D["vent_line_z"]
    vline = _tube_along([(hx, dy_ + 45, hz), (hx, dy_ + 75, hz), (hx, dy_ + 75, vz), (hx, py + p["vent_od"] / 2, vz)], 33.4)
    add("vent_line", "Diverter vent line", vline, 20, "bought", "Steam header and water-seal vent")

    # 10 relief valve on the header top, discharge pipe to 2.3 m, stay to the vent pipe
    rvy = 60.0
    rv0 = hz + p["header_od"] / 2
    relief = zcyl(hx, rvy, rv0, 13.35, 20) + zcyl(hx, rvy, rv0 + 20, p["relief_d"] / 2, 100) + zcyl(hx, rvy, rv0 + 120, 20, 60)
    relief += bx(hx + 30, hx + 60, rvy - 4, rvy + 4, rv0 + 150, rv0 + 158)                             # test lever
    dis_x = hx + 80
    disch = _tube_along([(hx + p["relief_d"] / 2, rvy, rv0 + 70), (dis_x, rvy, rv0 + 70), (dis_x, rvy, p["vent_top"])], 26.7)
    zst = p["vent_top"] - 100
    ux, uy = hx - dis_x, py - rvy
    un = math.hypot(ux, uy)
    ux, uy = ux / un, uy / un
    dstay = _tube_along([(dis_x, rvy, zst), (hx - ux * p["vent_od"] / 2, py - uy * p["vent_od"] / 2, zst)], 12.0)
    add("relief", "Certified relief valve", relief, 10, "bought", "Certified relief valve")
    add("discharge", "Relief discharge pipe and stay", disch + dstay, 20, "bought", "Certified relief valve")

    # 11 steam hose, diverter coupling to the first hood (routing is indicative; the hose is flexible)
    hcx = D["hood_inlet_x"][0]
    hood_top_cpl = p["hood_h"] + 3 + 80
    c0 = hx + 75
    hose = _tube_along([(c0, dy_, hz), (c0 + 200, dy_, hz), (c0 + 330, dy_, hz - 250), (c0 + 330, dy_, 650),
                        (hcx, 0, 650), (hcx, 0, hood_top_cpl)], p["hose_od"])
    add("hose", "Steam hose", hose, 11, "bought", "Steam hose")

    # 12 steam hoods: double-skin insulated shell, galvanised skirt, perforated manifold, handles
    hl, hw, hh, ins = p["hood_l"], p["hood_w"], p["hood_h"], p["hood_ins_t"]
    for i, cx in enumerate(D["hood_cx"]):
        n = i + 1
        ix = D["hood_inlet_x"][i]
        hbody = box(cx, 0, hh / 2, hl, hw, hh) - box(cx, 0, hh / 2 - ins / 2 - 0.5, hl - 2 * ins, hw - 2 * ins, hh - ins + 1)
        hbody -= zcyl(ix, 0, hh - ins - 1, 15.3, ins + 2)
        add(f"hood{n}", f"Hood {n} shell", hbody, 12, "made", "Steam hoods (2)")
        sk, lp, skt = p["skirt_depth"], p["skirt_lap"], p["skirt_t"]
        skirt = box(cx, 0, (lp - sk) / 2, hl + 2 * skt, hw + 2 * skt, sk + lp) - box(cx, 0, (lp - sk) / 2, hl, hw, sk + lp + 2)
        add(f"skirt{n}", f"Hood {n} skirt", skirt, 12, "made", "Steam hoods (2)")
        mz = hh - ins - 15 - 15
        man = xcyl(cx - (hl - 2 * ins - 80) / 2, 0, mz, 15, hl - 2 * ins - 80)
        man += zcyl(ix, 0, mz, 15, hh - mz)                                         # riser through the top
        for dxh in (-300, 300):
            man += bx(cx + dxh - 10, cx + dxh + 10, -2, 2, mz + 14.9, hh - ins)     # hanger straps
        man += zcyl(ix, 0, hh, 35, 3) - zcyl(ix, 0, hh - 1, 15, 5)                 # top flange
        man += zcyl(ix, 0, hh + 3, 20, 80)                                          # hose coupling
        add(f"manifold{n}", f"Hood {n} manifold and inlet", man, 12, "made", "Steam hoods (2)")
        hd = []
        for sy_ in (1, -1):
            hd.append(box(cx, sy_ * (hw / 2 + 60), hh - 60, 900, 30, 30))
            for sx_ in (-400, 400):
                hd.append(box(cx + sx_, sy_ * (hw / 2 + 30), hh - 60, 30, 60, 30))
        add(f"handles{n}", f"Hood {n} handles", fuse(hd), 12, "made", "Steam hoods (2)")

    # 3 feed tank on two saddles with two ratchet straps
    tx, tr, tl = p["tank_x"], p["tank_r"], p["tank_l"]
    tz = D["tank_z"]
    tank = ycyl(tx, -tl / 2, tz, tr, tl)
    tank += ycyl(tx, tl / 2, tz - tr + 60, 15, 40)                           # outlet bulkhead and strainer
    tank += zcyl(tx + 120, 0, tz + tr - 20, 40, 40)                          # filler cap
    add("tank", "Feed water drum", tank, 3, "bought", "Feed water tank, 125 L")
    sl, swd, sht = p["saddle"]
    sad = []
    for sy_ in (-p["saddle_y"], p["saddle_y"]):
        sd = bx(tx - sl / 2, tx + sl / 2, sy_ - swd / 2, sy_ + swd / 2, T, T + sht) - ycyl(tx, sy_ - swd, tz, tr, 2 * swd)
        sad.append(sd)
    add("saddles", "Drum saddles (2)", fuse(sad), 17, "made", "Feed water tank, 125 L")
    straps = []
    for sy_ in (-p["saddle_y"] - 70, p["saddle_y"] + 70):
        ring = ycyl(tx, sy_ - 12.5, tz, tr + 2, 25) - ycyl(tx, sy_ - 13, tz, tr, 26)
        ring = ring & bx(tx - tr - 5, tx + tr + 5, sy_ - 15, sy_ + 15, tz, tz + tr + 5)
        straps.append(ring)
        for sx_ in (-1, 1):
            straps.append(bx(tx + sx_ * (tr + 1) - 1, tx + sx_ * (tr + 1) + 1, sy_ - 12.5, sy_ + 12.5, T + 10, tz))
            straps.append(bx(tx + sx_ * (tr + 1) - 15, tx + sx_ * (tr + 1) + 15, sy_ - 20, sy_ + 20, T, T + 10))   # lashing point
    add("straps", "Ratchet straps (2)", fuse(straps), 21, "bought", "Feed water tank, 125 L")
    sfix = []
    for sy_ in (-p["saddle_y"], p["saddle_y"]):
        for dx in (-sl / 2 + 25, sl / 2 - 25):
            sfix += bolt_z(tx + dx, sy_, T + 30, T - 10, 10)
    add("saddle_bolts", "M10 saddle bolts (4)", group(sfix), 21, "fixing", None)

    # 4, 13, 16 pump and alarm box (pump, needle valve, flow meter, battery, alarm controller)
    bx0, bx1, by0, by1, bh = p["pbox"]
    pbox = bx(bx0, bx1, by0, by1, T, T + bh)
    pbox += zcyl(bx0 + 40, by1 - 40, T + bh, 8, 10) + zcyl(bx0 + 80, by1 - 40, T + bh, 8, 10)   # indicators
    add("pbox", "Pump and alarm box", pbox, 4, "bought", "Feed pump")

    # 19 feed lines: suction hose from the drum, 12.7 mm stainless line to the economizer inlet with two clips
    suction = _tube_along([(tx, tl / 2 + 40, tz - tr + 60), (tx, (by0 + by1) / 2, tz - tr + 60), (bx0, (by0 + by1) / 2, tz - tr + 60)], 16.0)
    xf = D["fb_x0"] - 40
    yfl = (by0 + by1) / 2
    feed = _tube_along([((bx0 + bx1) / 2, yfl, T + bh), ((bx0 + bx1) / 2, yfl, T + bh + 80), (xf, yfl, T + bh + 80),
                        (xf, e_in[1], T + bh + 80), (xf, e_in[1], e_in[2]), (fx - el / 2 - 20, e_in[1], e_in[2])], p["eco_tube_od"])
    clips = []
    for zc_ in (D["fb_z0"] + 400, D["fb_z0"] + 850):
        clips.append(bx(xf + p["eco_tube_od"] / 2, D["fb_x0"], e_in[1] - 10, e_in[1] + 10, zc_ - 10, zc_ + 10))
    add("feed", "Feed lines", suction + feed, 19, "bought", "Feed lines")
    add("clips", "Feed line clips (2)", fuse(clips), 19, "made", "Feed lines")

    # drill the bolt and stud holes: each part loses the shanks of the fixings that pass through it
    for k, f in (("skids", "skid_bolts"), ("shell", "roof_bolts"), ("roof", "roof_bolts"), ("eco_box", "eco_bolts"),
                 ("eco_box", "lid_bolts"), ("eco_lid", "lid_bolts"), ("post", "post_bolts"), ("pot", "pot_bolts"),
                 ("glands", "gland_studs"), ("saddles", "saddle_bolts")):
        C[k] = C[k]._replace(shape=C[k].shape - C[f].shape)
    return C


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
               "Firebox, fiber lined", "Monotube steam coil", "Flue-gas economizer", "Chimney and spark arrestor",
               "Steam header and water-seal vent", "Certified relief valve", "Steam hose", "Steam hoods (2)"]


def build_parts(p=PARAMS):
    """{BOM item name: solid} for the main items, in GROUP_ORDER. Fixings are left out."""
    C = build_components(p)
    out = {}
    for g in GROUP_ORDER:
        shapes = [c.shape for c in C.values() if c.group == g]
        if shapes:
            out[g] = fuse(shapes)
    return out


def build(p=PARAMS):
    """Whole assembly as one compound, fixings included."""
    from build123d import Compound
    return Compound(children=[c.shape for c in build_components(p).values()])


MAIN_PARTS = {  # file stem: component keys, for individual exports
    "steamroot-firebox": ["skids", "shell", "roof", "board", "lining", "brackets", "stand", "grate", "door", "hinges", "latch", "damper", "guides", "glands"],
    "steamroot-coil": ["coil", "outlet"],
    "steamroot-header": ["post", "header", "pot", "stay", "diverter", "vent_line", "relief", "discharge"],
    "steamroot-hood": ["hood1", "skirt1", "manifold1", "handles1"],
}


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
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
    chk("Economizer flange on the firebox roof", S("eco_box"), S("roof"), "touch")
    chk("Economizer flange clear of the roof bolts", S("eco_box"), S("roof_bolts"), 3.0)
    chk("Economizer lid on the box", S("eco_lid"), S("eco_box"), "touch")
    chk("Tube bank on its support bars", S("eco_bank"), S("eco_box"), "touch")
    chk("Tube bank clear of the lid", S("eco_bank"), S("eco_lid"), 20.0)
    chk("Chimney over the spigot", S("chimney"), S("eco_lid"), "touch")
    chk("Spark arrestor cap on the chimney", S("cap"), S("chimney"), "touch")
    chk("Jumper on the economizer outlet", S("jumper"), S("eco_bank"), "touch")
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
    }
    return m


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    if "--mass" in sys.argv:
        m = construction_masses()
        for k, v in m.items():
            print(f"  {k:36s} {v:6.1f} kg")
        print(f"  {'total':36s} {sum(m.values()):6.1f} kg")
        sys.exit(0)
    from build123d import export_step, export_stl, Compound
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    C = build_components()
    stl_tol = dict(tolerance=0.5, angular_tolerance=0.3)
    for stem, keys in MAIN_PARTS.items():
        c = Compound(children=[C[k].shape for k in keys])
        export_step(c, str(root / "step" / f"{stem}.step"))
        export_stl(c, str(root / "stl" / f"{stem}.stl"), **stl_tol)
    asm = Compound(children=[c.shape for c in C.values()])
    export_step(asm, str(root / "step" / "steamroot.step"))
    export_stl(asm, str(root / "stl" / "steamroot.stl"), **stl_tol)
    bb = asm.bounding_box()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm "
          f"(x {bb.min.X:.0f} to {bb.max.X:.0f}, y {bb.min.Y:.0f} to {bb.max.Y:.0f}, z {bb.min.Z:.0f} to {bb.max.Z:.0f})")
    D = derived()
    print(f"firebox {PARAMS['fb_l']:.0f} x {PARAMS['fb_w']:.0f} x {PARAMS['fb_h']:.0f} on skids, top {D['fb_top']:.0f}; "
          f"inside floor {D['F']:.0f}; coil {D['cz0'] - PARAMS['tube_od']/2:.0f} to {D['coil_top'] + PARAMS['tube_od']/2:.1f}; ceiling {D['ceil']:.0f}")
    print(f"water seal: dip leg {D['dip']:.0f} mm below the static line at {D['water_line']:.0f}; annulus rise {D['rise']:.0f} mm; "
          f"pot {D['pot_bot']:.0f} to {D['pot_top']:.0f}; header at {D['hz']:.0f}")
    pts = eco_bank_points()
    Lb = sum(math.dist(a, c) for a, c in zip(pts[:-1], pts[1:]))
    print(f"economizer serpentine centreline (square corners) {Lb/1000:.2f} m")
    print_checks()

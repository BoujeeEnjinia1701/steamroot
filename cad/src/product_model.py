"""SteamRoot product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: filleted firebox and economizer casings, a firebox door
with a ceramic glass window onto the fire bed and coil, bolted access panel, stainless chimney with a
spark arrestor cage and rain cap, a teal water-seal pot with a level sight tube, pressure gauge, bronze
relief valve, diverter valve with lever, a strapped feed water drum, pump and alarm enclosure with lit
indicators, trailer detail (mudguards, tail lights, jockey wheel, leaf springs, treaded tyres), two
aluminum steam hoods with stiffening beads and handles, HOT and pressure labels, a soil bed and gravel
pad, and the shared clay mannequin standing at the firebox for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and derived() in model.py: the 960 mm firebox on its
skids with the coil above the fire, the evaporator bank box and economizer above it, the header at 1.55 m on
its post, the seal pot standing on the deck with its overflow to the ground behind the trailer, the
primary and secondary air dampers, the feed lines, and the hood handles on foot plates (updated 2026-10-02
to the constructable design, STR-DDR-003, and the decisions of that day). Axes as model.py: X along the trailer (drawbar at -X,
steam hoods at +X), Y across (front is -Y), Z up from the ground. Units: millimeters.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from math import cos, sin, radians
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Align, Axis, Box, Circle, Compound, Cone, Cylinder, Plane, Pos, RegularPolygon,  # noqa: E402
                       Rot, Sphere, Spline, Text, Torus, extrude, fillet, sweep)
from model import PARAMS, GROUP_ORDER, build_components, derived, fuse, _tube_along  # noqa: E402

TITLE = "SteamRoot: towable wood-fired soil steamer that never holds pressure"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); steam generator on its "
             "trailer at left with the operator at the firebox, two steam hoods on the soil bed at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): trailer and wheels, feed "
             "drum and pump, firebox opened to show the lining, fire bed and monotube coil, evaporator bank box, "
             "economizer, chimney, "
             "steam header with water-seal pot and relief valve, hose and the two steam hoods"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 22, "az": -35,
     "note": "Detail render from the front right and slightly above (about 22 deg elevation): the steam "
             "generator on its trailer, with the fire visible through the door window, the economizer, "
             "chimney and the open water-seal vent beside the header"},
]

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

# Colours (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_FRAME = "#2F343B"
C_DECK = "#8A9099"
C_FIREBOX = "#26282B"
C_STAINLESS = "#B8BEC6"
C_ALU = "#C9CED6"
C_GALV = "#9EA5AD"
C_TYRE = "#1C1F24"
C_RIM = "#A7ADB5"
C_HDPE = "#D9DDE1"
C_STRAP = "#374151"
C_WARN = "#EAB308"
C_INK = "#111827"
C_LINING = "#E8E2D4"
C_GRATE = "#3B3D40"
C_FIRE = "#F97316"
C_WOOD = "#5A3E2B"
C_BRONZE = "#B08D57"
C_HOSE = "#1C1F24"
C_SOIL = "#5B4636"
C_GRAVEL = "#B9B4AB"
C_CLAY = "#9CA3AF"
C_WATER = "#BFDBFE"
C_GLASS = "#EADBC8"
C_FACE = "#F5F5F4"
C_DARK = "#1F2328"
C_ENCL = "#3A3F47"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _cyl_y(r, length, x, y, z):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, length)


def _cyl_x(r, length, x, y, z):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, length)


def _text_front(txt, size, x, y, z, h=1.5):
    """Raised text on a face that looks toward -Y (front), reading along +X; back of the text at y."""
    return Pos(x, y, z) * extrude(Plane.XZ * Text(txt, font_size=size, font_path=FONT,
                                                 align=(Align.CENTER, Align.CENTER)), amount=h)


def _plate_front(w, h, x, y, z, t=2.0, r=6.0):
    """Label plate on a face that looks toward -Y; back of the plate at y."""
    p = Pos(x, y - t / 2, z) * Box(w, t, h)
    return _fillet_try(p, p.edges().filter_by(Axis.Y), [r, r / 2])


def _label_front(lines, w, h, x, y, z, size):
    """Yellow warning plate with raised black text; returns (plate, text)."""
    plate = _plate_front(w, h, x, y, z)
    n = len(lines)
    txt = None
    for i, s in enumerate(lines):
        zz = z + (n - 1) * size * 0.65 - i * size * 1.3
        t = _text_front(s, size, x, y - 2.0, zz, h=1.2)
        txt = t if txt is None else txt + t
    return plate, txt


def _grate(p, deck_top):
    """Grate exactly as model.py."""
    L, Wd, t = p["fb_l"], p["fb_w"], p["fb_shell_t"] + p["fb_lining_t"]
    floor_in = deck_top + t
    g = Pos(p["fb_x"], 0, floor_in + p["grate_z"]) * Box(L - 2 * t - 20, Wd - 2 * t - 20, 20)
    g = g - Pos(p["fb_x"], 0, floor_in + p["grate_z"]) * Box(L - 2 * t - 80, Wd - 2 * t - 80, 30)
    for i in range(-4, 5):
        g = g + Pos(p["fb_x"] + i * 60, 0, floor_in + p["grate_z"]) * Box(15, Wd - 2 * t - 40, 20)
    return g


def _wheel(p, side):
    """Tyre, rim and hub for the wheel at y = side * wy. Returns (tyre, rim)."""
    r, w = p["wheel_r"], p["wheel_w"]
    wy = p["deck_w"] / 2 + w / 2 + p["wheel_gap"]
    tyre = Rot(90, 0, 0) * Cylinder(r, w)
    tyre = _fillet_try(tyre, tyre.edges(), [42.0, 30.0, 20.0])
    tyre -= Rot(90, 0, 0) * Cylinder(158, w + 2)
    # circumferential grooves and lateral tread blocks
    for yy in (-11.0, 11.0):
        tyre -= Pos(0, yy, 0) * Rot(90, 0, 0) * (Cylinder(r + 2, 6) - Cylinder(r - 8, 8))
    blocks = []
    for k in range(40):
        a = 360.0 * k / 40
        blocks.append(Rot(0, a, 0) * Pos(0, 0, r) * Box(9, w * 0.62, 16))
    tyre -= _union(blocks)
    # rim with dish, hub and lug nuts; outer face toward -Y before placement
    rim = Rot(90, 0, 0) * Cylinder(158, w - 14)
    rim -= Pos(0, -(w - 14) / 2 + 12, 0) * Rot(90, 0, 0) * Cylinder(128, 26)
    rim = _fillet_try(rim, rim.edges(), [4.0, 2.0])
    hub = Pos(0, -(w - 14) / 2 + 8, 0) * Rot(90, 0, 0) * Cylinder(55, 36)
    hub = _fillet_try(hub, hub.edges(), [6.0, 3.0])
    rim += hub
    nuts = []
    for k in range(5):
        a = radians(72 * k + 18)
        nuts.append(Pos(38 * cos(a), -(w - 14) / 2 - 12, 38 * sin(a)) * Rot(90, 0, 0) *
                    extrude(RegularPolygon(9, 6), amount=10, both=True))
    rim += _union(nuts)
    rim += Pos(0, -(w - 14) / 2 - 8, 0) * Rot(90, 0, 0) * Cylinder(22, 20)     # hub cap
    loc = Pos(p["axle_x"], side * wy, r) * (Rot(0, 0, 180) if side > 0 else Rot(0, 0, 0))
    return loc * tyre, loc * rim


def product_parts(P=PARAMS):
    p = P
    D = derived(p)
    CM = build_components(p)
    m = {g: fuse([c.shape for c in CM.values() if c.group == g]) for g in GROUP_ORDER}
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    deck_top = p["deck_z"] + p["deck_t"]
    DL, DW = p["deck_l"], p["deck_w"]
    x0 = -DL / 2

    # ------------------------------------------------------------------ 1 trailer
    E_FRAME = (0, 0, -380)
    rails = Pos(0, 0, p["deck_z"] + 35) * (Box(DL, DW, 70) - Box(DL - 160, DW - 160, 72))
    rails = _fillet_try(rails, rails.edges().filter_by(Axis.Z), [12.0, 6.0])
    for xc in (-500.0, 0.0, 500.0):
        rails += Pos(xc, 0, p["deck_z"] + 35) * Box(60, DW - 160, 60)
    # stake pockets on the side rails
    for xs in (-800.0, -300.0, 300.0, 800.0):
        for sy in (-1, 1):
            sp = Pos(xs, sy * (DW / 2 + 15), p["deck_z"] + 35) * (Box(60, 30, 70) - Box(40, 18, 72))
            rails += sp
    drawbar = Pos(x0 - p["drawbar_l"] / 2 + 20, 0, p["deck_z"] + 40) * Box(p["drawbar_l"] + 40, 80, 80)
    drawbar = _fillet_try(drawbar, drawbar.edges().filter_by(Axis.X), [8.0, 4.0])
    rails += drawbar
    # leaf springs and hangers over the axle
    for sy in (-1, 1):
        yy = sy * (DW / 2 - 80)
        spring = Pos(p["axle_x"], yy, 275) * Box(700, 60, 30)
        spring = _fillet_try(spring, spring.edges().filter_by(Axis.Y), [10.0, 5.0])
        rails += spring
        for sx in (-330, 330):
            rails += Pos(p["axle_x"] + sx, yy, 350) * Box(36, 50, 150)
    add("Trailer frame and drawbar", rails, C_FRAME, "painted", 1, "shell", E_FRAME)

    deck = Pos(0, 0, deck_top - 5) * Box(DL, DW, 10)
    deck = _fillet_try(deck, deck.edges().filter_by(Axis.Z), [20.0, 10.0])
    deck = _fillet_try(deck, deck.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
    add("Trailer deck plate", deck, C_DECK, "metal", 1, "shell", E_FRAME)

    axle = _cyl_y(30, DW + 2 * p["wheel_gap"], p["axle_x"], 0, p["wheel_r"])
    add("Axle", axle, C_DARK, "metal", 1, "shell", E_FRAME)

    # coupling head with hand lever
    cx_ = x0 - p["drawbar_l"] - 60
    coup = Pos(cx_, 0, p["deck_z"] + 40) * Box(120, 100, 60)
    coup = _fillet_try(coup, coup.edges(), [14.0, 8.0, 4.0])
    coup += Pos(cx_ - 30, 0, p["deck_z"] + 10) * Sphere(38) & Pos(cx_ - 30, 0, p["deck_z"] + 40) * Box(90, 90, 60)
    lever = Pos(cx_ + 10, 0, p["deck_z"] + 78) * Rot(0, -12, 0) * Box(150, 26, 16)
    lever = _fillet_try(lever, lever.edges(), [6.0, 3.0])
    add("Coupling head", coup, C_DARK, "painted", 1, "shell", E_FRAME)
    add("Coupling lever", lever, C_ACCENT, "painted", 1, "shell", E_FRAME)

    # jockey wheel jack (same axis and height as model.py)
    jx = x0 - p["drawbar_l"] + 150
    jack = Pos(jx, 0, 320) * Cylinder(30, 300)
    jack = _fillet_try(jack, jack.faces().sort_by(Axis.Z)[-1].edges(), [6.0, 3.0])
    jack += Pos(jx, 0, 145) * Cylinder(22, 70)
    jack += Pos(jx, 0, 505) * Cylinder(8, 70)
    crank = Pos(jx + 45, 0, 540) * Box(100, 14, 14) + Pos(jx + 95, 0, 560) * Cylinder(10, 50)
    add("Jockey wheel jack", jack + crank, C_DARK, "painted", 1, "shell", E_FRAME)
    fork = Pos(jx, 0, 95) * (Box(40, 80, 50) - Box(44, 50, 52))
    jw = _cyl_y(58, 40, jx, 0, 60)
    jw = _fillet_try(jw, jw.edges(), [12.0, 6.0])
    add("Jockey wheel fork", fork, C_DARK, "painted", 1, "shell", E_FRAME)
    add("Jockey wheel", jw, C_TYRE, "rubber", 1, "shell", E_FRAME)

    # tail lights and side reflectors
    tl = None
    for sy in (-1, 1):
        body = Pos(DL / 2 + 12, sy * (DW / 2 - 90), p["deck_z"] + 35) * Box(24, 130, 56)
        body = _fillet_try(body, body.edges().filter_by(Axis.X), [8.0, 4.0])
        tl = body if tl is None else tl + body
    add("Tail light housings", tl, C_DARK, "plastic", 1, "shell", E_FRAME)
    lens = None
    for sy in (-1, 1):
        for dy in (-30, 30):
            l_ = Pos(DL / 2 + 25, sy * (DW / 2 - 90) + dy, p["deck_z"] + 35) * Box(4, 50, 40)
            lens = l_ if lens is None else lens + l_
    add("Tail light lenses", lens, "#DC2626", "clear", 1, "shell", E_FRAME)
    refl = None
    for xs in (-900.0, 900.0):
        for sy in (-1, 1):
            r_ = Pos(xs, sy * (DW / 2 + 32), p["deck_z"] + 35) * Box(70, 4, 30)
            refl = r_ if refl is None else refl + r_
    add("Side marker reflectors", refl, "#F59E0B", "clear", 1, "shell", E_FRAME)

    # ------------------------------------------------------------------ 2 wheels and mudguards
    for side, nm in ((-1, "front"), (1, "rear")):
        tyre, rim = _wheel(p, side)
        e = (0, side * 380, -300)
        add(f"Tyre, {nm} side", tyre, C_TYRE, "rubber", 2, "shell", e)
        add(f"Wheel rim, {nm} side", rim, C_RIM, "metal", 2, "shell", e)
    for side in (-1, 1):
        wy = side * (DW / 2 + p["wheel_w"] / 2 + p["wheel_gap"])
        guard = _cyl_y(272, 150, p["axle_x"], wy, p["wheel_r"]) - _cyl_y(262, 152, p["axle_x"], wy, p["wheel_r"])
        guard &= Pos(p["axle_x"], wy, p["wheel_r"] + 200) * Box(700, 160, 400)
        guard += Pos(p["axle_x"], side * (DW / 2 + 6), p["wheel_r"] + 190) * Box(460, 12, 60)
        add(f"Mudguard, {'rear' if side > 0 else 'front'} side", guard, C_ACCENT, "painted", 1, "shell", E_FRAME)

    # ------------------------------------------------------------------ 3 feed water drum
    E_TANK = (-300, 0, 280)
    tz = deck_top + p["tank_r"] + 20
    drum = _cyl_y(p["tank_r"], p["tank_l"], p["tank_x"], 0, tz)
    drum = _fillet_try(drum, drum.edges(), [45.0, 30.0, 15.0])
    for yy in (-150.0, 150.0):                                        # rolling hoops
        drum += _cyl_y(p["tank_r"] + 8, 30, p["tank_x"], yy, tz)
    drum += Pos(p["tank_x"], 60, tz + p["tank_r"] - 5) * Cylinder(55, 40)      # filler boss
    add("Feed water drum, 125 L (HDPE)", drum, C_HDPE, "plastic", 3, "shell", E_TANK)
    capz = tz + p["tank_r"] + 22
    fcap = Pos(p["tank_x"], 60, capz) * Cylinder(48, 22)
    fcap = _fillet_try(fcap, fcap.faces().sort_by(Axis.Z)[-1].edges(), [6.0, 3.0])
    for k in range(12):
        a = 30 * k
        fcap -= Pos(p["tank_x"] + 48 * cos(radians(a)), 60 + 48 * sin(radians(a)), capz) * Cylinder(5, 30)
    add("Drum filler cap", fcap, C_ACCENT, "plastic", 3, "shell", E_TANK)
    # level sight tube on the front end of the drum
    ty0 = -p["tank_l"] / 2 - 26
    sight = Pos(p["tank_x"] + 150, ty0, tz) * Cylinder(10, 360)
    sight -= Pos(p["tank_x"] + 150, ty0, tz) * Cylinder(7, 362)
    add("Drum level sight tube", sight, C_WATER, "clear", 3, "shell", E_TANK)
    water = Pos(p["tank_x"] + 150, ty0, tz - 180 + 130) * Cylinder(6.5, 260)
    add("Drum sight tube water", water, "#60A5FA", "clear", 3, "internal", E_TANK)
    fit = None
    for zz in (tz - 190, tz + 190):
        f_ = Pos(p["tank_x"] + 150, ty0, zz) * Cylinder(14, 22) + _cyl_y(8, 30, p["tank_x"] + 150, ty0 + 14, zz)
        fit = f_ if fit is None else fit + f_
    add("Sight tube fittings", fit, C_STAINLESS, "metal", 3, "shell", E_TANK)
    # cradle with saddle
    cr = Pos(p["tank_x"], 0, deck_top + 60) * Box(2 * p["tank_r"] * 0.8, p["tank_l"] - 80, 120)
    cr -= _cyl_y(p["tank_r"] + 2, p["tank_l"], p["tank_x"], 0, tz)
    cr = _fillet_try(cr, cr.edges().filter_by(Axis.Y), [6.0, 3.0])
    add("Drum cradle", cr, C_FRAME, "painted", 3, "shell", (E_TANK[0], 0, E_TANK[2] - 120))
    # ratchet straps
    straps = None
    for yy in (-230.0, 230.0):
        s_ = _cyl_y(p["tank_r"] + 4, 45, p["tank_x"], yy, tz) - _cyl_y(p["tank_r"] - 1, 47, p["tank_x"], yy, tz)
        s_ &= Pos(p["tank_x"], yy, tz + 100) * Box(700, 60, 2 * p["tank_r"])
        straps = s_ if straps is None else straps + s_
    add("Drum ratchet straps", straps, C_STRAP, "fabric", 3, "shell", E_TANK)
    buck = None
    for yy in (-230.0, 230.0):
        b_ = Pos(p["tank_x"] + p["tank_r"] - 30, yy, tz + 160) * Rot(0, 40, 0) * Box(70, 52, 22)
        buck = b_ if buck is None else buck + b_
    add("Strap ratchets", buck, C_STAINLESS, "metal", 3, "shell", E_TANK)

    # ------------------------------------------------------------------ 4 feed pump and alarm enclosure (BOM 4 and 16)
    E_PUMP = (-150, 420, 180)
    ex, ey, ez = -300.0, 380.0, deck_top + 90
    base = Pos(ex, ey, deck_top + 60) * Box(220, 140, 120)
    base = _fillet_try(base, base.edges().filter_by(Axis.Z), [10.0, 5.0])
    base = _fillet_try(base, base.faces().sort_by(Axis.Z)[0].edges(), [3.0, 1.5])
    add("Pump enclosure base", base, C_ENCL, "plastic", 4, "shell", E_PUMP)
    lid = Pos(ex, ey, deck_top + 150.5) * Box(222, 142, 59)
    lid = _fillet_try(lid, lid.edges().filter_by(Axis.Z), [11.0, 5.0])
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [8.0, 4.0, 2.0])
    for k in range(-3, 4):                                            # cooling ribs on the lid
        lid -= Pos(ex + 24 * k, ey, deck_top + 180) * Box(8, 100, 4)
    add("Pump enclosure lid", lid, C_ACCENT, "plastic", 4, "shell", (E_PUMP[0], E_PUMP[1], E_PUMP[2] + 120))
    scr = None
    for sx in (-95, 95):
        for sy in (-55, 55):
            s_ = Pos(ex + sx, ey + sy, deck_top + 180.5) * Cylinder(5, 1.5)
            scr = s_ if scr is None else scr + s_
    add("Enclosure lid screws", scr, C_STAINLESS, "metal", 4, "shell", (E_PUMP[0], E_PUMP[1], E_PUMP[2] + 120))
    fy = ey - 70
    ind_g = _cyl_y(6, 4, ex - 60, fy - 1, deck_top + 80)
    ind_r = _cyl_y(6, 4, ex - 30, fy - 1, deck_top + 80)
    add("Pump running indicator (lit)", ind_g, "#22C55E", "emissive", 16, "shell", E_PUMP)
    add("Coil alarm indicator", ind_r, "#B91C1C", "plastic", 16, "shell", E_PUMP)
    grill = None
    for k in range(4):
        g_ = Pos(ex + 40 + 12 * k, fy - 1, deck_top + 80) * Box(6, 3, 40)
        grill = g_ if grill is None else grill + g_
    add("Alarm buzzer grille", grill, C_DARK, "plastic", 16, "shell", E_PUMP)
    # feed lines, economizer to bank link and coil inlet jumper: exactly as model.py
    add("Suction hose, feed line, bank link and coil jumper", fuse([CM["feed"].shape, CM["clips"].shape, CM["jumper"].shape, CM["bk_link"].shape]),
        C_STAINLESS, "metal", 19, "shell", (-150, 300, 150))

    # ------------------------------------------------------------------ 5 firebox
    L, Wd, Hh = p["fb_l"], p["fb_w"], p["fb_h"]
    t = p["fb_shell_t"] + p["fb_lining_t"]
    fx = p["fb_x"]
    fb0 = D["fb_z0"]                                   # firebox floor on the skids
    fbz = fb0 + Hh / 2
    door_x0, door_x1 = fx - 190, fx + 190
    door_z0 = D["F"] + p["door_open"][2] - p["door_lap"]
    door_z1 = D["F"] + p["door_open"][2] + p["door_open"][1] + p["door_lap"]
    open_box = Pos(fx, -Wd / 2 + t / 2, (door_z0 + door_z1) / 2) * Box(300, t + 20, 240)
    E_FB = (0, -700, 0)
    outer = Pos(fx, 0, fbz) * Box(L, Wd, Hh)
    outer = _fillet_try(outer, outer.edges().filter_by(Axis.Z), [14.0, 8.0])
    shell = outer - Pos(fx, 0, fbz) * Box(L - 2 * p["fb_shell_t"], Wd - 2 * p["fb_shell_t"], Hh - 2 * p["fb_shell_t"])
    shell -= Pos(fx, 0, fb0 + Hh - t / 2) * Cylinder(p["chimney_d"] / 2, t + 2)
    shell -= open_box
    # angle-iron bands top and bottom (weld seams read as parting lines)
    for zb in (fb0 + 20, fb0 + Hh - 20):
        band = Pos(fx, 0, zb) * Box(L + 12, Wd + 12, 40) - Pos(fx, 0, zb) * Box(L - 2, Wd - 2, 42)
        band = _fillet_try(band, band.edges().filter_by(Axis.Z), [18.0, 10.0])
        shell += band
    shell -= open_box
    add("Firebox shell (high-temperature black)", shell, C_FIREBOX, "painted", 5, "shell", E_FB)
    lining = Pos(fx, 0, fbz) * (Box(L - 2 * p["fb_shell_t"], Wd - 2 * p["fb_shell_t"], Hh - 2 * p["fb_shell_t"])
                                - Box(L - 2 * t, Wd - 2 * t, Hh - 2 * t))
    lining -= Pos(fx, 0, fb0 + Hh - t / 2) * Cylinder(p["chimney_d"] / 2, t + 2)
    lining -= open_box
    add("Ceramic fiber lining", lining, C_LINING, "paper", 5, "internal", (0, 0, 0))
    add("Cast grate", _grate(p, fb0), C_GRATE, "metal", 5, "internal", (0, 0, 0))
    skids = None
    for xs in (fx - p["skid_dx"], fx + p["skid_dx"]):
        sk_ = Pos(xs, 0, deck_top + p["skid"] / 2) * Box(p["skid"], DW, p["skid"])
        skids = sk_ if skids is None else skids + sk_
    add("Firebox skids", skids, C_FRAME, "painted", 17, "shell", (0, 0, -150))
    floor_in = D["F"]
    bed_z = floor_in + p["grate_z"] + 10
    embers = Pos(fx, 0, bed_z + 12) * Box(L - 2 * t - 120, Wd - 2 * t - 140, 24)
    embers = _fillet_try(embers, embers.edges(), [10.0, 5.0])
    add("Fire bed (glowing)", embers, C_FIRE, "emissive", None, "internal", (0, 0, 0))
    logs = None
    for yy, zz, rr in ((-70, bed_z + 60, 40), (70, bed_z + 60, 40), (0, bed_z + 125, 36)):
        lg = _cyl_x(rr, 300, fx, yy, zz)
        lg = _fillet_try(lg, lg.edges(), [8.0, 4.0])
        logs = lg if logs is None else logs + lg
    add("Wood charge", logs, C_WOOD, "wood", None, "internal", (0, 0, 0))

    # door with ceramic glass window, hinges and latch
    E_DOOR = (0, -1050, 0)
    dz = (door_z0 + door_z1) / 2
    door = Pos(fx, -Wd / 2 - 10, dz) * Box(380, 20, 300)
    door = _fillet_try(door, door.edges().filter_by(Axis.Y), [14.0, 8.0])
    door = _fillet_try(door, door.faces().sort_by(Axis.Y)[0].edges(), [4.0, 2.0])
    door -= Pos(fx, -Wd / 2 - 10, dz + 20) * Box(170, 30, 110)
    frame = Pos(fx, -Wd / 2 - 22, dz + 20) * (Box(200, 6, 140) - Box(168, 8, 108))
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.Y), [6.0, 3.0])
    door += frame
    add("Firebox door", door, C_FIREBOX, "painted", 5, "shell", E_DOOR)
    glass = Pos(fx, -Wd / 2 - 8, dz + 20) * Box(176, 6, 116)
    add("Ceramic glass window", glass, C_GLASS, "clear", 5, "shell", E_DOOR)
    hinges = None
    for zz in (door_z0 + 50, door_z1 - 50):
        h_ = Pos(door_x0 - 8, -Wd / 2 - 18, zz) * Cylinder(10, 60)
        hinges = h_ if hinges is None else hinges + h_
    latch = Pos(door_x1 - 40, -Wd / 2 - 30, dz) * Cylinder(14, 12, rotation=(90, 0, 0))
    latch += Pos(door_x1 - 40, -Wd / 2 - 45, dz - 50) * Box(18, 18, 110)
    add("Door hinges and latch", hinges + latch, C_STAINLESS, "metal", 5, "shell", E_DOOR)
    grip = Pos(door_x1 - 40, -Wd / 2 - 45, dz - 70) * Cylinder(14, 80)
    grip = _fillet_try(grip, grip.edges(), [5.0, 3.0])
    add("Latch grip (hardwood)", grip, "#8B5E3C", "wood", 5, "shell", E_DOOR)
    # primary air damper: slotted slide plate under the door (model.py position)
    dmp_z = D["F"] + p["air_open"][2] + p["air_open"][1] / 2
    dmp = Pos(fx, -Wd / 2 - 5, dmp_z) * Box(160, 10, 60)
    dmp = _fillet_try(dmp, dmp.edges().filter_by(Axis.Y), [8.0, 4.0])
    for k in range(-2, 3):
        dmp -= Pos(fx + 28 * k, -Wd / 2 - 5, dmp_z) * Box(12, 14, 36)
    dknob = _cyl_y(10, 20, fx + 70, -Wd / 2 - 20, dmp_z)
    add("Primary air damper plate", dmp, C_GRATE, "metal", 5, "shell", E_FB)
    add("Primary air damper knob", dknob, C_ACCENT, "plastic", 5, "shell", E_FB)
    # secondary air damper slide on the door, above the window line (model.py position)
    s2w, s2h, s2b = p["air2_open"]
    d2z = D["F"] + s2b + s2h / 2
    d2 = Pos(fx, -Wd / 2 - 24, d2z) * Box(s2w + 40, 6, 50)
    d2 = _fillet_try(d2, d2.edges().filter_by(Axis.Y), [6.0, 3.0])
    add("Secondary air damper slide", d2, C_GRATE, "metal", 5, "shell", E_DOOR)
    add("Secondary air damper knob", _cyl_y(8, 16, fx - s2w / 2 - 5, -Wd / 2 - 43, d2z), C_ACCENT, "plastic", 5, "shell", E_DOOR)
    # HOT label above the door
    pl, tx = _label_front(["HOT SURFACE", "DO NOT TOUCH"], 250, 90, fx, -Wd / 2, door_z1 + 120, 22)
    add("HOT label plate (firebox)", pl, C_WARN, "painted", 5, "shell", E_FB)
    add("HOT label text (firebox)", tx, C_INK, "plastic", 5, "shell", E_FB)
    # pipe glands where the coil ends leave the +X wall
    gl = None
    r_ = p["coil_mean_d"] / 2
    cz0 = D["cz0"]
    ztop = D["coil_top"]
    for zz, rr in ((cz0, 22), (ztop, 28)):
        g_ = _cyl_x(rr, 16, fx + L / 2 + 8, 0, zz) - _cyl_x(p["tube_od"] / 2 * 0.6 if zz == cz0 else p["tube_od"] / 2, 20, fx + L / 2 + 8, 0, zz)
        gl = g_ if gl is None else gl + g_
    add("Pipe glands", gl, C_STAINLESS, "metal", 5, "shell", E_FB)

    # ------------------------------------------------------------------ 6 coil (exactly model.py)
    add("Monotube steam coil (316 stainless)", m["Monotube steam coil"], C_STAINLESS, "metal", 6, "internal", (0, 0, 800))

    # ------------------------------------------------------------------ 22 evaporator bank box (model.py envelope)
    E_BK = (0, 0, 1150)
    bz0, bh = D["bk_z0"], p["bk_h"]
    bkc = Pos(fx, 0, bz0 + bh / 2) * Box(L, Wd, bh)
    bkc = _fillet_try(bkc, bkc.edges().filter_by(Axis.Z), [14.0, 8.0])
    bkc -= Pos(fx, 0, bz0 + bh / 2) * Box(L - 4, Wd - 4, bh + 2)
    bkc += Pos(fx, 0, bz0 + bh - 1) * Box(L, Wd, 2)
    bkc += Pos(fx, 0, bz0 + 12.5) * Box(L + 50, Wd + 50, 25) - Pos(fx, 0, bz0 + 12.5) * Box(L - 2, Wd - 2, 27)
    add("Evaporator bank box", bkc, C_FIREBOX, "painted", 22, "shell", E_BK)
    add("Evaporator bank (316 stainless)", CM["bk_bank"].shape, C_STAINLESS, "metal", 22, "internal", E_BK)

    # ------------------------------------------------------------------ 7 economizer
    E_ECO = (0, 0, 1450)
    ez = D["eco_floor"] + p["eco_h"] / 2
    ebox = Pos(fx, 0, ez) * Box(p["eco_l"], p["eco_w"], p["eco_h"])
    ebox = _fillet_try(ebox, ebox.edges().filter_by(Axis.Z), [16.0, 8.0])
    ebox = _fillet_try(ebox, ebox.faces().sort_by(Axis.Z)[-1].edges(), [8.0, 4.0])
    add("Economizer casing", ebox, "#9AA1A9", "metal", 7, "shell", E_ECO)
    fl = Pos(fx, 0, D["eco_z0"] + 3) * Box(p["eco_l"] + 30, p["eco_w"] + 30, 6)
    fl = _fillet_try(fl, fl.edges().filter_by(Axis.Z), [18.0, 10.0])
    add("Economizer base flange", fl, C_FRAME, "painted", 7, "shell", (0, 0, 1150))
    ey0 = -p["eco_w"] / 2
    panel = _plate_front(p["eco_l"] - 80, p["eco_h"] - 70, fx, ey0, ez, t=4.0, r=10.0)
    add("Economizer access panel", panel, C_STAINLESS, "metal", 7, "shell", E_ECO)
    bolts = None
    for bx in (-200, -67, 67, 200):
        for bz in (-80, 80):
            b_ = _cyl_y(7, 6, fx + bx, ey0 - 7, ez + bz)
            bolts = b_ if bolts is None else bolts + b_
    add("Access panel bolts", bolts, C_DARK, "metal", 7, "shell", E_ECO)
    brand = _text_front("STEAMROOT", 34, fx, ey0 - 4, ez, h=1.5)
    add("STEAMROOT mark", brand, C_ACCENT, "painted", None, "shell", E_ECO)
    # internal tube bank (8 m of 12.7 mm tube, drawn as straight passes)
    bank = None
    for i in range(4):
        for j in range(4):
            tb = _cyl_x(p["eco_tube_od"] / 2, p["eco_l"] - 60, fx, -150 + 100 * j, ez - 90 + 60 * i)
            bank = tb if bank is None else bank + tb
    add("Economizer tube bank", bank, "#C7A36A", "metal", 7, "internal", (0, 0, 1150))
    drain = _cyl_x(10, 60, fx - p["eco_l"] / 2 - 30, 0, D["eco_floor"] + 24)
    drain += _cyl_x(16, 30, fx - p["eco_l"] / 2 - 55, 0, D["eco_floor"] + 24)
    add("Condensate drain valve", drain, C_BRONZE, "metal", 7, "shell", E_ECO)
    dlever = Pos(fx - p["eco_l"] / 2 - 55, -30, D["eco_floor"] + 46) * Box(14, 70, 8)
    add("Drain valve lever", dlever, C_ACCENT, "painted", 7, "shell", E_ECO)

    # ------------------------------------------------------------------ 8 chimney and spark arrestor
    E_CH = (0, 0, 1900)
    cb = D["eco_top"]
    ch_top = p["chimney_top"] - p["cap_h"]
    ch_len = ch_top - cb
    rch = p["chimney_d"] / 2
    chim = Pos(fx, 0, cb + ch_len / 2) * Cylinder(rch, ch_len)
    chim += Pos(fx, 0, cb + 30) * Cylinder(rch + 18, 60)                  # base collar
    chim += Pos(fx, 0, cb + ch_len * 0.55) * Cylinder(rch + 6, 24)         # joint band
    chim = _fillet_try(chim, chim.edges(), [3.0, 1.5])
    add("Chimney flue (stainless)", chim, C_STAINLESS, "metal", 8, "shell", E_CH)
    rc = rch + 45
    cage = Pos(fx, 0, ch_top + 6) * (Cylinder(rc, 12) - Cylinder(rch - 4, 14))
    cage += Pos(fx, 0, ch_top + 82) * (Cylinder(rc, 10) - Cylinder(rc - 12, 12))
    for k in range(16):
        a = radians(22.5 * k)
        cage += Pos(fx + (rc - 5) * cos(a), (rc - 5) * sin(a), ch_top + 44) * Cylinder(4, 76)
    add("Spark arrestor cage", cage, C_STAINLESS, "metal", 8, "shell", E_CH)
    mesh = Pos(fx, 0, ch_top + 44) * (Cylinder(rc - 10, 76) - Cylinder(rc - 13, 78))
    add("Spark arrestor mesh (6 mm)", mesh, C_DARK, "metal", 8, "shell", E_CH)
    rain = Pos(fx, 0, ch_top + 87 + 16.5) * Cone(rc + 8, 26, 33)
    add("Rain cap", rain, C_STAINLESS, "metal", 8, "shell", E_CH)

    # ------------------------------------------------------------------ 9 steam header, seal pot, vent, diverter
    E_HDR = (450, -450, 350)
    hx = fx + L / 2 + p["header_dx"]
    hz = p["header_z"]
    ho = p["header_od"] / 2
    header = _cyl_y(ho, p["header_len"], hx, 0, hz)
    header += _cyl_y(ho + 10, 18, hx, p["header_len"] / 2 - 9, hz)
    header = _fillet_try(header, header.edges(), [3.0, 1.5])
    add("Steam header, DN50", header, C_STAINLESS, "metal", 9, "shell", E_HDR)
    pot_y = -p["header_len"] / 2 - p["seal_pot_od"] / 2 - 10
    pot_top = D["pot_top"]
    pot_bot = D["pot_bot"]
    rp = p["seal_pot_od"] / 2
    pot = Pos(hx, pot_y, (pot_top + pot_bot) / 2) * Cylinder(rp, pot_top - pot_bot)
    pot = _fillet_try(pot, pot.edges(), [8.0, 4.0])
    for zz in (pot_top - 40, pot_bot + 50):
        pot += Pos(hx, pot_y, zz) * Cylinder(rp + 6, 16)
    add("Water-seal pot on the deck, 890 mm dip leg", pot, C_ACCENT, "painted", 9, "shell", E_HDR)
    foot = Pos(hx, pot_y, deck_top + 5) * Box(p["foot"][0], p["foot"][0], p["foot"][1])
    add("Seal pot foot plate", foot, C_FRAME, "painted", 17, "shell", E_HDR)
    add("Seal pot overflow with loop seal (galvanized)", fuse([CM["overflow"].shape, CM["ovf_stay"].shape, CM["ovf_clip"].shape]),
        C_GALV, "metal", 9, "shell", (450, -650, 0))
    sy_ = pot_y - rp - 16
    sz_ = D["water_line"] - 250
    stube = Pos(hx + 30, sy_, sz_) * (Cylinder(9, 700) - Cylinder(6.5, 702))
    add("Seal level sight tube", stube, C_WATER, "clear", 9, "shell", E_HDR)
    swater = Pos(hx + 30, sy_, (sz_ - 340 + D["water_line"]) / 2) * Cylinder(6, D["water_line"] - sz_ + 340)
    add("Seal water column", swater, "#60A5FA", "clear", 9, "internal", E_HDR)
    sfit = None
    for zz in (sz_ - 360, sz_ + 360):
        f_ = Pos(hx + 30, sy_, zz) * Cylinder(13, 22) + Pos(hx + 15, sy_ + 8, zz) * Box(30, 16, 12)
        sfit = f_ if sfit is None else sfit + f_
    add("Sight tube valves", sfit, C_BRONZE, "metal", 9, "shell", E_HDR)
    link = _cyl_y(20, abs(pot_y + p["header_len"] / 2), hx, (pot_y - p["header_len"] / 2) / 2, hz)
    vent = Pos(hx, pot_y, (pot_top + p["vent_top"]) / 2 - 20) * Cylinder(p["vent_od"] / 2, p["vent_top"] - pot_top - 40)
    vent += Pos(hx, pot_y, p["vent_top"] - 20) * Cylinder(p["vent_od"] / 2 + 18, 40) \
        - Pos(hx, pot_y, p["vent_top"] - 30) * Cylinder(p["vent_od"] / 2, 30)
    add("Vent pipe, DN32, to 2.3 m", link + vent, C_STAINLESS, "metal", 9, "shell", E_HDR)
    # diverter: body, lever and quick coupling (outlet face at the model's hose start)
    dvy = D["div_y"]                                   # diverter on the back end of the header, as model.py
    dv = Pos(hx, dvy, hz) * Box(70, 90, 70)
    dv = _fillet_try(dv, dv.edges(), [12.0, 8.0, 4.0])
    add("Three-way diverter valve", dv, C_BRONZE, "metal", 9, "shell", E_HDR)
    dl = Pos(hx, dvy, hz + 40) * Cylinder(10, 12) + Pos(hx + 45, dvy, hz + 50) * Rot(0, -10, 0) * Box(110, 18, 10)
    dl = _fillet_try(dl, dl.edges().filter_by(Axis.Z), [4.0, 2.0])
    add("Diverter lever", dl, C_ACCENT, "painted", 9, "shell", E_HDR)
    add("Diverter vent line", CM["vent_line"].shape, C_STAINLESS, "metal", 20, "shell", E_HDR)
    qc = _cyl_x(22, 40, hx + 55, dvy, hz)
    add("Steam quick coupling", qc, C_STAINLESS, "metal", 9, "shell", E_HDR)
    # header post and pot stay, exactly as model.py
    add("Header post and pot stay", fuse([CM["post"].shape, CM["stay"].shape]), C_FRAME, "painted", 17, "shell", E_HDR)
    # pressure gauge on a siphon (BOM 14), dial facing -Y
    gy = -60.0
    gz = hz + 140
    siph = Pos(hx, gy, hz + ho + 20) * Cylinder(8, 40) + Pos(hx, gy, gz - 60) * Torus(18, 5) \
        + Pos(hx, gy, gz - 50) * Cylinder(8, 30)
    add("Gauge siphon", siph, C_BRONZE, "metal", 14, "shell", E_HDR)
    case = _cyl_y(52, 34, hx, gy, gz)
    case = _fillet_try(case, case.edges(), [6.0, 3.0])
    case -= _cyl_y(46, 10, hx, gy - 14, gz)
    add("Pressure gauge case", case, C_STAINLESS, "metal", 14, "shell", E_HDR)
    face = _cyl_y(46, 2, hx, gy - 10, gz)
    add("Gauge dial, 0 to 1 bar", face, C_FACE, "paper", 14, "shell", E_HDR)
    marks = None
    for k in range(11):
        a = radians(225 - 27 * k)
        mk = Pos(hx + 38 * cos(a), gy - 11.5, gz + 38 * sin(a)) * Rot(0, -(225 - 27 * k), 0) * Box(8, 1.0, 2)
        marks = mk if marks is None else marks + mk
    add("Gauge scale marks", marks, C_INK, "plastic", 14, "shell", E_HDR)
    redz = None
    for k in range(3):
        a = radians(225 - 27 * (8 + k))
        rz = Pos(hx + 33 * cos(a), gy - 11.8, gz + 33 * sin(a)) * Rot(0, -(225 - 27 * (8 + k)), 0) * Box(5, 1.0, 12)
        redz = rz if redz is None else redz + rz
    add("Gauge red zone", redz, "#DC2626", "plastic", 14, "shell", E_HDR)
    a0 = radians(225 - 27 * 0.4)
    needle = Pos(hx + 17 * cos(a0), gy - 12.5, gz + 17 * sin(a0)) * Rot(0, -(225 - 27 * 0.4), 0) * Box(36, 1.2, 2.5)
    needle += _cyl_y(4, 3, hx, gy - 12.5, gz)
    add("Gauge needle", needle, "#DC2626", "plastic", 14, "shell", E_HDR)
    gglass = _cyl_y(47, 2, hx, gy - 15, gz)
    add("Gauge glass", gglass, "#E5EEF5", "clear", 14, "shell", E_HDR)
    # pressure label on the seal pot
    pl, tx = _label_front(["OPEN VENT", "0.1 BAR MAX", "NEVER PLUG"], 110, 120, hx, pot_y - rp - 1, hz - 560, 14)
    add("Pressure label plate (seal pot)", pl, C_WARN, "painted", 9, "shell", E_HDR)
    add("Pressure label text (seal pot)", tx, C_INK, "plastic", 9, "shell", E_HDR)

    # ------------------------------------------------------------------ 10 relief valve
    E_RV = (450, -150, 650)
    rv_y = 60.0                                        # as model.py
    add("Relief discharge pipe to 2.3 m", CM["discharge"].shape, C_STAINLESS, "metal", 20, "shell", E_RV)
    rvb = Pos(hx, rv_y, hz + 90) * Cylinder(p["relief_d"] / 2, 120)
    rvb = _fillet_try(rvb, rvb.faces().sort_by(Axis.Z)[-1].edges(), [10.0, 5.0])
    rvb += Pos(hx, rv_y, hz + 38) * extrude(RegularPolygon(26, 6), amount=16, both=True)
    rvb += _cyl_x(18, 50, hx + p["relief_d"] / 2 + 15, rv_y, hz + 70)
    rvb += Pos(hx, rv_y, hz + 190) * Cylinder(20, 80)
    rvb = _fillet_try(rvb, rvb.faces().sort_by(Axis.Z)[-1].edges(), [5.0, 2.0])
    add("Certified relief valve, 15 psi", rvb, C_BRONZE, "metal", 10, "shell", E_RV)
    rlev = Pos(hx - 30, rv_y, hz + 215) * Rot(0, -20, 0) * Box(80, 10, 8)
    add("Relief valve test lever", rlev, C_STAINLESS, "metal", 10, "shell", E_RV)
    tag = Pos(hx, rv_y - p["relief_d"] / 2 - 2, hz + 120) * Box(34, 2, 22)
    add("Relief valve set-pressure tag", tag, "#DC2626", "painted", 10, "shell", E_RV)

    # ------------------------------------------------------------------ 12 hoods and 11 hose (accessory group)
    hl, hw, hh, ins = p["hood_l"], p["hood_w"], p["hood_h"], p["hood_ins_t"]
    hood_x0 = DL / 2 + p["hood_offset"]
    inlets = []
    for i in range(int(p["n_hoods"])):
        cx = hood_x0 + hl / 2 + i * (hl + p["hood_gap"])
        e = (700 + 250 * i, 0, 0)
        outer = Pos(cx, 0, hh / 2) * Box(hl, hw, hh)
        outer = _fillet_try(outer, outer.edges().filter_by(Axis.Z), [30.0, 15.0])
        outer = _fillet_try(outer, outer.faces().sort_by(Axis.Z)[-1].edges(), [16.0, 8.0])
        for k in range(-2, 3):                                            # stiffening beads on the top skin
            bead = Pos(cx + 200 * k, 0, hh) * Rot(90, 0, 0) * Cylinder(10, hw - 140)
            bead = _fillet_try(bead, bead.edges(), [4.0, 2.0])
            outer += bead
        body = outer - Pos(cx, 0, hh / 2 - ins / 2) * Box(hl - 2 * ins, hw - 2 * ins, hh)
        add(f"Steam hood {i + 1} (aluminum double skin)", body, C_ALU, "metal", 12, "accessory", e)
        skirt = Pos(cx, 0, -p["skirt_depth"] / 2) * (Box(hl, hw, p["skirt_depth"]) - Box(hl - 6, hw - 6, p["skirt_depth"] + 2))
        add(f"Steam hood {i + 1} soil skirt", skirt, C_GALV, "metal", 12, "accessory", e)
        man = _cyl_x(15, hl - 2 * ins - 40, cx, 0, hh - ins - 30)
        add(f"Steam hood {i + 1} perforated manifold", man, C_STAINLESS, "metal", 12, "accessory", e)
        ix = cx - hl / 2 + 150
        inl = Pos(ix, 0, hh + 40) * Cylinder(20, 80)
        inl += Pos(ix, 0, hh + 8) * extrude(RegularPolygon(34, 6), amount=16, both=True)
        add(f"Steam hood {i + 1} inlet coupling", inl, C_STAINLESS, "metal", 12, "accessory", e)
        inlets.append((ix, 0, hh + 80))
        hdl = None
        hts = p["handle_tube"][0]
        fpw, fpt = p["handle_foot"]
        for sy in (1, -1):                                 # 30 mm square bar on standoffs and foot plates (ballast rated)
            yy = sy * (hw / 2 + 60)
            bar = Pos(cx, yy, hh - 60) * Box(900, hts, hts)
            bar = _fillet_try(bar, bar.edges().filter_by(Axis.X), [4.0, 2.0])
            for sx in (-400, 400):
                bar += Pos(cx + sx, sy * (hw / 2 + (fpt + 60 - hts / 2) / 2), hh - 60) * Box(30, 60 - hts / 2 - fpt + 1, 30)
                bar += Pos(cx + sx, sy * (hw / 2 + fpt / 2), hh - 60) * Box(fpw, fpt, fpw)
            hdl = bar if hdl is None else hdl + bar
        add(f"Steam hood {i + 1} handles", hdl, C_DARK, "painted", 12, "accessory", e)
        pl, tx = _label_front(["HOT STEAM"], 220, 60, cx + 250, -hw / 2, 110, 24)
        add(f"HOT label plate (hood {i + 1})", pl, C_WARN, "painted", 12, "accessory", e)
        add(f"HOT label text (hood {i + 1})", tx, C_INK, "plastic", 12, "accessory", e)
        add(f"Steam hood {i + 1} accent band", Pos(cx - 350, -hw / 2 - 1, 110) * Box(120, 2, 60),
            C_ACCENT, "painted", 12, "accessory", e)

    # 11 hose: smooth run from the diverter coupling (model start point) to the first hood inlet (model end point)
    hs = (hx + 75, dvy, hz)
    mi = inlets[0]
    pts = [hs, (hs[0] + 140, dvy, hz - 40), (hs[0] + 260, dvy - 40, hz - 420), (hs[0] + 330, dvy - 120, 700),
           (hs[0] + 420, -160, 420), (mi[0] - 180, -110, 470), (mi[0] - 30, -20, 470), (mi[0], 0, mi[2] + 60),
           (mi[0], 0, mi[2])]
    try:
        path = Spline(*pts)
        prof = Plane(origin=path @ 0, z_dir=path % 0) * Circle(p["hose_od"] / 2)
        hose = sweep(prof, path)
        if not hose.is_valid:
            raise ValueError
    except Exception:
        hose = m["Steam hose"]
    add("Steam hose, EPDM 25 mm", hose, C_HOSE, "rubber", 11, "accessory", (500, -150, 150))
    ferr = _cyl_x(p["hose_od"] / 2 + 5, 50, hs[0] + 22, dvy, hz) + Pos(mi[0], 0, mi[2] + 25) * Cylinder(p["hose_od"] / 2 + 5, 50)
    add("Hose ferrules", ferr, C_STAINLESS, "metal", 11, "accessory", (500, -150, 150))

    # ------------------------------------------------------------------ context: soil bed, gravel pad, operator
    bx0, bx1 = hood_x0 - 150, hood_x0 + 2 * hl + p["hood_gap"] + 150
    bed = Pos((bx0 + bx1) / 2, 0, -40) * Box(bx1 - bx0, hw + 400, 80)
    bed = _fillet_try(bed, bed.edges().filter_by(Axis.Z), [60.0, 30.0])
    for k in range(int((bx1 - bx0) // 120)):                               # shallow furrows at the bed ends
        xk = bx0 + 60 + 120 * k
        for sy in (-1, 1):
            bed -= Pos(xk, sy * (hw / 2 + 150), 0) * Box(30, 100, 16)
    add("Soil bed", bed, C_SOIL, "fabric", None, "context", (0, 0, 0))
    gx0, gx1 = x0 - p["drawbar_l"] - 200, bx0 - 10
    pad = Pos((gx0 + gx1) / 2, -200, -40) * Box(gx1 - gx0, DW + 800, 80)
    pad = _fillet_try(pad, pad.edges().filter_by(Axis.Z), [80.0, 40.0])
    add("Gravel pad", pad, C_GRAVEL, "paper", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(-20, -930, 0) * Rot(0, 0, 157) * mannequin(1750, "stand", head_tilt=-8.0)
    add("Operator at the firebox, 1.75 m (clay mannequin)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:48s} {q['group']:9s} {q['material']:8s} valid={s.is_valid}")

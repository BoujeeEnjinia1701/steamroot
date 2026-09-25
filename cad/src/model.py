"""SteamRoot parametric model (build123d), TRL 3 general arrangement.

Run from the repo root:  python cad/src/model.py
Exports the assembly and the main parts as STEP and STL into cad/step and cad/stl.

Level of detail: massing plus. Main dimensions and interfaces (coil inlet and outlet,
header, water-seal pot, hose, hood manifold) are correct; fabrication detail is not.
PRELIMINARY, NOT FOR FABRICATION. The regulatory ruling from the local boiler authority
is an open prerequisite (see docs/REVIEW.md).

Axes: X along the trailer (drawbar at -X, steam hoods at +X), Y across, Z up from the ground.
Units: millimeters.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
# docs/04-calcs/sizing.py imports this dictionary, so the calculation and the model share one source.
PARAMS = {
    # Trailer (used single-axle garden or utility trailer)
    "deck_l": 2000.0, "deck_w": 1200.0, "deck_t": 80.0, "deck_z": 420.0,
    "wheel_r": 230.0, "wheel_w": 120.0, "wheel_gap": 20.0, "axle_x": 150.0, "drawbar_l": 800.0,
    # Feed water tank, 125 L HDPE drum lying across the deck
    "tank_r": 250.0, "tank_l": 640.0, "tank_x": -700.0, "tank_volume_l": 125.0,
    # Firebox: 3 mm steel shell, ceramic fiber board lining
    "fb_l": 700.0, "fb_w": 600.0, "fb_h": 650.0, "fb_x": 250.0,
    "fb_shell_t": 3.0, "fb_lining_t": 50.0, "grate_z": 60.0,
    # Monotube coil: 316 stainless, 25.4 mm OD x 1.65 mm wall, wound around the fire bed
    "coil_mean_d": 420.0, "tube_od": 25.4, "tube_wall": 1.65, "coil_turns": 11, "coil_pitch": 40.0,
    "coil_z0": 90.0,          # bottom of the coil above the inside of the firebox floor
    # Flue-gas economizer box on top of the firebox (8 m of 12.7 mm x 1.2 mm stainless tube inside)
    "eco_l": 520.0, "eco_w": 460.0, "eco_h": 260.0, "eco_tube_od": 12.7, "eco_tube_wall": 1.2, "eco_tube_len": 8000.0,
    # Chimney with spark arrestor cap
    "chimney_d": 150.0, "chimney_top": 2400.0, "cap_h": 120.0,
    # Steam header (DN50) above the economizer, water-seal pot (1 m seal) and vent pipe
    "header_od": 60.3, "header_len": 300.0, "header_z": 1600.0, "header_dx": 130.0,
    "seal_depth": 1000.0, "seal_pot_od": 114.3, "vent_od": 42.2, "vent_top": 2300.0,
    "relief_d": 70.0,
    # Steam hose, 25 mm bore, 6 m
    "hose_od": 44.0, "hose_len": 6000.0,
    # Steam hoods (two, used alternately): open-bottom insulated pans
    "hood_l": 1200.0, "hood_w": 1000.0, "hood_h": 250.0, "hood_ins_t": 40.0, "hood_skin_t": 1.0,
    "skirt_depth": 60.0, "hood_gap": 150.0, "hood_offset": 400.0, "n_hoods": 2,
}


def _tube_along(points, od):
    """Round tube through a polyline of (x, y, z) points (massing; square joints)."""
    from build123d import Cylinder, Vector, Sphere, Pos, Plane
    out = None
    for a, b in zip(points[:-1], points[1:]):
        a, b = Vector(*a), Vector(*b)
        d = b - a
        pl = Plane(origin=(a + b) * 0.5, z_dir=d.normalized())
        seg = pl * Cylinder(od / 2, d.length)
        joint = Pos(*b) * Sphere(od / 2)
        out = seg + joint if out is None else out + seg + joint
    return out


def build_parts(p=PARAMS):
    """Return an ordered dict {part name: build123d shape}. Names match the BOM items."""
    from build123d import (Box, Cylinder, Pos, Rot, Helix, Plane, Circle, sweep)
    parts = {}
    deck_top = p["deck_z"] + p["deck_t"]

    # 1 Trailer frame, drawbar and jack
    frame = Pos(0, 0, p["deck_z"] + p["deck_t"] / 2) * Box(p["deck_l"], p["deck_w"], p["deck_t"])
    frame = frame - Pos(0, 0, p["deck_z"] + p["deck_t"] / 2 - 10) * Box(p["deck_l"] - 160, p["deck_w"] - 160, p["deck_t"])
    frame = frame + Pos(0, 0, deck_top - 5) * Box(p["deck_l"], p["deck_w"], 10)          # deck plate
    x0 = -p["deck_l"] / 2
    drawbar = (Pos(x0 - p["drawbar_l"] / 2, 0, p["deck_z"] + 40) * Box(p["drawbar_l"], 80, 80)
               + Pos(x0 - p["drawbar_l"] - 60, 0, p["deck_z"] + 40) * Box(120, 100, 60))   # coupling
    jack = Pos(x0 - p["drawbar_l"] + 150, 0, p["deck_z"] / 2) * Cylinder(30, p["deck_z"])
    axle = Pos(p["axle_x"], 0, p["wheel_r"]) * Rot(90, 0, 0) * Cylinder(30, p["deck_w"] + 2 * p["wheel_gap"])
    parts["Trailer frame and drawbar"] = frame + drawbar + jack + axle

    # 2 Wheels
    wy = p["deck_w"] / 2 + p["wheel_w"] / 2 + p["wheel_gap"]
    wheel = lambda y: Pos(p["axle_x"], y, p["wheel_r"]) * Rot(90, 0, 0) * Cylinder(p["wheel_r"], p["wheel_w"])
    parts["Wheels"] = wheel(wy) + wheel(-wy)

    # 3 Feed water tank
    tz = deck_top + p["tank_r"] + 20
    tank = Pos(p["tank_x"], 0, tz) * Rot(90, 0, 0) * Cylinder(p["tank_r"], p["tank_l"])
    cradle = Pos(p["tank_x"], 0, deck_top + 60) * Box(2 * p["tank_r"] * 0.8, p["tank_l"] - 80, 120)
    parts["Feed water tank, 125 L"] = tank + cradle

    # 4 Feed pump (12 V diaphragm) with battery tray beside it
    parts["Feed pump"] = Pos(-300, 380, deck_top + 90) * Box(220, 140, 180)

    # 5 Firebox: steel shell, fiber lining, grate, door and air damper
    L, Wd, Hh, t = p["fb_l"], p["fb_w"], p["fb_h"], p["fb_shell_t"] + p["fb_lining_t"]
    fbz = deck_top + Hh / 2
    shell = Pos(p["fb_x"], 0, fbz) * (Box(L, Wd, Hh) - Box(L - 2 * t, Wd - 2 * t, Hh - 2 * t))
    shell = shell - Pos(p["fb_x"], 0, deck_top + Hh - t / 2) * Cylinder(p["chimney_d"] / 2, t + 2)  # flue opening
    floor_in = deck_top + t
    grate = Pos(p["fb_x"], 0, floor_in + p["grate_z"]) * Box(L - 2 * t - 20, Wd - 2 * t - 20, 20)
    grate = grate - Pos(p["fb_x"], 0, floor_in + p["grate_z"]) * Box(L - 2 * t - 80, Wd - 2 * t - 80, 30)
    for i in range(-4, 5):
        grate = grate + Pos(p["fb_x"] + i * 60, 0, floor_in + p["grate_z"]) * Box(15, Wd - 2 * t - 40, 20)
    door = Pos(p["fb_x"], -Wd / 2 - 10, deck_top + 280) * Box(380, 20, 300)
    damper = Pos(p["fb_x"], -Wd / 2 - 25, deck_top + 110) * Box(160, 30, 70)
    parts["Firebox, fiber lined"] = shell + grate + door + damper

    # 6 Monotube steam coil, helix around the fire bed, inlet at the bottom, outlet at the top
    r = p["coil_mean_d"] / 2
    height = p["coil_pitch"] * p["coil_turns"]
    cz0 = floor_in + p["coil_z0"] + p["tube_od"] / 2
    path = Pos(p["fb_x"], 0, cz0) * Helix(pitch=p["coil_pitch"], height=height, radius=r)
    prof = Plane(origin=path @ 0, z_dir=path % 0) * Circle(p["tube_od"] / 2)
    coil = sweep(prof, path, is_frenet=True)
    xin = p["fb_x"] + r
    x_out_wall = p["fb_x"] + L / 2
    hx = x_out_wall + p["header_dx"]
    # outlet: from the top of the helix out through the +X wall, up to the header
    top = path @ 1
    outlet = _tube_along([(top.X, top.Y, top.Z), (x_out_wall + 60, top.Y, top.Z),
                          (x_out_wall + 60, 0, top.Z), (x_out_wall + 60, 0, p["header_z"]),
                          (hx - p["header_od"] / 2, 0, p["header_z"])], p["tube_od"])
    # inlet: economizer outlet comes down the +X face and enters the bottom of the helix
    bot = path @ 0
    inlet = _tube_along([(bot.X, bot.Y, bot.Z), (x_out_wall + 30, bot.Y, bot.Z),
                         (x_out_wall + 30, bot.Y, deck_top + Hh + 60)], p["tube_od"] * 0.6)
    parts["Monotube steam coil"] = coil + outlet + inlet

    # 7 Flue-gas economizer box with condensate drain
    ez = deck_top + Hh + p["eco_h"] / 2
    eco = Pos(p["fb_x"], 0, ez) * Box(p["eco_l"], p["eco_w"], p["eco_h"])
    drain = Pos(p["fb_x"] - p["eco_l"] / 2 - 30, 0, deck_top + Hh + 30) * Rot(0, 90, 0) * Cylinder(10, 60)
    parts["Flue-gas economizer"] = eco + drain

    # 8 Chimney and spark arrestor
    cb = deck_top + Hh + p["eco_h"]
    ch_len = p["chimney_top"] - p["cap_h"] - cb
    chimney = Pos(p["fb_x"], 0, cb + ch_len / 2) * Cylinder(p["chimney_d"] / 2, ch_len)
    cap = Pos(p["fb_x"], 0, p["chimney_top"] - p["cap_h"] / 2) * Cylinder(p["chimney_d"] / 2 + 45, p["cap_h"])
    parts["Chimney and spark arrestor"] = chimney + cap

    # 9 Steam header, water-seal pot with 1 m dip leg, vent pipe and diverter valve
    hz = p["header_z"]
    header = Pos(hx, 0, hz) * Rot(90, 0, 0) * Cylinder(p["header_od"] / 2, p["header_len"])
    pot_y = -p["header_len"] / 2 - p["seal_pot_od"] / 2 - 10
    pot_top = hz + 60
    pot_bot = hz - p["seal_depth"] - 150          # dip leg reaches 1 m below the water line
    pot = Pos(hx, pot_y, (pot_top + pot_bot) / 2) * Cylinder(p["seal_pot_od"] / 2, pot_top - pot_bot)
    link = Pos(hx, (pot_y - p["header_len"] / 2) / 2, hz) * Rot(90, 0, 0) * Cylinder(20, abs(pot_y + p["header_len"] / 2))
    vent = Pos(hx, pot_y, (pot_top + p["vent_top"]) / 2) * Cylinder(p["vent_od"] / 2, p["vent_top"] - pot_top)
    diverter = Pos(hx + p["header_od"] / 2 + 60, 0, hz) * Box(90, 70, 70)
    bracket = Pos(hx, pot_y / 2, deck_top + (pot_bot - deck_top) / 2 if pot_bot > deck_top else deck_top) * Box(40, 40, 10)
    parts["Steam header and water-seal vent"] = header + pot + link + vent + diverter + bracket

    # 10 Certified relief valve on the header top
    rv_y = p["header_len"] / 2 - 50
    relief = (Pos(hx, rv_y, hz + 90) * Cylinder(p["relief_d"] / 2, 120)
              + Pos(hx, rv_y, hz + 190) * Cylinder(20, 80))
    parts["Certified relief valve"] = relief

    # 12 Steam hoods: double skin, insulated, soil skirt, perforated manifold and handles
    hl, hw, hh, ins = p["hood_l"], p["hood_w"], p["hood_h"], p["hood_ins_t"]
    hood_x0 = p["deck_l"] / 2 + p["hood_offset"]
    hoods = None
    manifold_inlets = []
    for i in range(int(p["n_hoods"])):
        cx = hood_x0 + hl / 2 + i * (hl + p["hood_gap"])
        body = Pos(cx, 0, hh / 2) * (Box(hl, hw, hh) - Pos(0, 0, -ins / 2) * Box(hl - 2 * ins, hw - 2 * ins, hh))
        skirt = Pos(cx, 0, -p["skirt_depth"] / 2) * (Box(hl, hw, p["skirt_depth"]) - Box(hl - 6, hw - 6, p["skirt_depth"] + 2))
        manifold = Pos(cx, 0, hh - ins - 30) * Rot(0, 90, 0) * Cylinder(15, hl - 2 * ins - 40)
        inlet = Pos(cx - hl / 2 + 150, 0, hh + 40) * Cylinder(20, 80)
        handles = (Pos(cx, hw / 2 + 60, hh - 60) * Box(900, 30, 30) + Pos(cx, -hw / 2 - 60, hh - 60) * Box(900, 30, 30))
        for sx in (-400, 400):
            for sy in (1, -1):
                handles = handles + Pos(cx + sx, sy * (hw / 2 + 30), hh - 60) * Box(30, 60, 30)
        h = body + skirt + manifold + inlet + handles
        hoods = h if hoods is None else hoods + h
        manifold_inlets.append((cx - hl / 2 + 150, 0, hh + 80))

    # 11 Steam hose: diverter outlet down to the first hood inlet (routing is indicative)
    dx = hx + p["header_od"] / 2 + 105
    mi = manifold_inlets[0]
    parts["Steam hose"] = _tube_along([(dx, 0, hz), (dx + 150, 0, hz), (dx + 150, 0, 500),
                                       (mi[0], 0, 500), (mi[0], 0, mi[2])], p["hose_od"])
    parts["Steam hoods (2)"] = hoods
    return parts


def build(p=PARAMS):
    """Whole assembly as one compound."""
    from build123d import Compound
    return Compound(children=list(build_parts(p).values()))


MAIN_PARTS = {  # file stem: part name, for individual exports
    "steamroot-firebox": "Firebox, fiber lined",
    "steamroot-coil": "Monotube steam coil",
    "steamroot-header": "Steam header and water-seal vent",
    "steamroot-hood": "Steam hoods (2)",
}


if __name__ == "__main__":
    from build123d import export_step, export_stl, Compound
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    stl_tol = dict(tolerance=0.5, angular_tolerance=0.3)
    for stem, name in MAIN_PARTS.items():      # export single parts before they join the assembly
        export_step(parts[name], str(root / "step" / f"{stem}.step"))
        export_stl(parts[name], str(root / "stl" / f"{stem}.stl"), **stl_tol)
    sizes = {n: (s.bounding_box().size, s.volume) for n, s in parts.items()}
    asm = Compound(children=list(parts.values()))
    export_step(asm, str(root / "step" / "steamroot.step"))
    export_stl(asm, str(root / "stl" / "steamroot.stl"), **stl_tol)
    bb = asm.bounding_box()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm "
          f"(x {bb.min.X:.0f} to {bb.max.X:.0f}, y {bb.min.Y:.0f} to {bb.max.Y:.0f}, z {bb.min.Z:.0f} to {bb.max.Z:.0f})")
    for n, (sz, v) in sizes.items():
        print(f"  {n:36s} {sz.X:6.0f} x {sz.Y:6.0f} x {sz.Z:6.0f} mm, volume {v / 1e6:8.2f} L")

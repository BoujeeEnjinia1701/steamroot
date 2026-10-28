"""SteamRoot concept option B (STR-OPT-001): vented fire-tube kettle, modelled at detail level D3 (kit 1.9).

A wood fire in a lined firebox heats the 5 mm floor of a welded steel kettle and rises through seven vertical
60.3 mm fire tubes to a smoke box and the chimney. The kettle holds a pool of about 70 L of water (250 mm
deep) at atmospheric pressure; a float switch in a side chamber runs the same 12 V pump to keep the level,
and steam leaves through a side nozzle in the steam space to the same header, water-seal vent, relief valve,
diverter, hose and hoods as option A. Option B shares with A the trailer, skids, feed drum, pump box, hose,
hoods and the whole header and water-seal vent group, so the two options differ only in how the steam is
raised: once-through forced flow in a small coil (A) against pool boiling in a large vented vessel (B).

Not chosen; not on the drawing, BOM or build plan (STANDARDS section 24). CONCEPT, NOT FOR FABRICATION.
Axes as model.py: X along the trailer, Y across (operator and firebox door at -Y), Z up from the ground; mm.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

import model as M  # noqa: E402
from model import bx, zcyl, ycyl, xcyl, rhs_z, box, _tube_along, PARAMS, derived  # noqa: E402
import str_parts as sp  # noqa: E402

# option B dimensions (mm); the shared parts take theirs from model.PARAMS
PB = dict(
    fb_l=600.0, fb_w=500.0, fb_h=450.0, shell_t=3.0, lining_t=50.0,
    door_open=(260.0, 200.0, 130.0), air_open=(160.0, 60.0, 15.0), grate=(300.0, 20.0), grate_z=100.0,
    k_h=450.0, k_floor_t=5.0, k_wall_t=3.0, k_top_t=5.0, k_overhang=25.0, water_depth=250.0, gasket_t=3.0,
    tube_od=60.3, tube_wall=3.2, tube_pitch=130.0,
    smoke_h=150.0, smoke_t=2.0,
    jacket_t=50.0, clad_t=0.7,
    nozzle_od=26.7, feed_od=12.7,
)

SHARED = ("trailer", "wheels", "skids", "skid_bolts", "tank", "saddles", "straps", "saddle_bolts", "pbox", "hose",
          "post", "post_bolts", "header", "pot", "pot_bolts", "stay", "overflow", "ovf_stay", "ovf_clip", "ovf_bolts",
          "diverter", "vent_line", "relief", "discharge")
SHARED_WELD_GROUPS = ("Steam header and water-seal vent", "Steam hoods (2)")


def components():
    p, q = PARAMS, PB
    D = derived(p)
    C = M.build_components(p)
    keys = list(SHARED) + [k for k in C if k.startswith(("hood", "skirt", "manifold", "handles"))]
    out = M.parts_from({k: C[k] for k in keys})
    out += [M._part(nm, sh, mat, "weld", None, grp, "welds") for nm, sh, mat, bom, grp in C["welds"].pieces if grp in SHARED_WELD_GROUPS]
    for o in out:                           # option B carries no BOM lines (STANDARDS section 24)
        o["bom"] = None
    own = []
    W = []

    def add(name, shape, mat, kind="made", group="Kettle"):
        own.append(M._part(name, shape, mat, kind, None, group, "B"))

    def weld(name, *a):
        W.append(M._part(name, sp.weld(*a), "mild_steel", "weld", None, "Kettle", "B"))

    def ring(name, *a, mat="mild_steel"):
        W.append(M._part(name, sp.ring_weld(*a), mat, "weld", None, "Kettle", "B"))

    def fix(pieces):
        for nm, sh in pieces:
            own.append(M._part(nm, sh, "zinc_plated", "fastener", None, "Kettle", "B"))

    T = D["deck_top"]
    fx = p["fb_x"]
    L, Wd, H, sh, lt = q["fb_l"], q["fb_w"], q["fb_h"], q["shell_t"], q["lining_t"]
    z0 = T + p["skid"]
    top = z0 + H
    t = sh + lt
    F = z0 + t
    fa, ft = p["frame_angle"]

    # ---------------------------------------------------------------- firebox under the kettle (open top)
    dw, dh, db = q["door_open"]
    aw, ah, ab = q["air_open"]
    yd = -Wd / 2
    door_cut = bx(fx - dw / 2, fx + dw / 2, yd - 1, yd + t + 1, F + db, F + db + dh)
    air_cut = bx(fx - aw / 2, fx + aw / 2, yd - 1, yd + t + 1, F + ab, F + ab + ah)
    shell = box(fx, 0, z0 + H / 2, L, Wd, H) - bx(fx - L / 2 + sh, fx + L / 2 - sh, -Wd / 2 + sh, Wd / 2 - sh, z0 + sh, top + 1)
    shell -= door_cut + air_cut
    add("B firebox shell, 3 mm steel, open top", shell, "mild_steel")
    fr = bx(fx - L / 2 - fa, fx + L / 2 + fa, -Wd / 2 - fa, Wd / 2 + fa, top - ft, top) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, top - ft - 1, top + 1)
    fr += bx(fx - L / 2 - ft, fx + L / 2 + ft, -Wd / 2 - ft, Wd / 2 + ft, top - fa, top - ft) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, top - fa - 1, top)
    add("B firebox top frame, 25 x 25 x 3 angle", fr, "mild_steel")
    for (ay, d, u, ln, ax) in ((-Wd / 2, (1, 0, 0), (0, -1, 0), L, fx - L / 2), (Wd / 2, (1, 0, 0), (0, 1, 0), L, fx - L / 2),
                               (-Wd / 2, (0, 1, 0), (-1, 0, 0), Wd, fx - L / 2), (-Wd / 2, (0, 1, 0), (1, 0, 0), Wd, fx + L / 2)):
        if d == (1, 0, 0):
            for xa, xb in ((fx - L / 2 + 4, fx - 165), (fx - 115, fx + 115), (fx + 165, fx + L / 2 - 4)):
                weld("Weld, B firebox frame to shell (stitch)", (xa, ay, top - fa), d, xb - xa, 3, u, (0, 0, -1))
        else:
            for ya, yb in ((-Wd / 2 + 4, -40), (40, Wd / 2 - 4)):
                weld("Weld, B firebox frame to shell (stitch)", (ax, ya, top - fa), d, yb - ya, 3, u, (0, 0, -1))
    lining = bx(fx - L / 2 + sh, fx + L / 2 - sh, -Wd / 2 + sh, Wd / 2 - sh, z0 + sh, top) - bx(fx - L / 2 + t, fx + L / 2 - t, -Wd / 2 + t, Wd / 2 - t, F, top + 1)
    lining -= door_cut + air_cut
    add("B ceramic fibre lining, 50 mm, walls and floor", lining, "insulated_white", "bought")
    skx = [fx - p["skid_dx"], fx + p["skid_dx"]]
    for x in skx:
        for sx_ in (-1, 1):
            weld("Weld, B firebox to skid", (x + sx_ * p["skid"] / 2, -Wd / 2 + 3, z0), (0, 1, 0), Wd - 6, 4, (sx_, 0, 0), (0, 0, -1))
    # grate on a stand
    gs, gt = q["grate"]
    gz = F + q["grate_z"]
    ringp = bx(fx - gs / 2, fx + gs / 2, -gs / 2, gs / 2, gz - 25, gz) - bx(fx - gs / 2 + 25, fx + gs / 2 - 25, -gs / 2 + 25, gs / 2 - 25, gz - 26, gz + 1)
    ringp -= bx(fx - gs / 2 + 2, fx + gs / 2 - 2, -gs / 2 + 2, gs / 2 - 2, gz - 23, gz - 2) - bx(fx - gs / 2 + 23, fx + gs / 2 - 23, -gs / 2 + 23, gs / 2 - 23, gz - 24, gz - 1)
    add("B grate stand ring, 25 x 25 x 2 SHS", ringp, "mild_steel")
    k = 0
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            k += 1
            cx_, cy_ = fx + sx_ * (gs / 2 - 12.5), sy_ * (gs / 2 - 12.5)
            add(f"B grate stand leg {k}, 25 x 25 x 2 SHS", rhs_z(cx_, cy_, F + 5, gz - 25, 25, 2), "mild_steel")
            add(f"B grate stand foot pad {k}", bx(cx_ - 30, cx_ + 30, cy_ - 30, cy_ + 30, F, F + 5), "mild_steel")
    grate = bx(fx - gs / 2, fx + gs / 2, -gs / 2, gs / 2, gz, gz + gt)
    for i in range(-5, 6):
        grate -= bx(fx + i * 25 - 6, fx + i * 25 + 6, -gs / 2 + 25, gs / 2 - 25, gz - 1, gz + gt + 1)
    add("B cast iron grate, 300 x 300", grate, "mild_steel", "bought")
    # door, hinges, latch, primary air damper
    lap = 20.0
    dz0, dz1 = F + db - lap, F + db + dh + lap
    dx0, dx1 = fx - dw / 2 - lap, fx + dw / 2 + lap
    add("B firebox door plate, 3 mm", bx(dx0, dx1, yd - 3, yd, dz0, dz1), "mild_steel")
    add("B door plug, ceramic fibre board", bx(fx - dw / 2 + 4, fx + dw / 2 - 4, yd, yd + t - 4, F + db + 4, F + db + dh - 4), "insulated_white")
    zm = (dz0 + dz1) / 2
    add("B door handle bar", bx(fx - 60, fx + 60, yd - 33, yd - 23, zm - 8, zm + 8), "mild_steel")
    for sx_ in (-1, 1):
        add("B door handle standoff", bx(fx + sx_ * 60 - 8, fx + sx_ * 60 + 8, yd - 23, yd - 3, zm - 8, zm + 8), "mild_steel")
        for zz, vv in ((zm + 8, 1), (zm - 8, -1)):
            weld("Weld, B door handle standoff", (fx + sx_ * 60 - 6, yd - 3, zz), (1, 0, 0), 12, 2.5, (0, 0, vv), (0, -1, 0))
    for zh in (dz0 + 40, dz1 - 40):
        hg = zcyl(dx1 + 10, yd - 9, zh - 30, 8, 60) + bx(dx1 - 15, dx1 + 4, yd - 6, yd - 3, zh - 30, zh + 30)
        hg += bx(dx1 + 16, dx1 + 40, yd - 3, yd, zh - 30, zh + 30) + bx(dx1 + 2, dx1 + 18, yd - 6, yd - 3, zh - 30, zh + 30)
        add("B weld-on door hinge", hg, "zinc_plated", "bought")
        weld("Weld, B hinge leaf to door", (dx1 - 15, yd - 3, zh - 27), (0, 0, 1), 54, 2.5, (-1, 0, 0), (0, -1, 0))
        weld("Weld, B hinge leaf to shell", (dx1 + 40, yd, zh - 27), (0, 0, 1), 54, 2.5, (1, 0, 0), (0, -1, 0))
    add("B door latch keeper", bx(dx0 - 30, dx0 - 6, yd - 20, yd, zm + 10, zm + 30), "zinc_plated", "bought")
    add("B door turn latch bar", bx(dx0 - 30, dx0 + 40, yd - 26, yd - 20, zm + 10, zm + 30), "zinc_plated", "bought")
    add("B door latch boss", bx(dx0 + 20, dx0 + 40, yd - 20, yd - 3, zm + 10, zm + 30), "zinc_plated", "bought")
    az0, az1 = F + ab, F + ab + ah
    pz0, pz1 = az0 - 20, az1 + 20
    add("B primary air damper slide, 3 mm", bx(fx - aw / 2 - 30, fx + aw / 2 + 30, yd - 6, yd - 3, pz0, pz1), "mild_steel")
    add("B damper knob", ycyl(fx - aw / 2 - 10, yd - 26, (pz0 + pz1) / 2, 10, 20), "matte_black")
    for zg, sgn in ((pz1, 1), (pz0, -1)):
        g = bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 3, yd, zg if sgn > 0 else zg - 6, zg + 6 if sgn > 0 else zg)
        g += bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 9, yd - 3, zg if sgn > 0 else zg - 6, zg + 6 if sgn > 0 else zg)
        g += bx(fx - aw / 2 - 60, fx + aw / 2 + 60, yd - 9, yd - 6, (zg - 6 if sgn > 0 else zg), (zg if sgn > 0 else zg + 6))
        add("B damper guide", g, "mild_steel")
        weld("Weld, B damper guide to shell", (fx - aw / 2 - 56, yd, zg + 6 if sgn > 0 else zg - 6), (1, 0, 0), aw + 112, 2.5, (0, 0, sgn), (0, -1, 0))

    # ---------------------------------------------------------------- kettle on the firebox, with a rope gasket
    g0 = top                                           # gasket on the firebox frame
    k0 = g0 + q["gasket_t"]                            # underside of the kettle floor and frame
    k1 = k0 + q["k_h"]                                 # top of the top sheet
    gsk = bx(fx - L / 2 - fa, fx + L / 2 + fa, -Wd / 2 - fa, Wd / 2 + fa, g0, k0) - bx(fx - L / 2 + 2, fx + L / 2 - 2, -Wd / 2 + 2, Wd / 2 - 2, g0 - 1, k0 + 1)
    add("B kettle gasket, flattened ceramic rope", gsk, "insulated_white", "bought")
    kw, kf, ktt, ov = q["k_wall_t"], q["k_floor_t"], q["k_top_t"], q["k_overhang"]
    kbody = box(fx, 0, (k0 + k1 - ktt) / 2, L, Wd, k1 - ktt - k0) - bx(fx - L / 2 + kw, fx + L / 2 - kw, -Wd / 2 + kw, Wd / 2 - kw, k0 + kf, k1)
    ktop = bx(fx - L / 2 - ov, fx + L / 2 + ov, -Wd / 2 - ov, Wd / 2 + ov, k1 - ktt, k1)
    kfr = bx(fx - L / 2 - fa, fx + L / 2 + fa, -Wd / 2 - fa, Wd / 2 + fa, k0, k0 + ft) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, k0 - 1, k0 + ft + 1)
    kfr += bx(fx - L / 2 - ft, fx + L / 2 + ft, -Wd / 2 - ft, Wd / 2 + ft, k0 + ft, k0 + fa) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, k0, k0 + fa + 1)
    tp = q["tube_pitch"]
    tubes_xy = [(fx, 0.0), (fx - tp, 0.0), (fx + tp, 0.0)] + [(fx + sx_ * tp / 2, sy_ * tp * math.sqrt(3) / 2) for sx_ in (-1, 1) for sy_ in (-1, 1)]
    ro = q["tube_od"] / 2
    for x_, y_ in tubes_xy:
        kbody -= zcyl(x_, y_, k0 - 1, ro, kf + 2)
        ktop -= zcyl(x_, y_, k1 - ktt - 1, ro, ktt + 2)
    # nozzles: steam take-off in the steam space (+X wall), feed inlet below the water (-X wall), float chamber and
    # sight glass connections (-Y wall), drain (+Y wall)
    zw = k0 + kf + q["water_depth"]                    # water level mark
    zn = k1 - ktt - 60
    no = q["nozzle_od"] / 2
    kbody -= xcyl(fx + L / 2 - kw - 1, 0, zn, no - 2.87, kw + 2)
    zfeed = k0 + kf + 60
    kbody -= xcyl(fx - L / 2 - 1, 150, zfeed, q["feed_od"] / 2 - 1.2, kw + 2)
    xf_, xs_ = fx + 150, fx - 150
    for zz in (zw - 60, zw + 60):
        kbody -= ycyl(xf_, -Wd / 2 - 1, zz, 7.5, kw + 2)
    for zz in (k0 + kf + 60, zw + 120):
        kbody -= ycyl(xs_, -Wd / 2 - 1, zz, 4.5, kw + 2)
    zd = k0 + 45
    kbody -= ycyl(fx + 200, Wd / 2 - kw - 1, zd, 7.5, kw + 2)
    add("B kettle body, 3 mm walls and 5 mm floor, welded", kbody, "mild_steel")
    add("B kettle top tube sheet, 5 mm, with flange", ktop, "mild_steel")
    add("B kettle bottom frame, 25 x 25 x 3 angle", kfr, "mild_steel")
    for (ay, d, u, ln, ax) in ((-Wd / 2, (1, 0, 0), (0, -1, 0), L, fx - L / 2), (Wd / 2, (1, 0, 0), (0, 1, 0), L, fx - L / 2),
                               (-Wd / 2, (0, 1, 0), (-1, 0, 0), Wd, fx - L / 2), (-Wd / 2, (0, 1, 0), (1, 0, 0), Wd, fx + L / 2)):
        if d == (1, 0, 0):
            for xa, xb in ((fx - L / 2 + 4, fx - 165), (fx - 115, fx + 115), (fx + 165, fx + L / 2 - 4)):
                weld("Weld, B kettle frame to wall (stitch)", (xa, ay, k0 + fa), d, xb - xa, 3, u, (0, 0, 1))
        else:
            for ya, yb in ((-Wd / 2 + 4, -40), (40, Wd / 2 - 4)):
                weld("Weld, B kettle frame to wall (stitch)", (ax, ya, k0 + fa), d, yb - ya, 3, u, (0, 0, 1))
    for i, (x_, y_) in enumerate(tubes_xy):
        tube = zcyl(x_, y_, k0, ro, k1 - k0) - zcyl(x_, y_, k0 - 1, ro - q["tube_wall"], k1 - k0 + 2)
        add(f"B fire tube {i + 1}, 60.3 x 3.2 steel", tube, "mild_steel")
        ring("Weld, B fire tube to kettle floor", (x_, y_, k0), "-z", ro, 4)
        ring("Weld, B fire tube to top sheet", (x_, y_, k1), "+z", ro, 4)
    kb = sp.Fix()
    xs_r = [fx - L / 2 - fa / 2 + i * (L + fa) / 4 for i in range(5)]
    for xr in xs_r:
        for yr in (-Wd / 2 - fa / 2, Wd / 2 + fa / 2):
            kb += sp.bolt(10, 2 * ft + q["gasket_t"], (xr, yr, k0 + ft), "-z")
    for xr in (fx - L / 2 - fa / 2, fx + L / 2 + fa / 2):
        kb += sp.bolt(10, 2 * ft + q["gasket_t"], (xr, 0.0, k0 + ft), "-z")
    for i, o in enumerate(own):
        if o["name"].startswith(("B firebox top frame", "B kettle bottom frame", "B kettle gasket")):
            sh_ = o["shape"]
            for hcyl in kb.holes:
                sh_ = sh_ - hcyl
            own[i] = M._part(o["name"], sh_, o["material_name"], o["kind"], None, o["group"], "B")
    fix(kb)

    # insulation jacket and aluminium cladding round the kettle walls
    jt, ct = q["jacket_t"], q["clad_t"]
    zj0, zj1 = k0 + fa + 3, k1 - ktt - 18
    jacket = bx(fx - L / 2 - jt, fx + L / 2 + jt, -Wd / 2 - jt, Wd / 2 + jt, zj0, zj1) - bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, zj0 - 1, zj1 + 1)
    clad = bx(fx - L / 2 - jt - ct, fx + L / 2 + jt + ct, -Wd / 2 - jt - ct, Wd / 2 + jt + ct, zj0, zj1) - bx(fx - L / 2 - jt, fx + L / 2 + jt, -Wd / 2 - jt, Wd / 2 + jt, zj0 - 1, zj1 + 1)
    pens = [xcyl(fx + L / 2 - 1, 0, zn, no + 5, jt + 5), xcyl(fx - L / 2 - jt - 5, 150, zfeed, 9, jt + 7)]
    pens += [ycyl(xf_, -Wd / 2 - jt - 5, zz, 12, jt + 6) for zz in (zw - 60, zw + 60)]
    pens += [ycyl(xs_, -Wd / 2 - jt - 5, zz, 9, jt + 6) for zz in (k0 + kf + 60, zw + 120)]
    pens += [ycyl(fx + 200, Wd / 2 - 1, zd, 13, jt + 6)]
    for pc in pens:
        jacket -= pc
        clad -= pc
    add("B kettle insulation jacket, 50 mm mineral wool", jacket, "insulated_white", "bought")
    add("B kettle cladding, 0.7 mm aluminium", clad, "aluminium")

    # smoke box on the top sheet flange, bolted; chimney and spark arrestor cap
    st_, shh = q["smoke_t"], q["smoke_h"]
    s0 = k1
    sfl = bx(fx - L / 2 - ov, fx + L / 2 + ov, -Wd / 2 - ov, Wd / 2 + ov, s0, s0 + 3) - bx(fx - L / 2 + st_, fx + L / 2 - st_, -Wd / 2 + st_, Wd / 2 - st_, s0 - 1, s0 + 4)
    sbox = bx(fx - L / 2, fx + L / 2, -Wd / 2, Wd / 2, s0 + 3, s0 + 3 + shh) - bx(fx - L / 2 + st_, fx + L / 2 - st_, -Wd / 2 + st_, Wd / 2 - st_, s0 + 2, s0 + 3 + shh - st_)
    smoke = sfl + sbox
    smoke -= zcyl(fx, 0, s0 + shh, p["chimney_d"] / 2 - 1, 10)
    sb = sp.Fix()
    for xr in [fx - L / 2 - ov / 2 + i * (L + ov) / 4 for i in range(5)]:
        for yr in (-Wd / 2 - ov / 2, Wd / 2 + ov / 2):
            sb += sp.bolt(8, 3 + ktt, (xr, yr, s0 + 3), "-z")
    for hcyl in sb.holes:
        smoke -= hcyl
    for i, o in enumerate(own):
        if o["name"].startswith("B kettle top tube sheet"):
            sh_ = o["shape"]
            for hcyl in sb.holes:
                sh_ = sh_ - hcyl
            own[i] = M._part(o["name"], sh_, "mild_steel", "made", None, "Kettle", "B")
    add("B smoke box, 2 mm steel with flange, welded", smoke, "mild_steel")
    fix(sb)
    stop = s0 + 3 + shh
    spig = zcyl(fx, 0, stop - st_, p["chimney_d"] / 2 - 1, p["spigot_h"] + st_) - zcyl(fx, 0, stop - st_ - 1, p["chimney_d"] / 2 - 2.5, p["spigot_h"] + st_ + 2)
    add("B chimney spigot", spig, "stainless")
    ring("Weld, B spigot to smoke box (underside)", (fx, 0, stop - st_), "-z", p["chimney_d"] / 2 - 1, 3, mat="stainless")
    ch0 = stop
    cap0 = p["chimney_top"] - p["cap_h"]
    ri = p["chimney_d"] / 2 - 1
    add("B chimney, 150 mm single-wall stainless", zcyl(fx, 0, ch0, ri + 0.8, cap0 + 50 - ch0) - zcyl(fx, 0, ch0 - 1, ri, cap0 + 52 - ch0), "stainless", "bought")
    add("B spark arrestor cap collar", zcyl(fx, 0, cap0, ri + 4.0, 50) - zcyl(fx, 0, cap0 - 1, ri + 0.8, 52), "stainless", "bought")
    add("B spark arrestor cage, 6 mm mesh, with rain cap",
        zcyl(fx, 0, cap0 + 50, p["chimney_d"] / 2 + 45, p["cap_h"] - 50) - zcyl(fx, 0, cap0 + 49, p["chimney_d"] / 2 + 42, p["cap_h"] - 52), "stainless", "bought")

    # steam take-off to the shared header, feed line from the pump box, level controls, drain
    hx, hz = D["hx"], D["hz"]
    xr_ = fx + L / 2 + jt + 30
    take = _tube_along([(fx + L / 2, 0, zn), (xr_, 0, zn), (xr_, 0, hz), (hx - p["header_od"] / 2, 0, hz)], q["nozzle_od"], 2.87)
    add("B steam take-off, 3/4 in steel pipe to the header", take, "galvanised", "bought")
    ring("Weld, B steam nozzle to kettle wall", (fx + L / 2, 0, zn), "+x", no, 3)
    bx0, bx1, by0, by1, bh = p["pbox"]
    feed = _tube_along([((bx0 + bx1) / 2, (by0 + by1) / 2, T + bh), ((bx0 + bx1) / 2, (by0 + by1) / 2, zfeed),
                        ((bx0 + bx1) / 2, 150, zfeed), (fx - L / 2, 150, zfeed)], q["feed_od"], 1.2)
    add("B feed line, 316 stainless 12.7 mm", feed, "stainless", "bought")
    yc = -Wd / 2 - jt - ct - 35
    add("B float switch chamber, 60 mm", zcyl(xf_, yc, zw - 90, 30, 180), "brass", "bought")
    for zz in (zw - 60, zw + 60):
        add("B float chamber connection, 15 mm", ycyl(xf_, yc + 30, zz, 7.5, -Wd / 2 - (yc + 30)), "brass", "bought")
    yg = -Wd / 2 - jt - ct - 20
    add("B level sight glass, 16 mm", zcyl(xs_, yg, k0 + kf + 40, 8, zw + 140 - (k0 + kf + 40)), "polycarbonate", "bought")
    for zz in (k0 + kf + 60, zw + 120):
        add("B sight glass cock, 9 mm", ycyl(xs_, yg + 8, zz, 4.5, -Wd / 2 - (yg + 8)), "brass", "bought")
    add("B kettle drain valve", ycyl(fx + 200, Wd / 2, zd, 10, jt + 20), "brass", "bought")
    return out + own + W

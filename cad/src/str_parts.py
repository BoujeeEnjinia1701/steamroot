"""SteamRoot repo-specific CAD helpers beside .kit/cad_parts.py (kit 1.9, STANDARDS section 24).

    bolt()        cad_parts.hex_bolt_set on any axis: the face under the head at a point, the joint along a direction
    stud()        a stud welded to a plate (or screwed into it) with a washer and an ISO 4032 nut on top
    screw()       a hex head screw into a tapped hole with its washer (no nut)
    clearance()   the clearance hole for a bolt through a joint (ISO 273 medium series), as a cylinder to subtract
    weld()        a fillet weld bead along any axis, its two legs on two faces
    ring_weld()   a fillet weld bead round a tube where it meets a plate
    Fix           a list of (name, shape) fastener pieces that also carries the holes they need

All sizes in millimetres; directions are "+x", "-x", "+y", "-y", "+z", "-z". Threads are drawn as plain
shanks, as is usual in assembly CAD. Each helper returns (name, shape) pairs so the model makes one
cad_parts.part() per bolt, washer and nut.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Cylinder, Plane, Polygon, Pos, Rot, Vector, extrude, revolve, Axis, Location  # noqa: E402
import cad_parts as cp  # noqa: E402

# rotation taking the library's "into the joint" direction (-Z) to the direction asked for
_TURN = {"-z": Rot(0, 0, 0), "+z": Rot(180, 0, 0), "+y": Rot(90, 0, 0), "-y": Rot(-90, 0, 0),
         "+x": Rot(0, -90, 0), "-x": Rot(0, 90, 0)}
_VEC = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}
# ISO 273 clearance holes, medium series
CLEAR = {5: 5.5, 6: 6.6, 8: 9.0, 10: 11.0, 12: 13.5, 16: 17.5}


class Fix(list):
    """Fastener pieces [(name, shape), ...] plus the clearance holes they need (.holes, shapes to subtract)."""

    def __init__(self, *a):
        super().__init__(*a)
        self.holes = []

    def __iadd__(self, other):
        super().__iadd__(other)
        self.holes += getattr(other, "holes", [])
        return self


def _place(shape, at, into):
    return Pos(*at) * _TURN[into] * shape


def clearance(d, at, into, length, extra=1.0):
    """Clearance hole cylinder for an Md bolt from the point 'at' along 'into' for 'length' mm (plus 'extra'
    at each end so the cut is clean)."""
    v = _VEC[into]
    c = Pos(*(at[i] + v[i] * length / 2 for i in range(3))) * _TURN[into] * Cylinder(CLEAR[int(d)] / 2, length + 2 * extra)
    return c


def bolt(d, grip, at, into, grade="8.8", finish="zinc plated"):
    """Hex bolt (ISO 4017), two washers (ISO 7089) and a nut (ISO 4032) clamping a joint 'grip' thick. 'at' is the
    point on the face under the head; 'into' the direction from that face through the joint."""
    out = Fix()
    for nm, shp in cp.hex_bolt_set(int(d), grip):
        nm = nm.replace("hex bolt", f"hex bolt {grade}, {finish}")
        out.append((nm, _place(shp, at, into)))
    out.holes.append(clearance(d, at, into, grip))
    return out


def stud(d, at, into, through, welded=True):
    """Stud from the face at 'at' (welded on, or screwed in) along 'into' through 'through' mm of parts, then a
    washer and a nut on the far face."""
    s, k, m, d2, h, p = cp.ISO[int(d)]
    L = through + h + m + 2 * p
    v = _VEC[into]
    far = tuple(at[i] + v[i] * through for i in range(3))
    flip = {"+z": "-z", "-z": "+z", "+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}[into]
    rod = Pos(*at) * _TURN[flip] * cp.round_bar(d, L, chamfer_ends=0.5)
    out = Fix([(f"M{d}x{L:.0f} {'weld stud' if welded else 'stud'}, zinc plated", rod),
               (f"M{d} washer (ISO 7089)", _place(Rot(180, 0, 0) * Pos(0, 0, -h) * cp.washer(int(d)), far, flip)),
               (f"M{d} hex nut (ISO 4032)", _place(Rot(180, 0, 0) * Pos(0, 0, -h - m) * cp.hex_nut(int(d)), far, flip))])
    out.holes.append(clearance(d, at, into, through))
    return out


def screw(d, length, at, into):
    """Hex head screw (ISO 4017) into a tapped hole, with a washer under the head; the hole is the tapping drill."""
    h = cp.ISO[int(d)][4]
    out = Fix([(f"M{d}x{length:.0f} hex screw 8.8 (ISO 4017), zinc plated", _place(Pos(0, 0, h) * cp.hex_bolt(int(d), length), at, into)),
               (f"M{d} washer (ISO 7089)", _place(cp.washer(int(d)), at, into))])
    v = _VEC[into]
    out.holes.append(Pos(*(at[i] + v[i] * length / 2 for i in range(3))) * _TURN[into] * Cylinder(d / 2 + 0.05, length + 2))
    return out


def weld(at, along, length, leg, u, v):
    """Fillet weld bead from the point 'at' (the root, in the corner) along the unit vector 'along' for 'length' mm,
    its legs 'leg' long along the unit vectors u and v (the faces of the two parts)."""
    a, u_, v_ = Vector(*along).normalized(), Vector(*u).normalized(), Vector(*v).normalized()
    # cad_parts.weld_fillet: along +X with its legs on +Y and +Z. Build the frame x=a, y=u, z=v; if it is
    # left-handed, start the bead at the far end and run it backwards.
    if abs(a.cross(u_).dot(v_) - 1.0) < 1e-6:
        loc, x0 = Location(Plane(origin=Vector(*at), x_dir=a, z_dir=v_)), 0.0
    else:
        loc = Location(Plane(origin=Vector(*at) + a * length, x_dir=-a, z_dir=v_))
    return loc * cp.weld_fillet(length, leg)


def ring_weld(center, axis, r_tube, leg):
    """Fillet weld bead round a tube of outside radius r_tube where it meets a plate: 'center' is the tube axis
    on the plate face, 'axis' the direction from the plate along the tube."""
    prof = Plane.XZ * Polygon((r_tube, 0), (r_tube + leg, 0), (r_tube, leg), align=None)
    ring = revolve(prof, Axis.Z, 360)
    return Pos(*center) * _TURN[{"+z": "-z", "-z": "+z", "+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}[axis]] * ring

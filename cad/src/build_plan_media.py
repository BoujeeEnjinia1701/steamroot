"""SteamRoot prototype build plan pictures (STR-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything; "sheets 105" draws one making sketch. Every picture is drawn
from cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/STR-DWG-101 to 126        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          12 V wiring of the pump and alarms (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, helix_point, coil_display  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
COIL_SWEPT = C["coil"].shape                              # the true swept tube, for the coil sketch views
C["coil"] = C["coil"]._replace(shape=coil_display(P))      # light version for pictures (same centreline)
FX = P["fb_x"]


def _tris(shape, tol=1.0):
    """Tessellate for the pictures with a 0.4 rad angular step: the coil's hundreds of pieces
    otherwise give over two million triangles and run the machine out of memory."""
    import numpy as np
    verts, tris = shape.tessellate(tol, 0.4)
    return np.array([[p.X, p.Y, p.Z] for p in verts]), np.array(tris)


bv._tris = _tris

COL = {"trailer": "#6B7280", "wheels": "#1F2937", "skids": "#1D4ED8", "shell": "#9A3412", "roof": "#B45309",
       "board": "#FDE68A", "lining": "#FCD34D", "brackets": "#475569", "stand": "#0F766E", "grate": "#292524",
       "door": "#7C2D12", "hinges": "#111827", "latch": "#111827", "damper": "#4338CA", "guides": "#4338CA",
       "coil": "#B87333", "outlet": "#B87333", "glands": "#0E7490", "jumper": "#7C3AED", "eco_box": "#D4A017",
       "eco_bank": "#94A3B8", "eco_lid": "#CA8A04", "chimney": "#9CA3AF", "cap": "#374151", "post": "#1D4ED8",
       "header": "#0F766E", "pot": "#0D9488", "stay": "#1D4ED8", "relief": "#DC2626", "discharge": "#F87171",
       "diverter": "#111827", "vent_line": "#14B8A6", "tank": "#2563EB", "saddles": "#92400E", "straps": "#F59E0B",
       "pbox": "#4B5563", "feed": "#7C3AED", "clips": "#7C3AED", "hose": "#111827", "hood": "#D1D5DB",
       "skirt": "#A1A1AA", "manifold": "#0369A1", "handles": "#52525B", "bolt": "#111827",
       "bk_box": "#C2410C", "bk_bank": "#94A3B8", "bk_lining": "#FCD34D", "damper2": "#6366F1", "overflow": "#0EA5E9",
       "ovf_clip": "#1D4ED8"}


def S(*keys):
    out = None
    for k in keys:
        s = C[k].shape
        out = s if out is None else out + s
    return out


def comp(*keys):
    """A compound of copies: giving a shape to a compound takes it out of any compound that held it before."""
    import copy
    from build123d import Compound
    return Compound(children=[copy.copy(C[k].shape) for k in keys])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of a shape inside a box, cut solid by solid (cutting the coil's compound whole runs out of memory)."""
    from build123d import Pos, Box, Compound
    box = Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)
    kids = []
    for so in shape.solids():
        bb = so.bounding_box()
        if bb.max.X < x0 or bb.min.X > x1 or bb.max.Y < y0 or bb.min.Y > y1 or bb.max.Z < z0 or bb.min.Z > z1:
            continue
        if bb.min.X >= x0 and bb.max.X <= x1 and bb.min.Y >= y0 and bb.max.Y <= y1 and bb.min.Z >= z0 and bb.max.Z <= z1:
            kids.append(so)
            continue
        kids += [x for x in (so & box).solids() if x.volume > 1e-6]
    return Compound(children=kids)


def made():
    return {
        "trailer": part("Trailer, used (with wheels)", comp("trailer", "wheels"), COL["trailer"]),
        "shell": part("Firebox shell", C["shell"].shape, COL["shell"]),
        "skids": part("Firebox skids (2)", C["skids"].shape, COL["skids"]),
        "brackets": part("Coil brackets (3)", C["brackets"].shape, COL["brackets"]),
        "guides": part("Damper guides (2)", C["guides"].shape, COL["guides"]),
        "lining": part("Fibre lining, walls and floor", C["lining"].shape, COL["lining"]),
        "stand": part("Grate stand and cast grate", comp("stand", "grate"), COL["stand"]),
        "door": part("Door, hinges and latch", comp("door", "hinges", "latch"), COL["door"]),
        "damper": part("Primary air damper slide", C["damper"].shape, COL["damper"]),
        "damper2": part("Secondary air damper", comp("damper2", "guides2"), COL["damper2"]),
        "bank": part("Evaporator bank box and tube", comp("bk_box", "bk_lining", "bk_bank", "bk_sups", "bk_cover"), COL["bk_box"]),
        "overflow": part("Seal pot overflow, stay and clip", comp("overflow", "ovf_stay", "ovf_clip"), COL["overflow"]),
        "coil": part("Monotube coil", C["coil"].shape, COL["coil"]),
        "glands": part("Tube gland plates (2)", C["glands"].shape, COL["glands"]),
        "roof": part("Roof and roof board", comp("roof", "board"), COL["roof"]),
        "eco": part("Economizer box and tube bank", comp("eco_box", "eco_bank"), COL["eco_box"]),
        "lid": part("Economizer lid", C["eco_lid"].shape, COL["eco_lid"]),
        "chimney": part("Chimney and spark arrestor", comp("chimney", "cap"), COL["chimney"]),
        "post": part("Header post", C["post"].shape, COL["post"]),
        "header": part("Steam header and gauge", C["header"].shape, COL["header"]),
        "outlet": part("Coil outlet pipe", C["outlet"].shape, COL["outlet"]),
        "pot": part("Water-seal pot and vent", C["pot"].shape, COL["pot"]),
        "stay": part("Pot stay", C["stay"].shape, COL["stay"]),
        "relief": part("Relief valve and discharge pipe", comp("relief", "discharge"), COL["relief"]),
        "diverter": part("Diverter and vent line", comp("diverter", "vent_line"), COL["diverter"]),
        "saddles": part("Drum saddles (2)", C["saddles"].shape, COL["saddles"]),
        "tank": part("Feed drum and straps", comp("tank", "straps"), COL["tank"]),
        "pbox": part("Pump and alarm box", C["pbox"].shape, COL["pbox"]),
        "feed": part("Feed lines, link and jumper", comp("feed", "clips", "jumper", "bk_link"), COL["feed"]),
        "hose": part("Steam hose", C["hose"].shape, COL["hose"]),
        "hood": part("Steam hood (2; one shown)", comp("hood1", "skirt1", "manifold1", "handles1"), COL["hood"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"trailer": (0, 0, -1000), "shell": (0, 0, 0), "skids": (0, 0, -500), "brackets": (0, -1000, 1150),
           "guides": (0, -1800, -150), "lining": (0, -1000, 0), "stand": (0, -1000, -800),
           "door": (0, -1800, 250), "damper": (0, -1800, -450), "coil": (0, 0, 1000), "glands": (650, 0, 1200),
           "roof": (0, 0, 1700), "bank": (0, 0, 2050), "eco": (0, 0, 2450), "lid": (0, 0, 2800), "chimney": (0, 0, 3050),
           "damper2": (0, -1800, 550), "overflow": (350, -2000, 700),
           "post": (900, 0, -250), "header": (900, 0, 600), "outlet": (450, 0, 1300), "pot": (900, -800, 0),
           "stay": (900, -350, -200), "relief": (900, 0, 1150), "diverter": (900, 500, 900),
           "saddles": (-1000, 0, -500), "tank": (-1000, 0, 250), "pbox": (-1500, -1150, -450), "feed": (-1300, 0, 1400),
           "hose": (900, 1200, 0), "hood": (-200, 0, 0)}
    order = ["trailer", "shell", "skids", "brackets", "guides", "lining", "stand", "door", "damper", "damper2", "coil",
             "glands", "roof", "bank", "eco", "lid", "chimney", "post", "header", "outlet", "pot", "stay", "overflow", "relief",
             "diverter", "saddles", "tank", "pbox", "feed", "hose", "hood"]
    parts = []
    for k in order:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "SteamRoot prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the operator side (front), right and above; the second hood is the same as the first",
                       elev=16, azim=-62, size=(12, 10), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="SteamRoot", date=DATE)
    out = []
    t, F, top = D["t"], D["F"], D["fb_top"]
    z0 = D["fb_z0"]
    at0 = lambda sh: b.Pos(-FX, 0, -z0) * sh  # noqa: E731   firebox parts with the shell's bottom at 0

    def sheet(num, *a, change=None, new=False, **k):
        if only and num not in only:
            return
        kw = dict(base)
        if change:      # revised on 2026-10-02 for the decisions of that day
            kw.update(date="2026-10-02", rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC"),
                                                              ("P2", change, "2026-10-02", "AC")])
        elif new:
            kw.update(date="2026-10-02")
        out.append(bv.component_sheet(*a, **k, **kw))

    sheet(101, Part("Firebox shell", C["shell"].shape, COL["shell"]), [M["skids"], M["trailer"], M["roof"]],
          dwg_no="STR-DWG-101", title="SteamRoot firebox shell: making sketch", material="Mild steel sheet 3 mm; angle 25 x 25 x 3 mm",
          change="960 tall (one coil turn fewer); upper tube slot lowered 40",
          view_shape=at0(C["shell"].shape), inset_view=(18, -62),
          notes=["Open-topped box 700 long, 600 wide, 960 tall, 3 mm sheet, welded",
                 "  inside and out. Front is the door side, back the trailer side.",
                 "Door opening in the front, centred: 300 wide x 240 tall, bottom",
                 "  183 up from the bottom edge (the board floor is 53 thick).",
                 "Air inlet in the front, centred: 160 wide x 60 tall, bottom 68 up.",
                 "Two tube slots in the right end (towards the header), centred on",
                 "  the width: 40 wide, from 446 to 516 up and from 846 to 916 up.",
                 "Top frame: 25 x 25 x 3 angle round the outside, top flush with the",
                 "  wall tops; 14 holes 9 mm for the roof bolts, about 180 apart.",
                 "Weld on before lining: coil brackets (sketch 103), damper guides",
                 "  (sketch 107), hinge leaves, latch keeper, gland studs, clip lugs.",
                 "Check: diagonals of the top equal within 3; walls flat within 3."])

    sk = C["skids"].shape
    one = sk & (b.Pos(FX - P["skid_dx"], 0, 0) * b.Box(100, 2000, 5000))
    sheet(102, Part("Firebox skid", one, COL["skids"]), [M["shell"], M["trailer"]],
          dwg_no="STR-DWG-102", title="SteamRoot firebox skid (make 2): making sketch", material="Square steel tube 50 x 50 x 3 mm",
          view_shape=b.Pos(-(FX - P["skid_dx"]), 0, -D["deck_top"]) * one, inset_view=(20, -62),
          notes=["Make two. Cut 1200 long (the deck width) from 50 x 50 x 3 tube;",
                 "  square the ends and cap them with 3 mm plate.",
                 "Drill 13 mm through both walls, 40 from each end, on the centre line:",
                 "  these line up with the trailer's two side rails.",
                 "Fit: the skids run across the deck, 500 apart (centres), each 100 in",
                 "  from the ends of the firebox. Weld each to the firebox floor with",
                 "  50 mm stitch welds every 150, both sides.",
                 "Each end is held to the side rail by one M12 bolt through the skid,",
                 "  the deck and the rail, nyloc nut under the rail.",
                 "The skids hold the firebox floor 50 above the deck: an air gap",
                 "  that keeps the deck cool. Never fill it in.",
                 "Check: both skids flat on a level floor; no rock."])

    br = C["brackets"].shape.solids()[0]
    sheet(103, Part("Coil brackets", C["brackets"].shape, COL["brackets"]), [M["coil"], M["stand"]],
          dwg_no="STR-DWG-103", title="SteamRoot coil bracket (make 3): making sketch", material="Stainless steel 316 angle 40 x 40 x 5 mm",
          view_shape=b.Pos(-FX, -br.bounding_box().center().Y, -br.bounding_box().min.Z) * br, inset_view=(-12, -50),
          notes=["Make three from 40 x 40 x 5 stainless angle: one 112 long (back wall)",
                 "  and two about 190 long (the two end walls); cut each to fit.",
                 "One leg lies flat on top (the coil sits on it); the other hangs down.",
                 "Weld each to the inside of the shell with stainless rod, square to",
                 "  the wall, before the lining goes in:",
                 "  back wall: centred, top 410 above the inside of the floor board;",
                 "  left end: 105 in front of the centre line, top about 423 up;",
                 "  right end: 105 in front of the centre line, top about 436 up.",
                 "  (The coil climbs 40 mm a turn, so the three tops differ.)",
                 "Each top sits just under the lowest turn of the coil: set the",
                 "  final height with the coil in place and shim if needed.",
                 "Check: the coil rests on all three, level within 3 mm."])

    sheet(104, Part("Fibre lining", C["lining"].shape, COL["lining"]), [M["shell"], M["stand"]],
          change="Walls 907 tall for the 960 firebox",
          dwg_no="STR-DWG-104", title="SteamRoot fibre lining: cutting sketch", material="Ceramic fibre: 25 mm blanket (2 layers) and 50 mm board",
          view_shape=at0(C["lining"].shape), inset_view=(18, -62),
          notes=["Floor: 50 mm board 694 x 594 (the inside of the shell), laid first.",
                 "Walls: two layers of 25 mm blanket, rigidised, 907 tall, standing",
                 "  on the floor board. Cut the back and front 694 long and the two",
                 "  ends 494 long, so the ends fit between them.",
                 "Roof board: 50 mm board 594 x 494 with a 150 hole in the centre,",
                 "  pinned under the roof plate (it comes off with the roof).",
                 "Cut through the front: door opening 300 x 240 and air inlet",
                 "  160 x 60, lined up with the shell openings.",
                 "Cut through the right end: the two tube slots, 40 wide.",
                 "Slot each wall where the coil brackets pass: bracket size plus 1.",
                 "Hold the blanket with stainless pins welded to the shell, about",
                 "  250 apart, and speed washers. Wear a mask: see the safety stops."])

    sheet(105, Part("Grate stand", C["stand"].shape, COL["stand"]), [M["lining"], M["coil"]],
          dwg_no="STR-DWG-105", title="SteamRoot grate stand: making sketch", material="Square steel tube 25 x 25 x 2 mm; plate 5 mm",
          view_shape=b.Pos(-FX, 0, -F) * C["stand"].shape, inset_view=(25, -62),
          notes=["A square frame of 25 x 25 tube, 300 x 300 outside, mitred and",
                 "  welded, on four legs of the same tube, 70 long.",
                 "Weld a 60 x 60 x 5 pad under each leg so the stand does not sink",
                 "  into the floor board. Overall height 100.",
                 "The 300 x 300 cast grate sits loose on the frame; its top is",
                 "  120 above the floor board.",
                 "Fit: stand it in the middle of the floor, under the coil. The space",
                 "  under the grate is the ash pit; the air inlet opens into it.",
                 "Check: the grate sits flat and does not rock; there is 280 from",
                 "  the grate top to the lowest turn of the coil."])

    sheet(106, Part("Firebox door", C["door"].shape, COL["door"]), [M["shell"], M["lining"]],
          change="Secondary air slot 150 x 20 through the plate and plug",
          dwg_no="STR-DWG-106", title="SteamRoot firebox door: making sketch", material="Mild steel sheet 3 mm; 46 mm fibre board; 16 mm bar",
          view_shape=b.Pos(-FX, 0, -z0) * C["door"].shape, inset_view=(15, -70),
          notes=["Door plate 340 wide x 280 tall, 3 mm: it laps the 300 x 240",
                 "  opening by 20 all round.",
                 "Plug: 49 mm fibre board 292 x 232, screwed to the inside of the plate",
                 "  with stainless screws and washers, centred, so it sits 4 inside the",
                 "  opening all round when the door is shut.",
                 "Handle: 16 mm round bar 120 long on two 20 mm standoffs, centred.",
                 "Secondary air slot: 150 wide x 20 tall through plate and plug,",
                 "  centred, its bottom 200 above the door's bottom edge (above",
                 "  the fire bed); its slide is on sketch 124.",
                 "Hinges: two weld-on lift-off hinges on the right edge, 40 in from",
                 "  top and bottom; weld the shell leaves with the door held shut.",
                 "Latch: a turn latch on the left edge with a keeper welded to the shell.",
                 "Fit: the door closes onto 12 mm ceramic rope glued round the opening.",
                 "Check: the door shuts on the rope all round; the plug clears the",
                 "  lining by about 4 mm."])

    sheet(107, Part("Primary air damper slide", C["damper"].shape + C["guides"].shape, COL["damper"]), [M["shell"], M["door"]],
          change="Named the primary (under-grate) air damper; secondary damper on sketch 124",
          dwg_no="STR-DWG-107", title="SteamRoot primary air damper slide and guides: making sketch", material="Mild steel sheet 3 mm; flat bar 6 mm",
          view_shape=b.Pos(-FX, 0, -z0) * (C["damper"].shape + C["guides"].shape), inset_view=(15, -70),
          notes=["Slide: 3 mm plate 220 wide x 100 tall with a 20 mm knob.",
                 "Guides: two strips 280 long built from 6 x 6 bar and a 3 mm lip,",
                 "  welded to the front of the shell above and below the air inlet,",
                 "  so the slide moves sideways between them.",
                 "Top guide: underside 148 above the bottom of the shell;",
                 "  bottom guide: top 48 above. Air inlet 160 x 60 between them.",
                 "The slide is a loose fit (about 1 mm): it must move by hand when hot.",
                 "This is the primary air, under the grate. Set it with the secondary",
                 "  slide on the door to hold the excess air near 1.5 (see the plan).",
                 "Check: the slide covers the inlet when shut and moves freely;",
                 "  the top guide clears the door plate by at least 3 mm."])

    sheet(108, Part("Monotube coil", C["coil"].shape, COL["coil"]), [M["shell"], M["brackets"]],
          change="10 turns (was 11) so the evaporator bank fits within 8 L of water",
          dwg_no="STR-DWG-108", title="SteamRoot monotube coil: making sketch", material="Stainless steel 316 tube 25.4 OD x 1.65 wall",
          view_shape=b.Pos(-FX, 0, -(D["cz0"] - P["tube_od"] / 2)) * COIL_SWEPT, inset_view=(25, -62),
          notes=["About 13.5 m of 25.4 x 1.65 stainless tube in one length, no joints",
                 "  inside the firebox.",
                 "Wind 10 turns on a 395 mm drum (mean diameter 420), 40 mm a turn,",
                 "  so the tubes stand 14.6 apart. Use a turned wooden or steel former",
                 "  and wind slowly by hand; anneal nothing.",
                 "Leave both ends on the right side, at the same point of the turn:",
                 "  bend each out square to the coil, 150 long, so each tail ends 10",
                 "  outside the shell. The lower tail is the inlet, the upper the outlet.",
                 "Overall: 445 across, 425 tall; tails 1016 and 1416 above the ground",
                 "  when the coil sits on its brackets.",
                 "Pressure test with water before fitting (see the safety stops).",
                 "Check: round within 5; no kinks or flats; both tails level."])

    gl = C["glands"].shape.solids()[0]
    sheet(109, Part("Tube gland plate", gl, COL["glands"]), [M["shell"], M["coil"]],
          dwg_no="STR-DWG-109", title="SteamRoot tube gland plate (make 2): making sketch", material="Mild steel plate 6 mm",
          view_shape=b.Pos(-gl.bounding_box().center().X, 0, -gl.bounding_box().center().Z) * gl, inset_view=(15, -25),
          notes=["Make two: 6 mm plate 80 wide x 100 tall.",
                 "Drill a 26.0 hole for the coil tail, centred across, 35 above the",
                 "  bottom edge: a sliding fit on the 25.4 tube.",
                 "Drill four 7 mm holes for the M6 studs, 56 apart across and 76 apart",
                 "  up, centred on the plate.",
                 "Weld four M6 studs to the shell round each slot to suit.",
                 "Fit: pack the slot round the tail with 12 mm ceramic rope, slide the",
                 "  plate over the tail end, and nip the nuts so the rope seals but",
                 "  the tube can still slide as it grows when hot.",
                 "Fit the plates before the unions go on the tail ends.",
                 "Check: the tube slides in the plate by hand."])

    rf = C["roof"].shape + C["board"].shape
    sheet(110, Part("Firebox roof", rf, COL["roof"]), [M["shell"], M["eco"]],
          change="No economizer studs on the roof; the bank box frame is bolted down with the roof",
          dwg_no="STR-DWG-110", title="SteamRoot firebox roof and roof board: making sketch", material="Mild steel sheet 3 mm; 50 mm fibre board",
          view_shape=b.Pos(-FX, 0, -(top - P["fb_lining_t"])) * rf, inset_view=(25, -62),
          notes=["Roof plate: 3 mm sheet 750 x 650, the outside of the top frame.",
                 "Cut a 150 hole in the centre for the flue.",
                 "Drill 14 holes 9 mm, 12.5 in from the edge, to match the frame:",
                 "  five along each side, two more at each end.",
                 "The evaporator bank box (sketch 122) stands on the roof: its",
                 "  bottom frame takes the same 14 bolts, M8 x 35.",
                 "Roof board: 50 mm fibre board 594 x 494 with a 150 hole, pinned",
                 "  under the plate with stainless pins and speed washers, centred.",
                 "Fit: on a 12 mm ceramic rope gasket on the frame; bank box frame",
                 "  on a second gasket on top; 14 M8 bolts through all three, nuts",
                 "  under the frame. The board fits inside the wall lining.",
                 "Check: the roof seats on the rope all round; no light shows."])

    ebx = C["eco_box"].shape
    sheet(111, Part("Economizer box", ebx, COL["eco_box"]), [M["roof"], M["shell"], M["lid"]],
          change="Sits on the evaporator bank box, not the roof",
          dwg_no="STR-DWG-111", title="SteamRoot economizer box: making sketch", material="Mild steel sheet 2 mm; plate 6 mm; flat bar 25 x 3 mm",
          view_shape=b.Pos(-FX, 0, -D["eco_z0"]) * ebx, inset_view=(20, -62),
          notes=["Base: 6 mm plate 580 x 520 with a 150 hole in the centre and twelve",
                 "  9 mm holes for the studs on the bank box top, 15 in from the edge.",
                 "Walls: 2 mm sheet, 520 x 460 outside, 260 tall, welded to the base.",
                 "Top flange: 25 mm wide, 3 mm, round the top outside, with eight",
                 "  7 mm holes for the lid bolts.",
                 "Two 25 x 3 support bars across the inside, 240 apart, tops 54 above",
                 "  the base: the tube bank rests on them.",
                 "Bulkhead union holes, 13 mm: left end 190 behind the centre line,",
                 "  212 above the base; right end 152 in front, 60 above the base.",
                 "Drain: 12 mm hole in the left end, 14 above the base, and a 20 mm",
                 "  stub with a valve. Flue water is acid: stainless valve.",
                 "The outlet union feeds the evaporator bank, not the coil.",
                 "Check: the base sits flat on the bank box; the lid seats all round."])

    bank = C["eco_bank"].shape
    sheet(112, Part("Economizer tube bank", bank, COL["eco_bank"]), [M["eco"], M["feed"]],
          dwg_no="STR-DWG-112", title="SteamRoot economizer tube bank: making sketch", material="Stainless steel 316 tube 12.7 OD x 1.2 wall",
          view_shape=b.Pos(-FX, 0, -D["eco_floor"]) * bank, inset_view=(62, -62),
          notes=["About 7.3 m of 12.7 x 1.2 stainless tube, bent into a serpentine in",
                 "  three layers. Each straight run is 310 long between bends.",
                 "All bends 38 radius (a standard 1/2 in hand bender): runs and",
                 "  layers 76 apart. Top layer 212 above the box floor, six runs;",
                 "  middle layer 136 up, six runs; bottom layer 60 up, five runs.",
                 "Water goes in at the top layer, left end, 190 behind the centre line,",
                 "  and out at the bottom layer, right end, 152 in front: the gas",
                 "  rises past colder and colder tube (counterflow).",
                 "The layers join with short risers at the left end.",
                 "Fit: lower the bank into the open box onto the support bars, then",
                 "  connect each end to its bulkhead union in the end wall.",
                 "Check: pressure test with water; no run touches the walls."])

    sheet(113, Part("Economizer lid", C["eco_lid"].shape, COL["eco_lid"]), [M["eco"], M["chimney"]],
          dwg_no="STR-DWG-113", title="SteamRoot economizer lid and spigot: making sketch", material="Mild steel sheet 2 mm; tube 148 OD",
          view_shape=b.Pos(-FX, 0, -D["eco_top"]) * C["eco_lid"].shape, inset_view=(25, -62),
          notes=["Lid: 2 mm plate 570 x 510 with a 148 hole in the centre and eight",
                 "  7 mm holes matching the box's top flange.",
                 "Spigot: 148 OD tube, 60 tall, welded into the hole. The chimney",
                 "  (150 bore) slides over it.",
                 "Fit: on a ceramic rope gasket on the top flange; eight M6 bolts.",
                 "The lid comes off to clean the tube bank: clean it every few days",
                 "  of firing; soot cuts the heat recovered.",
                 "Check: the chimney slides over the spigot by hand and stands upright."])

    sheet(114, Part("Header post", C["post"].shape, COL["post"]), [M["header"], M["trailer"], M["pot"]],
          dwg_no="STR-DWG-114", title="SteamRoot header post: making sketch", material="Square steel tube 50 x 50 x 3 mm; plate 10 mm and 6 mm",
          view_shape=b.Pos(-D["hx"], 0, -D["deck_top"]) * C["post"].shape, inset_view=(20, -62),
          notes=["Foot: 10 mm plate 150 x 150 with four 11 mm holes, 100 apart.",
                 "Post: 50 x 50 x 3 tube, 1004 long, welded square on the foot.",
                 "Saddle: 6 mm plate 80 x 60 welded on top; two pairs of 9 mm holes",
                 "  for the two M8 U-bolts that hold the header, 40 apart.",
                 "Fit: the post stands on the deck 130 to the right of the firebox,",
                 "  in line with the header; four M10 bolts through the deck.",
                 "The header rests on the saddle, 1550 above the ground.",
                 "Check: the post is upright both ways within 2 mm over its height."])

    sheet(115, Part("Steam header", C["header"].shape, COL["header"]), [M["post"], M["pot"], M["outlet"], M["diverter"]],
          dwg_no="STR-DWG-115", title="SteamRoot steam header: making sketch", material="Stainless pipe DN50 (60.3 OD); threaded sockets",
          view_shape=b.Pos(-D["hx"], 0, -D["hz"]) * C["header"].shape, inset_view=(25, -50),
          notes=["300 long of DN50 stainless pipe with welded end caps (front and back).",
                 "Weld on: a 25 mm (1 in) socket in the left side, centred, for the",
                 "  coil outlet; a 3/4 in socket on top 60 behind the centre for the",
                 "  relief valve; a 1/4 in socket on top 70 in front for the gauge;",
                 "  a DN32 branch out of the front cap to the seal pot;",
                 "  a 3/4 in nipple out of the back cap to the diverter.",
                 "Nothing on the header may ever close it off from the seal pot.",
                 "Fit: rests on the post saddle under two U-bolts.",
                 "Gauge: 0 to 1 bar on a siphon loop, facing the operator.",
                 "Check: pressure test with water with the seal pot side plugged",
                 "  for the test only; remove the plug after the test."])

    sheet(116, Part("Water-seal pot", C["pot"].shape, COL["pot"]), [M["header"], M["post"], M["stay"], M["overflow"]],
          change="Overflow half coupling at the static water mark; seal limit 0.084 bar",
          dwg_no="STR-DWG-116", title="SteamRoot water-seal pot, dip leg and vent: making sketch", material="Steel pipe 114.3 OD and 42.2 OD; plate 10 mm",
          view_shape=b.Pos(-D["hx"], -D["pot_y"], -D["deck_top"]) * C["pot"].shape, inset_view=(20, -62),
          notes=["Pot: 114.3 OD pipe, 1200 tall, bottom cap welded on a 10 mm foot",
                 "  plate 200 x 200 (four 11 mm holes, 160 apart); top cap welded.",
                 "Dip leg: 42.2 OD pipe inside, against the back wall, its open end",
                 "  100 above the pot bottom; its top is closed and joined to the",
                 "  header branch through the pot wall, 1040 above the foot.",
                 "Static water mark: 990 above the foot (890 above the dip leg end).",
                 "Overflow: 3/4 in half coupling welded in the right side with its",
                 "  bore bottom at the mark (centre 1000 above the foot); the overflow",
                 "  pipe (sketch 125) screws in. The pot can never fill above the mark,",
                 "  so steam can push the water down only 890: 0.084 bar at most.",
                 "Vent: 42.2 OD pipe from the centre of the top cap up to 2300 above",
                 "  the ground. Never valve, cap or narrow the vent.",
                 "Sight tube on the front, drain valve on the right near the bottom.",
                 "Check: fill to the mark; water shows in the sight tube."])

    sheet(117, Part("Pot stay", C["stay"].shape, COL["stay"]), [M["post"], M["pot"]],
          dwg_no="STR-DWG-117", title="SteamRoot pot stay: making sketch", material="Flat bar 40 x 6 mm; band 40 x 3 mm",
          view_shape=b.Pos(-D["hx"], 0, -(D["deck_top"] + 600)) * C["stay"].shape, inset_view=(20, -62),
          notes=["Clamp band: 40 x 3 strip rolled round the pot (114.3), bolted closed",
                 "  with one M8 bolt through two ears.",
                 "Stay: 40 x 6 flat bar, 132 long, welded to the band at one end",
                 "  and to the front face of the header post at the other.",
                 "It holds the pot upright 600 above the deck.",
                 "Check: the pot does not move when pushed at the top."])

    sd = C["saddles"].shape.solids()[0]
    sheet(118, Part("Drum saddle", sd, COL["saddles"]), [M["tank"], M["trailer"]],
          dwg_no="STR-DWG-118", title="SteamRoot drum saddle (make 2): making sketch", material="Hardwood 40 mm, two layers glued",
          view_shape=b.Pos(-P["tank_x"], -sd.bounding_box().center().Y, -D["deck_top"]) * sd, inset_view=(20, -62),
          notes=["Make two. Glue and screw two pieces of 40 mm hardwood, 400 x 100.",
                 "Cut the top to a 250 radius, centred, so the drum sits 20 above the",
                 "  deck at its lowest point.",
                 "Two 11 mm holes for M10 coach bolts through the deck, 25 in",
                 "  from the ends.",
                 "Fit: across the deck, 440 apart (centres), under the drum.",
                 "The drum is held down by two ratchet straps to lashing points.",
                 "Check: the drum sits in both saddles without rocking."])

    hd = C["hood1"].shape
    cx = D["hood_cx"][0]
    sheet(119, Part("Hood shell", hd, COL["hood"]), [part("Hood parts", comp("skirt1", "manifold1", "handles1"), COL["hood"])],
          change="Backing plates for the ballast-rated handles",
          dwg_no="STR-DWG-119", title="SteamRoot hood shell (make 2): making sketch", material="Aluminium sheet 1 mm; mineral wool 40 mm",
          view_shape=b.Pos(-cx, 0, 0) * hd, inset_view=(25, -62),
          notes=["Make two. Outer pan: 1 mm aluminium, 1200 x 1000 x 250, open at",
                 "  the bottom, corners folded and riveted.",
                 "Inner pan: 1 mm aluminium, 1120 x 920 x 210, open at the bottom.",
                 "Fill the 40 mm gap at the top and sides with mineral wool slab;",
                 "  close the bottom edge with a riveted U-channel.",
                 "Fit hardwood blocks in the wool at the four handle foot plates and",
                 "  the inlet, with a 3 mm aluminium backing plate 100 square inside",
                 "  each handle block, so bolts clamp on wood and plate, not on wool.",
                 "Inlet hole: 30.6 through both skins, centred across, 150 in from",
                 "  the end nearest the trailer.",
                 "Check: the hood lies flat on a floor; no wool shows."])

    skr = C["skirt1"].shape
    sheet(120, Part("Hood skirt", skr, COL["skirt"]), [part("Hood parts", comp("hood1", "manifold1", "handles1"), COL["hood"])],
          dwg_no="STR-DWG-120", title="SteamRoot hood skirt (make 2): making sketch", material="Galvanised steel sheet 1.5 mm",
          view_shape=b.Pos(-cx, 0, 0) * skr, inset_view=(15, -62),
          notes=["Make two. A band 100 tall of 1.5 mm galvanised sheet that fits",
                 "  round the outside of the hood: 1203 x 1003 outside.",
                 "Fold the corners; join the ends with rivets.",
                 "The top 40 laps the hood's outer skin; rivet at about 100 centres.",
                 "The bottom 60 goes into the soil: it stops steam escaping sideways.",
                 "Check: the band is tight on the hood; the bottom edge is straight."])

    mn = C["manifold1"].shape
    sheet(121, Part("Hood manifold", mn, COL["manifold"]), [part("Hood parts", comp("hood1", "skirt1", "handles1"), COL["hood"])],
          dwg_no="STR-DWG-121", title="SteamRoot hood manifold and inlet (make 2): making sketch", material="Stainless tube 30 OD; plate 3 mm",
          view_shape=b.Pos(-cx, 0, 0) * mn, inset_view=(-60, -62),
          notes=["Make two. Manifold: 30 OD stainless tube 1040 long, ends capped.",
                 "Drill 4 mm holes every 50 along the underside, in two rows 30",
                 "  degrees each side of straight down (about 40 holes).",
                 "Riser: 30 OD tube 70 long welded upright into the manifold as a tee,",
                 "  150 in from the hood end nearest the trailer.",
                 "Top flange: 3 mm plate, 70 round, welded to the riser; the steam",
                 "  coupling screws into the riser above it.",
                 "Two hanger straps 20 x 2 hold the manifold 15 below the inner skin.",
                 "Fit: the riser goes up through the hood; the flange is bolted on top",
                 "  with high-temperature sealant under it.",
                 "Check: blow through it: air comes out of every hole."])

    bkb = C["bk_box"].shape + C["bk_lining"].shape + C["bk_cover"].shape
    bz0 = D["bk_z0"]
    sheet(122, Part("Evaporator bank box", bkb, COL["bk_box"]), [M["roof"], M["eco"], part("Bank tube", C["bk_bank"].shape, COL["bk_bank"])],
          new=True, dwg_no="STR-DWG-122", title="SteamRoot evaporator bank box: making sketch",
          material="Mild steel sheet 2 mm; angle 25 x 25 x 3 mm; 25 mm fibre blanket and board",
          view_shape=b.Pos(-FX, 0, -bz0) * bkb, inset_view=(22, -62),
          notes=["Walls: 2 mm sheet, 700 x 600 outside (the firebox size), 170 tall,",
                 "  open at the bottom. Top: 2 mm plate welded on, 150 hole in the",
                 "  centre for the flue gas.",
                 "Bottom frame: 25 x 25 x 3 angle round the outside, horizontal leg",
                 "  outward, with 14 holes 9 mm matching the roof bolts.",
                 "Weld twelve M8 studs on the top plate for the economizer base.",
                 "Tail slot: in the right end, 152 in front of the centre line,",
                 "  18 wide, from the bottom edge up to 113: the box lowers over the",
                 "  bank tails. A 3 mm cover with two 16.5 holes closes it (2 x M5).",
                 "Line the walls with 25 mm blanket and pin 25 mm board under the top.",
                 "Fit: on a rope gasket on the roof; the 14 roof bolts clamp it.",
                 "Check: the bank tails slide in the cover holes; no light shows."])

    bkt = C["bk_bank"].shape + C["bk_sups"].shape
    sheet(123, Part("Evaporator bank tube", bkt, COL["bk_bank"]), [M["roof"], part("Bank box", C["bk_box"].shape, COL["bk_box"])],
          new=True, dwg_no="STR-DWG-123", title="SteamRoot evaporator bank tube and supports: making sketch",
          material="Stainless steel 316 tube 15.88 OD x 1.24 wall (5/8 x 0.049 in); flat bar 6 mm",
          view_shape=b.Pos(-FX, 0, -bz0) * bkt, inset_view=(35, -62),
          notes=["About 6.4 m of 15.88 x 1.24 stainless tube in one length, bent",
                 "  into two layers of five runs; bends 47.6 radius (a standard",
                 "  5/8 in bender), runs 95 apart, bend tips 290 each side of the",
                 "  centre. Layers 45 and 105 above the roof plate, joined by a",
                 "  riser at the left end.",
                 "Water goes in at the top layer and out at the bottom layer, both",
                 "  at the right end, 152 in front of the centre: the hottest gas",
                 "  meets the last of the water (counterflow).",
                 "Supports: two 6 mm bars across the box, 300 apart, standing on the",
                 "  roof plate under the bottom layer; two 6 mm spacers between layers.",
                 "Pressure test with water before fitting (see the safety stops).",
                 "Check: the bank sits on all four bars; tails level and square."])

    d2 = C["damper2"].shape + C["guides2"].shape
    sheet(124, Part("Secondary air damper", d2, COL["damper2"]), [M["door"], M["shell"]],
          new=True, dwg_no="STR-DWG-124", title="SteamRoot secondary air damper slide and guides: making sketch",
          material="Mild steel sheet 3 mm; flat bar 3 mm",
          view_shape=b.Pos(-FX, 0, -z0) * d2, inset_view=(15, -70),
          notes=["Slide: 3 mm plate 190 wide x 50 tall with a 16 mm knob at the left.",
                 "Guides: two strips 250 long built from 3 mm bar and a 3 mm lip,",
                 "  welded to the outside of the door plate above and below the",
                 "  secondary air slot, so the slide moves sideways between them.",
                 "The slot is 150 x 20; the slide covers it with 15 to spare.",
                 "Loose fit, about 1 mm: it must move by hand when hot (gloves).",
                 "Secondary air enters above the fire bed and burns the gases off",
                 "  the wood; the primary slide sets the burning rate.",
                 "Check: the slide shuts the slot; the door still closes and latches."])

    ov = C["overflow"].shape + C["ovf_stay"].shape + C["ovf_clip"].shape
    sheet(125, Part("Seal pot overflow", ov, COL["overflow"]), [M["pot"], M["post"], M["trailer"]],
          new=True, dwg_no="STR-DWG-125", title="SteamRoot seal pot overflow, loop seal and clips: making sketch",
          material="Galvanised steel pipe 3/4 in (26.7 OD); flat bar 40 x 6 mm",
          view_shape=b.Pos(-D["hx"], -D["pot_y"], -D["deck_top"]) * ov, inset_view=(20, -40),
          notes=["About 2.6 m of 3/4 in pipe and six elbows, screwed together:",
                 "  from the pot's half coupling 60 to the right, then down 450,",
                 "  across 70, up 350 to the crown, back toward the trailer end,",
                 "  across to the centre line behind the deck, and down to 80",
                 "  above the ground, open end pointing down.",
                 "The U holds 350 of water (a loop seal): steam in the pot cannot",
                 "  blow out of the overflow while the vent carries a surge.",
                 "Drain plug under the U: drain the U with the pot (frost).",
                 "Trap stay: 40 x 6 bar from the pot's clamp band to the down-leg.",
                 "Rear clip: 6 mm plate on the rear rail end (2 x M8), arm and band.",
                 "Check: pour water in the pot above the mark: it runs out at the",
                 "  ground; the outlet is behind the trailer, never at the operator."])

    hdl = C["handles1"].shape
    sheet(126, Part("Hood handles", hdl, COL["handles"]), [part("Hood", comp("hood1", "skirt1"), COL["hood"])],
          new=True, dwg_no="STR-DWG-126", title="SteamRoot hood handles for ballast (make 2 sets): making sketch",
          material="Steel square tube 30 x 30 x 2.5 mm; plate 3 mm",
          view_shape=b.Pos(-cx, 0, 0) * hdl, inset_view=(25, -62),
          notes=["Make two sets (one a hood). Each side: a 900 long bar of 30 x 30",
                 "  x 2.5 tube, ends capped, on two standoffs 800 apart.",
                 "Standoffs: 30 x 30 tube 57 long, welded to the bar and to a 100 x",
                 "  100 x 3 foot plate with four 7 mm holes.",
                 "Fit: foot plates on the hood sides, centred 60 down from the top,",
                 "  through-bolted (4 x M6 each) to the backing plates in the wall.",
                 "Sized to carry ballast weights: up to 40 kg a hood, hung two a",
                 "  side, at a load factor of 2 (bending about 34 MPa in the bar).",
                 "Take the weights off before the hood is lifted and moved.",
                 "Check: a 20 kg weight hung mid-bar: no visible bend or play."])
    return out


# ----------------------------------------------------------------- joints
def joints():
    out = []
    hx, hz, py = D["hx"], D["hz"], D["pot_y"]
    T = D["deck_top"]
    # 01 skid end bolted to the side rail (cut through the bolt)
    ry = P["deck_w"] / 2 - P["rail_w"] / 2
    xs = FX - P["skid_dx"]
    w = (xs - 90, xs + 90, ry - 70, P["deck_w"] / 2 + 5, P["deck_z"] - 25, T + 90)
    out.append(bv.joint([
        part("Trailer side rail and deck", win(C["trailer"].shape, *w), COL["trailer"]),
        part("Firebox skid", win(C["skids"].shape, *w), COL["skids"]),
        part("M12 bolt, nyloc nut under the rail", win(C["skid_bolts"].shape, *w), COL["bolt"]),
        part("Firebox shell, welded to the skid", win(C["shell"].shape, *w), COL["shell"])],
        OUT / "joint-01.png", "Joint 1: skid end on the trailer's side rail (back left corner)",
        subtitle="Cut through the bolt. The skid is welded under the firebox and bolted through the deck into the rail",
        cut="-X", elev=12, azim=-30, size=(8, 6)))
    # 02 coil bracket through the lining, coil resting on it (back wall)
    xh, yh, zh = helix_point(90)
    w = (xh - 90, xh + 90, yh - 60, P["fb_w"] / 2 + 5, zh - 75, zh + 22)
    out.append(bv.joint([
        part("Firebox shell (back wall)", win(C["shell"].shape, *w), COL["shell"]),
        part("Fibre lining, slotted round the bracket", win(C["lining"].shape, *w), COL["lining"]),
        part("Coil bracket, welded to the shell", win(C["brackets"].shape, *w), COL["brackets"]),
        part("Lowest turn of the coil", win(C["coil"].shape, *w), COL["coil"])],
        OUT / "joint-02.png", "Joint 2: coil bracket through the lining (back wall)",
        subtitle="Cut open, seen from inside the firebox. The coil rests on the bracket; nothing else holds it",
        cut="-X", elev=18, azim=-100, size=(8, 6)))
    # 03 lower firebox cut open: grate, stand, door plug, air inlet, damper
    w = (FX - 360, FX + 360, -P["fb_w"] / 2 - 40, P["fb_w"] / 2 + 5, D["fb_z0"] - 5, D["cz0"] + 60)
    out.append(bv.joint([
        part("Firebox shell", win(C["shell"].shape, *w), COL["shell"]),
        part("Fibre lining", win(C["lining"].shape, *w), COL["lining"]),
        part("Grate stand", win(C["stand"].shape, *w), COL["stand"]),
        part("Cast grate", win(C["grate"].shape, *w), COL["grate"]),
        part("Door with its board plug", win(C["door"].shape, *w), COL["door"]),
        part("Air damper slide in its guides", win(C["damper"].shape + C["guides"].shape, *w), COL["damper"]),
        part("Lowest turns of the coil", win(C["coil"].shape, *w), COL["coil"])],
        OUT / "joint-03.png", "Joint 3: the lower firebox, cut through the middle",
        subtitle="Seen from the right. Air comes in under the grate; wood goes in through the door; the coil starts 280 above the grate",
        cut="-X", elev=8, azim=0, size=(8, 6.5)))
    # 04 coil tails through the wall slots, gland plates, unions
    w = (D["fb_x1"] - 70, D["fb_x1"] + 75, -60, 60, D["cz0"] - 50, D["coil_top"] + 120)
    out.append(bv.joint([
        part("Firebox shell (right end)", win(C["shell"].shape, *w), COL["shell"]),
        part("Fibre lining", win(C["lining"].shape, *w), COL["lining"]),
        part("Coil tails", win(C["coil"].shape, *w), COL["coil"]),
        part("Gland plates on M6 studs", win(C["glands"].shape + C["gland_studs"].shape, *w), COL["glands"]),
        part("Union, coil outlet pipe", win(C["outlet"].shape, *w), COL["outlet"]),
        part("Union and reducer, inlet jumper", win(C["jumper"].shape, *w), COL["jumper"])],
        OUT / "joint-04.png", "Joint 4: coil tails out through the wall slots",
        subtitle="Cut through the tails. Each slot runs 30 mm above its tail; the gland plate covers it and rope packing seals it",
        cut="+Y", elev=10, azim=-90, size=(8, 6.5)))
    # 05 roof, economizer flange, box, bank, lid, spigot, chimney (cut)
    w = (FX - 380, FX + 380, -330, 330, D["fb_top"] - 70, D["lid_top"] + 160)
    out.append(bv.joint([
        part("Firebox shell and top frame", win(C["shell"].shape, *w), COL["shell"]),
        part("Roof plate, bolted to the frame", win(C["roof"].shape + C["roof_bolts"].shape, *w), COL["roof"]),
        part("Roof board", win(C["board"].shape, *w), COL["board"]),
        part("Evaporator bank box, lined", win(C["bk_box"].shape + C["bk_lining"].shape, *w), COL["bk_box"]),
        part("Evaporator bank on its bars", win(C["bk_bank"].shape + C["bk_sups"].shape, *w), COL["bk_bank"]),
        part("Economizer box on studs", win(C["eco_box"].shape + C["eco_bolts"].shape, *w), COL["eco_box"]),
        part("Economizer tube bank", win(C["eco_bank"].shape, *w), COL["eco_bank"]),
        part("Lid and spigot", win(C["eco_lid"].shape + C["lid_bolts"].shape, *w), COL["eco_lid"]),
        part("Chimney over the spigot", win(C["chimney"].shape, *w), COL["chimney"])],
        OUT / "joint-05.png", "Joint 5: roof, evaporator bank, economizer and chimney, cut",
        subtitle="Seen from the front. Flue gas rises through the roof hole, past both tube banks and up the chimney",
        cut="+Y", elev=8, azim=-90, size=(8, 6.5)))
    # 06 header on its post: saddle, U-bolts, coil outlet, relief, diverter, link
    w = (hx - 120, hx + 120, py - 70, D["div_y"] + 60, hz - 130, hz + 240)
    out.append(bv.joint([
        part("Header post and saddle", win(C["post"].shape, *w), COL["post"]),
        part("U-bolts", win(C["post_bolts"].shape, *w), COL["bolt"]),
        part("Steam header and gauge", win(C["header"].shape, *w), COL["header"]),
        part("Coil outlet pipe", win(C["outlet"].shape, *w), COL["outlet"]),
        part("Relief valve and discharge", win(C["relief"].shape + C["discharge"].shape, *w), COL["relief"]),
        part("Diverter and hose coupling", win(C["diverter"].shape, *w), COL["diverter"]),
        part("Branch to the seal pot", win(C["pot"].shape, *w), COL["pot"]),
        part("Diverter vent line", win(C["vent_line"].shape, *w), COL["vent_line"])],
        OUT / "joint-06.png", "Joint 6: the steam header on its post",
        subtitle="Seen from the right and above. Coil steam comes in from the left; the seal pot branch can never be closed",
        elev=20, azim=-20, size=(8, 6.5)))
    # 07 seal pot cut open: dip leg, water mark, vent, link
    # y window chosen so the common centre the cut uses is the pot axis (the sight tube sets the low side)
    w = (hx - 110, hx + 200, py - 120, py + P["seal_pot_od"] / 2 + 18, D["water_line"] - 560, D["vent_line_z"] + 60)
    import build123d as b
    wr = P["seal_pot_od"] / 2 - 3.05                 # water in the pot and in the dip leg, at the static mark
    water = b.Pos(hx, py, D["pot_bot"] + 6) * b.extrude(b.Circle(wr), D["water_line"] - D["pot_bot"] - 6)
    dip_y = py + (wr - P["dip_od"] / 2 - 1)
    water -= b.Pos(hx, dip_y, D["dip_end"]) * b.extrude(b.Circle(P["dip_od"] / 2), 3000)
    water += b.Pos(hx, dip_y, D["dip_end"]) * b.extrude(b.Circle(P["dip_od"] / 2 - 3.56), D["water_line"] - D["dip_end"])
    out.append(bv.joint([
        part("Seal pot, dip leg and vent", win(C["pot"].shape, *w), COL["pot"]),
        part("Water at the mark", win(water, *w), "#93C5FD", alpha=0.9),
        part("Dip leg top and branch from the header", win(C["header"].shape, *w), COL["header"]),
        part("Vent pipe; the diverter vent line joins above", win(C["vent_line"].shape, *w), COL["vent_line"]),
        part("Pot stay and clamp band", win(C["stay"].shape, *w), COL["stay"]),
        part("Overflow at the water mark, loop seal", win(C["overflow"].shape + C["ovf_stay"].shape, *w), COL["overflow"])],
        OUT / "joint-07.png", "Joint 7: the water-seal pot, cut open (upper part)",
        subtitle="Seen from the front. The overflow holds the water at the mark; over 0.084 bar steam empties the dip leg to the vent",
        cut="+Y", elev=6, azim=-90, size=(8, 9)))
    # 08 hood edge cut open: skin, skirt, manifold, hanger, inlet riser, flange, coupling
    cx = D["hood_cx"][0]
    ix = D["hood_inlet_x"][0]
    w = (ix - 260, ix + 140, -120, 130, -70, P["hood_h"] + 90)
    out.append(bv.joint([
        part("Hood shell (double skin, wool between)", win(C["hood1"].shape, *w), COL["hood"]),
        part("Skirt, riveted round the outside", win(C["skirt1"].shape, *w), COL["skirt"]),
        part("Manifold, riser, flange and coupling", win(C["manifold1"].shape, *w), COL["manifold"]),
        part("Steam hose", win(C["hose"].shape, *w), COL["hose"])],
        OUT / "joint-08.png", "Joint 8: hood end, cut through the steam inlet",
        subtitle="Seen from the front. The skirt goes 60 mm into the soil; steam leaves the manifold through holes on its underside",
        cut="+Y", elev=10, azim=-90, size=(8, 6)))
    # 09 door hinge and latch
    yd = -P["fb_w"] / 2
    dz = (D["F"] + P["door_open"][2] - P["door_lap"], D["F"] + P["door_open"][2] + P["door_open"][1] + P["door_lap"])
    w = (FX - 250, FX + 250, yd - 60, yd + 60, dz[0] - 40, dz[1] + 20)
    out.append(bv.joint([
        part("Firebox shell (front)", win(C["shell"].shape, *w), COL["shell"]),
        part("Door and handle", win(C["door"].shape, *w), COL["door"]),
        part("Lift-off hinges", win(C["hinges"].shape, *w), COL["hinges"]),
        part("Turn latch and keeper", win(C["latch"].shape, *w), COL["latch"]),
        part("Primary damper slide and guides", win(C["damper"].shape + C["guides"].shape, *w), COL["damper"]),
        part("Secondary damper on the door", win(C["damper2"].shape + C["guides2"].shape, *w), COL["damper2"])],
        OUT / "joint-09.png", "Joint 9: door hinges, latch and the two air dampers",
        subtitle="Seen from the front left. The door hinges on its right edge and latches on its left",
        elev=14, azim=-120, size=(8, 6)))
    # 10 drum on its saddles with a strap
    tx = P["tank_x"]
    w = (tx - 300, tx + 300, -P["tank_l"] / 2 - 20, 0, D["deck_top"] - 85, D["tank_z"] + 280)
    out.append(bv.joint([
        part("Trailer deck", win(C["trailer"].shape, *w), COL["trailer"]),
        part("Hardwood saddle, bolted to the deck", win(C["saddles"].shape + C["saddle_bolts"].shape, *w), COL["saddles"]),
        part("Feed drum, 125 L", win(C["tank"].shape, *w), COL["tank"]),
        part("Ratchet strap to a lashing point", win(C["straps"].shape, *w), COL["straps"])],
        OUT / "joint-10.png", "Joint 10: feed drum on its saddles (front half)",
        subtitle="The drum lies across the deck in two curved saddles; a ratchet strap over each holds it down",
        elev=15, azim=-35, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    sh = M["shell"]
    st(1, [sh], [mv(M["skids"], (0, 0, -250))], "skids under the firebox shell",
       "Shell standing on the bench. Two skids across the floor, 500 apart, stitch welded both sides", elev=12, azim=-62)
    st(2, [sh, M["skids"]], [mv(M["brackets"], (0, 0, 650)), mv(M["guides"], (0, -200, 0)),
                             mv(part("Hinge and latch leaves", comp("hinges", "latch"), COL["hinges"]), (0, -200, 0))],
       "weld on the brackets, guides and hinge leaves",
       "Coil brackets inside (stainless rod); damper guides, hinges, latch keeper, gland studs and clip lugs outside",
       elev=30, azim=-62, label_done=False)
    st(3, [M["trailer"]], [mv(part("Firebox shell with skids", comp("shell", "skids", "brackets", "guides"), COL["shell"]), (0, 0, 500))],
       "firebox onto the trailer",
       "Lift with a hoist or four people. Skids across the deck; four M12 bolts through the skids, deck and side rails",
       elev=18, azim=-62, label_done=False)
    fb = [M["trailer"], part("Firebox shell", comp("shell", "skids", "brackets", "guides"), COL["shell"])]
    st(4, fb, [mv(M["lining"], (0, 0, 1100))], "fibre lining into the firebox",
       "Floor board first, then two layers of blanket on the walls; cut round the door, air inlet, slots and brackets",
       elev=22, azim=-62, label_done=False)
    fb2 = fb + [M["lining"]]
    st(5, fb2, [mv(M["stand"], (0, 0, 1100))], "grate stand and grate",
       "Lowered in through the open top; stand in the middle of the floor, grate loose on top",
       elev=40, azim=-62, label_done=False)
    fb3 = fb2 + [M["stand"]]
    st(6, fb3[1:], [mv(M["door"], (0, -450, 0)), mv(M["damper"], (-500, -60, 0)), mv(M["damper2"], (-500, -450, 0))], "door and air dampers",
       "Hang the door on its hinges; rope round the opening. Slide both damper slides into their guides from the side",
       elev=14, azim=-62, label_done=False)
    fb4 = fb3 + [M["door"], M["damper"], M["damper2"]]
    st(7, fb4, [mv(M["coil"], (-66, 0, 700))], "coil into the firebox",
       "Lower it in 66 mm toward the left so the tails clear; at 30 mm above the brackets slide it right, tails out through the slots; set it down",
       elev=30, azim=-62, label_done=False)
    fb5 = fb4 + [M["coil"]]
    st(8, fb5, [mv(M["glands"], (250, 0, 0))], "gland plates over the coil tails",
       "Pack each slot round the tail with ceramic rope, slide the plate on, nip the four M6 nuts. Tube must still slide",
       elev=14, azim=-35, label_done=False)
    fb6 = fb5 + [M["glands"]]
    st(9, fb6, [mv(M["roof"], (0, 0, 500))], "roof onto the firebox",
       "Ceramic rope gasket on the top frame; roof with its board lowered on; 14 M8 bolts round the edge",
       elev=24, azim=-62, label_done=False)
    fb7 = fb6 + [M["roof"]]
    st(10, [part("Economizer box", C["eco_box"].shape, "#D1D5DB")], [mv(part("Tube bank", C["eco_bank"].shape, COL["eco_bank"]), (0, 0, 400))],
       "tube bank into the economizer box (on the bench)",
       "Lower the bank onto the two support bars; connect each end to its bulkhead union through the end wall",
       elev=30, azim=-62, label_done=True)
    bank_parts = part("Evaporator bank on its bars", comp("bk_bank", "bk_sups"), COL["bk_bank"])
    bank_box = part("Bank box, lined", comp("bk_box", "bk_lining", "bk_cover"), COL["bk_box"])
    st(11, fb7, [mv(bank_parts, (0, 0, 250)), mv(bank_box, (0, 0, 650)), mv(M["eco"], (0, 0, 1050)), mv(M["lid"], (0, 0, 1350))],
       "evaporator bank, economizer and lid onto the roof",
       "Bank on its bars, box lowered over it, slot cover on, 14 roof bolts. Economizer on the box studs; lid, eight M6 bolts",
       elev=20, azim=-62, label_done=False)
    fb8 = fb7 + [M["bank"], M["eco"], M["lid"]]
    st(12, fb8, [mv(M["chimney"], (0, 0, 450))], "chimney and spark arrestor",
       "Chimney slid over the spigot, three self-drilling screws; cap pushed on top, mesh in place",
       elev=16, azim=-62, label_done=False)
    fb9 = fb8 + [M["chimney"]]
    st(13, fb9, [mv(M["post"], (0, 0, 400)), mv(M["header"], (0, 0, 650))], "header post and header",
       "Post on the deck, four M10 bolts. Header on the saddle under two U-bolts, sockets as the header sketch shows",
       elev=18, azim=-40, label_done=False)
    fb10 = fb9 + [M["post"], M["header"]]
    st(14, [fb[1], M["coil"], M["glands"], M["roof"], M["post"], M["header"]], [mv(M["outlet"], (0, -350, 0))], "coil outlet pipe to the header",
       "Union onto the upper coil tail, other end into the header's side socket. Tighten the union last, without strain",
       elev=18, azim=-40, label_done=False)
    fb11 = fb10 + [M["outlet"]]
    st(15, fb11, [mv(M["pot"], (0, -350, 0)), mv(M["stay"], (0, -200, 0)), mv(M["overflow"], (0, -350, 0))],
       "water-seal pot, stay and overflow",
       "Pot on its foot plate (four M10 bolts), stay band round it; overflow into its half coupling, trap stay and rear clip",
       elev=18, azim=-40, label_done=False)
    fb12 = fb11 + [M["pot"], M["stay"], M["overflow"]]
    st(16, fb12, [mv(M["relief"], (0, 0, 450)), mv(M["diverter"], (0, 350, 0))], "relief valve and diverter",
       "Relief valve upright on top of the header, discharge pipe to 2.3 m, stay to the vent. Diverter on the back nipple, vent line into the vent",
       elev=18, azim=-40, label_done=False)
    fb13 = fb12 + [M["relief"], M["diverter"]]
    st(17, fb13, [mv(M["saddles"], (0, 0, 300)), mv(M["tank"], (0, 0, 600))], "feed drum on its saddles",
       "Saddles across the deck, two M10 coach bolts each. Drum in the saddles, outlet toward the pump box; two ratchet straps",
       elev=20, azim=-62, label_done=False)
    fb14 = fb13 + [M["saddles"], M["tank"]]
    st(18, fb14, [mv(M["pbox"], (0, -750, 0)), mv(M["feed"], (-250, 0, 250))], "pump box and feed lines",
       "Box bolted down. Suction hose to the pump; feed line to the economizer (two clips); bank link; jumper to the coil",
       elev=20, azim=-50, label_done=False)
    st(19, [part("Hood shell", comp("hood1"), COL["hood"])],
       [mv(part("Skirt", C["skirt1"].shape, COL["skirt"]), (0, 0, -250)),
        mv(part("Manifold and inlet", C["manifold1"].shape, COL["manifold"]), (0, 0, -300)),
        mv(part("Handles", C["handles1"].shape, COL["handles"]), (0, 0, 200))],
       "build each hood (on the bench, make two)",
       "Hood upside down: manifold hung, riser up through the top; skirt riveted on; handles bolted to the backing plates",
       elev=-25, azim=-62, label_done=True)
    full = fb14 + [M["pbox"], M["feed"]]
    st(20, full + [M["hood"]], [mv(M["hose"], (0, 200, 300))], "steam hose to a hood",
       "Hose from the diverter coupling to the hood inlet, whip checks fitted at both ends. Moved only with steam to the vent",
       elev=18, azim=-62, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 6.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 66); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 64, "SteamRoot prototype: 12 V wiring of the feed pump and alarms", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 60.6, "Bought parts wired at block level inside the pump and alarm box. Stranded copper; ferrules or crimped lugs on every terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/steamroot", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((14, 12.6), 66, 41.4, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(15.5, 52.8, "Inside the pump and alarm box", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(17, 40, 14, 10, "Battery", "12 V 20 Ah\nsealed lead acid", "#374151")
    blk(36, 40, 12, 10, "Fuse", "10 A blade,\nnear the battery", "#7C3AED")
    blk(53, 40, 12, 10, "Main switch", "2-pole,\nweatherproof", "#7C3AED")
    blk(17, 17, 16, 14, "Feed pump", "12 V diaphragm,\nabout 4 L/min,\nneedle valve and\nflow meter after it", "#16A34A")
    blk(37.5, 17, 13.5, 12, "Buzzer and lamp", "on the box lid,\nloud enough to\nhear at the hoods", "#DC2626")
    blk(58, 17, 18, 14, "Alarm controller", "type K input,\nalarm set about\n150 C, relay out", "#0F766E")
    blk(86, 40, 22, 11, "Coil outlet thermocouple", "type K, clamped to\nthe outlet pipe beside\nthe header", "#B87333")
    blk(86, 19, 22, 11, "Tank float switch", "low level, in the\ndrum, about 20 L left", "#2563EB")
    wire([(31.3, 45), (35.7, 45)], RED); lab(33.5, 47.2, "2.5 mm²", RED, "center")
    wire([(48.3, 45), (52.7, 45)], RED); lab(50.5, 47.2, "2.5 mm²", RED, "center")
    wire([(56, 39.7), (56, 35), (25, 35), (25, 31.3)], RED); lab(30, 36.6, "pump +, 2.5 mm²", RED)
    wire([(62, 39.7), (62, 31.3)], RED); lab(62.7, 35.4, "controller +, 0.75 mm²", RED)
    wire([(16.7, 44), (15.6, 44), (15.6, 14.6), (67, 14.6), (67, 16.7)], GRY, 1.4)
    wire([(25, 14.6), (25, 16.7)], GRY, 1.4); wire([(44.25, 14.6), (44.25, 16.7)], GRY, 1.4)
    wire([(57.7, 24), (51.3, 24)], RED, 1.3); lab(54.5, 26.2, "alarm out", RED, "center")
    wire([(85.7, 44), (81, 44), (81, 28), (76.3, 28)], "#B87333", 1.3); lab(81.7, 36, "thermocouple cable,\ntype K, no joints", "#B87333")
    wire([(85.7, 23), (76.3, 23)], BLU, 1.3); lab(81, 21.2, "float, 0.75 mm²", BLU, "center")
    ax.text(16, 9.4, "The alarms only warn: they do not stop the fire. On an alarm, close the air damper, keep the feed running if the tank has water,",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(16, 6.6, "and never restart the feed into a hot, dry coil. All circuits are 12 V; no mains wiring is part of this build.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(16, 3.9, "Red: 12 V supply. Grey: 0 V return (2.5 mm² to the pump, 0.75 mm² to the buzzer and controller). Blue: float switch. Copper: thermocouple (type K cable all the way).", fontsize=7.2, color=MUT)
    OUT.mkdir(parents=True, exist_ok=True)
    o = OUT / "wiring.png"
    fig.savefig(o, facecolor="white"); plt.close(fig)
    return o


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "joints": joints, "steps": steps, "wiring": wiring}
    i = 0
    while i < len(args):
        a = args[i]
        if a == "sheets":
            nums = []
            while i + 1 < len(args) and args[i + 1].isdigit():
                nums.append(int(args[i + 1])); i += 1
            print("sheets ->", sheets(set(nums) or None))
        else:
            print(a, "->", fns[a]())
        i += 1

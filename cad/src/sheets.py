"""SteamRoot general arrangement drawing STR-DWG-002 Rev P4 (constructable design, STR-DDR-003, with the 2026-10-02 decisions).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/STR-DWG-002.svg, .pdf and .png with .kit/drawing.py from cad/src/model.py.
STR-DWG-001 is the concept blueprint sheet in media/. PRELIMINARY, NOT FOR FABRICATION.
"""
import shutil
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
sys.path.insert(0, str(ROOT / "docs" / "04-calcs"))
from drawing import Sheet, project_views  # noqa: E402
from model import build_components, coil_display, derived, PARAMS as P  # noqa: E402
from build123d import Compound  # noqa: E402
from sizing import run  # noqa: E402

c = run()
C = build_components()
C["coil"] = C["coil"]._replace(shape=coil_display())     # same centreline; the swept helix is very slow to project
asm = Compound(children=[c.shape for c in C.values()])
D = derived()
bb = asm.bounding_box()
work = ROOT / "cad" / "drawings" / "_views"
views = project_views(asm, work)

s = Sheet(project="SteamRoot", title="General arrangement, working position", dwg_no="STR-DWG-002", rev="P4",
          author="Amish Chadha", date="2026-10-02", theme="technical",
          material="PRELIMINARY, NOT FOR FABRICATION. Boiler authority ruling OPEN (prerequisite)",
          revisions=[("P1", "Preliminary GA from TRL 3 model; regulatory ruling open", "2026-09-25", "AC"),
                     ("P2", "Notes per STR-DDR-002: relief valve capacity, towed mass, R6 limits", "2026-09-25", "AC"),
                     ("P3", "Constructable design per STR-DDR-003; making sketches STR-DWG-101 to 121", "2026-10-01", "AC"),
                     ("P4", "Evaporator bank, dampers, seal pot overflow, ballast handles (2026-10-02)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 96, label="Isometric view", sublabel="Not to scale")

s.add_notes("Items (BOM numbers)", [
    "1 Trailer frame and drawbar; 2 Wheels (2)",
    "3 Feed tank 125 L; 4 Feed pump 12 V",
    f"5 Firebox {P['fb_l']:.0f} x {P['fb_w']:.0f} x {P['fb_h']:.0f} on skids, {P['fb_lining_t']:.0f} fiber; 2 air dampers",
    f"6 Coil 316 SS {P['tube_od']} x {P['tube_wall']}, {c['L_coil']:.1f} m, {P['coil_turns']} turns, above the fire",
    f"22 Evaporator bank {P['fb_l']:.0f} x {P['fb_w']:.0f} x {P['bk_h']:.0f}, {c['L_bank']:.1f} m of {P['bk_tube_od']} tube",
    f"7 Economizer {P['eco_l']:.0f} x {P['eco_w']:.0f} x {P['eco_h']:.0f}, {P['eco_tube_len']/1000:.1f} m tube",
    f"8 Chimney DN{P['chimney_d']:.0f}, outlet {P['chimney_top']/1000:.1f} m, 6 mm mesh",
    f"9 Header DN50 at {P['header_z']/1000:.2f} m; dip leg {D['dip']:.0f}; vent {P['vent_top']/1000:.1f} m",
    f"  Seal pot overflow at the water mark, {P['ovf_trap']:.0f} loop seal, to ground at rear",
    f"10 Certified relief valve, 15 psi (1.03 bar), rated {c['rv_rated_kg_h']:.0f} kg/h",
    f"11 Steam hose, 25 bore x {P['hose_len']/1000:.0f} m",
    f"12 Hoods (2), {P['hood_l']:.0f} x {P['hood_w']:.0f} x {P['hood_h']:.0f}, handles for {P['ballast_kg']:.0f} kg ballast",
    "17 to 21 Skids, post, stay, saddles; brackets, stand, glands;",
    "  feed lines; vent line and relief discharge; fixings",
], x=276, y=140, width=140)

s.add_notes("Key dimensions and notes", [
    f"Overall, working position: {bb.size.X/1000:.2f} m long, {c['width']:.2f} m wide, {bb.size.Z/1000:.2f} m high (mm on sheet)",
    f"Deck {P['deck_l']:.0f} x {P['deck_w']:.0f} at {P['deck_z'] + P['deck_t']:.0f} above ground; towed {c['m_empty_tank']:.0f} kg drained ({c['m_total']:.0f} kg full)",
    f"Normal pressure: header {c['p_header']/1e5:.3f} bar (limit 0.1), bank inlet {c['p_inlet']/1e5:.2f} bar (limit 0.15); seal {c['p_seal']/1e5:.3f} bar",
    "Steam side always open to the vent; diverter has no closed position; no isolating valve",
    "Hose moved between hoods only after steam is diverted to the vent",
    "Water in heated section %.1f L flooded; 30 kg/h steam, %.0f kW firing (CAL-001)" % (c["V_heated"], c["fb"]["Q_in"]),
    "Firebox and chimney outdoors only; generator never inside a greenhouse",
    "OPEN PREREQUISITE: written ruling from the local boiler authority",
    "on this open-vented fired coil. No detail design or build before it.",
    "Making sketches STR-DWG-101 to 121; build plan STR-BLD-001",
], x=20, y=196, width=205)

out = ROOT / "cad" / "drawings" / "STR-DWG-002"
s.save(out)
shutil.rmtree(work, ignore_errors=True)
print(f"wrote {out}.svg, .pdf, .png at scale 1:{1/s.scale:g}")

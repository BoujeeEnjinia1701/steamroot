"""SteamRoot concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py and the figures from docs/04-calcs/sizing.py (STR-CAL-001),
so the media, the model and the calculation stay in step. Not for fabrication.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
sys.path.insert(0, str(ROOT / "docs" / "04-calcs"))
from concept import Part, render_all  # noqa: E402
from model import build_components, coil_display, GROUP_ORDER  # noqa: E402
from build123d import Compound  # noqa: E402
from sizing import run  # noqa: E402

C = build_components()
C["coil"] = C["coil"]._replace(shape=coil_display())   # same centreline; the swept helix takes minutes to tessellate
g = {grp: Compound(children=[c.shape for c in C.values() if c.group == grp]) for grp in GROUP_ORDER}
c = run()
fb = c["fb"]

STYLE = [  # (model part name, label, color, BOM item, exploded offset in mm)
    ("Trailer frame and drawbar", "Trailer frame and drawbar", "#4B5563", 1, (0, 0, -380)),
    ("Wheels", "Wheels", "#1F2937", 2, (0, 0, -760)),
    ("Firebox skids", "Firebox skids", "#1D4ED8", 17, (0, 0, -150)),
    ("Feed water tank, 125 L", "Feed water tank, 125 L", "#2563EB", 3, (-350, 0, 250)),
    ("Feed pump", "Pump and alarm box", "#7C3AED", 4, (-200, 500, 150)),
    ("Feed lines", "Feed lines", "#A855F7", 19, (-350, 0, 450)),
    ("Firebox, fiber lined", "Firebox, fiber lined", "#9A3412", 5, (0, -700, 0)),
    ("Monotube steam coil", "Monotube steam coil", "#B87333", 6, (0, 0, 0)),
    ("Flue-gas economizer", "Flue-gas economizer", "#D4A017", 7, (0, 0, 700)),
    ("Chimney and spark arrestor", "Chimney and spark arrestor", "#6B7280", 8, (0, 0, 1300)),
    ("Steam header and water-seal vent", "Steam header and water-seal vent", "#0F766E", 9, (450, -500, 350)),
    ("Certified relief valve", "Certified relief valve", "#DC2626", 10, (450, 450, 650)),
    ("Steam hose", "Steam hose", "#111827", 11, (650, 0, 250)),
    ("Steam hoods (2)", "Steam hoods, 1.2 x 1.0 m (2)", "#D1D5DB", 12, (1000, 0, 0)),
]
parts = [Part(label, g[name], color, bom, off) for name, label, color, bom, off in STYLE]

soil_kw = c["Q_steam"] * c["d15"]["eta_hood"]
render_all(
    parts, project="SteamRoot", title="Biomass steam trailer, TRL 3 model", dwg_no="STR-DWG-001",
    key_figures=[
        f"Open-vented: water seal {c['p_seal']/1e5:.3f} bar; coil inlet {c['p_inlet']/1e5:.2f} bar gauge (calc.)",
        f"30 kg/h steam from {fb['wood_kg_h']:.0f} kg/h wood, {100*fb['eta']:.0f} % fuel to steam (calc.)",
        f"{c['d15']['ms']:.1f} kg steam per m2 to 70 C at 15 cm (calc.)",
        f"{c['rate15_2']:.1f} m2/h at 15 cm, {c['rate5_2']:.1f} m2/h at 5 cm, two hoods (calc.)",
        f"Towed mass {c['m_empty_tank']:.0f} kg drained ({c['m_total']:.0f} kg full), width {c['width']:.2f} m (calc.)",
    ],
    cut_exclude=("Wheels", "Steam hose"),
    flow={"title": "energy flow at 30 kg/h steam, 15 cm depth (all values calculated estimates, STR-CAL-001)",
          "unit": "kW (est.)",
          "stages": [("Wood fuel in", round(fb["Q_in"], 1)), ("Steam generator", round(c["Q_steam"], 1)),
                     ("Steam hoods", round(c["Q_steam"], 1)), ("Soil, 0 to 16.5 cm", round(soil_kw, 1))],
          "losses": [(1, "Flue and shell", round(fb["Q_in"] - c["Q_steam"], 1)),
                     (2, "Skirt and hood", round(c["Q_steam"] - soil_kw, 1))]},
)

# The kit exports glTF at a very fine tessellation; the 15 m helix then makes model.glb about 10 MB.
# Re-export the same colored parts at a coarser tolerance for the web viewer.
from build123d import Compound, Color, export_gltf  # noqa: E402
import matplotlib.colors as mc  # noqa: E402
kids = []
for p_ in parts:
    sh = p_.shape
    sh.color = Color(*mc.to_rgb(p_.color))
    sh.label = p_.name
    kids.append(sh)
export_gltf(Compound(children=kids), str(ROOT / "media" / "model.glb"), binary=True,
            linear_deflection=1.0, angular_deflection=0.3)

"""SteamRoot concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the trailer (drawbar at -X, steam hood at +X), Y across, Z up. Millimeters.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

# Trailer (small single-axle garden trailer class)
DECK_L, DECK_W, DECK_T = 2000.0, 1200.0, 80.0
WHEEL_R, WHEEL_W = 230.0, 120.0
DECK_Z = 420.0                      # underside of the deck frame
deck_top = DECK_Z + DECK_T

frame = Pos(0, 0, DECK_Z + DECK_T / 2) * Box(DECK_L, DECK_W, DECK_T)
drawbar = Pos(-DECK_L / 2 - 400, 0, DECK_Z + DECK_T / 2) * Box(800, 80, 80)
jack = Pos(-DECK_L / 2 - 650, 0, DECK_Z / 2) * Cylinder(30, DECK_Z)
axle_x = 150.0
wheel = lambda y: Pos(axle_x, y, WHEEL_R) * Rot(90, 0, 0) * Cylinder(WHEEL_R, WHEEL_W)
wheels = wheel(DECK_W / 2 + WHEEL_W / 2 + 20) + wheel(-(DECK_W / 2 + WHEEL_W / 2 + 20))
trailer = frame + drawbar + jack

# Feed water tank, about 125 L, lying across the deck at the front
TANK_R, TANK_L = 250.0, 640.0
tank = Pos(-700, 0, deck_top + TANK_R + 20) * Rot(90, 0, 0) * Cylinder(TANK_R, TANK_L)

# Feed pump (12 V diaphragm class) beside the tank
pump = Pos(-300, 380, deck_top + 90) * Box(220, 140, 180)

# Firebox: 700 x 600 x 650 mm steel box with refractory lining, open inside so the coil shows in section
FB_L, FB_W, FB_H, FB_WALL = 700.0, 600.0, 650.0, 40.0
fb_x = 250.0
firebox = Pos(fb_x, 0, deck_top + FB_H / 2) * (
    Box(FB_L, FB_W, FB_H) - Pos(0, 0, FB_WALL / 2) * Box(FB_L - 2 * FB_WALL, FB_W - 2 * FB_WALL, FB_H - FB_WALL))
door = Pos(fb_x, -FB_W / 2 - 10, deck_top + 250) * Box(360, 20, 280)
firebox = firebox + door

# Monotube steam coil: massing as a hollow cylinder (about 15 m of 25.4 mm tube wound on 420 mm)
coil = Pos(fb_x, 0, deck_top + FB_WALL + 120 + 220) * (Cylinder(230, 440) - Cylinder(190, 450))

# Flue-gas economizer box on top of the firebox
ECO_H = 260.0
eco_z = deck_top + FB_H + ECO_H / 2
economizer = Pos(fb_x, 0, eco_z) * Box(520, 460, ECO_H)

# Chimney with spark arrestor cap, top at about 2.4 m above ground
CH_R = 75.0
ch_base = deck_top + FB_H + ECO_H
CH_TOP = 2400.0
chimney = Pos(fb_x, 0, (ch_base + CH_TOP - 120) / 2) * Cylinder(CH_R, CH_TOP - 120 - ch_base)
chimney = chimney + Pos(fb_x, 0, CH_TOP - 60) * Cylinder(CH_R + 45, 120)

# Steam header with open vent standpipe (1 m water seal) and certified relief valve
hdr_x = fb_x + FB_L / 2 + 90
header = Pos(hdr_x, 0, deck_top + FB_H - 80) * Rot(90, 0, 0) * Cylinder(40, 300)
standpipe = Pos(hdr_x, -110, deck_top + FB_H - 80 + 520) * Cylinder(25, 1000)
relief = Pos(hdr_x, 110, deck_top + FB_H - 80 + 110) * Cylinder(35, 140)
relief = relief + Pos(hdr_x, 110, deck_top + FB_H - 80 + 220) * Cylinder(20, 90)

# Steam hose from the header down to the hood (massing only)
hose = Pos(hdr_x + 300, 0, deck_top + FB_H - 80) * Rot(0, 90, 0) * Cylinder(22, 600)
hose = hose + Pos(hdr_x + 600, 0, (deck_top + FB_H - 80 + 260) / 2) * Cylinder(22, deck_top + FB_H - 80 - 260)

# Steam hood: 1.2 x 1.0 m open-bottom insulated pan resting on the soil behind the trailer
HOOD_L, HOOD_W, HOOD_H, HOOD_T = 1200.0, 1000.0, 250.0, 40.0
hood_x = hdr_x + 600 + HOOD_L / 2 - 100
hood = Pos(hood_x, 0, HOOD_H / 2) * (
    Box(HOOD_L, HOOD_W, HOOD_H) - Pos(0, 0, -HOOD_T / 2) * Box(HOOD_L - 2 * HOOD_T, HOOD_W - 2 * HOOD_T, HOOD_H))
handles = (Pos(hood_x, HOOD_W / 2 + 60, HOOD_H - 40) * Box(900, 40, 40)
           + Pos(hood_x, -HOOD_W / 2 - 60, HOOD_H - 40) * Box(900, 40, 40))
hood = hood + handles

parts = [
    Part("Trailer frame and drawbar", trailer, "#4B5563", 1, (0, 0, -380)),
    Part("Wheels", wheels, "#1F2937", 2, (0, 0, -760)),
    Part("Feed water tank, 125 L", tank, "#2563EB", 3, (-350, 0, 250)),
    Part("Feed pump", pump, "#7C3AED", 4, (-200, 500, 150)),
    Part("Firebox, refractory lined", firebox, "#9A3412", 5, (0, -700, 0)),
    Part("Monotube steam coil", coil, "#B87333", 6, (0, 0, 0)),
    Part("Flue-gas economizer", economizer, "#D4A017", 7, (0, 0, 650)),
    Part("Chimney and spark arrestor", chimney, "#6B7280", 8, (0, 0, 1250)),
    Part("Steam header and vent standpipe", header + standpipe, "#0F766E", 9, (350, -350, 250)),
    Part("Certified relief valve", relief, "#DC2626", 10, (350, 450, 500)),
    Part("Steam hose", hose, "#111827", 11, (500, 0, 150)),
    Part("Steam hood, 1.2 x 1.0 m", hood, "#D1D5DB", 12, (900, 0, 0)),
]

render_all(
    parts, project="SteamRoot", title="Biomass steam trailer concept", dwg_no="STR-DWG-001",
    key_figures=["Open-vented, below 0.1 bar gauge in normal use", "About 30 kg/h steam, about 35 kW wood fire (estimate)",
                 "About 14 kg steam per m2 to 70 C at 15 cm (estimate)", "About 2 m2/h at 15 cm, 6 m2/h at 5 cm (estimate)",
                 "About 8 kg/h wood, 62 % fuel to steam (estimate)"],
    cut_exclude=("Wheels", "Steam hose"),
    flow={"title": "energy flow at 30 kg/h steam (all values estimates; economizer returns about 2.4 kW to feed water)", "unit": "kW (est.)",
          "stages": [("Wood fuel in", 35.1), ("Steam generator", 21.8), ("Steam hood", 21.8),
                     ("Soil, 0 to 15 cm", 11.8)],
          "losses": [(1, "Flue and shell", 13.3), (2, "Hood losses", 10.0)]},
)

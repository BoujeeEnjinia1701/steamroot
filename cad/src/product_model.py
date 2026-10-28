"""SteamRoot product model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is: trailer, skids, firebox with its
lining, grate, door, hinges, latch and both air dampers, the monotube coil on its brackets, the evaporator
bank box with the bank and its gas-pass baffle, the economizer with its baffles, the chimney and spark
arrestor at the +Y side, the steam header, water-seal pot, overflow and relief valve, the feed drum and pump
box, the hose and both hoods with their ballast-rated handles, every bolt, washer, nut, stud and weld bead.
Only the site is added, as context parts: a cultivated market-garden bed under the two hoods, a gravel pad
under the trailer, the beds on either side, and a 1.75 m mannequin standing on the gravel at the firebox
door for scale. Ground level is model z = 0 (the tyres stand on it, the hood skirts press 60 mm into the
bed); every site part reaches below it.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the machine in its working position), "exploded" (made and bought parts only, each moved
by its group's explode offset), "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "SteamRoot: towable wood-fired soil steamer that never holds pressure"

# camera and sun from the front right (operator side, -Y) and above; sun within 60 degrees of the camera
_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=38,-70", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 18, "az": -38, "args": _SITE,
     "note": "Site render on a market-garden bed from the front right and a little above (about 18 deg elevation): "
             "the steam generator on its trailer on a gravel pad, operator at the firebox door, steam hose to the "
             "first of two insulated hoods pressed into the cultivated bed; 1.75 m person for scale"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 24, "az": -40,
     "note": "Studio render from the front right and above (about 24 deg elevation): trailer, lined firebox with "
             "door and air dampers, evaporator bank box and economizer under the chimney, header with the "
             "water-seal pot and relief valve, feed drum, hose and both hoods"},
    {"name": "exploded", "groups": ["exploded"], "explode": True, "el": 26, "az": -55,
     "note": "Exploded view from the front right and above (about 26 deg elevation): trailer and wheels down, "
             "firebox pulled toward the operator, bank box, economizer and chimney lifted above the coil, header "
             "group and relief valve out to the side, hose and hoods to the right; fasteners and welds left out"},
]


def site():
    """Market-garden site: a cultivated bed under the hoods, neighbouring beds, a gravel pad under the trailer and
    a mannequin. Ground level is z = 0; every site part reaches below it."""
    P, D = M.PARAMS, M.derived()
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    hx0 = D["hood_x0"]
    bx0, bx1 = hx0 - 200, hx0 + 2 * P["hood_l"] + P["hood_gap"] + 400
    ctx("Cultivated bed under the hoods", break_edges(Pos((bx0 + bx1) / 2, 0, -140) * Box(bx1 - bx0, P["hood_w"] + 300, 300), 40), "soil")
    for sy in (-1, 1):
        ctx(f"Neighbouring bed {'left' if sy > 0 else 'right'}",
            break_edges(Pos((bx0 + bx1) / 2, sy * (P["hood_w"] + 300 + 450) / 2 + sy * 380, -160) * Box(bx1 - bx0, 900, 300), 60), "soil")
    gx0, gx1 = -P["deck_l"] / 2 - P["drawbar_l"] - 400, bx0 - 50
    ctx("Gravel pad under the trailer", Pos((gx0 + gx1) / 2, -250, -95) * Box(gx1 - gx0, P["deck_w"] + 1600, 200), "concrete")
    try:
        import context_parts
        man = Pos(-20, -980, 5) * Rot(0, 0, 157) * context_parts.mannequin(1750.0, "stand", head_tilt=-8.0)
        out.append(part("Operator 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:      # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    parts = [p for p in M.components(M.CHOSEN) if p["kind"] != "context"]
    out = []
    for p in parts:
        q = dict(p)
        q["group"] = "shell"
        out.append(q)
        if p["kind"] in ("made", "bought"):
            e = dict(p)
            e["group"] = "exploded"
            out.append(e)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "context" for p in ps), "context")

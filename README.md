# SteamRoot

![TRL 2](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 3 of 9 (analytical proof of concept on paper) · **Prototype budget:** $1,800 USD · **Difficulty:** 5 of 5

Low-pressure, biomass-fired steam generator with a flue-gas economizer and a steam-hood trailer for soil pasteurization, operated near atmospheric pressure to stay out of pressure vessel code.

![SteamRoot concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement STR-DWG-002 (PDF)](cad/drawings/STR-DWG-002.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Herbicide-free weed and pathogen control by steaming soil works, but the portable boilers that do it are inefficient and diesel-fired.

## Concept

Low-pressure, biomass-fired steam generator with a flue-gas economizer and a steam-hood trailer for soil pasteurization, operated near atmospheric pressure to stay out of pressure vessel code.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

TRL 3 status (paper only): the sizing note [STR-CAL-001](docs/04-calcs/01-sizing.md) finds 30 kg/h of steam at a header pressure of about 0.03 bar with 7 L of water in the heated section, but about 54 % fuel-to-steam efficiency against a 65 % target, about 1.9 m²/h at 15 cm against 2 m²/h, 536 kg loaded against 500 kg, and $1,915 in parts against $1,800. A written ruling from the local boiler authority is an open prerequisite before any detail design or build. TRL 4 work is on hold.

## Key components

- Once-through monotube coil, 25.4 mm 316 stainless
- Fiber-lined firebox
- Economizer coil
- Fixed-rate feed pump with coil outlet and tank level alarms
- Water-seal vent and certified relief valve
- Two steam hoods used alternately
- Thermocouples

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This design involves open fire, carbon monoxide and steam. Keep operating pressure and water volume below local boiler and pressure vessel code thresholds, get a written ruling from the local boiler authority before any build, fit a certified relief valve, and never operate it unattended.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (STR-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `STR-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).

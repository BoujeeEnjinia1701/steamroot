# SteamRoot

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $1,500 USD · **Difficulty:** 5 of 5

Low-pressure, biomass-fired steam generator with a flue-gas economizer and a steam-hood trailer for soil pasteurization, operated near atmospheric pressure to stay out of pressure vessel code.

![SteamRoot concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Herbicide-free weed and pathogen control by steaming soil works, but the portable boilers that do it are inefficient and diesel-fired.

## Concept

Low-pressure, biomass-fired steam generator with a flue-gas economizer and a steam-hood trailer for soil pasteurization, operated near atmospheric pressure to stay out of pressure vessel code.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Coil-type once-through generator (copper or stainless)
- Firebox
- Economizer coil
- Feed pump
- Certified relief valve
- Steam hood
- Thermocouples

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This design involves heat and pressurized steam. Keep operating pressure and water volume below local boiler and pressure vessel code thresholds, fit a certified relief valve, and never operate it unattended.

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

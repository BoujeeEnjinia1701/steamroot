---
doc_id: STR-REQ-001
title: SteamRoot requirements
project: SteamRoot
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, including pressure and safety requirements
---

# SteamRoot requirements

These are first-pass requirements for the concept. Targets are proposals for review and will be checked by calculation at TRL 3. Safety requirements (R6, R7, R9 and R10) take priority over performance requirements if they conflict.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Pasteurize soil to working depth | Soil at 70 °C (158 °F) or more for 20 to 30 min at 10 to 15 cm depth across at least 80 % of the hood footprint | Heat balance calculation; later thermocouple probes at 15 cm |
| R2 | Treat beds at a useful rate | 2 m²/h or more at 15 cm depth; 5 m²/h or more at 5 cm depth (weed seed bank only) | Calculation from steam output and steam per m² |
| R3 | Generate enough steam | 30 kg/h or more of saturated steam, continuous, from one firebox | Heat transfer and combustion calculation |
| R4 | Limit fuel use | 4 kg or less of dry wood (about 16 MJ/kg, 20 % moisture) per m² at 15 cm depth | Energy balance calculation |
| R5 | Use biomass efficiently | 65 % or more of fuel energy delivered as steam, with the economizer | Energy balance calculation; later flue temperature and fuel weighing |
| R6 | Stay near atmospheric pressure | Normal working pressure 0.1 bar gauge (1.5 psi) or less at every point on the steam side; an open vent to atmosphere that cannot be closed or isolated | Pressure drop calculation; design review |
| R7 | Keep stored energy low | 8 L or less of water in the heated section; no closed steam drum | Volume calculation from the coil geometry |
| R8 | Run between refills | 3 h or more of steaming per feed water fill | Tank volume and steam rate |
| R9 | Protect against overpressure | A certified steam relief valve, sized for full steam output and set at the lowest available certified pressure, 1 bar (15 psi) or less, as a second line of protection behind R6 | Valve rating and capacity check |
| R10 | Protect the operator and site | Chimney outlet 2.2 m or more above ground with a spark arrestor (mesh 6 mm or finer); fire outdoors only; steam diverted to the vent, not the hood, before the hood is lifted; hood handles 60 °C or cooler | Design review; later surface temperature check |
| R11 | Tow with farm vehicles | Loaded mass 500 kg or less with a full tank; overall width 1.5 m or less | Mass estimate from the massing model and BOM |
| R12 | Build within the concept budget | Parts cost $1,500 or less | Priced BOM |

## Assumptions

- Soil to 15 cm depth: bulk density 1,300 kg/m³, gravimetric water content 20 % (dry basis), starting temperature 15 °C, heated to 75 °C so that the coldest point reaches 70 °C.
- Specific heat of dry mineral soil 0.84 kJ/(kg K), of water 4.18 kJ/(kg K).
- 70 °C for 30 minutes is widely used as a soil pasteurization target for most weed seeds and fungal pathogens. Some hard-seeded weeds and heat-tolerant viruses need higher temperatures; this is accepted.
- Pressure thresholds for boiler and pressure vessel rules vary by jurisdiction. R6 and R9 are set to be well below common low-pressure thresholds, but compliance must be confirmed locally.

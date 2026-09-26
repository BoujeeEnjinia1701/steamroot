---
doc_id: STR-REQ-001
title: SteamRoot requirements
project: SteamRoot
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-09-25'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply Amish's 2026-09-25 decisions (two hoods in R2, $1,800 budget in R12); correct the wood heating value in R4; add TRL 3 status from STR-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# SteamRoot requirements

These requirements were checked by calculation at TRL 3 in STR-CAL-001 v0.2 (`docs/04-calcs/01-sizing.md`). On 2026-09-25 Amish accepted the recommendations from the TRL 3 review (STR-DDR-002): R2 is restated to the calculated two-hood rate, R6 is split into a header limit and a coil inlet limit, R9 is worded for a standard 15 psi valve sized for the dry-coil refeed flash, R11 applies as towed with the tank drained, R12 is $2,200, and R4 and R5 keep their targets. Of the fifteen checks, two are not met (R4, R5), three are at risk, one is not verifiable at TRL 3 and nine are met on paper. Safety requirements (R6, R7, R9 and R10) take priority over performance requirements if they conflict.

> **Safety:** SteamRoot is a fired steam generator. Meeting these requirements on paper does not make it safe or legal to build. A written ruling from the local boiler authority is an open prerequisite for any detail design or build.

*Table 1. Requirements and TRL 3 status.*

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (STR-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Pasteurize soil to working depth | Soil at 70 °C (158 °F) or more for 20 to 30 min at 10 to 15 cm depth across at least 80 % of the hood footprint | Heat balance calculation; later thermocouple probes at 15 cm | Not verifiable at TRL 3 (1D model holds 70 °C at 15 cm if the front reaches 16.5 cm) |
| R2 | Treat beds at a useful rate | About 1.9 m²/h (1.85 m²/h or more) at 15 cm depth; 3.4 m²/h or more at 5 cm depth (weed seed bank only), with two hoods used alternately. Restated from 2 and 5 m²/h until soil tests exist (decided by Amish, 2026-09-25, STR-DDR-002) | Calculation from steam output, steam per m² and hood cycle | At risk (thin margin): 1.88 m²/h at 15 cm, 3.41 m²/h at 5 cm |
| R3 | Generate enough steam | 30 kg/h or more of saturated steam, continuous, from one firebox | Heat transfer and combustion calculation | Met: 30 kg/h at 40.7 kW firing |
| R4 | Limit fuel use | 4 kg or less of wood at 20 % moisture (wet basis; about 14.5 MJ/kg lower heating value) per m² at 15 cm depth. Target kept (decided by Amish, 2026-09-25) | Energy balance calculation | Not met: 5.4 kg/m² (4.4 kg/m² even at 65 % efficiency; about 72 % needed) |
| R5 | Use biomass efficiently | 65 % or more of fuel energy delivered as steam, with the economizer. Target kept; a convective evaporator bank with controlled air is under study (decided by Amish, 2026-09-25) | Energy balance calculation; later flue temperature and fuel weighing | Not met: 54 % (study in STR-CAL-001, section 4: 65 % needs about 3.3 m of evaporator bank at λ = 2.0, or λ near 1.5) |
| R6 | Stay near atmospheric pressure | Normal working pressure 0.1 bar gauge (1.5 psi) or less at the steam header, where the vent limit applies, and 0.15 bar gauge (2.2 psi) or less at the coil inlet; an open vent to atmosphere that cannot be closed or isolated (redefined by Amish, 2026-09-25) | Pressure drop calculation; design review | Met: header 0.033 bar, coil inlet 0.110 bar; open vent met by design |
| R7 | Keep stored energy low | 8 L or less of water in the heated section; no closed steam drum | Volume calculation from the coil geometry | Met: 7.0 L flooded |
| R8 | Run between refills | 3 h or more of steaming per feed water fill | Tank volume and steam rate | Met: 4.2 h |
| R9 | Protect against overpressure | A certified steam relief valve set at the lowest standard certified pressure, 15 psi (1.03 bar) or less, with rated capacity for both the full steam output and the dry-coil refeed flash (about 155 kg/h, 14 mm orifice), as a second line of protection behind R6 (reworded by Amish, 2026-09-25) | Valve rating and capacity check | Met on paper: 15 psi set, maker's rating 170 kg/h (375 lb/h) for the 3/4 in valve, 10 % over the flash |
| R10 | Protect the operator and site | Chimney outlet 2.2 m or more above ground with a spark arrestor (mesh 6 mm or finer); fire outdoors only; steam diverted to the vent, not the hood, before the hood is lifted; hood handles 60 °C or cooler | Design review; later surface temperature check | Met: 2.4 m, 6 mm mesh, hood skin 23 °C |
| R11 | Tow with farm vehicles | 500 kg or less as towed, with the feed tank and seal pot drained (filled on site); overall width 1.5 m or less (restated by Amish, 2026-09-25) | Mass estimate from the model and BOM | Mass met: 402 kg as towed (536 kg full). Width at risk: 1.48 m |
| R12 | Build within the prototype budget | Parts cost $2,200 or less, which leaves about 15 % contingency over the priced BOM (raised from $1,800 by Amish on 2026-09-25, STR-DDR-002; first raised from $1,500) | Priced BOM | Met: $1,915 ($285 contingency) |

## Assumptions

- Soil to 15 cm depth: bulk density 1,300 kg/m³, gravimetric water content 20 % (dry basis), starting temperature 15 °C. At TRL 3 the soil is modeled with a condensation front: soil above the front reaches 100 °C, and the front must reach 16.5 cm so that 15 cm stays at 70 °C or more through a 25-minute hold (STR-CAL-001, section 2). The TRL 2 model heated a uniform layer to 75 °C.
- Specific heat of dry mineral soil 0.84 kJ/(kg K), of water 4.18 kJ/(kg K).
- 70 °C for 30 minutes is widely used as a soil pasteurization target for most weed seeds and fungal pathogens. Some hard-seeded weeds and heat-tolerant viruses need higher temperatures; this is accepted.
- Wood at 20 % moisture (wet basis) has a lower heating value of about 14.5 MJ/kg for a typical hardwood analysis. Earlier versions quoted about 16 MJ/kg, which was too high.
- Pressure thresholds for boiler and pressure vessel rules vary by jurisdiction. R6 and R9 are set to be well below common low-pressure thresholds, but compliance must be confirmed locally. The written ruling from the local boiler authority is an open prerequisite.
- R11 assumes the machine is towed with the feed tank and seal pot drained and filled from a water supply at the site. Towing full puts it at about 536 kg.
- The R9 capacity check uses the maker's published capacity for the Watts Series 315, 3/4 in, 15 psi valve (375 lb/h); it must be confirmed for the valve actually bought.
- The R2 treatment rate assumes two hoods used alternately, a 25-minute hold, 2 minutes to reset a hood and 1 minute of vented steam each time the hose is moved.

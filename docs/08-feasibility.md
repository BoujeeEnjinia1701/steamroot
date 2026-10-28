---
doc_id: STR-FEA-001
title: SteamRoot feasibility assessment
project: SteamRoot
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade), from STR-STM-001, STR-CAL-001 v0.5, STR-BLD-001 and the D3 model"
---

# SteamRoot feasibility assessment

Overall verdict: SteamRoot is feasible on paper as a design and as a workshop build, and its working principle holds (STR-STM-001: no claim fails outright; four failed details were fixed), but two things outside the drawing decide whether it can go further: the Texas boiler authority's written ruling (STR-REG-001, R1) and how real bed soils pass steam under a light hood (STEM S11, which fails with fixes proposed to Amish), which only TRL 4 soil tests can settle. Fuel efficiency is feasible only with the gas-pass baffles, the 3.2 m chimney and the dampers set, and then only just (66.1 % at λ = 1.5 against the 65 % target, inside its uncertainty). Method: STANDARDS section 23.

> **Safety:** Feasibility on paper is not permission to build. No part may be bought, built or fired before the written ruling exists (STR-DEC-001, decided 2026-10-02).

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design: steam generation | 30 kg/h at near-atmospheric pressure from 7.3 L of heated water; water seal at 0.084 bar, certified relief valve, no isolating valve | High | Dry-coil refeed flash (141 kg/h on a 30 s basis) is inside the relief valve's 170 kg/h, but the basis is not bounded (STEM S15 to S17, DEC #20); a latching pump trip now stops an unattended restart (STEM E2, DEC S4) | STR-STM-001 S13 to S18; STR-CAL-001 sections 5 and 6 |
| Design: fuel efficiency | 66.1 % at λ = 1.5 with the gas-pass baffles; 62.5 to 66.9 % in the one-at-a-time sensitivities; 59.8 % without baffles | Medium | Rests on the single-zone firebox model (F, h), the unburned loss and the operator holding λ near 1.5; the reviewer estimates about 61 %; PR-004 (wood per m2) not met at 4.36 kg/m2; the draft needs the 3.2 m outlet (DEC S3) | STR-STM-001 S5 to S7, S12; STR-CAL-001 section 4, Table 6a; STR-DEC-001 S1, S3, #12 |
| Design: soil treatment | Front to 16.5 cm holds 70 °C at 15 cm for 25 min (1D); 1.88 m2/h at 15 cm with two hoods | Low | In soils finer than sand the steam cannot pass 16.5 cm at full flow under a 256 Pa hood (STEM S11): leakage at the skirt, slower fronts or both; bed preparation proposed (DEC #18), ballast and skirt depth from TRL 4 tests (decided 2026-10-02) | STR-STM-001 S9 to S11; STR-CAL-001 sections 2 and 3 |
| Design: handling and operation | One trained operator with a helper; hoods moved between settings | Medium | A 31.3 kg hood 1.2 m wide is beyond one person and borderline for two (STEM B4 fails; a wheel kit is recommended, DEC S2); the battery runs to about 100 % depth of discharge at an assumed 4 A pump (STEM E3, DEC #16) | STR-STM-001 B4, E3 |
| Materials | 316 stainless coil, bank and economizer tubes; 304 stainless bank baffle and 316L economizer baffles; 3 mm and 2 mm mild steel boxes; ceramic fibre linings; aluminium double-skin hoods | High | Fibre lining is fragile under loading (accepted 2026-09-25); acidic condensate at the economizer cold end (stainless tube, 316L baffles) | STR-STM-001 C3, C5; BOM |
| Manufacturing and assembly | Stock sections, sheet, tube and catalogue fittings; welding, hand tube bending, coil winding on a former; 585-part D3 model with every bolt, nut and weld bead, no interferences | High | Coil winding and the two serpentines need a jig and care; 128 making sketches and a stepped build plan exist | STR-BLD-001; `cad/fidelity.json`; STR-DWG-101 to 128 |
| Power and controls | 12 V battery, diaphragm pump at a fixed rate, coil outlet and tank level alarms with a latching pump trip, manual dampers | Medium | Battery capacity to confirm with the pump chosen (E3); fixed-rate feed means a pump fault must be caught by alarm | STR-STM-001 E2, E3; wiring picture in STR-BLD-001 |
| Supply of parts | Used trailer, stainless tube, fittings, hose, relief valve and lining from ordinary suppliers; one price checked live (relief valve, USD 68.19 on 2026-10-25) | Medium | Indicative prices elsewhere; steam-rated hose and the no-closed-position diverter must be sourced as rated parts | BOM; STR-MKT-001 |
| Regulatory | Designed to the Texas exemption for boilers designed for atmospheric pressure with two independent means against pressure build-up | Low | The ruling is not obtained; if refused, the design would have to become a code boiler, which changes the pitch | STR-REG-001 R1 to R3 |

Ratings: High, Medium, Low.

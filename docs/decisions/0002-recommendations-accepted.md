---
doc_id: STR-DDR-002
title: SteamRoot recommendations accepted
project: SteamRoot
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 3 review recommendations accepted by Amish, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Items 10 to 12 decided by Amish on 2026-10-02 (STR-DEC-001, items 1 to 3); the ruling is still to be obtained"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Item 1 consequence updated: evaporator bank now in the model within R7 (STR-CAL-001 v0.4)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 9); items 10 to 12 remained open at this record and were decided by Amish on 2026-10-02 (STR-DEC-001, items 1 to 3): "i approve your recommendations for all 555 open decisions." The ruling of item 10 is still to be obtained.

## Context

The TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25) and STR-DDR-001 left several items "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every open item that carried a recommendation is therefore decided as recommended. Where the recommendation listed several options, the recommended option is the decision. Items with no recommendation stay open. TRL 4 remains on hold by Amish's earlier instruction, and the repo stays at `trl: 3`, `trl_target: 3`.

> **Safety:** None of these decisions replaces the written ruling from the local boiler authority, which is still an open prerequisite for any detail design or build.

## Decision

*Table 1. Items decided by Amish on 2026-09-25.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | R5 efficiency and R4 wood use | Decided by Amish, 2026-09-25: go with recommendation. Keep the targets (65 %, 4 kg/m²) and study a convective evaporator bank in the flue with controlled primary and secondary air at the next paper step. | STR-CAL-001 v0.2, section 4, adds the study: about 3.3 m of 25.4 mm tube (0.26 m²) reaches 65 % at λ = 2.0; almost none is needed at λ = 1.5. R4 needs about 72 %. Baseline design unchanged; R4 and R5 still not met. |
| 2 | R2 treatment rate | Decided by Amish, 2026-09-25: go with recommendation (a). Accept about 1.9 m²/h at 15 cm and restate the 5 cm target at about 3.4 m²/h, until soil tests exist. | STR-REQ-001 v0.4: R2 from 2 and 5 m²/h to 1.85 (about 1.9) and 3.4 m²/h. Status from not met to at risk (1.88 and 3.41 m²/h). |
| 3 | R6 pressure | Decided by Amish, 2026-09-25: go with recommendation. 0.1 bar gauge at the header, where the vent limit applies, and 0.15 bar gauge at the coil inlet. | STR-REQ-001 v0.4: R6 split. Status from not met (0.110 bar against 0.1) to met (header 0.033, inlet 0.110). Drawing note updated. |
| 4 | R9 relief valve | Decided by Amish, 2026-09-25: go with recommendation (both parts). Word the set pressure as "15 psi (1.03 bar) or less" and size the valve for the dry-coil refeed flash (about 155 kg/h, 14 mm orifice) as well as 30 kg/h. | STR-REQ-001 v0.4 reworded. Maker's capacity table checked: Watts Series 315, 3/4 in, 15 psi, 375 lb/h (170 kg/h), so the BOM valve is kept. Status from at risk to met on paper. BOM note, drawing note and CAL-001 updated. |
| 5 | R11 mass | Decided by Amish, 2026-09-25: go with recommendation (a). "500 kg or less as towed, with the tank drained"; fill on site. | STR-REQ-001 v0.4 restated. Status from not met (536 kg full) to met (402 kg as towed). Width stays at risk (1.48 m). |
| 6 | R12 budget | Decided by Amish, 2026-09-25: go with recommendation (a). Raise the budget to about $2,200 for about 15 % contingency. | `project.yaml` `budget_usd` from 1800 to 2200; R12 from $1,800 to $2,200. Status from not met to met ($1,915, $285 contingency). |
| 7 | Firebox lining | Decided by Amish, 2026-09-25: go with recommendation. Ceramic fiber lining, not castable (castable would add about 200 kg). | Recorded in STR-PRC-001 v0.4. Design already used fiber; no geometry change. |
| 8 | Hose between hoods | Decided by Amish, 2026-09-25: go with recommendation. One hose moved between hoods with a steam-rated coupling, after steam is diverted to the vent. | Recorded in STR-PRC-001 v0.4. BOM already had one hose; no change. |
| 9 | Fuel | Decided by Amish, 2026-09-25: go with recommendation (the design proposal). Wood only, no liquid fuel backup. | Recorded in STR-PRC-001 v0.4 and STR-DDR-001 v0.2. |

## Items still open

*Table 2. Items left open at this record; decided on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| 10 | Written ruling from the local boiler authority | Approved as a prerequisite; not obtained. Blocks detail design and any build. Confirmed by Amish on 2026-10-02 (STR-DEC-001, item 1): the design is reviewed against the ruling and anything stricter is adopted. |
| 11 | Which jurisdiction is "home" and which authority to ask | Decided by Amish, 2026-10-02 (STR-DEC-001, item 2): Texas; the ruling is asked of the Texas Department of Licensing and Regulation's boiler program. |
| 12 | The named market garden and nursery (first co-design partners) | Decided by Amish, 2026-10-02 (STR-DEC-001, item 3): one market garden and one nursery within driving distance of Irving that already steam, solarize or chemically treat soil, found through Texas A&M AgriLife Extension; none is named or agreed yet. |

## Consequences

- Requirement status (STR-CAL-001 v0.2, 15 checks): 2 not met (R4, R5), 3 at risk (R2 at 15 cm and at 5 cm, R11 width), 1 not verifiable at TRL 3 (R1), 9 met. Before these decisions: 7 not met, 2 at risk, 1 not verifiable, 4 met.
- Documents bumped: STR-PRB-001 v0.4, STR-PRC-001 v0.4, STR-REQ-001 v0.4, STR-CAL-001 v0.2, STR-DDR-001 v0.2. Drawing STR-DWG-002 moved to Rev P2 for note changes (relief valve rating, towed mass, R6 limits); geometry is unchanged.
- The evaporator bank was added to the model on 2026-10-02: 6.4 m of 15.88 mm tube with one coil turn fewer keeps the heated section at 7.3 L, inside R7, with R6 met and R11 mass at risk (STR-CAL-001 v0.4).
- TRL 4 work that these decisions point to (measuring efficiency, soil tests that would settle R2, confirming the valve capacity on a bought unit) is decided but on hold, because TRL 4 is on hold by Amish's instruction.
- Cross-repo actions: none.

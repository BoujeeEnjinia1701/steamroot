---
doc_id: STR-DDR-001
title: SteamRoot TRL 2 review decisions
project: SteamRoot
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the decisions Amish made on the TRL 2 review items, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 6); items 7 to 11 remain proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-24) listed six items as "Proposed, awaiting Amish", each with a recommendation. On 2026-09-25 Amish reviewed the review points for every repo in the portfolio and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This record lists what that instruction decides for SteamRoot and what it leaves open. TRL 4 work is on hold by the same instruction.

> **Safety:** Several of these decisions are safety architecture choices (open vent, relief valve, coil material). They are decisions about the concept only. They do not replace the written ruling from the local boiler authority, which is still an open prerequisite (item 7).

## Options considered

The options for each item are in the TRL 2 review note and in `docs/02-concept.md` (STR-PRC-001 v0.2). Table 1 repeats the recommendation that was chosen.

## Decision

*Table 1. Items decided by Amish on 2026-09-25.*

| # | Item | Decision |
| --- | --- | --- |
| 1 | Pressure architecture | Decided by Amish, 2026-09-25: go with recommendation. Open-vented steam side with a water-seal vent as the primary pressure limit, a certified relief valve as the second line, and no isolating valve anywhere on the steam side. |
| 2 | Coil type and material | Decided by Amish, 2026-09-25: go with recommendation. Single monotube coil in 25.4 mm OD 316 stainless tube (not parallel 12.7 mm circuits, not soft copper). |
| 3 | Treatment rate option | Decided by Amish, 2026-09-25: go with recommendation. Hood steaming with two hoods used alternately. |
| 4 | Feed control | Decided by Amish, 2026-09-25: go with recommendation. Fixed pump rate with a coil outlet temperature alarm (and the tank low-level alarm proposed with it at TRL 2). |
| 5 | Budget | Decided by Amish, 2026-09-25: go with recommendation (a). `budget_usd` raised from $1,500 to $1,800 to allow about 20 % contingency. |
| 6 | First users and first jurisdiction | Decided by Amish, 2026-09-25: go with recommendation. Involve one market garden and one nursery first; design the regulatory check to Amish's home jurisdiction first. |

The TRL 2 review also recommended a written ruling from the local boiler authority before any TRL 3 detail work. Amish approved that recommendation with the rest. The ruling cannot be obtained in a documentation session, so the TRL 3 work was limited to paper calculations, a massing-plus model and a preliminary drawing, and the ruling is carried as an open prerequisite (item 7).

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| 7 | Written ruling from the local boiler authority on an open-vented, fired monotube coil | Approved as a prerequisite; not yet obtained. Blocks detail design and any build. |
| 8 | Which jurisdiction is "home" and which authority to ask | Proposed, awaiting Amish (Amish to name it). |
| 9 | The named market garden and nursery (first co-design partners) | Proposed, awaiting Amish. No partner is named. |
| 10 | Wood only, no liquid fuel backup (design choice in STR-PRC-001 not listed in the review) | Proposed, awaiting Amish. |
| 11 | New items raised by the TRL 3 calculation (CAL-001): requirement gaps on R2, R4, R5, R6, R11 and R12, relief valve wording for R9, and the lining and hose-coupling choices | Proposed, awaiting Amish. See `docs/REVIEW.md`, session 2026-09-25. |

## Consequences

- `project.yaml`: `budget_usd` is 1800.
- `docs/03-requirements.md` (STR-REQ-001 v0.3): R2 is stated for two hoods; R12 is $1,800.
- `docs/02-concept.md` (STR-PRC-001 v0.3): the open vent, the stainless monotube coil, two hoods and the fixed-rate feed with alarms are recorded as decided.
- `docs/01-problem.md` (STR-PRB-001 v0.3): first users and first jurisdiction are recorded as decided; the named partners and the named jurisdiction stay open.
- `bom/bom.csv`: a second hood and the feed and coil alarms are added.
- The TRL 3 calculation (STR-CAL-001) shows that the decided configuration misses several requirements. Those results do not reverse any decision here; they are new items for Amish.

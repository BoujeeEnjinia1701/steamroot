---
doc_id: STR-DDR-004
title: SteamRoot concept selection and STEM check fixes
project: SteamRoot
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Concept selection between option A (monotube coil) and option B (vented fire-tube kettle), within 10 %, sent to Amish without a pick; gas-pass baffles decided under the standing instruction of 2026-10-23; hood handling sent to Amish (kit 1.9.1 upgrade); after the independent review: baffle figures revised, chimney outlet 3.2 m and latching pump trip decided under the standing instruction (Part 2a), hood handling recommendation changed to a wheel kit"
---

# 0004: Concept selection and STEM check fixes

- **Date:** 2026-10-25
- **Status:** proposed for the concept choice (Part 1) and the hood handling (Part 3), awaiting Amish. Part 2, the gas-pass baffles, and Part 2a, the chimney outlet and the latching pump trip, were decided under Amish's standing instruction of 2026-10-23 and are recorded in STR-DEC-001 as S1, S3 and S4; he can reverse them.

> **Safety:** Neither option may be built or fired before the written ruling from the Texas Department of Licensing and Regulation's boiler program, and the design is reviewed against that ruling.

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements, and a STEM check of every claim (STANDARDS sections 20 and 21). SteamRoot was designed before kit 1.8, so its current design is option A. The STEM check (STR-STM-001) found details that failed in A and could be fixed without changing the principle (S6 and S7; after the independent review also S12 and E2), and two that fail with fixes that change how the machine is used (S11 and B4).

## Part 1: concept selection

### Options considered

- **A, monotube coil generator (current design):** once-through forced flow through an economizer, evaporator bank and 25.4 mm stainless coil; 7.3 L of water heated; 66.1 % fuel to steam; USD 2,720; 509 kg as towed.
- **B, vented fire-tube kettle:** pool boiling of about 70 L in a welded steel kettle with seven fire tubes, float-switch level control; about 50 % fuel to steam; about USD 2,300; about 50 kg lighter dry; needs a second open vent and stiffened walls before it could meet the relief set pressure (STEM OB5).
- A third principle, roasting excavated soil in a fired drum, was set aside: it changes the user-facing scope and is not steaming (STR-OPT-001).

### Scoring and recommendation

Weighted against STR-URS-001: A 132, B 120 of 180 (STR-OPT-001, Table 2). The gap is 9.1 %, inside the 10 % band, so both go to Amish without a pick. A leads on fuel use (UR-004), stored energy (UR-005), operator protection (UR-007) and the regulatory case (UR-011); B leads on tolerating a feed interruption (UR-003), towed mass (UR-008), cost (UR-009), simpler operation (UR-010), workshop build (UR-012) and maintenance. Proposed, awaiting Amish (STR-DEC-001 #14): choose A or B. Until he decides, the drawing, BOM and build plan stay on option A, the design he has decided on since 2026-09-25, and `concept_chosen` in `project.yaml` is left unset.

The runner-up's best idea for A: detect a feed loss directly with a flow switch on the feed line (suggestion in `docs/REVIEW.md`).

## Part 2: gas-pass baffles (decided under the standing instruction of 2026-10-23)

### Context

STR-CAL-001 v0.4 assumed gas-side coefficients of 30 W/(m2 K) in the evaporator bank and 25 in the economizer. In the model the gas rises slowly (about 0.1 m/s) through the full width of both boxes, where a tube-bank correlation gives about 12. Efficiency would then be 59.8 %, not 68.9 %, and R5 (PR-005, 65 %) would not be met (STEM S6 and S7).

### Options considered

| Option | Effect | Cost and mass | Verdict |
| --- | --- | --- | --- |
| (a) Gas-pass baffles: one 1.5 mm 304 stainless plate between the two bank layers, two 1 mm 316L plates between the three economizer layers on flat-bar ledges (316L after the review, for the acid condensate); flue openings moved so the gas enters each box at the -Y side and crosses the tubes sideways; chimney to the +Y side | Gas crosses the tubes at 0.7 to 1.1 m/s; coefficients 22.4 and 21.5 W/(m2 K) with fouling and 10 % edge bypass (25.4 and 23.8 before the review); efficiency 66.1 % at λ = 1.5; heated water and steam-side pressures unchanged; 1.75 Pa of gas-side loss in the two boxes | About USD 50 (estimate, not checked live); 7.4 kg | Chosen: keeps the working principle, R6 and R7 |
| (b) Longer bank of the same tube | More area at the same low coefficient | Heated water above the 8 L of R7 | Rejected |
| (c) Smaller-bore bank tube | More area per litre | Bank inlet above the 0.15 bar of R6 | Rejected |
| (d) Thicker linings to cut shell loss | About 1 point of efficiency | About 15 kg against R11 | Rejected |

### Decision

Option (a), implemented on 2026-10-24: `cad/src/model.py` (PARAMS `flue_y_in`, `flue_y_out`, `bk_baffle_*`, `eco_baffle_*`), STR-CAL-001 v0.5 (correlation-based coefficients, gas-side losses in the draft check), BOM lines 5, 7, 8 and 22, STR-BLD-001 v0.4, STR-PRS-001 statuses. Recorded in STR-DEC-001 as S1, decided under Amish's standing instruction of 2026-10-23; he can reverse it.

### Consequences

PR-005 moves from met to at risk (66.1 % against 65 %, after the review's corrections), PR-004 from at risk to not met (4.36 against 4 kg/m2; the proposed restatement to 4.5 still covers it), PR-011 to not met at 509 kg (with Part 2a), PR-012 rises to USD 2,720 (with Part 2a). The draft question this raised is Part 2a.

## Part 2a: chimney outlet and latching pump trip (decided under the standing instruction of 2026-10-23)

The independent review of the STEM check (STR-STM-001, Independent review) found two further failed details.

- **Draft (STEM S12).** With the grate and fuel bed counted (about 3 Pa), the 2.4 m outlet gave 11.4 Pa of draft against 11.3 Pa of gas-side losses, leaving nothing for the dampers. Options: (a) raise the outlet to 3.2 m; (b) larger damper openings, which do not help without draft; (c) an induced-draft fan, which needs power and changes the 12 V budget; (d) fewer baffle passes, which undoes Part 2. Chosen: (a), a 1.2 m flue section (about USD 60 and 2.5 kg, estimates): 16.8 Pa of draft, 5.4 Pa for the dampers, 7,530 of 12,600 mm2 needed at λ = 1.5. Wide open the dampers reach about λ = 1.6. STR-DEC-001 S3.
- **Dry-coil restart (STEM E2).** The coil alarm only warned, and a pump that stalls on a weak battery and recovers would refeed a hot coil unattended; a dry coil reaches 150 °C in about 16 to 20 s. Options: (a) a latching relay that cuts the pump on a coil alarm until reset by hand; (b) a timed lockout, which still restarts by itself. Chosen: (a), about USD 10 (BOM line 16). STR-DEC-001 S4.

Neither changes the working principle, pitch or scope.

## Part 3: hood handling (to Amish)

### Context

Each hood weighs 31.3 kg and its handles are 1.12 m apart. The revised NIOSH lifting equation gives 23 kg as the most one person should lift even in ideal conditions, and one person cannot reach both handles (STEM B4). The independent review added that with the horizontal multiplier for a load held 40 to 60 cm out, the equation allows only about 10 to 14 kg, so even a two-person share of 15.6 kg is borderline. The design brief says one trained adult runs SteamRoot with a second person nearby (UR-010).

### Options considered

- (a) A two-person lift: the helper already required nearby lifts the other handle; ballast weights are lifted off first. No cost. Changes the operating model in UR-010 from "nearby" to "lifts each hood with the operator".
- (b) A hood wheel kit: two small wheels on a lever frame at one end of each hood so one person tips and rolls it. Keeps one-person operation; adds an estimated 4 kg and some cost per hood (not priced), and the hood mass counts in R11.
- (c) Lighter hoods: the double skin and wool are already thin; little to gain.

### Recommendation

(b), changed after the independent review: a two-person share is itself borderline, and a wheel kit or lifting aid keeps one-person operation. (a) only as an interim. Proposed, awaiting Amish (STR-DEC-001 S2). PR-016 records the requirement as not met for one person until he decides.

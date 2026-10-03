# Review note: SteamRoot

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that the follow-up actions from the open-decision sign-off be carried out ("APPROVED CHANGES, COMPLETE THESE"), with the render scenes prepared for new photoreal renders. This section records each follow-up of the list below ("Follow-up actions to carry approved decisions into the design").

### Approved follow-ups carried out

1. Decision 1 (obtain the ruling and review the design against it): not done: outreach by Amish; the ruling is not yet obtained.
2. Decision 2 (write to the Texas Department of Licensing and Regulation): not done: outreach by Amish.
3. Decision 4 (size the evaporator bank with dampers, reshape the firebox, propose a restated R4): done. `docs/04-calcs/sizing.py` now runs a forward model of firebox, bank and economizer and a six-option study (STR-CAL-001 v0.4, section 4, Table 4). Chosen: 6.4 m of 15.88 x 1.24 mm 316 tube in two layers, coil cut from 11 to 10 turns, firebox reshaped from 1000 to 960 mm, excess air held near 1.5 by the primary and secondary dampers. Efficiency 68.9 % (61.3 % with dampers open), wood 4.18 kg/m², heated water 7.32 L. R4 restatement proposed (register item 12).
4. Decision 4 (bank and dampers in the model; check R6, R7, R11): done. `cad/src/model.py`: bank box, lining, tube, supports, slot cover, economizer to bank link, rerouted jumper, secondary air slot and slide on the door, longer roof bolts. R6 met (bank inlet 0.128 bar), R7 met (7.3 L), R11 mass at risk (499 kg).
5. Decision 6 (overflow in the model; constructability checks): done. Overflow from a half coupling at the static mark, 350 mm loop seal, trap stay, crossing to the trailer centre line behind the deck and down to 80 mm above the ground; rear clip on the rear rail. Constructability checks: 124 of 124 pass (was 93; 31 added for the new parts and clearances). STEP and STL regenerated, with a new `steamroot-bank` part file.
6. Decision 6 (STR-DWG-116 and STR-DWG-002): done. STR-DWG-116 Rev P2; STR-DWG-002 Rev P4; new sketch STR-DWG-125 for the overflow.
7. Decision 6 (seal pot section 3.17, step 15, joint 7, S4): done in STR-BLD-001 v0.3; joint 7 redrawn as a front cut through the pot and overflow.
8. Decision 6 (overflow in the BOM, priced): done. BOM line 9 USD 150 to USD 220 (pipe, elbows, half coupling, plug, stay and clip; typical hardware store prices, not checked live).
9. Decision 6 (overflow check in STR-CAL-001): done, section 5. With the overflow the annulus cannot rise, so the seal blows at the 890 mm dip leg depth: 0.084 bar, under the 0.094 bar limit whatever the fill; the 110 mm rise is removed. A loop seal (3.29 kPa) was needed because the refeed flash raises the pot head space by about 2.35 kPa and would otherwise blow steam out at ground level.
10. Decision 8 (draining and ice check in the operator instructions): not done: the operator instructions are not yet written (TRL 4 work); the rule is in safety stops S4 and S10 of the build plan, now including the loop seal plug.
11. Decision 10 (product model; renders, card and social preview on Amish's Mac): product model done; renders not done here. `cad/src/product_model.py` now takes the firebox on skids, coil, bank box, economizer and chimney heights, header post, pot on its foot plate, overflow, diverter position, discharge and vent line, dampers, feed lines and handles from `model.py`. Render scenes exported to `/home/claude/renders/steamroot` (hero, exploded, detail; one .npz and .json each plus `steamroot__jobs.json`). `media/render-*.png`, `media/card.png` and `media/social-preview.png` are to be rendered on Amish's Mac.
12. Decision 11 (handles sized for ballast; ballast load in the hood section): done. Handles 30 x 30 x 2.5 steel tube on standoffs and 100 x 100 x 3 foot plates through-bolted to backing plates; 40 kg a hood at a load factor of 2 gives about 34 MPa (factor 7 on yield). Noted in STR-BLD-001 sections 3.20 and 3.29; new sketch STR-DWG-126.
13. Decision 11 (skirt leakage in the TRL 4 soil test plan): not done: TRL 4 work, on hold.

### Requirement status changes (STR-CAL-001 v0.4)

- R4: not met (5.6 kg/m²) to at risk (4.2 kg/m² with the dampers set).
- R5: not met (51 %) to met on paper (69 %), only while the dampers hold λ near 1.5.
- R11 mass: met (468 kg) to at risk (499 kg towed with the hoods; 437 kg without).
- Unchanged in kind: R6 met (header 0.033 bar, bank inlet 0.128 bar, seal 0.084 bar), R7 met (6.9 L to 7.3 L), R9 met (flash 155 to 138 kg/h, margin 10 % to 23 %), R2 and R11 width at risk, R1 not verifiable.
- Cost: Value-engineering target: USD 2,200. Estimated cost of the constructable design: USD 2,600 (USD 400 over the target). Mass 633 kg full, 499 kg towed drained.

### Documents changed and new versions

- `cad/src/model.py` (bank, dampers, overflow, handles, 124 checks); `cad/step/`, `cad/stl/` regenerated
- `docs/04-calcs/sizing.py`; `docs/04-calcs/01-sizing.md` STR-CAL-001 v0.4
- `bom/bom.csv` (lines 1, 5, 6, 9, 12, 19, 21 revised; line 22 added); `bom/bom-notes.md`
- `docs/03-requirements.md` STR-REQ-001 v0.7; `docs/02-concept.md` STR-PRC-001 v0.7; `docs/05-build-plan.md` STR-BLD-001 v0.3; `docs/06-design-decisions.md` STR-DEC-001 v0.3; `docs/decisions/0002-recommendations-accepted.md` STR-DDR-002 v0.3; `docs/decisions/0003-design-for-construction.md` STR-DDR-003 v0.3; `README.md`
- Drawings: STR-DWG-002 Rev P4; STR-DWG-101, 104, 106, 107, 108, 110, 111, 116, 119 Rev P2; new STR-DWG-122 to 126; insets of 109, 112, 113, 120 and 121 regenerated
- Pictures: overview, joints 1 to 10 (5, 7 and 9 changed), steps 1 to 20 (6, 10, 11, 15, 18 and 19 changed); concept media (hero, cutaway, exploded, flow, blueprint, `model.glb`). `cad/src/concept_media.py` now cuts the cutaway solid by solid (the coil compound needed about 5 GB in one boolean).
- `cad/src/product_model.py`, `cad/src/sheets.py`, `cad/src/build_plan_media.py`

### Proposed, awaiting Amish

- Register item 12: restate R4 as 4.5 kg/m² or less at 15 cm with the dampers set (options 4.5, 5.0 or keep 4).
- Register item 13: count R11 without the hoods, which ride on a second vehicle (437 kg), or save mass elsewhere.
- The overflow's 350 mm loop seal is a detail the 2026-10-02 decision did not name; it keeps the decided overflow from venting steam at ground level during a refeed flash. It changes the safety case slightly and should be confirmed by Amish and put to the authority with the rest.
- Appearance deviations in `product_model.py`: the cast grate is drawn as a bar grid sized to the lining rather than the 300 mm grate, and the door carries a ceramic glass window the made door does not have.

### Safety notes

- R5 now depends on the operator holding the dampers near λ = 1.5; less excess air also raises carbon monoxide, so the CO alarm rule stands.
- Each start pushes about 0.3 L of seal water out of the overflow; the pot must be topped up to the mark before every start (S4) or the seal is shallower than drawn (safe direction, but the vent then opens earlier).
- The overflow loop seal must be kept full and drained in frost (S4, S10).

### Cross-repo actions

None.

## Session 2026-10-02: open decisions decided by Amish

Amish wrote on 2026-10-02: "i approve your recommendations for all 555 open decisions." Every open decision in this repo's register was decided as recommended and moved to "Decisions made" in `docs/06-design-decisions.md`, dated 2026-10-02.

### Decisions recorded

11 decisions recorded (register items 1 to 11). The register's "Open decisions" section now reads: "None. All open decisions were decided on 2026-10-02."

### Documents changed

- `docs/06-design-decisions.md` v0.2
- `docs/decisions/0003-design-for-construction.md` v0.2
- `docs/decisions/0001-trl2-review-decisions.md` v0.3
- `docs/decisions/0002-recommendations-accepted.md` v0.2
- `docs/03-requirements.md` v0.6
- `docs/02-concept.md` v0.6
- `docs/01-problem.md` v0.5
- `docs/05-build-plan.md` v0.2
- `README.md` (DDR-003 status; not a controlled document)

PDFs re-rendered with `python3 .kit/render.py`. The CAD model, BOM quantities and prices, and pictures were not changed.

### Follow-up actions to carry approved decisions into the design

1. Decision 1 (documents): Obtain the written ruling (see decision 2) and review the design against it before any purchase or build; record any stricter requirement it sets as a new decision.
2. Decision 2 (documents): Write to the Texas Department of Licensing and Regulation's boiler program for the ruling on an open-vented, fired monotube coil, with the design precis and drawing attached.
3. Decision 4 (calculations): In the next paper iteration, size the evaporator bank with primary and secondary air dampers in `docs/04-calcs/sizing.py` so the heated water stays at 8 L or less (smaller-bore bank tube or fewer firebox turns), reshape the firebox in the same study, and propose a restated R4.
4. Decision 4 (model): Add the evaporator bank and air dampers to `cad/src/model.py` once sized, and check R6, R7 and R11.
5. Decision 6 (model): Add the seal pot overflow branch at the static water mark and its pipe down to ground level at the back of the trailer, away from the operator's side, to `cad/src/model.py`, and rerun the constructability checks.
6. Decision 6 (drawings): Regenerate the water-seal pot making sketch (STR-DWG-116) and STR-DWG-002 with the overflow branch and pipe.
7. Decision 6 (build plan pictures and renders): Add the overflow to the seal pot section 3.17, step 15 and joint 7 pictures of STR-BLD-001, and to the S4 check.
8. Decision 6 (BOM): Add the overflow branch, pipe and clips to the header and water-seal BOM line and price them.
9. Decision 6 (calculations): Check in STR-CAL-001 that the overflow sets the seal depth so the pot cannot exceed the 0.094 bar limit, including the 110 mm rise outside the dip leg.
10. Decision 8 (documents): Add the seal pot draining and ice check to the operator instructions when they are written.
11. Decision 10 (build plan pictures and renders): Update `cad/src/product_model.py` to the constructable design (1000 mm firebox with the coil above the fire, skids, header at 1.55 m on a post, seal pot on the deck) and regenerate `media/render-*.png`, `media/card.png` and `media/social-preview.png` on Amish's Mac.
12. Decision 11 (model): Size the hood handles and their standoffs in `cad/src/model.py` to carry ballast weights, and note the ballast load in the hood section of STR-BLD-001.
13. Decision 11 (documents): When TRL 4 is opened, include skirt leakage measured at the hood edge in the soil test plan.

### Points found in the review

- R4 (4 kg wood per m²) needs about 72 % efficiency (STR-CAL-001 section 4), so the evaporator bank study aimed at R5's 65 % cannot close R4; the register treats them as closing together.
- The evaporator bank length moved from about 3.3 m (STR-DDR-002, item 1) to about 4.3 m (STR-CAL-001 v0.3) after the taller firebox; STR-DDR-002 still quotes the old figure.
- The seal pot overflow (item 6) and the freezing rule (item 8) both protect the water seal, which is the pressure limit for the whole machine; they should be read together as one safety question rather than as an option and an operating rule.
- Item 10 is listed last although every other build item depends on it; it should sit first in the register as in the other repos.

TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (STR-PRB-001 v0.2): problem, users and context, constraints, out of scope, prior work on steam soil disinfestation (described without links), safety note.
- `docs/03-requirements.md` (STR-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, planned verification and stated assumptions.
- `docs/02-concept.md` (STR-PRC-001 v0.2): how it works, 15 main components numbered to match the exploded view and BOM, first-order energy and pressure numbers with assumptions, design choices, a full safety section, open questions.
- `cad/src/concept_media.py`: massing model (trailer, wheels, feed tank, feed pump, firebox, coil, economizer, chimney, header and vent standpipe, relief valve, hose, hood) with the 1.75 m person for scale.
- `media/`: hero, blueprint sheet STR-DWG-001 (PNG and PDF), cutaway, exploded view with BOM callouts, energy flow diagram (values marked as estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 15 lines with indicative prices, items 1 to 12 numbered to match the exploded view; `bom/bom-notes.md`.
- `README.md`: hero image and links line.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Heat to pasteurize soil to 15 cm | about 19.6 MJ/m² | |
| Steam needed at 15 cm | about 14 kg/m² (60 % hood transfer efficiency) | |
| Steam output | 30 kg/h (design point) | R3 met by design |
| Fuel to steam efficiency | about 62 % with economizer, 55 % without | R5 (65 %) **not met** |
| Wood use | about 7.9 kg/h, about 3.6 kg/m² at 15 cm | R4 met, thin margin |
| Treatment rate | about 2.2 m²/h at 15 cm, 6.5 m²/h at 5 cm (steam limited) | R2 met only with two hoods; about 1.2 m²/h with one |
| Steam-side pressure | about 0.05 bar coil drop, vent limit about 0.1 bar gauge | R6 met by design |
| Water in heated section | under 6 L | R7 met |
| Loaded mass | about 490 kg | R11 met, thin margin |
| Parts cost | about $1,500 | R12 met, no contingency |

Requirements not met or at risk:

- **R5 not met.** The economizer can only put about 2.4 kW into 30 kg/h of feed water before it nears boiling, so it lifts efficiency from about 55 % to about 62 %. Closing the gap needs a better firebox and coil or a combustion air preheater.
- **R2 at risk.** A single hood spends 25 minutes of each cycle holding temperature, which cuts the real rate to about 1.2 m²/h. Two hoods used alternately are needed to reach 2 m²/h.
- **R1 unverified.** Every rate and fuel figure depends on the assumed 60 % hood transfer efficiency.
- A 12.7 mm coil, as first imagined, would need more than 2 bar at its inlet. The concept now uses a 25.4 mm coil to stay near atmospheric pressure.

### Proposed, awaiting Amish

1. Open-vented architecture: water-seal vent standpipe as the primary pressure limit, certified relief valve as the second line, no isolating valve anywhere on the steam side.
2. Monotube coil in 25.4 mm 316 stainless (alternatives: parallel 12.7 mm circuits; soft copper, about $100 cheaper but weak if run dry).
3. Hood steaming with two hoods used alternately (alternatives: one hood plus an insulating blanket; accept about 1.2 m²/h).
4. Feed control: fixed pump rate with a coil outlet temperature alarm (alternative: thermostat-controlled pump speed).
5. Budget: parts use the full $1,500 with no contingency. Options: (a) raise `budget_usd` to $1,800 to allow 20 % contingency; (b) keep $1,500 and accept the risk; (c) cut scope, for example a sheet instead of a hood. Recommended: (a). `project.yaml` is unchanged.
6. First users: one market garden and one nursery; first jurisdiction for the regulatory check: Amish's home jurisdiction.

### Safety concerns

- This is the riskiest concept in the portfolio. The documents carry safety blockquotes for sealing, relief valve, local boiler rules, steam burns, dry coil, fire, carbon monoxide and hot surfaces, and must keep them.
- **Regulatory status is the gating risk.** Whether an open-vented, fired coil is exempt from boiler and pressure vessel rules is unconfirmed and differs by jurisdiction. Recommend a written ruling from the local boiler authority before any TRL 3 detail work.
- **Dry-coil restart** is the most likely serious failure: a biomass fire cannot be switched off, so a pump or tank failure overheats the coil, and refeeding it can flash violently.
- **Carbon monoxide** in greenhouses: steam may go into a greenhouse, but the generator must never do so.
- **Fire** from sparks in dry fields: spark arrestor, cleared ground and burn-ban compliance are required.

### Recommended next step

Review this note and the media. Decide on items 1, 2 and 5 above. If approved, confirm regulatory status first, then run `/advance-trl3` to check the efficiency, two-phase pressure drop and hood heat transfer by calculation.

## Session 2026-09-25: TRL 3

Authority: on 2026-09-25 Amish wrote "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." The TRL 2 recommendations above are recorded as decided in STR-DDR-001, and the repo now claims TRL 3 (`trl: 3`, `trl_target: 3`). TRL 4 is on hold by Amish's instruction.

**Regulatory prerequisite, still open.** The approved recommendation included getting a written ruling from the local boiler authority before TRL 3 detail work. That ruling cannot be obtained in a documentation session, and it has not been obtained. This session therefore did only paper calculations, a massing-plus model and a preliminary drawing. The ruling is marked as an open prerequisite in STR-DDR-001, STR-PRB-001, STR-PRC-001, STR-REQ-001, STR-CAL-001, in the notes and title block of drawing STR-DWG-002, and in `bom/bom-notes.md`. No detail design, purchase or build should happen before it.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (STR-DDR-001 v0.1): the six decided items and the five items still open.
- `docs/04-calcs/01-sizing.md` (STR-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: first-principles sizing (soil heat with a condensation-front model, hood cycle, combustion and firebox heat transfer, economizer, two-phase pressure drop, stored water, dry-coil refeed, relief valve sizing, mass and cost) with a results table for every requirement. The script reads geometry from the model and prices from the BOM and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (helical coil, fiber-lined firebox, economizer, chimney, header with a 1 m water-seal pot and vent, relief valve, hose, two hoods with skirts, trailer). Exports `cad/step/steamroot.step` and `cad/stl/steamroot.stl` plus firebox, coil, header and hood parts.
- `cad/src/sheets.py` and `cad/drawings/STR-DWG-002.svg`, `.pdf`, `.png`: general arrangement at Rev P1 (STR-DWG-001 is the concept blueprint in `media/`).
- `bom/bom.csv`: 16 lines, all priced with a supplier or supplier type; second hood and feed and coil alarms added; `bom/bom-notes.md` updated.
- `cad/src/concept_media.py`: now builds the media from `model.py` and quotes CAL-001; all media refreshed.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` bumped to v0.3 with the decisions and TRL 3 results; `project.yaml` (TRL 3, budget $1,800, evidence list); `README.md` (TRL badge, status line, key components).

### Requirement status (STR-CAL-001), not met first

| ID | Result | Target | Status |
| --- | --- | --- | --- |
| R2 | 1.88 m²/h at 15 cm; 3.41 m²/h at 5 cm (two hoods) | 2 and 5 m²/h | Not met |
| R4 | 5.4 kg wood per m² at 15 cm | 4 kg/m² | Not met |
| R5 | 53.5 % fuel to steam | 65 % | Not met |
| R6 | 0.110 bar gauge at the coil inlet (header 0.033 bar) | 0.1 bar | Not met (10 % over); open vent met |
| R11 | 536 kg loaded with a full tank | 500 kg | Not met |
| R12 | $1,915 parts | $1,800 | Not met |
| R9 | Standard certified valve is 15 psi = 1.03 bar; 6.2 mm orifice needed | 1 bar (15 psi) or less | At risk |
| R11 | 1.48 m width | 1.5 m | At risk |
| R1 | Holds 70 °C at 15 cm in the 1D model if the front reaches 16.5 cm | 70 °C, 20 to 30 min | Not verifiable at TRL 3 |
| R3, R7, R8, R10 | 30 kg/h at 40.7 kW; 7.0 L; 4.2 h; 2.4 m chimney, 23 °C hood skin | | Met |

Counts: 7 not met, 2 at risk, 1 not verifiable at TRL 3, 4 met (14 checks on 12 requirements).

Numbers from the TRL 2 note that changed: efficiency 62 % became 53.5 %; wood use 7.9 kg/h became 10.1 kg/h because the wood heating value at 20 % moisture is 14.5 MJ/kg, not 16; steam per m² at 15 cm 14 became 15.6 kg/m² (soil behind the steam front sits at 100 °C); rate at 5 cm 6.5 became 3.41 m²/h (hold limited); loaded mass 490 became 536 kg (second hood, seal pot, heavier trailer assumption); coil pressure drop 0.05 became 0.077 bar (two-phase and curvature effects); parts cost $1,500 became $1,915.

### Decisions recorded

Decided by Amish, 2026-09-25, going with the recommendation (STR-DDR-001): open-vented architecture with water-seal vent and certified relief valve; 25.4 mm 316 stainless monotube coil; two hoods used alternately; fixed-rate feed with coil outlet and tank level alarms; `budget_usd` raised to $1,800; first users one market garden and one nursery, first jurisdiction Amish's home jurisdiction.

### Items still awaiting Amish

1. **Regulatory ruling** from the local boiler authority: approved, not obtained. Open prerequisite.
2. Which jurisdiction is "home" and which authority to ask.
3. The named market garden and nursery (no partner is named).
4. Wood only, no liquid fuel backup (from STR-PRC-001; not in the TRL 2 review list). **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).
5. How to close R5 and R4: options are (a) a convective evaporator bank in the flue before the economizer, (b) controlled primary and secondary air to reach λ near 1.5, (c) a combustion air preheater (about 62 % alone), or (d) relax R5 to about 55 % and R4 to about 5.5 kg/m². Recommendation: study (a) with (b) at the next paper step, and keep the targets for now. **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).
6. How to treat R2: (a) accept 1.9 m²/h at 15 cm and restate the 5 cm target at about 3.4 m²/h; (b) a third hood (helps 5 cm only, to 4.43 m²/h); (c) raise steam output, which needs a bigger firebox. Recommendation: (a) until soil tests exist. **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).
7. R6: accept 0.11 bar at the coil inlet (the header is at 0.03 bar) or reduce coil drop with a shorter coil or larger tube. Recommendation: redefine R6 as 0.1 bar at the header and 0.15 bar at the coil inlet, because the vent limit applies at the header. **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).
8. R9 wording: change "1 bar (15 psi) or less" to "15 psi (1.03 bar) or less", the lowest standard certified set pressure. Also size the valve for the dry-coil refeed flash (about 14 mm orifice), not only for 30 kg/h. Recommendation: both. **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).
9. R11 mass: (a) tow with the tank and seal pot drained (402 kg) and fill on site; (b) a 100 L tank (3.3 h per fill); (c) raise the limit to 550 kg. Recommendation: (a), written into the requirement as "500 kg or less as towed, with the tank drained". **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).
10. R12 cost: $1,915 is $115 over the new $1,800 budget with no contingency. Options: (a) raise the budget to about $2,200 for 15 % contingency; (b) keep $1,800 and cut, for example one hood; (c) accept. Recommendation: (a). `budget_usd` stays at 1800. **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).
11. Design details raised at TRL 3: fiber lining instead of castable (recommended, for mass); one hose moved between hoods with a steam-rated coupling instead of two hoses (recommended, for cost). **Decided by Amish, 2026-09-25: go with recommendation** (STR-DDR-002).

### Safety concerns

- **Regulatory status** is still the gating risk (see above).
- **Dry-coil refeed.** A dry coil near 520 °C can flash about 1.3 kg of water; if that happens over 30 s it is about 155 kg/h, five times the design flow. The vent and relief valve are sized for 30 kg/h. The coil outlet alarm and the rule never to refeed a hot, dry coil remain essential.
- **Steam jets at the hood skirt.** In soils finer than sand the pressure needed to push steam through the treated layer (about 2,400 Pa in a sandy loam) is ten times what the 29 kg hood can hold down (235 Pa), so steam will escape under the skirt. This is a burn hazard at foot level.
- **Hose changeover.** Two hoods mean the hot hose coupling is moved about twice an hour. Steam must be diverted to the vent first.
- **Hot surfaces and fire.** Firebox skin about 100 °C, flue gas about 450 °C at the spark arrestor.
- **Carbon monoxide** in greenhouses and **fire** in dry fields, as in the TRL 2 note.

### Other notes

- No TRL 4 material exists in the repo; none was created. `firmware/` and `electronics/` hold only placeholders.
- Citations: the TRL 2 documents describe prior work without sources, and there is no list of unchecked citations. No sources were added. The only web check made was the relief valve price (SupplyHouse.com listing for Watts 315M2-015, $68.19, 2026-09-25). Prior-work sources are still to be cited.
- The media render takes about eight minutes because of the helical coil in the hidden-line projection. `media/model.glb` is re-exported at a coarser tessellation to keep it small.

### Recommended next step

Obtain the written ruling from the local boiler authority, and have Amish decide items 5 to 11 above. After that, a second paper iteration at TRL 3 (a revised coil and flue layout to address R5 and R4, and restated R2, R6, R9 and R11) is the right next step. **TRL 4 is on hold by Amish's instruction.** For the record only, TRL 4 would need: the regulatory ruling in hand; a lab test article of the coil, header and water seal; a test plan and report (TST, `environment: lab`) for steam output, efficiency, pressure at the coil inlet and header, dry-coil alarm response and relief valve capacity; soil permeability and skirt leakage tests with the hood; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

Authority: on 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in STR-DDR-002 (`docs/decisions/0002-recommendations-accepted.md`). Items without a recommendation stay open.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| R12 budget | Raise to about $2,200 for 15 % contingency | `budget_usd` 1800; $1,915 BOM, $115 over | `budget_usd` 2200; $285 contingency; met |
| R2 rate | Accept the two-hood rate until soil tests exist | Targets 2 and 5 m²/h; not met | Targets 1.85 (about 1.9) and 3.4 m²/h; 1.88 and 3.41 m²/h; at risk |
| R6 pressure | 0.1 bar at the header, 0.15 bar at the coil inlet | 0.110 bar against 0.1 at the inlet; not met | Header 0.033, inlet 0.110 bar; met |
| R9 relief valve | Word as 15 psi (1.03 bar) or less; size for the refeed flash | At risk; capacity unconfirmed | Watts Series 315, 3/4 in, 375 lb/h (170 kg/h) against a 155 kg/h flash; met on paper; valve unchanged |
| R11 mass | 500 kg or less as towed, tank drained | 536 kg full; not met | 402 kg as towed; met (width 1.48 m still at risk) |
| R5 and R4 | Keep targets; study an evaporator bank with controlled air | No study | CAL-001 section 4: about 3.3 m of 25.4 mm tube reaches 65 % at λ = 2.0; R4 needs about 72 %; both still not met |
| Firebox lining | Ceramic fiber | Proposed | Decided; no geometry change |
| Hose | One hose moved between hoods | Proposed | Decided; no BOM change |
| Fuel | Wood only | Proposed | Decided |

Files changed: `project.yaml` (budget), `README.md` (budget, status line, new write-up sections), STR-PRB-001 v0.4, STR-PRC-001 v0.4, STR-REQ-001 v0.4, STR-CAL-001 v0.2 and `sizing.py`, STR-DDR-001 v0.2, new STR-DDR-002 v0.1, `bom/bom.csv` and `bom/bom-notes.md` (notes only; total unchanged at $1,915), drawing STR-DWG-002 Rev P1 to P2 (notes only; geometry unchanged), concept media key figures (towed mass). All PDFs, drawings and media were regenerated.

### Requirement status (STR-CAL-001 v0.2), not met first

| ID | Result | Target | Status |
| --- | --- | --- | --- |
| R4 | 5.4 kg/m² at 15 cm | 4 kg/m² | Not met |
| R5 | 53.5 % | 65 % | Not met |
| R2 | 1.88 m²/h at 15 cm; 3.41 m²/h at 5 cm | 1.85 and 3.4 m²/h | At risk (thin margin) |
| R11 | 1.48 m width | 1.5 m | At risk |
| R1 | Holds 70 °C at 15 cm in the 1D model if the front reaches 16.5 cm | 70 °C, 20 to 30 min | Not verifiable at TRL 3 |
| R3, R6, R7, R8, R9, R10, R11 mass, R12 | 30 kg/h; header 0.033 and inlet 0.110 bar; 7.0 L; 4.2 h; 170 kg/h valve; 2.4 m chimney; 402 kg towed; $1,915 | | Met |

Counts: 2 not met, 3 at risk, 1 not verifiable at TRL 3, 9 met (15 checks on 12 requirements). Before: 7 not met, 2 at risk, 1 not verifiable, 4 met.

### Items still awaiting Amish

1. Written ruling from the local boiler authority: approved, not obtained. Open prerequisite for any detail design or build.
2. Which jurisdiction is "home" and which authority to ask (no recommendation).
3. The named market garden and nursery (no recommendation).

### Cross-repo actions

None. No SteamRoot decision needs a change in another repo.

### Notes

- The evaporator bank is not yet in the model. About 4 m of bank tube would add about 1.5 L of water and take the heated section to about 8.5 L, over R7's 8 L, so the next paper iteration must resolve R7 together with R5, R6 and R11.
- `README.md` now has the Concept rationale, Burning platform, Where it could be used and What sparked the idea sections, with cited figures (Oerke 2006, FiBL 2025, the US 2016 critical use exemption rule, UNEP 2014).
- **TRL 4 remains on hold** by Amish's instruction. Decided items that need TRL 4 work (measured efficiency, soil permeability and skirt tests for R1 and R2, capacity check of the valve actually bought) are recorded as decided but on hold. Nothing was built, bought or tested.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added an appearance model for photoreal renders. It changes no design figure, requirement, BOM line or calculation.

### What was done

- New `cad/src/product_model.py`: `product_parts()` returns 104 named parts (75 shell, 8 internal, 18 accessory, 3 context), each with colour, material, BOM line, group and exploded offset. It also defines `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view of the generator on its trailer without the person, the ground or the hoods). Every shape is valid and tessellates at the export tolerance.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced separately by the portfolio render pipeline.

### What the appearance model adds

- Filleted firebox, economizer, drum, hood and enclosure edges; angle-iron bands at the firebox top and bottom and a base flange under the economizer, read as seams.
- Firebox door with a ceramic glass window onto a glowing fire bed, a wood charge and the coil; hinges, latch with a hardwood grip, and a slotted air damper plate with a knob.
- Economizer access panel with eight bolts, a raised STEAMROOT mark, condensate drain valve with a lever, and an internal tube bank for the exploded view.
- Stainless chimney with a base collar and joint band, spark arrestor cage with a 6 mm mesh screen, and a conical rain cap.
- Teal water-seal pot with deck flange and level sight tube, DN50 header with end flange, vent pipe with an open top cap, diverter valve with lever and steam quick coupling, bronze relief valve with test lever and set-pressure tag, and a 0 to 1 bar gauge on a siphon.
- Labels as thin raised parts: "HOT SURFACE / DO NOT TOUCH" on the firebox, "OPEN VENT / 0.1 BAR MAX / NEVER PLUG" on the seal pot, and "HOT STEAM" on each hood.
- Feed drum with rolling hoops, filler cap, level sight tube and two fabric ratchet straps on a saddle cradle; pump and alarm enclosure with a lid, screws, a lit running indicator, an alarm indicator and a buzzer grille.
- Trailer detail: perimeter frame with crossmembers and stake pockets, deck plate, leaf springs and hangers, coupling head and lever, jockey wheel jack, teal mudguards, tail lights and side reflectors, treaded tyres, and rims with hubs and wheel nuts.
- Aluminum steam hoods with stiffening beads, round handles on standoffs, galvanized skirts, inlet couplings and teal accent bands.
- Context: a gravel pad under the trailer, a soil bed under the hoods, and the shared clay mannequin (1.75 m, standing pose) at the firebox, facing the door.

### Differences from model.py (Proposed, awaiting Amish)

All main dimensions and interfaces come from `PARAMS` in `model.py`, and the coil geometry is used unchanged. These appearance choices differ from the massing model:

1. **Door opening in the firebox.** The massing shell is a closed box behind the door. The appearance model cuts a 300 x 240 mm opening in the shell and lining behind the door so the window shows the fire. Recommendation: add the opening to `model.py` at the next model revision, since a real firebox needs it.
2. **Header support mast and stay.** `model.py` shows the header carried only by the coil outlet pipe. The appearance model adds a 50 mm square mast from the deck to the header underside and a stay to the seal pot. Recommendation: accept as a placeholder and size the support at detail design.
3. **Economizer to coil jumper.** The coil inlet in `model.py` ends beside the economizer box. The appearance model adds a short jumper into the economizer +X face. Recommendation: add it to `model.py`.
4. **Feed lines.** Drum to pump and pump to economizer lines are drawn as indicative 16 mm hoses; `model.py` has none. Recommendation: accept as indicative routing.
5. **Steam hose routing.** The hose starts and ends at the `model.py` points (diverter coupling and first hood inlet) but runs as a smooth drooping curve instead of the square polyline. Recommendation: accept; `model.py` already calls the routing indicative.
6. **Items drawn that the BOM lists as not drawn.** The pressure gauge (item 14) and the alarm indicators and buzzer (item 16) are shown on the header and the pump enclosure. The battery (item 13) is still not drawn. Recommendation: accept; no BOM change.
7. **Appearance additions with no BOM line of their own.** Mudguards, tail lights, reflectors, leaf springs and the jockey wheel are shown as part of the used trailer (item 1); drum straps are shown with the drum (item 3). Recommendation: accept; they come with a used trailer or cost a few dollars.
8. **Air damper height.** The damper plate sits about 15 mm lower than the `model.py` box so it clears the door. Recommendation: accept.
9. **Hoods and hose in the accessory group.** This keeps them out of the detail view so the generator can fill the frame; they still appear in the hero and exploded views.

### Status

This is an appearance model only: no tolerances, no fabrication detail, labelled CONCEPT, NOT FOR FABRICATION. `trl` stays 3 in `project.yaml`, and TRL 4 remains on hold by Amish's instruction. The written ruling from the local boiler authority is still an open prerequisite for any detail design or build.

### Safety

The renders show hot surfaces and a pressure-limiting vent. The labels in the model repeat the Safety section: the water seal and vent must never be plugged or valved off, and the firebox, flue, header and hoods are burn hazards in use.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, constructable design and prototype build plan

Authority: Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept in a separate design decisions register; on 2026-09-30 he wrote "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations"; on 2026-10-01 he set budgets as value-engineering targets. TRL stays 3; nothing was built, bought or tested.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten as a constructable model: every component keyed and modelled as made or bought, with fixings, and 93 build123d constructability checks (`python cad/src/model.py --check`), all passing, including the order in which the coil goes into the firebox. `--mass` prints the parts added for construction.
- `docs/decisions/0003-design-for-construction.md` (STR-DDR-003 v0.1, Draft): every design change with its reason, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (STR-BLD-001 v0.1): the illustrated build plan. `cad/src/build_plan_media.py` draws the overview, 21 making sketches (`cad/drawings/STR-DWG-101` to `121`), 10 joint close-ups, 20 step pictures and the 12 V wiring diagram (`docs/05-build-plan/`).
- `docs/06-design-decisions.md` (STR-DEC-001 v0.1): 11 open decisions, 8 items to confirm when parts are bought, the value engineering section and the decisions made.
- `bom/bom.csv`: lines 5, 6 and 8 respecified, lines 17 to 21 added; `docs/04-calcs/sizing.py` and STR-CAL-001 v0.3 rerun for the new geometry; STR-REQ-001 v0.5 and STR-PRC-001 v0.5 updated; STR-DWG-002 Rev P3; STEP, STL and concept media regenerated; `project.yaml` (`design_state: constructable`, new evidence); `README.md` (links, "Building the prototype").

### Design changes made for construction (STR-DDR-003)

1. C1 Firebox 1000 mm tall (was 650 mm) with the coil above the fire: door opening 300 x 240 mm, grate on a stand with an ash pit, air inlet and slide damper below the coil; 280 mm of fire space.
2. C2 Three stainless coil brackets welded to the shell through the lining.
3. C3 Bolted roof on an angle frame; the coil goes in from the top and its tails slide out through wall slots closed by gland plates with rope packing; unions outside; separate outlet pipe; the inlet jumper rerouted so nothing crosses.
4. C4 Economizer as a bolted box on studs with a serpentine tube bank (7.3 m, bent on a standard 38 mm radius) on support bars, a bolted lid carrying the chimney spigot, and bulkhead unions.
5. C5 Firebox skids welded under the firebox and bolted into the trailer side rails, with a 50 mm air gap.
6. C6 Seal pot on a foot plate; dip leg 890 mm below the static mark so the seal still blows at 1.0 m of water (0.094 bar); pot top raised; header lowered to 1550 mm.
7. C7 Header post with saddle and U-bolts; pot stay.
8. C8 Diverter at the back of the header with a vent line into the vent pipe.
9. C9 Relief valve on a socket with a discharge pipe to 2.3 m and a stay.
10. C10 Hose routed clear of the trailer to a coupling on the hood.
11. C11 Hood riser, flange and hung manifold; skirt riveted round the outside.
12. C12 Drum saddles, ratchet straps, suction hose and stainless feed line with clips.
13. C13 Pump and alarm box with battery and controller.
14. C14 Door with board plug, hinges and latch; damper slide in guides.

### Key results (STR-CAL-001 v0.3)

- Efficiency 51.4 % (was 53.5 %) and wood 5.6 kg/m² at 15 cm (was 5.4): **R5 and R4 still not met**, gaps about 2 points wider because the taller firebox loses 3.5 kW through its walls (was 2.6 kW).
- Coil inlet 0.108 bar, header 0.033 bar, seal limit 0.094 bar: R6 met. Water in the heated section 6.9 L: R7 met.
- Towed mass 468 kg (602 kg full): R11 mass met with 32 kg to spare; width 1.48 m at risk as before.
- Value-engineering target: USD 2,200. Estimated cost of the constructable design: USD 2,275 (USD 75 over the target).
- Status counts: 2 not met (R4, R5), 3 at risk, 1 not verifiable at TRL 3, 8 met; R12 USD 75 over the target.

### Proposed, awaiting Amish

All in the register (`docs/06-design-decisions.md`): accept STR-DDR-003; how to recover the efficiency lost to the taller firebox (A1); a seal pot overflow at the static mark (A2, a safety case change); relief discharge up or down (A3); plus the open items carried over (boiler authority ruling, jurisdiction, partners, evaporator bank, seal freezing, hood stowage, hood ballast).

### Safety concerns

- The boiler authority ruling is still the gating prerequisite: build plan safety stop S1.
- C6 corrects a real flaw: as drawn, a 1 m dip leg would have let the header reach about 0.11 bar and pushed seal water into the vent. The corrected geometry keeps 0.094 bar.
- The build plan adds stops for welding, ceramic fibre handling, cold pressure tests, never firing a dry coil and never refeeding a hot, dry coil.

### Stale media (made on Amish's Mac, not regenerated here)

`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png`, and the appearance model `cad/src/product_model.py`, show the concept: a 650 mm firebox with the coil round the fire, no skids or roof frame, the header at 1.6 m and the seal pot through the deck. They are stale and need updating.

### Recommended next step

Amish to review STR-DDR-003 and the register. Then the second paper iteration at TRL 3 (evaporator bank, controlled air and firebox shape, decisions 4 and 5). TRL 4 stays on hold.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.

## 2026-10-03: decisions recorded

Amish decided on 2026-10-03: "Cost over target - i accept all the cost variations and overruns". Recorded for this repo: the estimated cost of USD 2,600 against the USD 2,200 target (USD 400 over).

- `docs/06-design-decisions.md`: row added to decisions made; value engineering section says the overrun was accepted by Amish on 2026-10-03.

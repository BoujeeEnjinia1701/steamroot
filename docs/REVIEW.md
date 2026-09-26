# Review note: SteamRoot

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

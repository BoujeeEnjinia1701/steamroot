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

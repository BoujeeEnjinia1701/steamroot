---
doc_id: STR-DEC-001
title: SteamRoot design decisions register
project: SteamRoot
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review notes, the decision records and the build plan work; budget treated as a value-engineering target
---

# SteamRoot design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Decision 1 gates everything else. No part of SteamRoot may be bought, built or fired before the written ruling from the local boiler authority exists, and that ruling overrides any decision here that it is stricter than.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Written ruling from the local boiler authority on an open-vented, fired monotube coil | Obtain it before any purchase or build (approved by Amish, 2026-09-25, as a prerequisite; not yet obtained) | Obtain it first; review the design against it | Everything: build plan safety stop S1 | STR-DDR-001, item 7; STR-DDR-002, item 10 |
| 2 | Which jurisdiction is "home" and which authority to ask | Amish to name them | None (Amish's choice) | Decides who gives ruling 1 | STR-DDR-002, item 11 |
| 3 | The named market garden and nursery (first co-design partners) | Amish to name them | None (Amish's choice) | Not part of the build; sets the soil for the first tests | STR-DDR-002, item 12 |
| 4 | How to close R5 (65 % efficiency) and R4 (4 kg wood per m²): add the evaporator bank and controlled primary and secondary air to the model | Bank of about 4.3 m of 25.4 mm tube in the flue at λ = 2.0, or 1.3 m at λ = 1.5 (STR-CAL-001 v0.3, Table 5a); each must keep R7 (8 L) | Next paper iteration, together with 5 | Firebox roof, flue and economizer; not in this prototype | STR-DDR-002, item 1 |
| 5 | Efficiency lost to the taller firebox (51.4 %, was 53.5 %) | (a) accept for the first prototype; (b) 75 mm lining with the box 50 mm larger each way (about 53.8 %, about 8 kg more); (c) fold the firebox shape into the evaporator bank study (4) | (c), keeping (a) for now | Firebox shell and lining sizes | STR-DDR-003, A1 |
| 6 | Seal pot level: condensate raises it, boiling lowers it; overfilling raises the seal limit | (a) an overflow pipe at the static water mark, draining to the ground; (b) level mark and top-up by hand only, as now | (a); it changes the safety case, so it needs Amish's approval | Seal pot (one more branch) | STR-DDR-003, A2; STR-PRC-001 open questions |
| 7 | Relief valve discharge direction | (a) up to 2.3 m beside the vent, as modelled; (b) down to the ground at the front of the trailer | (a), subject to ruling 1 | Discharge pipe and stay | STR-DDR-003, A3 |
| 8 | Seal pot freezing | (a) drain the pot after every day of use and in frost, through its drain valve; (b) insulate and trace-heat it | (a) | None (operating rule) | STR-PRC-001 open questions |
| 9 | Where the two hoods ride when towing (the deck has no room for them) | (a) carried on a second vehicle; (b) a rack over the feed drum (about 15 kg more and higher centre of mass); (c) hung on the trailer sides (width over 1.5 m) | (a) for the prototype | Not part of the trailer build | STR-PRC-001 open questions |
| 10 | Accept the design for construction (changes C1 to C14: taller firebox with the coil above the fire, bolted roof, coil brackets and glands, economizer layout, skids, seal pot and dip leg, header post, vent line, relief discharge, hose, hood, drum and feed details) | (a) accept as made; (b) accept with changes | (a); the changes were made under Amish's 2026-09-30 instruction to make the design physically buildable and are open for his review | The whole build plan follows them | STR-DDR-003 |
| 11 | Hood ballast and real soil behaviour (skirt leakage, permeability, starting moisture) | Decide after soil tests at TRL 4: ballast weights on the hood, a deeper skirt, or lower steam rate in fine soils | Decide from TRL 4 tests (TRL 4 is on hold) | Hood handles could carry ballast; nothing built now | STR-CAL-001, section 2; STR-PRC-001 open questions |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The used trailer: rated 750 kg or more, axle rated for the 602 kg full mass, and side rails that take an M12 bolt 40 mm in from the deck edge (80 mm rails assumed) | The skids bolt into the side rails; the full machine weighs 602 kg on site | STR-DDR-003, C5; STR-CAL-001 |
| 2 | The relief valve's rated capacity, 375 lb/h (170 kg/h) or more at 15 psi, on the valve actually bought, with its code stamp | R9 is met only on the maker's table | STR-DDR-002, item 4 |
| 3 | The three-way diverter cannot stop in a position that closes both outlets, and is rated for saturated steam | The open vent must never be isolated | STR-PRC-001; STR-DDR-003, C8 |
| 4 | The steam hose and couplings are rated for saturated steam (not hot water), with whip checks | Burn hazard at the hose | BOM line 11 |
| 5 | The cast grate is 300 x 300 mm; if not, the grate stand is resized to suit | The stand is made to the grate | STR-DDR-003, C1 |
| 6 | The ceramic fibre blanket and board are rated for 1260 °C, with rigidizer for the walls | The lining faces the fire | BOM line 5 |
| 7 | The feed pump's shut-off pressure is 3 bar or less | It caps the coil inlet pressure if the coil blocks | STR-CAL-001, section 6 |
| 8 | The alarm controller takes a type K thermocouple and drives a relay; the float switch trips with about 20 L left | The dry-coil and low-tank alarms | BOM line 16 |

## Value engineering

Value-engineering target: USD 2,200 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,275 (USD 75 over the target). Main cost drivers and savings worth trying:

- The largest lines are the firebox (USD 260), the stainless coil (USD 235), the used trailer (USD 200), the steam hose (USD 180), the two hoods (USD 280 together) and the header and water-seal assembly (USD 150).
- Making the design constructable added USD 360: the taller firebox and longer coil (USD 55), steelwork for the skids, post, stay and saddles (USD 70), firebox internals and glands (USD 50), feed lines and stainless fittings (USD 95), the relief discharge and vent line (USD 45) and fixings and straps (USD 45).
- Savings worth trying: copper instead of stainless for the cold feed line from the pump (about USD 20; the economizer and jumper stay stainless); offcut or reclaimed steel for the skids, post and stand; buying the stainless fittings from one supplier as a kit; a used trailer that already has cross members for the skids. The safety parts (relief valve, diverter, hose, seal and vent) are not candidates for savings.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Open-vented steam side with a water-seal vent and a certified relief valve, no isolating valve; 25.4 mm 316 stainless monotube coil; two hoods used alternately; fixed-rate feed with coil outlet and tank level alarms; budget USD 1,800; first users one market garden and one nursery, first jurisdiction Amish's home jurisdiction; get the boiler authority ruling first | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | STR-DDR-001 |
| 2026-09-25 | Wood only, no liquid fuel backup | Amish: go with recommendation | STR-DDR-001, item 10; STR-DDR-002, item 9 |
| 2026-09-25 | Keep the R5 and R4 targets and study an evaporator bank with controlled air; R2 restated to about 1.9 and 3.4 m²/h; R6 split into 0.1 bar at the header and 0.15 bar at the coil inlet; R9 worded as 15 psi (1.03 bar) or less and sized for the refeed flash; R11 as towed with the drum drained; budget USD 2,200; fibre lining; one hose moved between the hoods | Amish: "i accept all your recommendations, go with them across all repos." | STR-DDR-002, items 1 to 8 |
| 2026-10-01 | The budget is a value-engineering target, not a limit; cost is reported over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; STR-CAL-001 v0.3 |

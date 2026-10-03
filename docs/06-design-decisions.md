---
doc_id: STR-DEC-001
title: SteamRoot design decisions register
project: SteamRoot
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review notes, the decision records and the build plan work; budget treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for all eleven open decisions on 2026-10-02 (STR-DDR-003 accepted); moved to decisions made"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved decisions carried into the design (STR-CAL-001 v0.4); value engineering restated at USD 2,600; two new proposals opened: R4 restatement and the R11 mass basis"
---

# SteamRoot design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Decision 1 gates everything else. No part of SteamRoot may be bought, built or fired before the written ruling from the local boiler authority exists, and that ruling overrides any decision here that it is stricter than.

## Open decisions

The eleven decisions of the 2026-10-02 sign-off are made. Carrying them into the design raised two new questions, proposed here and awaiting Amish.

| # | Question | Options | Recommendation | Source |
| --- | --- | --- | --- | --- |
| 12 | Restate R4 (wood per m² at 15 cm), as planned on 2026-10-02. With the bank and dampers the design uses 4.2 kg/m² (4.7 kg/m² with the dampers open); 4 kg/m² needs about 72 % efficiency. | (a) 4.5 kg/m² or less with the dampers set; (b) 5.0 kg/m² or less, which also covers open dampers; (c) keep 4 kg/m² and seek the rest in lower steam demand | (a): met with 7 % margin and still rewards air control. Proposed, awaiting Amish | STR-CAL-001 v0.4, section 4 |
| 13 | R11 is now at risk at 499 kg as towed, because the bank, overflow and steel handles added 36 kg. The hoods ride on a second vehicle for the prototype (decided 2026-10-02). | (a) count R11 without the hoods, as they are towed: 437 kg; (b) keep the hoods in R11 and save mass elsewhere (lighter bank box, aluminium skids); (c) restate R11 | (a), since it follows the decision already made; record it in STR-REQ-001. Proposed, awaiting Amish | STR-CAL-001 v0.4, section 7 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The used trailer: rated 750 kg or more, axle rated for the 633 kg full mass, and side rails that take an M12 bolt 40 mm in from the deck edge (80 mm rails assumed) | The skids bolt into the side rails; the full machine weighs 602 kg on site | STR-DDR-003, C5; STR-CAL-001 |
| 2 | The relief valve's rated capacity, 375 lb/h (170 kg/h) or more at 15 psi, on the valve actually bought, with its code stamp | R9 is met only on the maker's table | STR-DDR-002, item 4 |
| 3 | The three-way diverter cannot stop in a position that closes both outlets, and is rated for saturated steam | The open vent must never be isolated | STR-PRC-001; STR-DDR-003, C8 |
| 4 | The steam hose and couplings are rated for saturated steam (not hot water), with whip checks | Burn hazard at the hose | BOM line 11 |
| 5 | The cast grate is 300 x 300 mm; if not, the grate stand is resized to suit | The stand is made to the grate | STR-DDR-003, C1 |
| 6 | The ceramic fibre blanket and board are rated for 1260 °C, with rigidizer for the walls | The lining faces the fire | BOM line 5 |
| 7 | The feed pump's shut-off pressure is 3 bar or less | It caps the coil inlet pressure if the coil blocks | STR-CAL-001, section 6 |
| 8 | The alarm controller takes a type K thermocouple and drives a relay; the float switch trips with about 20 L left | The dry-coil and low-tank alarms | BOM line 16 |

## Value engineering

Value-engineering target: USD 2,200 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,600 (USD 400 over the target). Main cost drivers and savings worth trying:

- The largest lines are the two hoods (USD 310 together), the firebox (USD 265), the header and water-seal assembly with its overflow (USD 220), the stainless coil (USD 215), the used trailer (USD 200), the evaporator bank (USD 190) and the steam hose (USD 180).
- Carrying the 2026-10-02 decisions into the design added USD 325: the evaporator bank (USD 190), the seal pot overflow (USD 70), the bank link and reducing unions (USD 45), ballast-rated hood handles (USD 30), the secondary damper and fixings (USD 10 net), less USD 20 for one coil turn fewer.
- Making the design constructable added USD 360: the taller firebox and longer coil (USD 55), steelwork for the skids, post, stay and saddles (USD 70), firebox internals and glands (USD 50), feed lines and stainless fittings (USD 95), the relief discharge and vent line (USD 45) and fixings and straps (USD 45).
- Savings worth trying: copper instead of stainless for the cold feed line from the pump (about USD 20; the economizer and jumper stay stainless); offcut or reclaimed steel for the skids, post and stand; buying the stainless fittings from one supplier as a kit; a used trailer that already has cross members for the skids; welded rather than seamless 316 tube for the bank (already assumed); a bank box with 1.5 mm walls. The safety parts (relief valve, diverter, hose, seal and vent) are not candidates for savings.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Open-vented steam side with a water-seal vent and a certified relief valve, no isolating valve; 25.4 mm 316 stainless monotube coil; two hoods used alternately; fixed-rate feed with coil outlet and tank level alarms; budget USD 1,800; first users one market garden and one nursery, first jurisdiction Amish's home jurisdiction; get the boiler authority ruling first | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | STR-DDR-001 |
| 2026-09-25 | Wood only, no liquid fuel backup | Amish: go with recommendation | STR-DDR-001, item 10; STR-DDR-002, item 9 |
| 2026-09-25 | Keep the R5 and R4 targets and study an evaporator bank with controlled air; R2 restated to about 1.9 and 3.4 m²/h; R6 split into 0.1 bar at the header and 0.15 bar at the coil inlet; R9 worded as 15 psi (1.03 bar) or less and sized for the refeed flash; R11 as towed with the drum drained; budget USD 2,200; fibre lining; one hose moved between the hoods | Amish: "i accept all your recommendations, go with them across all repos." | STR-DDR-002, items 1 to 8 |
| 2026-10-01 | The budget is a value-engineering target, not a limit; cost is reported over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; STR-CAL-001 v0.3 |
| 2026-10-02 | The written ruling stays the gate: it is obtained before any purchase or build, the design is reviewed against it, and anything stricter it requires is adopted (the ruling itself is not yet obtained) | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-001, item 7; STR-DDR-002, item 10 |
| 2026-10-02 | Home jurisdiction: Texas. The written ruling is asked of the Texas Department of Licensing and Regulation's boiler program | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-002, item 11 |
| 2026-10-02 | First co-design partners: one market garden and one nursery within driving distance of Irving that already steam, solarize or chemically treat soil, found through Texas A&M AgriLife Extension's horticulture contacts (none is named or agreed yet) | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-002, item 12 |
| 2026-10-02 | In the next paper iteration, size the evaporator bank with primary and secondary air dampers so the heated water stays at 8 L or less (smaller-bore bank tube or fewer firebox turns), without relaxing R7; plan to restate R4, since even 65 % efficiency leaves it short (about 72 % needed) | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-002, item 1 |
| 2026-10-02 | Option (c), keeping (a) for now: the taller firebox's 51.4 % is accepted for the first prototype, and the firebox is reshaped inside the evaporator bank study | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-003, A1 |
| 2026-10-02 | Seal pot overflow at the static water mark, piped down to ground level at the back of the trailer away from the operator's side | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-003, A2; STR-PRC-001 open questions |
| 2026-10-02 | Relief valve discharge kept rising to 2.3 m beside the vent, with its low-point drain, subject to the authority's ruling | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-003, A3 |
| 2026-10-02 | Seal pot drained through its valve after every day of use and whenever frost is forecast; a pre-start check that the pot is free of ice and filled to its mark | Amish: "i approve your recommendations for all 555 open decisions." | STR-PRC-001 open questions |
| 2026-10-02 | The two hoods ride on a second vehicle for the prototype | Amish: "i approve your recommendations for all 555 open decisions." | STR-PRC-001 open questions |
| 2026-10-02 | Design for construction accepted: changes C1 to C14 of STR-DDR-003 as made, with the seal pot overflow decided separately (item 6) | Amish: "i approve your recommendations for all 555 open decisions." | STR-DDR-003 |
| 2026-10-02 | Hood ballast, skirt depth or steam rate decided from TRL 4 soil tests, with skirt leakage measured at the hood edge; the hood handles are sized to take ballast weights so no redesign is needed later | Amish: "i approve your recommendations for all 555 open decisions." | STR-CAL-001, section 2; STR-PRC-001 open questions |

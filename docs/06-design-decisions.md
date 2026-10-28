---
doc_id: STR-DEC-001
title: SteamRoot design decisions register
project: SteamRoot
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-25'
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
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Amish accepted the cost overrun against the value-engineering target on 2026-10-03; row added to decisions made; value engineering section updated"
- version: "0.5"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: S1 gas-pass baffles decided under Amish's standing instruction of 2026-10-23 (STEM S6, S7); proposed, awaiting Amish: #14 concept choice (A and B within 10 %), S2 hood handling (STEM B4), #16 battery, #17 new PR-016 to PR-018, #18 bed preparation, #19 product model site scene; after the independent review: S3 chimney outlet 3.2 m and S4 latching pump trip decided under the standing instruction, S1 updated (316L economizer baffles, 66.1 %), S2 recommendation changed to a wheel kit, #18 now covers STEM S11 as failed, #20 refeed flash basis and #21 firebox skin limit proposed; value engineering at USD 2,720"
---

# SteamRoot design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Decision 1 gates everything else. No part of SteamRoot may be bought, built or fired before the written ruling from the local boiler authority exists, and that ruling overrides any decision here that it is stricter than.

## Open decisions

The eleven decisions of the 2026-10-02 sign-off are made. Carrying them into the design raised two new questions (#12, #13), and the kit 1.9.1 upgrade of 2026-10-24 and 25 raised nine more (#14 to #21, S2). All are proposed here and awaiting Amish.

| # | Question | Options | Recommendation | Source |
| --- | --- | --- | --- | --- |
| 12 | Restate R4 (PR-004, wood per m² at 15 cm), as planned on 2026-10-02. With the bank, the gas-pass baffles and the dampers set the design uses 4.36 kg/m² (4.44 kg/m² with the dampers wide open, 5.18 kg/m² with 30 % moisture wood); 4 kg/m² needs about 72 % efficiency. | (a) 4.5 kg/m² or less with the dampers set; (b) 5.0 kg/m² or less, which also covers the λ = 2.0 sensitivity; (c) keep 4 kg/m² and seek the rest in lower steam demand | (a): met with 3 % margin and still rewards air control. Proposed, awaiting Amish | STR-CAL-001 v0.5, section 4 |
| 13 | R11 (PR-011) is not met at 509 kg as towed (499 kg before the gas-pass baffles added 7.4 kg and the taller chimney 2.5 kg). The hoods ride on a second vehicle for the prototype (decided 2026-10-02). | (a) count PR-011 without the hoods, as they are towed: 447 kg; (b) keep the hoods in PR-011 and save mass elsewhere (lighter bank box, aluminium skids); (c) restate PR-011 | (a), since it follows the decision already made; record it in STR-PRS-001. Proposed, awaiting Amish | STR-CAL-001 v0.5, section 7 |
| 14 | Concept choice: option A (monotube coil, the current design) or option B (vented fire-tube kettle). Weighted scores A 132, B 120 of 180, a 9.1 % gap, inside the 10 % band | (a) option A; (b) option B | No pick: within 10 %, so both go to Amish (STANDARDS section 21). The repo stays on A until he decides | STR-OPT-001; STR-DDR-004, Part 1 |
| 15 (S2) | Hood handling: each hood weighs 31.3 kg with handles 1.12 m apart, above the 23 kg load constant of the revised NIOSH lifting equation, and above the 10 to 14 kg it allows once the horizontal reach is counted (STEM B4, PR-016) | (a) two-person lift by the operator and the helper already on site, ballast lifted off first (15.6 kg each, borderline); (b) a hood wheel kit or lifting aid so one person tips and rolls each hood (about 4 kg a hood, not priced); (c) lighter hoods | (b), changed after the independent review showed a two-person share is borderline; (a) only as an interim. Proposed, awaiting Amish | STR-STM-001 B4; STR-DDR-004, Part 3 |
| 16 | Battery: at an assumed 4 A pump the 20 Ah lead-acid battery gives only about 15 to 16 Ah at a 4 A draw, so one 4.2 h fill takes it to about 100 % depth of discharge (STEM E3, PR-008) | (a) a 40 Ah battery with a low-voltage cut-off (about 6 kg more, counts in PR-011); (b) keep 20 Ah and charge between fills; (c) choose a lower-current pump | (a), sized from the datasheet of the pump chosen. Proposed, awaiting Amish | STR-STM-001 E3 |
| 17 | New product requirements added in the migration to STR-PRS-001: PR-016 hood handling, PR-017 two independent means against pressure (Texas Health and Safety Code 755.022(a)(4)), PR-018 workshop build | (a) accept; (b) amend; (c) drop | (a): each traces to a user requirement that had none. Proposed, awaiting Amish | STR-PRS-001; STR-URS-001 |
| 18 | Bed preparation and hood hold-down: STEM S11 fails. Even in clean sand the steam needs 92 % of the 256 Pa hood lift, and in sandy loam about nine times it; extension guidance is to till or loosen beds before steaming. The fixes change how the machine is used, so they come to Amish | (a) add "till or loosen the bed to working depth, moist but not wet" to the operating notes and PR-001 assumptions; (b) stakes or straps to hold the hood down; (c) a deeper skirt or a larger hood; (d) a lower steam flux; (e) wait for the TRL 4 soil tests decided on 2026-10-02 | (a) now, as an operating note, with the TRL 4 tests choosing among (b) to (d). Proposed, awaiting Amish | STR-STM-001 S11; MSU P4033 |
| 19 | Product model appearance (render only): a market-garden site with a cultivated bed, a gravel pad and a 1.75 m operator mannequin | (a) accept; (b) amend | (a). Proposed, awaiting Amish | `cad/src/product_model.py` |
| 20 | Refeed flash basis: the relief valve (170 kg/h) and the 350 mm overflow loop seal are sized for a 1.17 kg flash over 30 s with the coil at 519 °C. The independent review found the basis unbounded: a dry coil may reach 700 to 800 °C (about 2 kg) and the seal and valve sit at the header, downstream of the coil (STEM S15 to S17) | (a) bound the flash: the latching trip (S4) plus a rule and an interlock that the coil outlet must fall below 150 °C before the pump can be reset, and size the valve and loop seal for 2 kg over 15 s; (b) add a second relief upstream of the coil, at the economizer outlet; (c) both | (a): it keeps one relief valve and makes the basis explicit; (b) if the authority asks for it. Proposed, awaiting Amish | STR-STM-001 S15 to S17; STR-CAL-001 v0.5 section 6 |
| 21 | Firebox skin temperature: about 99 °C at the exit gas temperature and about 135 °C near the fire bed (STEM S8), with no requirement limiting it | (a) add a product requirement for touchable surfaces with a guard or warning at the operator side; (b) thicker lining at the fire bed (about 5 kg); (c) leave to the operating notes | (a), with a mesh guard on the door side. Proposed, awaiting Amish | STR-STM-001 S8; STR-RSK-001 H7 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The used trailer: rated 750 kg or more, axle rated for the 643 kg full mass, and side rails that take an M12 bolt 40 mm in from the deck edge (80 mm rails assumed) | The skids bolt into the side rails; the full machine weighs about 643 kg on site with the tank filled | STR-DDR-003, C5; STR-CAL-001 |
| 2 | The relief valve's rated capacity, 375 lb/h (170 kg/h) or more at 15 psi, on the valve actually bought, with its code stamp | R9 is met only on the maker's table | STR-DDR-002, item 4 |
| 3 | The three-way diverter cannot stop in a position that closes both outlets, and is rated for saturated steam | The open vent must never be isolated | STR-PRC-001; STR-DDR-003, C8 |
| 4 | The steam hose and couplings are rated for saturated steam (not hot water), with whip checks | Burn hazard at the hose | BOM line 11 |
| 5 | The cast grate is 300 x 300 mm; if not, the grate stand is resized to suit | The stand is made to the grate | STR-DDR-003, C1 |
| 6 | The ceramic fibre blanket and board are rated for 1260 °C, with rigidizer for the walls | The lining faces the fire | BOM line 5 |
| 7 | The feed pump's shut-off pressure is 3 bar or less | It caps the coil inlet pressure if the coil blocks | STR-CAL-001, section 6 |
| 8 | The alarm controller takes a type K thermocouple and drives a relay; the float switch trips with about 20 L left | The dry-coil and low-tank alarms | BOM line 16 |
| 9 | The feed pump's running current at 0.5 L/min against about 0.12 bar | It sizes the battery (DEC #16) | STR-STM-001 E3 |
| 10 | The stainless sheet for the gas-pass baffles (1.5 mm 304 for the bank, 1 mm 316L for the economizer) is flat and cut square to the drawing | The baffle edges set the gas gaps that make the passes work | STR-DEC-001 S1; BOM lines 7 and 22 |

## Value engineering

Value-engineering target: USD 2,200 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,720 (USD 520 over the target), of which USD 120 comes from the kit 1.9.1 fixes: the gas-pass baffles (USD 50, S1), the taller chimney (USD 60, S3) and the latching pump trip (USD 10, S4). Main cost drivers and savings worth trying:

Amish accepted the overrun on 2026-10-03: the estimated cost of USD 2,600 against the USD 2,200 target (USD 400 over). Amish: "Cost over target - i accept all the cost variations and overruns". It stays reported against the target as an accepted overrun, and the savings below remain worth trying. The USD 120 of fixes came after that acceptance and is reported here for his review.

- The largest lines are the two hoods (USD 310 together), the firebox (USD 265), the header and water-seal assembly with its overflow (USD 220), the stainless coil (USD 215), the evaporator bank with its baffle (USD 205), the chimney (USD 150), the used trailer (USD 200) and the steam hose (USD 180).
- Carrying the 2026-10-02 decisions into the design added USD 325: the evaporator bank (USD 190), the seal pot overflow (USD 70), the bank link and reducing unions (USD 45), ballast-rated hood handles (USD 30), the secondary damper and fixings (USD 10 net), less USD 20 for one coil turn fewer.
- Making the design constructable added USD 360: the taller firebox and longer coil (USD 55), steelwork for the skids, post, stay and saddles (USD 70), firebox internals and glands (USD 50), feed lines and stainless fittings (USD 95), the relief discharge and vent line (USD 45) and fixings and straps (USD 45).
- Savings worth trying: copper instead of stainless for the cold feed line from the pump (about USD 20; the economizer and jumper stay stainless); offcut or reclaimed steel for the skids, post and stand; buying the stainless fittings from one supplier as a kit; a used trailer that already has cross members for the skids; welded rather than seamless 316 tube for the bank (already assumed); a bank box with 1.5 mm walls. The safety parts (relief valve, diverter, hose, seal and vent) are not candidates for savings.

## Decided under Amish's standing instruction of 2026-10-23

Amish's standing instruction of 2026-10-23: when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it here; a fix that changes the working principle, pitch or scope goes to him instead. He can reverse any of these.

| # | Date | Decision | Options weighed | Cost | Record |
| --- | --- | --- | --- | --- | --- |
| S1 | 2026-10-24 | Gas-pass baffles: one 1.5 mm 304 stainless baffle between the two evaporator bank layers on split spacers, two 1 mm 316L baffles between the economizer layers on flat-bar ledges (25 mm under the lower, 10 mm under the upper; 316L after the independent review, for the acid condensate); the firebox roof opening, the bank box outlet and the economizer inlet moved to the -Y side, the economizer outlet and the chimney to the +Y side. Closes STEM S6 and S7: the assumed coefficients of 30 and 25 W/(m2 K) were about 12 at the real gas velocity (59.8 % efficiency); with the baffles, fouling and 10 % edge bypass 22.4 and 21.5 W/(m2 K) and 66.1 % | (a) baffles (chosen); (b) longer bank (breaks R7); (c) smaller-bore bank (breaks R6); (d) thicker linings (about 15 kg) | About USD 50 (estimate, not checked live) and 7.4 kg | STR-STM-001 S6, S7, C5; STR-DDR-004, Part 2; STR-CAL-001 v0.5 section 4 |
| S3 | 2026-10-25 | Chimney outlet raised from 2.4 to 3.2 m above ground (a 1.2 m flue section on the economizer lid; its stability in wind is not yet checked). Closes STEM S12: with the fuel bed counted (about 3 Pa), the 2.4 m outlet left 0.1 Pa for the dampers; at 3.2 m the draft is 16.8 Pa and 5.4 Pa is left, enough for λ = 1.5 with about 40 % spare opening | (a) taller chimney (chosen); (b) larger damper openings (no help without draft); (c) an induced-draft fan (needs power, changes the 12 V budget); (d) fewer baffle passes (loses S1) | About USD 60 (estimate, not checked live) and 2.5 kg | STR-STM-001 S12; STR-CAL-001 v0.5 section 4 |
| S4 | 2026-10-25 | Latching pump trip: the coil outlet alarm drives a latching relay that cuts the feed pump until it is reset by hand, so a pump that stalls and recovers cannot refeed a hot, dry coil unattended. Closes STEM E2 | (a) latching relay (chosen); (b) alarm only, as before (fails E2); (c) a timed lockout (still restarts by itself) | About USD 10 (estimate, not checked live) | STR-STM-001 E2; BOM line 16 |

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
| 2026-10-03 | Cost overrun accepted: the estimated cost of USD 2,600 against the USD 2,200 target (USD 400 over) | Amish: "Cost over target - i accept all the cost variations and overruns" | [REVIEW.md](REVIEW.md), session 2026-10-03 |

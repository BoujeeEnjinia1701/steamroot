---
doc_id: STR-DDR-003
title: SteamRoot design for construction
project: SteamRoot
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-02 (Tables 1 to 3); seal pot overflow accepted but not yet modelled; record stays Draft"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "A1 and A2 carried into the model: firebox reshaped to 960 mm inside the evaporator bank study; seal pot overflow with a 350 mm loop seal modelled and checked (STR-CAL-001 v0.4)"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. The changes in Tables 1 and 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 to A3), recorded in the design decisions register (STR-DEC-001, items 5 to 7 and 10). The seal pot overflow (A2) was added to the model on 2026-10-02 with a 350 mm loop seal; with the overflow the seal limit is 0.084 bar (STR-CAL-001 v0.4). For A1, the evaporator bank study reshaped the firebox to 960 mm with one coil turn fewer. The record stays Draft.

> **Safety:** Changes C6, C8 and C9 touch the open vent, the water seal and the relief valve. Each keeps the safety case of STR-PRC-001 as it stands (an open vent that cannot be isolated, a 0.094 bar seal limit, a certified 15 psi relief valve rated 170 kg/h); none changes it. The written ruling from the local boiler authority (the Texas Department of Licensing and Regulation's boiler program, decided 2026-10-02) is still an open prerequisite for any build, and its ruling overrides this record if it is stricter.

## Context

On 2026-09-30 Amish asked for a build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model (STR-DDR-002) was a massing model: it showed what SteamRoot does, but checking it with build123d found parts that overlap, float, have no fixing or cannot be put together in any order. A pairwise overlap check of the concept model found six clashes (the seal pot through the deck, the coil through the firebox lining and walls, the coil outlet into the header, the hose through the deck edge and into the hood, the relief valve into the header), and a review of each joint found the rest.

The changes keep what SteamRoot does: an open-vented, wood-fired monotube coil making 30 kg/h of steam at about 0.03 bar, an economizer, a 1 m water seal, a certified relief valve, one hose and two hoods on a towed trailer. Every change is in `cad/src/model.py`, which now runs 93 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch without overlapping, parts that must not touch are apart by at least the stated clearance, and the coil can be lowered into the firebox and slid into place. All 93 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| C1 | The coil filled the firebox from 90 mm above the floor to the roof (its top turn cut 11 mm into the roof lining), so there was nowhere to put the wood: the door covered a closed wall and opened onto the coil, and the grate (60 mm up) sat across the air damper. | Firebox 1000 mm tall (was 650), same 700 x 600 mm footprint. The coil keeps its 11 turns, 420 mm diameter and 40 mm pitch but sits above the fire: its lowest turn is 400 mm above the floor board. Below it, a 300 x 240 mm door opening, a 300 x 300 mm cast grate on a stand 100 mm up (the ash pit), and a 160 x 60 mm air inlet under the grate with a slide damper. 280 mm of fire space between the grate and the coil. | The coil cannot surround a fire that has to be fed by hand through a door. A coil above the fire bed is the usual layout for a wood-fired coil, and keeps the coil length, water volume and pressure drop. |
| C2 | The coil floated in the firebox with no support. | Three brackets of 40 x 40 x 5 mm stainless angle, welded to the shell at the back wall and both ends, pass through slots in the lining; the lowest turn rests on them. | The coil grows about 3 mm when hot; resting on three brackets lets it move. Stainless survives the fire. |
| C3 | The coil could not be put into a welded box, its two tails passed through the wall with no holes, and outside the wall the inlet riser ran through the outlet pipe. | The roof is a separate 3 mm plate, lined with 50 mm board, bolted with 14 M8 bolts to a 25 x 25 mm angle frame round the top of the walls. The coil goes in from the top: held 66 mm toward the back and 30 mm high, then slid forward so its tails pass out through two 40 x 70 mm slots in the end wall, then set down. The tails stop 10 mm outside the wall; gland plates with ceramic rope packing close the slots and let the tubes slide. Unions join the upper tail to a separate outlet pipe to the header, and the lower tail through a reducer to the inlet jumper, which runs up 175 mm in front of the centre line so nothing crosses. | A bolted roof also lets the coil be inspected and replaced. Sliding glands let the coil grow without stressing the wall. Unions keep every joint outside the fire. |
| C4 | The coil inlet ended in mid-air beside the economizer, which was a solid box with no tubes, no fixing and no flue path to the chimney. | The economizer is a 2 mm steel box with a 6 mm base flange on 12 studs welded to the roof, a bolted lid carrying the chimney spigot, and a serpentine of 12.7 mm stainless tube inside (three layers, about 7.3 m bent on a standard 38 mm radius, water in at the top and out at the bottom, so the gas meets colder tube as it rises) resting on two support bars. Bulkhead unions take the tube ends through the end walls. | Counterflow, and 0.29 m² of tube against the 0.22 m² the calculation needs. The lid comes off to clean soot off the tubes. |
| C5 | The firebox stood on the deck with no fixing, and its hot floor sat directly on the deck. | Two skids of 50 x 50 x 3 mm square tube run across the deck, welded under the firebox floor; each end is bolted through the deck into the trailer's side rail with one M12 bolt. | Bolting into the side rails puts the load where a used trailer is strong. The 50 mm air gap keeps the deck cool. |
| C6 | The seal pot reached 50 mm below the deck. Also, as drawn, a 1 m dip leg would have let the header rise to about 0.11 bar, not 0.094 bar, because the water the steam pushes out of the dip leg raises the level outside it, and that water would have overflowed into the vent. | The pot stands on a 10 mm foot plate on the deck. The dip leg ends 890 mm below the static water mark; the 110 mm the outside level rises adds the rest, so the seal still blows at 1.0 m of water, 0.094 bar. The pot top is raised so the highest water level stays 100 mm below it. The header drops from 1600 to 1550 mm to suit. | Keeps the stated seal limit exactly and keeps water out of the vent. |
| C7 | The header was held up only by the coil outlet tube. | A 50 mm square post on a bolted foot plate carries the header on a saddle under two U-bolts; a flat-bar stay holds the seal pot to the post. | The coil tube is not a structure, and it moves when hot. |
| C8 | The diverter had no path to the vent, so its vent position went nowhere. | The diverter moves to the back end of the header; a 1 in vent line runs from its vent port up and over the header into the vent pipe, 110 mm above the pot top. | Steam sent to the vent goes straight up the existing vent pipe, above head height, and nothing can close it. |
| C9 | The relief valve sat 3 mm into the header and discharged at the header with no pipe. | The valve stands on a 3/4 in socket on top of the header; a 3/4 in discharge pipe runs from its outlet up to 2.3 m, open at the top with a drain hole at the low point, tied to the vent pipe by a round-bar stay. | A safety valve must discharge somewhere safe; this matches the open vent's 2.3 m outlet. Set pressure and capacity are unchanged. |
| C10 | The hose ran through the deck edge and 20 cm³ into the hood top. | The hose runs from a coupling on the diverter, clear of the trailer, down to a coupling on top of the hood. | The hose must connect, not pass through things. |
| C11 | The hood inlet stub did not reach the manifold, the manifold floated, and the skirt butted the hood's bottom edge with nothing joining them. | A riser pipe tees into the manifold, passes up through the hood and carries a flange and the hose coupling on top; two straps hang the manifold from the inner skin. The skirt is a 100 mm band riveted round the outside of the hood, lapping it by 40 mm, with 60 mm below. | Every joint is now riveted, welded or bolted. The 60 mm skirt depth is unchanged. |
| C12 | The feed drum's cradle was a solid block that cut through the drum, and there were no feed lines. | Two hardwood saddles with a curved top, bolted to the deck, and two ratchet straps hold the drum. A suction hose runs from the drum outlet to the pump; a 12.7 mm stainless feed line runs from the pump up the back end of the firebox in two clips to the economizer inlet. | A drum must be held down for towing; the water has to get from the drum to the coil. |
| C13 | The pump stood alone; the battery and alarms were not drawn. | One pump and alarm box on the deck holds the pump, the 12 V battery and the alarm controller, wired as the build plan shows. | Keeps the 12 V parts together, dry and away from the fire. |
| C14 | The door was a plate on a closed wall, with no hinges or latch; the damper was a block. | A 3 mm door with a 46 mm fibre board plug, two lift-off hinges and a turn latch; a 3 mm slide damper in two guides. | Buildable from sheet and bought hardware. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Efficiency and wood use | Fuel-to-steam efficiency 51.4 % (was 53.5 %); wood 10.5 kg/h (was 10.1 kg/h) and 5.6 kg/m² at 15 cm (was 5.4 kg/m²). R4 and R5 stay not met; their gaps widen by about 2 points. | The taller firebox has 36 % more wall, so it loses 3.5 kW through the lining instead of 2.6 kW. The coil itself is unchanged. See A1. |
| Pressure | Coil inlet 0.108 bar (was 0.110 bar); header 0.033 bar and seal limit 0.094 bar unchanged. | Shorter outlet riser to the lower header. |
| Mass | Towed with the drum and seal drained 468 kg (was 402 kg), full 602 kg (was 536 kg); R11 mass still met, 32 kg under 500 kg. Width unchanged at 1.48 m. | Firebox 125 kg (was 98 kg); 41 kg of skids, post, brackets, stand, glands, lines and frames added. |
| Cost | BOM lines 5 and 6 repriced and lines 17 to 21 added: USD 2,275 (was USD 1,915), USD 75 over the USD 2,200 value-engineering target. | Parts added for construction. |
| Drawings | STR-DWG-002 Rev P3; making sketches STR-DWG-101 to 121 added. | Follows the model. |
| Documents | STR-CAL-001 v0.3, STR-REQ-001 v0.5 and STR-PRC-001 v0.5 updated for the figures above. No requirement changed status. | Follows the model. |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The taller firebox costs about 2 points of efficiency. | (a) accept for the first prototype; (b) 75 mm lining with the box made 50 mm larger each way, which brings efficiency back to about 53.8 % for about 8 kg more; (c) fold the firebox shape into the R5 evaporator bank study (STR-DDR-002, item 1), which reshapes the flue anyway. | (c), keeping (a) for now. Accepted 2026-10-02. |
| A2 | The seal pot level rises as steam condenses in it and falls as it boils off; an overfilled pot raises the seal limit. | (a) an overflow pipe at the static water mark, draining to the ground; (b) a level mark and top-up by hand only, as now. | (a): it fixes the seal depth so it cannot be overfilled. It is a change to the safety case, so it is proposed, not made. Accepted 2026-10-02: the overflow is piped down to ground level at the back of the trailer, away from the operator's side. It is to be added to the model and build plan (follow-up). |
| A3 | The relief valve discharge now goes up to 2.3 m. | (a) keep it, as modelled; (b) discharge down to the ground at the front of the trailer. | (a), subject to the boiler authority's ruling. Accepted 2026-10-02, subject to the authority's ruling. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan STR-BLD-001 (`docs/05-build-plan.md`) shows every component and step in pictures drawn from the model (`cad/src/build_plan_media.py`). Decisions are recorded in the design decisions register, STR-DEC-001 (`docs/06-design-decisions.md`), which accepted this record on 2026-10-02.
- Requirement status is unchanged in kind: 2 not met (R4, R5), 3 at risk (R2 twice, R11 width), 1 not verifiable at TRL 3 (R1), 8 met; R12 is reported against the value-engineering target, USD 75 over (STR-CAL-001 v0.3).
- The appearance model `cad/src/product_model.py` was brought into line with the constructable design on 2026-10-02 and its render scenes exported. The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` are rendered from those scenes on Amish's Mac, where Blender is.
- The trailer is bought used. Its side rails must be checked for the skid bolts when it is chosen; the drawings assume 80 mm rails.

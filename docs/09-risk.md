---
doc_id: STR-RSK-001
title: SteamRoot risk register and hazard analysis
project: SteamRoot
doc_type: Risk register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade): project risks, preliminary hazard analysis and first-pass design FMEA, from the safety sections of STR-PRC-001 and STR-BLD-001, STR-STM-001 and STR-CAL-001 v0.5"
---

# SteamRoot risk register and hazard analysis

The top project risk is regulatory: if the Texas boiler authority does not accept the open-vented design under the atmospheric-pressure exemption, SteamRoot cannot be built as conceived (R1). The top hazards are steam burns at the hood and hose (H1, H2), a refeed into a hot, dry coil (H3) and carbon monoxide (H5); the highest design FMEA risk numbers are the feed pump stopping unnoticed (F1), the water seal frozen or dry (F3) and a hood skirt leaking steam in fine soil (F8). Method: STANDARDS section 23. Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high; for detection, 5 means hard to detect).

> **Safety:** This register supports the safety sections of STR-PRC-001 and the safety stops of STR-BLD-001; it does not replace them. SteamRoot is a concept on paper; nothing may be built or fired before the written ruling from the boiler authority.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | The authority rules that SteamRoot is a regulated boiler | Texas Health and Safety Code 755.022(a)(4) read strictly: a 0.084 bar seal or a 1.03 bar relief valve not accepted as "atmospheric" or as two independent means | No build as designed; a code boiler would change the pitch | 3 | 5 | Project lead (Amish) | Ask for the written ruling first (decided 2026-10-02); present the seal, the relief valve and PR-017; adopt anything stricter it requires |
| P2 | Real beds pass steam too slowly under a light hood | Soil permeability far below sand; skirt leakage | PR-001 and PR-002 missed; burns at the skirt | 4 | 4 | Design lead with the co-design partners | Bed preparation note (DEC #18); TRL 4 soil tests choose ballast, skirt depth or steam rate (decided 2026-10-02) |
| P3 | Efficiency below 65 % in use | 66.1 % on paper with a 1.1-point margin; dampers left open; baffles left out; firebox exchange or unburned loss worse than modelled (S5, CAL Table 6a) | PR-005 and PR-004 missed; more wood per m2 | 4 | 3 | Design lead | Baffles in the build plan; damper settings and a flue oxygen reading at TRL 4; PR-004 restatement proposed (DEC #12) |
| P4 | Towed mass over 500 kg | 509 kg with both hoods after the baffles and the taller chimney | PR-011 not met | 5 | 2 | Design lead | Count PR-011 without the hoods, as towed (DEC #13); mass savings listed in DEC |
| P5 | No co-design partner found | Partners not yet named | Targets not reviewed by users; no site for TRL 4 | 2 | 3 | Project lead | Texas A&M AgriLife Extension route (decided 2026-10-02) |
| P6 | Cost above what small farms pay | USD 2,720 against the USD 2,200 target | Fewer builds | 3 | 2 | Project lead | Savings list in DEC; overrun to USD 2,600 accepted 2026-10-03, USD 120 of STEM fixes reported |
| P7 | Concept choice reopens the design | A and B within 10 % (STR-OPT-001) | Rework if B is chosen | 2 | 3 | Project lead (Amish) | Decision #14; B's best idea (feed-loss detection) offered to A either way |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Steam escaping at the hood skirt | Soil resists steam flow more than the hood's weight holds (STEM S11 fails) | Deep burns to feet and hands | 4 | 4 | Keep clear of the skirt; boots and gloves; bed preparation; hold-down, skirt or flux from TRL 4 tests (DEC #18) | Medium |
| H2 | Steam at the hose coupling or a lifted hood | Hose moved or hood lifted with steam on | Deep burns | 4 | 3 | Divert to the vent first (PR-010); steam-rated hose with whip checks; diverter with no closed position | Medium |
| H3 | Refeed into a hot, dry coil | Pump stops or tank runs dry with the fire burning; feed restarted | Steam and scalding water thrown from joints and the vent at 4.7 times the design flow or more (flash basis open, DEC #20) | 5 | 2 | Coil outlet and tank level alarms; latching pump trip with a manual reset (DEC S4); never refeed a hot dry coil; relief valve sized for the flash (PR-009) | Medium |
| H4 | Pressure build-up | Vent blocked, seal pot frozen or overfilled, a valve fitted between coil and vent | Rupture of a joint or the hose | 5 | 1 | Open vent that cannot be isolated (PR-006); overflow at the water mark; drain and frost check (decided 2026-10-02); certified relief valve | Low |
| H5 | Carbon monoxide | Incomplete wood combustion, more so at low excess air | Poisoning, death in enclosed spaces | 5 | 2 | Firebox and chimney outdoors only; personal CO alarm; tend the fire upwind | Low |
| H6 | Fire and sparks | Embers from the chimney or door; dry vegetation; burn bans | Wildfire, property damage | 4 | 2 | 6 mm spark arrestor; bare ground or gravel; extinguisher; check burn bans (REG R5) | Low |
| H7 | Hot surfaces | Firebox skin about 100 °C, about 135 °C near the fire bed (STEM S8), flue and chimney hotter, header and pot | Contact burns | 3 | 3 | Guarding by distance; gloves; hood handles stay cool (23 °C skin); skin limit and door-side guard proposed (DEC #21) | Medium |
| H8 | Manual handling of the hoods | 31.3 kg hood, handles 1.12 m apart (STEM B4 fails) | Back and shoulder injury | 3 | 4 | Wheel kit or lifting aid recommended, two-person lift as an interim (DEC S2); ballast lifted off first | Medium until decided |
| H9 | Soil biology harm | Soil behind the front at 100 °C | Loss of beneficial organisms; manganese and ammonium release | 2 | 4 | Do not over-steam; hold time 20 to 30 min; aerated steam as a future option (REVIEW) | Medium |
| H10 | Towing instability or overload | Towing with water aboard (643 kg) or hoods aboard | Loss of control | 4 | 2 | Tow drained, hoods on a second vehicle (decided 2026-10-02); axle rated for the full mass | Low |
| H11 | Fibre dust | Cutting and handling ceramic fibre lining | Respiratory irritation | 2 | 3 | Mask and gloves in the build plan safety stops | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Feed pump (BOM 4) | Meter 0.5 L/min into the economizer | Stops or loses prime | Coil runs dry (H3) | Battery flat (E3), air leak, blocked strainer | 5 | 3 | 3 | 45 | Coil outlet and tank alarms with a latching pump trip (DEC S4); add a feed flow switch (B's best idea, REVIEW); size the battery (DEC #16) |
| F2 | Monotube coil (BOM 6) | Boil 30 kg/h with 5 L of water | Scale blocks the bore or a weld leaks | Higher inlet pressure, hot spots, steam leak | Hard water; dry-out at the top of the helix | 4 | 2 | 3 | 24 | Rain or softened water; descale; pressure test before use (BLD safety stops) |
| F3 | Water-seal pot (BOM 9) | Limit pressure to 0.084 bar | Frozen, overfilled or dry | Raised relief pressure, or no seal (steam out the vent) | Frost; not refilled after a blow | 5 | 2 | 4 | 40 | Overflow at the mark; drain daily and in frost; pre-start check (decided 2026-10-02) |
| F4 | Relief valve (BOM 10) | Second line of protection | Stuck shut | No second protection if the seal fails | Corrosion, scale, never tested | 5 | 1 | 4 | 20 | Lever test as the maker directs; never plug or adjust |
| F5 | Gas-pass baffles (BOM 7, 22) | Make the gas cross the tubes | Missing, warped, misplaced or corroded | Efficiency falls to about 60 % (PR-005) | Left out at assembly; warping in the hot gas; acid condensate in the economizer | 3 | 2 | 3 | 18 | Build plan steps and sketches 127 and 128; 304 in the bank, 316L in the economizer; inspect when the lid is off |
| F6 | Air dampers (BOM 5) | Hold λ near 1.5 | Left open or jammed | Efficiency about 65 % at the λ = 1.6 the draft allows; more wood | Operator habit; distortion | 3 | 3 | 3 | 27 | Marked damper settings; flue oxygen check at TRL 4 |
| F7 | Diverter (BOM 9) | Send steam to hose or vent, never neither | A closed middle position | Coil isolated from the vent (H4) | Wrong valve bought | 5 | 1 | 2 | 10 | Confirm no closed position when bought (DEC to-confirm 3) |
| F8 | Hood and skirt (BOM 12) | Hold steam on the soil | Steam escapes under the skirt | Burns (H1); slow front; PR-001 missed | Fine soil, uneven bed, hood too light | 4 | 4 | 2 | 32 | Bed preparation (DEC #18); ballast and skirt depth from TRL 4 tests |
| F9 | Steam hose (BOM 11) | Carry steam 6 m to the hood | Burst or coupling leak | Burns (H2) | Hot-water hose bought instead of steam hose; wear | 5 | 1 | 2 | 10 | Steam-rated hose with whip checks; inspect before each use |
| F10 | Fibre lining (BOM 5) | Keep the shell near 100 °C | Cracked or fallen blanket | Hot spots on the shell; burns | Loading damage, vibration in towing | 3 | 3 | 3 | 27 | Pins and washers; inspect before lighting |
| F11 | Battery (BOM 13) | Run the pump and alarms | Runs flat in a session | Pump stops (F1); alarms dead | Undersized for the pump chosen (E3) | 4 | 3 | 3 | 36 | Size from the pump datasheet (DEC #16); charge between fills |

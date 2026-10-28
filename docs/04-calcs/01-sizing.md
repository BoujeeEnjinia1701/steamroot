---
doc_id: STR-CAL-001
title: SteamRoot sizing calculations
project: SteamRoot
doc_type: Calculation note
version: "0.5"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing calculations with script, assumptions and requirement status
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Rerun for the constructable design (STR-DDR-003): taller firebox, seal pot dip leg, tube bank, added parts; cost reported against the value-engineering target"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved 2026-10-02 decisions carried in: evaporator bank sized with primary and secondary air dampers inside 8 L (forward model of firebox, bank and economizer), firebox reshaped to 960 mm with 10 coil turns, seal pot overflow and loop seal checked, hood handles sized for ballast; R4 restatement proposed"
- version: "0.5"
  date: '2026-10-25'
  author: Amish Chadha
  change: "STEM check S6 and S7 (kit 1.9.1 upgrade): the assumed bank and economizer coefficients (30 and 25 W/(m2 K)) replaced by a tube-bank correlation at the gas velocity, which gives about 12 without baffles; gas-pass baffles added (STR-DEC-001 S1), 25.4 and 23.8 W/(m2 K) before the review; gas-side losses added to the draft check; requirement numbers moved to STR-PRS-001 IDs. After the independent review (2026-10-25): row factor per pass, gas emissivity 0.06, fouling and 10 % baffle bypass (bank 22.4, economizer 21.5 W/(m2 K)); fuel bed loss in the draft and the chimney outlet raised to 3.2 m (STR-DEC-001 S3); whole-coil two-phase friction and bank bend losses; economizer baffles 316L; one-at-a-time sensitivities (Table 6a); efficiency 66.1 %"
---

# SteamRoot sizing calculations

The decided configuration (open-vented stainless monotube coil, evaporator bank, economizer, two hoods, fixed-rate feed) makes 30 kg/h of steam at near-atmospheric pressure with little stored water. Version 0.4 carried in Amish's decisions of 2026-10-02 (evaporator bank, secondary air slide, 10 coil turns, 960 mm firebox). Version 0.5 corrects the gas side of the bank and economizer. Version 0.4 had assumed coefficients of 30 and 25 W/(m² K); the STEM check (STR-STM-001, S6 and S7) found that the flue gas rises through those boxes at about 0.1 m/s, where a tube-bank correlation gives about 12 W/(m² K) and the design would make only 60 % efficiency. Gas-pass baffles, fitted on 2026-10-24 under Amish's standing instruction of 2026-10-23 (STR-DEC-001 S1), make the gas cross the tubes at about 1 m/s and give 22.4 and 21.5 W/(m² K) after an allowance for fouling and for gas slipping round the baffle edges. With the dampers holding the excess air near λ = 1.5, fuel-to-steam efficiency is 66.1 % (PR-005 at risk, 65 % target, a margin smaller than several of the uncertainties in Table 6a) and wood use 4.36 kg/m² at 15 cm (PR-004 not met; the proposed restatement to 4.5 covers it). Once the fuel bed is counted the draft needed a taller chimney: the outlet is raised from 2.4 to 3.2 m (STR-DEC-001 S3), and with the dampers wide open the excess air reaches only about λ = 1.6. The heated section holds 7.3 L (PR-007 met). The seal pot overflow fixes the seal limit at 0.084 bar. The towed mass is 509 kg with both hoods (PR-011 not met). These are paper estimates; nothing here has been tested. Requirement IDs are those of STR-PRS-001, with the old R numbers in brackets.

> **Safety:** This note sizes a fired steam generator. It is a paper calculation, not a design approval. A written ruling from the local boiler authority (the Texas Department of Licensing and Regulation's boiler program, decided 2026-10-02) on whether an open-vented, fired monotube coil is exempt from boiler and pressure vessel rules is an **open prerequisite**. It has not been obtained. No part of this note may be used to build or operate the machine until that ruling exists and the design has been reviewed against it.

All numbers below are printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root). The script reads geometry from `cad/src/model.py` (`PARAMS`, `derived()` and the bank length), and prices from `bom/bom.csv`, so the model, the BOM and this note share one source.

## 1. Method and assumptions

The calculation has six parts: soil heat and steam demand, treatment rate, combustion and heat transfer, steam-side pressure, stored energy and relief, and mass and cost. Every assumption is listed in the `A` dictionary at the top of the script. The main ones are in Table 1.

*Table 1. Main assumptions.*

| Quantity | Value | Basis or range |
| --- | --- | --- |
| Design steam output | 30 kg/h saturated at about 1.01 bar | R3 target |
| Feed water | 15 °C; economizer outlet capped at 85 °C | Outlet held at least 15 K below boiling |
| Soil | 1,300 kg/m³ dry bulk density, 20 % water (dry basis), 15 °C start | As STR-REQ-001 |
| Specific heats | Soil 0.84, water 4.18 kJ/(kg K) | Handbook values |
| Soil conductivity | 1.2 W/(m K), giving 0.55 mm²/s diffusivity | Moist loam; range 0.8 to 1.6 |
| Soil permeability | 10⁻¹⁰, 10⁻¹¹, 10⁻¹² m² | Sand, sandy loam, loam (textbook ranges, not measured) |
| Hold at 70 °C | 25 min | R1 allows 20 to 30 min |
| Steam lost under the skirt | 10 % | Assumed; range 5 to 25 % |
| Hood | 1 mm aluminum double skin, 40 mm mineral wool, steel handles | As BOM item 12 |
| Wood | Dry C 50 %, H 6 %, O 43.3 %, N 0.2 %, ash 0.5 %; 20 % moisture (wet basis) | Typical hardwood analysis |
| Excess air ratio λ | 1.5 with the primary and secondary dampers set; about 1.6 at most with them wide open (draft limited) | Hand-fed batch firebox; λ 2.0 and 2.5 kept as sensitivities |
| Unburned loss | 4 % of fuel energy | CO and char; 6 % and 8 % in Table 6a |
| Coil radiative exchange factor F | 0.40 per unit tube area | Range 0.25 to 0.6 |
| Gas to coil convection | 20 W/(m² K) | Low-velocity cross flow; the correlation at the mean firebox velocity gives about 9, so 10 is in Table 6a |
| Bank and economizer gas side | Zukauskas in-line tube-bank correlation at the velocity through each gas pass, row correction per pass, plus gas radiation (emissivity 0.06 in the bank, 0.05 in the economizer); fouling 0.003 m² K/W; 10 % of the gas bypasses the baffle edges | v0.5 (STEM S6, S7) and the independent review; v0.4 assumed 30 and 25 W/(m² K) |
| Firebox and bank box linings | 50 mm and 25 mm ceramic fiber, 0.12 W/(m K) | As BOM items 5 and 22 |
| Trailer tare | 160 kg | Used 2.0 x 1.2 m trailer; range 130 to 250 kg |
| Relief valve rated capacity | 375 lb/h (170 kg/h) | Watts Series 315, 3/4 in, 15 psi set, maker's capacity table |
| Ballast per hood | 40 kg, load factor 2 on the handles | Sizing value only; the ballast itself is set by TRL 4 soil tests |

## 2. Soil heat and steam demand

**Model.** Steam condenses at a sharp front that moves down through the soil. Soil above the front sits at the steam temperature, 100 °C, and soil below it stays cold. When the hose moves to the other hood, the hot layer begins to lose heat to the cold soil below. For two semi-infinite regions at 100 °C and 15 °C the interface drops at once to 57.5 °C, so the front must go deeper than the working depth. Keeping 70 °C at 15 cm through a 25-minute hold needs an overshoot of 2 √(αt) erf⁻¹(0.294) = 1.53 cm, so the front must reach 16.5 cm.

**Energy.** The soil's volumetric heat capacity is 1,300 x (0.84 + 0.20 x 4.18) = 2,179 kJ/(m³ K). Heating 16.5 cm by 85 K takes 30.6 MJ/m². Condensate stays in the soil at 100 °C, so each kilogram of steam gives its latent heat, 2.257 MJ. Hood losses add 1.00 MJ/m² (wall loss of 178 W through U = 0.91 W/(m² K), and 0.80 MJ of stored heat per setting), and 10 % of the steam escapes under the skirt.

*Table 2. Steam demand per square meter.*

| Case | Soil heat | Steam | Hood efficiency | Heat time per 1.2 m² setting |
| --- | --- | --- | --- | --- |
| TRL 2 model (uniform 75 °C, 60 % hood) | 19.6 MJ/m² | 13.8 kg/m² | 60 % (assumed) | Not used |
| 15 cm working depth | 30.6 MJ/m² | 15.6 kg/m² | 87 % | 37.4 min |
| 5 cm working depth | 12.1 MJ/m² | 6.4 kg/m² | 84 % | 15.2 min |

**Soil permeability and ballast.** At full flow the steam passes down through the hot layer at 1.16 cm/s. By Darcy's law that takes 236 Pa through 16.5 cm of sand (10⁻¹⁰ m²), 2,362 Pa through a sandy loam (10⁻¹¹ m²) and 23,617 Pa through a loam (10⁻¹² m²). The hood now weighs 31.3 kg with its steel handles, so it lifts at 256 Pa. In anything finer than sand the steam will not push through at full flow: it will escape under the skirt, or the front will slow and the heat time will grow. Amish decided on 2026-10-02 that ballast, skirt depth or steam rate is chosen from TRL 4 soil tests, with skirt leakage measured at the hood edge, and that the handles are sized now to carry ballast. With 40 kg of ballast a hood lifts at 583 Pa, which raises the header to 0.036 bar (section 5). That still leaves loams far beyond what ballast alone can hold; the steam will find the skirt edge first, which is a burn hazard.

## 3. Treatment rate

Each setting needs the heat time above plus a 25-minute hold and 2 minutes to lift and reset the hood. With two hoods the hose moves between them after steam is diverted to the vent, which wastes about 1 minute of steam per setting. The rate is the lower of the steam limit, 1.2 m² / (heat time + 1 min), and the hood limit, (number of hoods x 1.2 m²) / (heat time + hold + move).

*Table 3. Treatment rate, m²/h.*

| Hoods | 15 cm | 5 cm |
| --- | --- | --- |
| 1 | 1.12 (hood limited) | 1.70 (hood limited) |
| 2 (decided; R2 restated to these values) | 1.88 (steam limited) | 3.41 (hood limited) |
| 3 | 1.88 (steam limited) | 4.43 (steam limited) |

R2 was restated by Amish on 2026-09-25 to the two-hood values, about 1.9 m²/h (1.85 or more) at 15 cm and 3.4 m²/h at 5 cm. Both are met with margins under 2 %, so they are marked at risk. The evaporator bank changes the wood burned, not the steam made, so these rates are unchanged.

## 4. Combustion, heat transfer and efficiency

**Fuel.** The Channiwala and Parikh correlation gives a dry higher heating value of 20.03 MJ/kg for the assumed analysis, a dry lower heating value of 18.72 MJ/kg, and 14.48 MJ/kg at 20 % moisture. Stoichiometric air is 4.76 kg per kilogram of wet fuel, so at λ = 1.5 there are 8.1 kg of flue gas per kilogram of wood (10.5 kg at λ = 2.0).

**Duty.** Raising 30 kg/h of water from 15 °C to dry saturated steam takes 21.78 kW.

**Model.** The design is run forward. The firebox is one well-stirred zone: heat to the coil is σ F A (T_g⁴ - T_w⁴) + h A (T_g - T_w) with 13.20 m of tube (1.05 m²) and a 110 °C wall, and the lining loses heat to the outside. The gas then crosses the evaporator bank, treated as a counterflow exchanger with water boiling at 100 °C inside, loses a little heat through the bank box walls, and crosses the economizer, a counterflow exchanger whose water outlet is capped at 85 °C. The firing rate is found so that the coil and the bank together boil exactly the feed the economizer delivers.

**Gas side of the bank and economizer (new in version 0.5).** Version 0.4 assumed the bank and economizer coefficients. Version 0.5 calculates them at the gas velocity through the minimum free area of each gas pass, with the Zukauskas correlation for in-line tube banks (Nu = C₂ C Re^m Pr^0.36, C and m = 0.80 and 0.40 for Re 10 to 100, 0.51 and 0.50 for Re 100 to 1,000, C₂ the row correction for the rows of each pass, as the independent review asked), flue gas properties for a mixture of 28.5 kg/kmol at the mean gas temperature of each exchanger, plus non-luminous gas radiation at an emissivity of 0.06 in the bank and 0.05 in the economizer (about 0.015 atm m each of water vapour and carbon dioxide; ±50 %). A soot and tar fouling resistance of 0.003 m² K/W is added, and 10 % of the gas is taken to slip round the baffle edges without crossing the tubes. Without baffles the gas rises through the full width of each box: 0.30 m² of free area in the bank and 0.20 m² in the economizer, about 0.1 m/s, Reynolds numbers near 20, and coefficients of 10.3 and 12.0 W/(m² K). The design would then make 59.8 % (52.0 % at λ = 2.0), and R5 would fail (STEM check S6 and S7).

Amish's standing instruction of 2026-10-23 asks for the best fix in the same session (STR-DEC-001 S1). The fix is a set of gas-pass baffles: a 1.5 mm 304 stainless plate between the two bank layers, open 73 mm at the +Y lining, and two 1 mm 316L stainless plates between the three economizer layers, open 58 mm at alternate sides (316L because the economizer runs wet with acid condensate, as the review pointed out). The firebox roof opening, the bank box outlet and the economizer inlet move to the -Y side and the economizer outlet and chimney to the +Y side, so the gas crosses each layer of tubes sideways. Table 4a gives the passes.

*Table 4a. Gas passes with the baffles (λ = 1.5).*

| Exchanger | Pass | Velocity | Reynolds number | Convective coefficient | Rows crossed |
| --- | --- | --- | --- | --- | --- |
| Bank | 1, under the baffle | 1.04 m/s | 241 | 21.2 W/(m² K) | 5 |
| Bank | 2, over the baffle | 1.12 m/s | 259 | 22.0 W/(m² K) | 5 |
| Bank | Gas radiation | | | 2.5 W/(m² K) | |
| Economizer | 1, bottom layer | 0.73 m/s | 183 | 20.0 W/(m² K) | 5 |
| Economizer | 2, middle layer | 0.99 m/s | 250 | 23.3 W/(m² K) | 6 |
| Economizer | 3, top layer | 0.85 m/s | 214 | 21.6 W/(m² K) | 6 |
| Economizer | Gas radiation | | | 1.2 W/(m² K) | |
| **Mean coefficients, clean** | | | | **Bank 24.0, economizer 23.0 W/(m² K)** | |
| **With fouling 0.003 m² K/W (design)** | | | | **Bank 22.4, economizer 21.5 W/(m² K)** | |

The baffles leave the water side untouched: the same 6.40 m of bank tube (0.319 m², 0.90 L), the same 7.3 m of economizer tube and the same 7.3 L of heated water.

**The study.** Version 0.4 sized the bank with primary and secondary dampers inside 8 L (decided 2026-10-02): 15.88 x 1.24 mm (5/8 x 0.049 in) 316 tube, two layers of five runs, 10 coil turns, a 960 mm firebox. Table 4 reruns that study with the gas-side coefficients calculated, and adds the baffles.

*Table 4. Bank, firebox and baffle study (F = 0.40).*

| Option | Efficiency | Wood | Wood at 15 cm | Firebox gas | Bank | Economizer | Stack | Water, flooded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v0.3 design: 11 turns, 1000 mm firebox, no bank, no baffles, λ = 2.0 | 49.8 % | 10.9 kg/h | 5.79 kg/m² | 526 °C | none | 1.99 kW | 471 °C | 6.93 L |
| v0.4 design as published (assumed 30 and 25 W/(m² K)), λ = 1.5 | 68.9 % | 7.9 kg/h | 4.18 kg/m² | 510 °C | 3.14 kW | 1.73 kW | 235 °C | 7.33 L |
| v0.4 design, coefficients calculated, no baffles, λ = 1.5 | 59.8 % | 9.1 kg/h | 4.82 kg/m² | 541 °C | 1.36 kW | 1.35 kW | 392 °C | 7.33 L |
| **Chosen (v0.5): v0.4 design with gas-pass baffles, λ = 1.5** | **66.1 %** | **8.2 kg/h** | **4.36 kg/m²** | **519 °C** | **2.51 kW** | **1.75 kW** | **284 °C** | **7.33 L** |
| Chosen at λ = 2.0 (a sensitivity: the dampers reach about 1.6) | 60.1 % | 9.0 kg/h | 4.80 kg/m² | 506 °C | 2.91 kW | 2.22 kW | 312 °C | 7.33 L |
| Chosen with baffles, 9 turns, 920 mm firebox, λ = 1.5 | 65.3 % | 8.3 kg/h | 4.42 kg/m² | 542 °C | 2.69 kW | 1.85 kW | 295 °C | 6.82 L |

Most of the gain over the v0.3 design still comes from air control; the baffles are what let the bank and economizer deliver what version 0.4 counted on. Ten turns remains the balance between efficiency and stored water.

*Table 5. Energy balance of the chosen design (λ = 1.5, F = 0.40).*

| Quantity | Value |
| --- | --- |
| Firing rate | 32.9 kW (8.2 kg/h of wood) |
| Heat to water: coil 17.53 kW, bank 2.51 kW, economizer 1.75 kW | 21.78 kW |
| Stack loss (flue gas leaves at 284 °C) | 5.7 kW |
| Shell loss through the firebox lining and the bank box walls | 4.1 kW |
| Unburned loss | 1.3 kW |
| Fuel to steam efficiency | 66.1 % |
| Firebox outer skin temperature (at the exit gas temperature; about 135 °C near the fire bed) | 99 °C |

The bank cools the gas from 519 °C to 366 °C. The economizer delivers 1.75 kW and the feed reaches the bank at about 65 °C; its 0.29 m² of tube is fully used.

*Table 6. Sensitivity of fuel-to-steam efficiency with the bank and baffles (%; without the bank in brackets).*

| λ | F = 0.25 | F = 0.40 | F = 0.60 |
| --- | --- | --- | --- |
| 1.5 | 63.8 (53.7) | 66.1 (58.8) | 68.3 (63.2) |
| 2.0 | 57.1 (43.2) | 60.1 (49.3) | 62.6 (54.6) |
| 2.5 | 48.6 (32.7) | 53.0 (39.7) | 56.8 (45.9) |

*Table 6a. One-at-a-time sensitivities at λ = 1.5, F = 0.40 (section H of the script; added after the independent review).*

| Case | Efficiency | Wood at 15 cm |
| --- | --- | --- |
| Design | 66.1 % | 4.36 kg/m² |
| Unburned loss 6 % | 64.3 % | 4.48 kg/m² |
| Unburned loss 8 % | 62.5 % | 4.61 kg/m² |
| Coil convection 10 W/(m² K) | 63.5 % | 4.54 kg/m² |
| λ = 1.6 (dampers wide open) | 64.9 % | 4.44 kg/m² |
| Wood at 30 % moisture | 65.3 % | 5.18 kg/m² |
| No fouling, no bypass | 66.9 % | 4.31 kg/m² |

PR-005 (R5, 65 %) is met at the design point with a margin of 1.1 points, and missed for F = 0.25, for an unburned loss of 6 % or more, for the lower coil convection the correlation gives, and with the dampers wide open. The margin is smaller than each of these uncertainties, so PR-005 is at risk; the reviewer put the likely value nearer 61 % (58 to 66 %). It must be measured at TRL 4 with a flue gas oxygen reading and fuel weighing.

**Dampers and draft.** Version 0.5 counts the gas-side losses: about 3.0 Pa through the grate and fuel bed (an Ergun estimate for a bed of 50 mm pieces, scaling with the flow squared; the independent review found this term missing), 3.39 Pa at the two 150 mm openings (1.5 velocity heads each at 2.39 m/s), 0.73 Pa in the baffled bank and 1.02 Pa in the baffled economizer (each tube row taking C_d d/s velocity heads at the channel velocity, C_d = 1.2, and 1.5 velocity heads per turn), and 3.30 Pa in the chimney and cap: 11.43 Pa in all. With the outlet 2.4 m above ground, the 1.70 m from the grate gave about 11.4 Pa of draft, which left nothing for the air openings (STEM S12). Raising the outlet to 3.2 m (STR-DEC-001 S3, a 1.2 m flue section) gives 2.50 m and 16.8 Pa with flue gas at a mean 400 °C, leaving 5.4 Pa across the air openings. At a discharge coefficient of 0.6 they must then total about 7,530 mm² at λ = 1.5. The primary inlet under the grate (160 x 60, 9,600 mm²) and the secondary slot in the door (150 x 20, 3,000 mm²) give 12,600 mm²: enough for λ = 1.5 with about 40 % to spare. Wide open they admit air for only about λ = 1.6, since more air raises the losses faster than the draft, so λ = 2.0 is now a sensitivity, not an operating case.

**Wood per square meter and PR-004 (R4).** With two hoods, 8.2 kg/h of wood treats 1.88 m²/h at 15 cm: 4.36 kg/m², 9 % over the 4 kg/m² target (4.44 kg/m² with the dampers wide open at λ = 1.6). At 5 cm it is 2.40 kg/m². PR-004 needs about 72 % efficiency at the current steam demand. Amish decided on 2026-10-02 to plan a restated R4. **Proposed, awaiting Amish (STR-DEC-001 #12):** restate PR-004 as 4.5 kg/m² or less at 15 cm with the dampers set, to be confirmed by fuel weighing at TRL 4. The options are (a) 4.5 kg/m², which the design meets with 3 % margin at λ = 1.5 and just meets with the dampers wide open, but not with 30 % moisture wood (Table 6a); (b) 5.0 kg/m², which also covers the λ = 2.0 sensitivity; (c) keep 4 kg/m² and look for the rest in lower steam demand (less skirt leakage). The recommendation is (a), since (b) would stop PR-004 from rewarding air control.

**Flue condensate.** At λ = 1.5 the flue gas holds 12.5 % water vapor by volume, so its dew point is about 51 °C. The cold end of the economizer, fed at 15 °C, runs wet with acidic condensate, which confirms the stainless tube, the stainless economizer baffles and the condensate drain.

## 5. Steam-side pressure

The coil bore is 22.1 mm. At 30 kg/h the mass flux is 21.7 kg/(m² s) and dry steam would move at 36.3 m/s (Reynolds number 39,033). The two-phase friction gradient comes from the Müller-Steinhagen and Heck correlation, averaged over a quality that rises linearly from the bank outlet quality to dry steam along the whole coil (the review found the boiling fraction of version 0.3 still in use), times a helical-coil factor of 1.26 (Ito).

The bank, upstream of the coil, has a 13.4 mm bore and a mass flux of 59.1 kg/(m² s). It heats the feed to boiling and takes it to a steam quality of about 0.07, with a drop of about 2,016 Pa including its 20 return bends at 0.3 velocity heads each. The fall from the bank down to the coil inlet adds head that is ignored here, which is conservative.

*Table 7. Pressure build-up at 30 kg/h.*

| Element | Pressure drop |
| --- | --- |
| Coil friction (two-phase mean 383 Pa/m, all-vapor 401 Pa/m) | 6,388 Pa |
| Coil acceleration | 789 Pa |
| Coil gravity | 17 Pa |
| Outlet riser to the header | 373 Pa |
| **Coil total** | **7,566 Pa** |
| Evaporator bank | 2,016 Pa |
| Hose, 6 m at 28.4 m/s, with fittings | 2,546 Pa |
| Hood manifold (assumed) | 500 Pa |
| Hood, at most its lift pressure | 256 Pa |
| **Header pressure** | **3,301 Pa (0.033 bar gauge)** |
| **Bank inlet pressure (the highest on the steam side)** | **12,883 Pa (0.129 bar gauge)** |

PR-006 and PR-013 (R6) are met: 0.033 bar at the header against 0.1 bar, and 0.129 bar at the inlet against 0.15 bar, a margin inside the ±30 % band of the correlations. With 40 kg of ballast on the hood in use the figures become 0.036 bar and 0.132 bar. The gas-pass baffles change only the gas side.

**Water seal and overflow.** When the header pressure pushes water down the dip leg, the same volume would rise in the annulus between the dip leg and the pot wall. With a 42.2 mm dip leg in a 114.3 mm pot the annulus area is 8.1 times the dip leg bore, so without an overflow the water outside would rise 110 mm while the water inside fell the full 890 mm to the dip leg end: 1.0 m of head, 9,402 Pa (0.094 bar). Amish decided on 2026-10-02 to fit an overflow at the static water mark. Its bore bottom is at the mark, so water pushed out of the dip leg spills away instead of rising round it, and the pot can never hold water above the mark. The seal therefore blows when the dip leg is pushed empty: 890 mm of head, 8,365 Pa (0.084 bar gauge). The overflow sets the seal depth so the pot cannot exceed the 0.094 bar limit, overfilled or not, and lowers the limit by the 110 mm rise. The margin over the 0.033 bar header pressure is 5,064 Pa. After a seal blow the pot holds less water than before; the seal is then shallower, which errs on the safe side, and the pre-start check in safety stop S4 refills it to the mark. In normal use the 0.033 bar header pressure pushes about 0.3 L of water out of the dip leg and over the overflow each time steam comes up. When the steam stops the level settles about 45 mm below the mark, so the pot is topped up to the mark before each start, as S4 already requires; steam condensing in the pot during a run partly makes this up.

**Overflow loop seal.** If the seal blows with the full dry-coil refeed flash (section 6), 141 kg/h of steam leaves the pot by the DN32 vent at about 68 m/s, which raises the pressure in the pot head space by about 2,450 Pa. An open overflow would then blow steam out at ground level. The overflow therefore runs through a U, a loop seal 350 mm deep, which holds 3,291 Pa before steam can pass. That is 34 % over the surge (about 16 % on flow), for a flash basis that is not yet bounded (STEM S15, STR-DEC-001 #20); the loop seal must be kept full (safety stop S4) and drained with the pot in frost (S10).

**Flow stability.** A single coil and bank fed by a positive-displacement diaphragm pump are not prone to the parallel-channel or Ledinegg instabilities of multi-tube boilers. At this low mass flux the flow will be stratified or wavy in the helix, so the top of the tube will dry out before the outlet and run hotter than the 110 °C wall assumed. At 0.083 MPa hoop stress this does not threaten the tube, but it will speed scaling.

## 6. Stored water, dry coil and relief valve

**Stored water.** Flooded, the coil holds 5.06 L, the bank 0.90 L, the economizer 0.61 L and the header 0.75 L: 7.32 L in total, under the 8 L limit of R7 by 8 %. The 0.3 m link between the economizer and the bank adds about 0.03 L.

**Dry coil and refeed.** The coil tube weighs 13.0 kg. If it runs dry it approaches the 519 °C firebox gas temperature and stores 2.73 MJ, enough to flash 1.17 kg of feed water. If the pump restarts and that happens over 30 s, the steam flow is 141 kg/h, 4.7 times the design flow, and the coil drop would scale to about 1.7 bar. The review pointed out that a dry coil no longer cools the gas, so it may reach 700 to 800 °C and flash about 2 kg, and that the 30 s basis is assumed; the flash basis is therefore open (STEM S15 to S17, STR-DEC-001 #20). Since 2026-10-24 a latching relay cuts the pump on a coil alarm until it is reset by hand, so a stalled pump cannot restart by itself into a dry coil (STR-DEC-001 S4). The tube itself is not at risk from pressure: hoop stress is 0.086 MPa in normal use and 2.0 MPa at the pump's 3 bar shut-off, against a yield strength of roughly 100 MPa for 316 at 700 °C. The hazard is steam and scalding water thrown from joints and the hose, which is why the coil outlet alarm and the rule never to refeed a hot, dry coil stay essential.

**Relief valve.** Napier's formula, with 10 % accumulation over a 15 psi (1.034 bar) set pressure and a derated coefficient of 0.878, needs a 30.2 mm² orifice (6.2 mm) for 30 kg/h and 142 mm² (13.4 mm) for the 141 kg/h refeed flash. The maker's capacity table for the Watts Series 315 gives 375 lb/h (170 kg/h) for the 3/4 in valve at 15 psi, which covers the refeed flash with about 21 % margin. The valve sits at the header, downstream of the coil, where the flash builds pressure first. PR-009 (R9) is met on paper for the 30 s basis; the capacity must be confirmed for the valve actually bought.

## 7. Mass, envelope, cost and hood handles

*Table 8. Loaded mass with a full tank.*

| Item | Mass |
| --- | --- |
| Trailer (tare, assumed) | 160.0 kg |
| Firebox (shell, fiber lining, grate, door; 960 mm tall) | 122.1 kg |
| Monotube coil (10 turns) | 13.0 kg |
| Evaporator bank (box, lining, tube, supports, link) | 26.0 kg |
| Gas-pass baffles and ledges (2026-10-24, STR-DEC-001 S1) | 7.4 kg |
| Economizer | 18.0 kg |
| Chimney and cap (outlet 3.2 m) | 6.6 kg |
| Header, seal pot, vent, relief valve | 18.0 kg |
| Seal water | 9.1 kg |
| Tank, empty | 8.0 kg |
| Feed water, full tank | 125.0 kg |
| Pump and battery | 8.0 kg |
| Steam hose | 5.4 kg |
| Hoods, 2 off, with steel handles | 62.5 kg |
| Instruments, alarms, safety kit | 8.0 kg |
| Supports and lines added for construction (skids, post, stays, saddles, brackets, grate stand, glands, both dampers, feed lines, vent line and discharge, seal pot overflow, frames, unions) | 46.0 kg |
| **Total** | **643 kg** |

PR-011 (R11) applies as towed, with the tank and seal pot drained (Amish, 2026-09-25): 509 kg against 500 kg, 9 kg over, so not met (the review also noted that tare, contingency and residual water make 540 to 600 kg plausible). The gas-pass baffles and their ledges add 7.4 kg and the taller chimney 2.5 kg to the 499 kg of version 0.4. The register records that the two hoods ride on a second vehicle for the prototype (2026-10-02); without them the trailer tows 447 kg, and counting PR-011 that way is proposed (STR-DEC-001 #13). The masses of the made parts come from the model volumes (`python cad/src/model.py --mass`: 32.8 kg of construction parts in the kit 1.9 model, against 42.5 kg in version 0.4, 25.8 kg of bank and 7.4 kg of baffles and ledges; the 46.0 kg allowance is kept because the whole model agrees with this table). The kit 1.9 model weighs about 507 kg dry with both hoods (`cad/fidelity.json`), within 1 % of this table less the water. Overall width is 1.48 m against 1.5 m. The chimney outlet is 3.20 m above ground, and one fill of the tank lasts 4.17 h.

**Hood handles for ballast.** Each handle is a 900 mm bar of 30 x 30 x 2.5 steel tube on two standoffs 800 mm apart, welded to 100 x 100 x 3 foot plates through-bolted to backing plates in the hood wall. With half of a 40 kg ballast on one handle, as one load at mid-span and a load factor of 2, the bar sees about 34 MPa, a factor of 7 on the 235 MPa yield of mild steel. Each standoff carries at most about 24 N m at its foot plate, taken by two M6 bolts and a backing plate: about 0.24 kN of tension a bolt about the plate's lower edge, far inside an M6 bolt's capacity.

The priced BOM (`bom/bom.csv`, 22 lines) totals USD 2,720.00. Value-engineering target: USD 2,200. Estimated cost of the constructable design: USD 2,720 (USD 520 over the target). The kit 1.9.1 changes add USD 120, all estimates not checked live: the gas-pass baffles USD 50 (316L on line 7, USD 35; line 22, USD 15), the taller chimney USD 60 (line 8) and the latching pump trip USD 10 (line 16). The overrun to USD 2,600 was accepted by Amish on 2026-10-03; the USD 120 above it is reported to him, not accepted. The 2026-10-02 changes add USD 325: the evaporator bank (USD 190), the seal pot overflow (USD 70), the bank link and reducing unions (USD 45), the ballast-rated handles (USD 30 for two hoods), the secondary damper (USD 10, less USD 5 of shell steel) and fixings (USD 5), less USD 20 for the shorter coil. Only the relief valve price was checked against a live listing (USD 68.19 on 2026-09-25 and again on 2026-10-25); the rest are indicative.

## 8. Results against requirements

*Table 9. Requirement status against STR-PRS-001, not met and at risk items first (old R numbers in brackets). Status words as STR-PRS-001.*

| ID | Requirement | Calculated value | Target | Status |
| --- | --- | --- | --- | --- |
| PR-004 (R4) | Wood per m² at 15 cm | 4.36 kg/m² with the baffles and dampers set (4.44 kg/m² wide open) | 4 kg/m² or less (restatement to 4.5 proposed) | Not met (was at risk) |
| PR-005 (R5) | Fuel to steam efficiency | 66.1 % at λ = 1.5 with the baffles (62.5 to 66.9 % in Table 6a; 59.8 % without the baffles) | 65 % or more | At risk (was met) |
| PR-002 (R2) | Treatment rate at 15 cm, two hoods | 1.88 m²/h (about 1.5 to 1.6 with edge strips, overlap and hose losses, STEM M2) | 1.85 m²/h or more (about 1.9) | At risk (thin margin) |
| PR-014 (R2) | Treatment rate at 5 cm, two hoods | 3.41 m²/h | 3.4 m²/h or more | At risk (thin margin) |
| PR-011 (R11) | Mass as towed, tank and seal pot drained | 509 kg (643 kg full; 447 kg without the hoods) | 500 kg or less | Not met (9 kg over) |
| PR-015 (R11) | Overall width | 1.48 m | 1.5 m or less | At risk (thin margin) |
| PR-008 (R8) | Steaming per fill and per battery charge | Water 4.2 h; battery about 100 % depth of discharge at an assumed 4 A pump | 3 h or more | At risk (was met; battery, STEM E3) |
| PR-001 (R1) | Soil at 70 °C for 20 to 30 min at 15 cm over 80 % of the footprint | Front to 16.5 cm holds 70 °C at 15 cm for 25 min in the 1D model; skirt leakage and permeability not quantified | 70 °C, 20 to 30 min | To verify at TRL 4 |
| PR-003 (R3) | Steam output | 30 kg/h with firebox gas at 519 °C and 32.9 kW firing | 30 kg/h or more | Met on paper |
| PR-006 (R6) | Normal pressure at the header; open vent | 0.033 bar gauge; seal 0.084 bar; vent cannot be isolated | 0.1 bar gauge or less | Met on paper |
| PR-013 (R6) | Normal pressure at the coil inlet (now the bank inlet) | 0.129 bar gauge | 0.15 bar gauge or less | Met on paper |
| PR-007 (R7) | Water in heated section, flooded | 7.3 L | 8 L or less | Met on paper |
| PR-009 (R9) | Certified relief valve, set pressure and capacity | 15 psi (1.03 bar) set; rated 170 kg/h against a 141 kg/h refeed flash (basis open, STEM S16) | 15 psi (1.03 bar) or less; capacity for the flash | Met on paper |
| PR-010 (R10) | Chimney outlet, spark arrestor mesh, hood handles | 3.2 m, 6 mm mesh, hood outer skin 23 °C | 2.2 m, 6 mm, 60 °C | Met by design |
| PR-012 (R12) | Parts cost against the value-engineering target | USD 2,720 | USD 2,200 target | Over target by USD 520 |
| PR-016 (new) | Hood handling, at most 23 kg per person | 31.3 kg hood, handles 1.12 m apart (STEM B4) | 23 kg per person | Not met for one person; proposed to Amish |

Summary: 3 not met (PR-004, PR-011, PR-016 for one person); 5 at risk (PR-005, PR-002, PR-014, PR-015, PR-008); 1 to verify at TRL 4 (PR-001); 6 met on paper or by design in this table (PR-003, PR-006, PR-013, PR-007, PR-009, PR-010); PR-012 is USD 520 over the value-engineering target. PR-017 and PR-018 are design-review requirements (STR-PRS-001). Status changes from version 0.4: PR-004 at risk to not met, PR-005 met to at risk, PR-008 met to at risk, PR-011 at risk to not met.

## 9. Limits of this note

- The firebox is one well-stirred zone. Real fireboxes have a hot flame zone and cooler corners; the exchange factor F and excess air λ carry most of the uncertainty (Table 6), and R5 now rests on λ near 1.5.
- The bank and economizer are single counterflow exchangers. Their gas-side coefficients now come from the Zukauskas correlation at the pass velocity (±25 % or so for tube banks) plus a gas radiation estimate (±50 %); leakage round the baffle edges is a flat 10 % and fouling a single resistance. Without the baffles the same method gives about 10 to 12 W/(m² K) and 60 %, which is why they are part of the design.
- The natural draft uses a mean flue temperature of 400 °C and loss coefficients from handbook practice; with 5.4 Pa left for the dampers and the fuel bed loss an estimate, the draft margin is modest and must be checked by measuring the firebox draft at TRL 4.
- The soil model is one-dimensional with a sharp front and no fingering, no lateral loss at the skirt beyond the assumed 10 %, and no change in permeability as condensate wets the soil.
- The two-phase pressure drop uses correlations developed for straight tubes with a curvature factor; the error band is about ±30 %.
- Prices are indicative except where the BOM names a checked listing.
- Nothing here has been tested. Every result needs measurement at TRL 4, which is on hold by Amish's instruction.

> **Safety:** Steam at 100 °C causes deep burns in under a second. The permeability result means steam may jet from under the hood skirt in finer soils, ballasted or not. The dry-coil refeed result means a restart into a hot coil can throw steam at more than four times the design flow, and the overflow's loop seal must be full to keep it from leaving at ground level. The firebox skin reaches about 100 °C, the bank box about the same and the flue about 500 °C at the bank. Carbon monoxide from the fire is lethal in enclosed spaces, and running with less excess air raises the carbon monoxide made. None of these hazards is controlled by this calculation.

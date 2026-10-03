---
doc_id: STR-CAL-001
title: SteamRoot sizing calculations
project: SteamRoot
doc_type: Calculation note
version: "0.4"
status: Draft
date: '2026-10-02'
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
---

# SteamRoot sizing calculations

The decided configuration (open-vented stainless monotube coil, evaporator bank, economizer, two hoods, fixed-rate feed) makes 30 kg/h of steam at near-atmospheric pressure with little stored water. Version 0.4 carries in Amish's decisions of 2026-10-02. An evaporator bank of about 6.4 m of 15.88 mm stainless tube now sits in a lined box between the firebox roof and the economizer, a secondary air slide on the door joins the primary damper, the coil has 10 turns instead of 11 and the firebox is 40 mm lower. With the dampers holding the excess air near λ = 1.5, fuel-to-steam efficiency is about 69 % (R5 met on paper) and wood use about 4.2 kg/m² at 15 cm (R4 at risk, 4 % over). With the dampers left open (λ = 2.0) the figures are 61 % and 4.7 kg/m². The heated section holds 7.3 L (R7 met). The seal pot overflow fixes the seal limit at 0.084 bar. The towed mass rises to 499 kg (R11 at risk). These are paper estimates; nothing here has been tested.

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
| Excess air ratio λ | 1.5 with the primary and secondary dampers set; 2.0 with them open | Hand-fed batch firebox; range 1.5 to 2.5 |
| Unburned loss | 4 % of fuel energy | CO and char |
| Coil radiative exchange factor F | 0.40 per unit tube area | Range 0.25 to 0.6 |
| Gas to coil convection | 20 W/(m² K) | Low-velocity cross flow |
| Evaporator bank and economizer coefficients | 30 and 25 W/(m² K) | Bare tube in cross flow, gas side controlled |
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

**Model (new in version 0.4).** Version 0.3 sized a bank for a target efficiency. Version 0.4 runs the design forward. The firebox is one well-stirred zone: heat to the coil is σ F A (T_g⁴ - T_w⁴) + h A (T_g - T_w) with 13.20 m of tube (1.05 m²) and a 110 °C wall, and the lining loses heat to the outside. The gas then crosses the evaporator bank, treated as a counterflow exchanger with water boiling at 100 °C inside, loses a little heat through the bank box walls, and crosses the economizer, a counterflow exchanger whose water outlet is capped at 85 °C. The firing rate is found so that the coil and the bank together boil exactly the feed the economizer delivers.

**The study.** Amish decided on 2026-10-02 to size the bank with primary and secondary air dampers so the heated water stays at 8 L or less, with a smaller-bore bank tube or fewer firebox turns, without relaxing R7, and to reshape the firebox in the same study (STR-DDR-002, item 1; STR-DDR-003, A1). The bank tube chosen is 15.88 x 1.24 mm (5/8 x 0.049 in) 316 stainless: it gives 50 % more surface per litre of water than the 25.4 mm coil tube. Two layers of five runs fill the 700 x 600 bank box and give 6.40 m of tube (0.319 m², 0.90 L), taken from the model. Table 4 compares the options.

*Table 4. Evaporator bank and firebox study (F = 0.40).*

| Option | Efficiency | Wood | Wood at 15 cm | Firebox gas | Bank | Economizer | Stack | Water, flooded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v0.3 design: 11 turns, 1000 mm firebox, no bank, λ = 2.0 | 51.4 % | 10.5 kg/h | 5.61 kg/m² | 520 °C | none | 2.44 kW | 451 °C | 6.93 L |
| 11 turns, 1000 mm, no bank, dampers set (λ = 1.5) | 60.5 % | 9.0 kg/h | 4.77 kg/m² | 520 °C | none | 2.44 kW | 415 °C | 6.93 L |
| 11 turns, 1000 mm, 6.4 m bank, λ = 1.5 | 69.7 % | 7.8 kg/h | 4.14 kg/m² | 490 °C | 2.98 kW | 1.65 kW | 225 °C | 7.83 L |
| **Chosen: 10 turns, 960 mm, 6.4 m bank, λ = 1.5** | **68.9 %** | **7.9 kg/h** | **4.18 kg/m²** | **510 °C** | **3.14 kW** | **1.73 kW** | **235 °C** | **7.33 L** |
| Chosen, dampers left open (λ = 2.0) | 61.3 % | 8.8 kg/h | 4.71 kg/m² | 502 °C | 3.30 kW | 2.09 kW | 296 °C | 7.33 L |
| 9 turns, 920 mm, 6.4 m bank, λ = 1.5 | 68.1 % | 7.9 kg/h | 4.23 kg/m² | 533 °C | 3.32 kW | 1.81 kW | 247 °C | 6.82 L |

Keeping 11 turns with the bank would hold 7.83 L, within 2 % of the R7 limit. Dropping one turn costs 0.8 points of efficiency and frees 0.5 L; the firebox is then reshaped 40 mm lower so the coil keeps the same clearance under the roof board, which saves a little shell loss and 3 kg. Dropping a second turn frees another 0.5 L but costs another point, so 10 turns is the balance. Most of the gain comes from air control: the dampers alone lift the v0.3 design from 51 % to 61 %, and the bank adds about 8 points more.

*Table 5. Energy balance of the chosen design (λ = 1.5, F = 0.40).*

| Quantity | Value |
| --- | --- |
| Firing rate | 31.6 kW (7.9 kg/h of wood) |
| Heat to water: coil 16.91 kW, bank 3.14 kW, economizer 1.73 kW | 21.78 kW |
| Stack loss (flue gas leaves at 235 °C) | 4.5 kW |
| Shell loss through the firebox lining and the bank box walls | 4.1 kW |
| Unburned loss | 1.3 kW |
| Fuel to steam efficiency | 68.9 % |
| Firebox outer skin temperature | 98 °C |

The bank cools the gas from 510 °C to 320 °C. The economizer then has less to work with: it delivers 1.73 kW and the feed reaches the bank at about 65 °C rather than 85 °C, which the bank and coil make up. The economizer's 0.29 m² of tube is fully used (log mean temperature difference 237 K).

*Table 6. Sensitivity of fuel-to-steam efficiency with the bank (%; without the bank in brackets).*

| λ | F = 0.25 | F = 0.40 | F = 0.60 |
| --- | --- | --- | --- |
| 1.5 | 66.4 (53.7) | 68.9 (58.8) | 71.2 (63.2) |
| 2.0 | 58.0 (43.2) | 61.3 (49.3) | 64.2 (54.6) |
| 2.5 | 47.9 (32.7) | 52.8 (39.7) | 56.6 (45.9) |

R5 (65 %) is met at λ = 1.5 for every exchange factor in the range, and missed at λ = 2.0 or leaner. It therefore depends on the operator holding the dampers near λ = 1.5, which must be measured at TRL 4 with a flue gas oxygen reading.

**Dampers and draft.** The 1.70 m from the grate to the chimney outlet gives a natural draft of about 11.4 Pa with flue gas at a mean 400 °C. At a discharge coefficient of 0.6 the air openings must total about 4,960 mm² at λ = 1.5 and 7,430 mm² at λ = 2.0. The primary inlet under the grate (160 x 60, 9,600 mm²) and the secondary slot in the door above the fire bed (150 x 20, 3,000 mm²) together give 12,600 mm², so both slides work partly closed and have room to trim.

**Wood per square meter and R4.** With two hoods, 7.9 kg/h of wood treats 1.88 m²/h at 15 cm: 4.18 kg/m², 4 % over the 4 kg/m² target (4.71 kg/m² with the dampers open). At 5 cm it is 2.30 kg/m². R4 needs about 72 % efficiency at the current steam demand. Amish decided on 2026-10-02 to plan a restated R4. **Proposed, awaiting Amish:** restate R4 as 4.5 kg/m² or less at 15 cm with the dampers set, to be confirmed by fuel weighing at TRL 4. The options are (a) 4.5 kg/m², which the design meets with 7 % margin at λ = 1.5 but not with the dampers open; (b) 5.0 kg/m², which also covers λ = 2.0; (c) keep 4 kg/m² and look for the rest in lower steam demand (less skirt leakage). The recommendation is (a), since (b) would stop R4 from rewarding air control.

**Flue condensate.** At λ = 1.5 the flue gas holds 12.5 % water vapor by volume, so its dew point is about 51 °C. The cold end of the economizer, fed at 15 °C, runs wet with acidic condensate, which confirms the stainless tube and the condensate drain.

## 5. Steam-side pressure

The coil bore is 22.1 mm. At 30 kg/h the mass flux is 21.7 kg/(m² s) and dry steam would move at 36.3 m/s (Reynolds number 39,033). The two-phase friction gradient comes from the Müller-Steinhagen and Heck correlation, averaged over a quality that rises linearly along the boiling length, times a helical-coil factor of 1.26 (Ito). The coil is still taken to do all the boiling, which overstates its drop slightly now that the bank does some.

The bank, upstream of the coil, has a 13.4 mm bore and a mass flux of 59.1 kg/(m² s). It heats the feed to boiling and takes it to a steam quality of about 0.10, with a drop of about 2,460 Pa including a 10 % allowance for the return bends. The fall from the bank down to the coil inlet adds head that is ignored here, which is conservative.

*Table 7. Pressure build-up at 30 kg/h.*

| Element | Pressure drop |
| --- | --- |
| Coil friction (two-phase mean 358 Pa/m, all-vapor 401 Pa/m) | 5,816 Pa |
| Coil acceleration | 789 Pa |
| Coil gravity | 17 Pa |
| Outlet riser to the header | 373 Pa |
| **Coil total** | **6,994 Pa** |
| Evaporator bank | 2,462 Pa |
| Hose, 6 m at 28.4 m/s, with fittings | 2,546 Pa |
| Hood manifold (assumed) | 500 Pa |
| Hood, at most its lift pressure | 256 Pa |
| **Header pressure** | **3,301 Pa (0.033 bar gauge)** |
| **Bank inlet pressure (the highest on the steam side)** | **12,758 Pa (0.128 bar gauge)** |

R6 is met: 0.033 bar at the header against 0.1 bar, and 0.128 bar at the inlet against 0.15 bar. The bank uses about half of the inlet margin. With 40 kg of ballast on the hood in use the figures become 0.036 bar and 0.131 bar.

**Water seal and overflow.** When the header pressure pushes water down the dip leg, the same volume would rise in the annulus between the dip leg and the pot wall. With a 42.2 mm dip leg in a 114.3 mm pot the annulus area is 8.1 times the dip leg bore, so without an overflow the water outside would rise 110 mm while the water inside fell the full 890 mm to the dip leg end: 1.0 m of head, 9,402 Pa (0.094 bar). Amish decided on 2026-10-02 to fit an overflow at the static water mark. Its bore bottom is at the mark, so water pushed out of the dip leg spills away instead of rising round it, and the pot can never hold water above the mark. The seal therefore blows when the dip leg is pushed empty: 890 mm of head, 8,365 Pa (0.084 bar gauge). The overflow sets the seal depth so the pot cannot exceed the 0.094 bar limit, overfilled or not, and lowers the limit by the 110 mm rise. The margin over the 0.033 bar header pressure is 5,064 Pa. After a seal blow the pot holds less water than before; the seal is then shallower, which errs on the safe side, and the pre-start check in safety stop S4 refills it to the mark. In normal use the 0.033 bar header pressure pushes about 0.3 L of water out of the dip leg and over the overflow each time steam comes up. When the steam stops the level settles about 45 mm below the mark, so the pot is topped up to the mark before each start, as S4 already requires; steam condensing in the pot during a run partly makes this up.

**Overflow loop seal.** If the seal blows with the full dry-coil refeed flash (section 6), 138 kg/h of steam leaves the pot by the DN32 vent at about 66 m/s, which raises the pressure in the pot head space by about 2,350 Pa. An open overflow would then blow steam out at ground level. The overflow therefore runs through a U, a loop seal 350 mm deep, which holds 3,291 Pa before steam can pass. That is 40 % over the surge; the loop seal must be kept full (safety stop S4) and drained with the pot in frost (S10).

**Flow stability.** A single coil and bank fed by a positive-displacement diaphragm pump are not prone to the parallel-channel or Ledinegg instabilities of multi-tube boilers. At this low mass flux the flow will be stratified or wavy in the helix, so the top of the tube will dry out before the outlet and run hotter than the 110 °C wall assumed. At 0.085 MPa hoop stress this does not threaten the tube, but it will speed scaling.

## 6. Stored water, dry coil and relief valve

**Stored water.** Flooded, the coil holds 5.06 L, the bank 0.90 L, the economizer 0.61 L and the header 0.75 L: 7.32 L in total, under the 8 L limit of R7 by 8 %. The 0.3 m link between the economizer and the bank adds about 0.03 L.

**Dry coil and refeed.** The coil tube weighs 13.0 kg. If it runs dry it approaches the 510 °C firebox gas temperature and stores 2.67 MJ, enough to flash 1.15 kg of feed water. If the pump restarts and that happens over 30 s, the steam flow is 138 kg/h, 4.6 times the design flow, and the coil drop would scale to about 1.5 bar. The tube itself is not at risk from pressure: hoop stress is 0.085 MPa in normal use and 2.0 MPa at the pump's 3 bar shut-off, against a yield strength of roughly 100 MPa for 316 at 700 °C. The hazard is steam and scalding water thrown from joints and the hose, which is why the coil outlet alarm and the rule never to refeed a hot, dry coil stay essential.

**Relief valve.** Napier's formula, with 10 % accumulation over a 15 psi (1.034 bar) set pressure and a derated coefficient of 0.878, needs a 30.2 mm² orifice (6.2 mm) for 30 kg/h and 139 mm² (13.3 mm) for the 138 kg/h refeed flash. The maker's capacity table for the Watts Series 315 gives 375 lb/h (170 kg/h) for the 3/4 in valve at 15 psi, which covers the refeed flash with about 23 % margin. R9 is met on paper; the capacity must be confirmed for the valve actually bought.

## 7. Mass, envelope, cost and hood handles

*Table 8. Loaded mass with a full tank.*

| Item | Mass |
| --- | --- |
| Trailer (tare, assumed) | 160.0 kg |
| Firebox (shell, fiber lining, grate, door; 960 mm tall) | 122.1 kg |
| Monotube coil (10 turns) | 13.0 kg |
| Evaporator bank (box, lining, tube, supports, link) | 26.0 kg |
| Economizer | 18.0 kg |
| Chimney and cap | 4.1 kg |
| Header, seal pot, vent, relief valve | 18.0 kg |
| Seal water | 9.1 kg |
| Tank, empty | 8.0 kg |
| Feed water, full tank | 125.0 kg |
| Pump and battery | 8.0 kg |
| Steam hose | 5.4 kg |
| Hoods, 2 off, with steel handles | 62.5 kg |
| Instruments, alarms, safety kit | 8.0 kg |
| Supports and lines added for construction (skids, post, stays, saddles, brackets, grate stand, glands, both dampers, feed lines, vent line and discharge, seal pot overflow, frames, unions) | 46.0 kg |
| **Total** | **633 kg** |

R11 applies as towed, with the tank and seal pot drained (Amish, 2026-09-25): 499 kg against 500 kg, at risk. The bank adds 26 kg, the overflow about 5 kg and the steel handles 5 kg; the lower firebox and the shorter coil save about 4 kg. The register records that the two hoods ride on a second vehicle for the prototype (2026-10-02); without them the trailer tows 437 kg. The masses of the made parts come from the model volumes (`python cad/src/model.py --mass`: 42.5 kg of construction parts and 26.0 kg of bank). Overall width is 1.48 m against 1.5 m. The chimney outlet stays 2.40 m above ground, and one fill of the tank lasts 4.17 h.

**Hood handles for ballast.** Each handle is a 900 mm bar of 30 x 30 x 2.5 steel tube on two standoffs 800 mm apart, welded to 100 x 100 x 3 foot plates through-bolted to backing plates in the hood wall. With half of a 40 kg ballast on one handle, as one load at mid-span and a load factor of 2, the bar sees about 34 MPa, a factor of 7 on the 235 MPa yield of mild steel. Each standoff carries at most about 24 N m at its foot plate, spread over four M6 bolts and a 100 mm backing plate.

The priced BOM (`bom/bom.csv`, 22 lines) totals USD 2,600.00. Value-engineering target: USD 2,200. Estimated cost of the constructable design: USD 2,600 (USD 400 over the target). The 2026-10-02 changes add USD 325: the evaporator bank (USD 190), the seal pot overflow (USD 70), the bank link and reducing unions (USD 45), the ballast-rated handles (USD 30 for two hoods), the secondary damper (USD 10, less USD 5 of shell steel) and fixings (USD 5), less USD 20 for the shorter coil. Only the relief valve price was checked against a live listing; the rest are indicative.

## 8. Results against requirements

*Table 9. Requirement status, not met and at risk items first. Status words: met, not met, at risk, not verifiable at TRL 3.*

| ID | Requirement | Calculated value | Target | Status |
| --- | --- | --- | --- | --- |
| R4 | Wood per m² at 15 cm | 4.2 kg/m² with the dampers set (4.7 kg/m² open) | 4 kg/m² or less (restatement to 4.5 proposed) | At risk (was not met) |
| R2 | Treatment rate at 15 cm, two hoods | 1.88 m²/h | 1.85 m²/h or more (about 1.9) | At risk (thin margin) |
| R2 | Treatment rate at 5 cm, two hoods | 3.41 m²/h | 3.4 m²/h or more | At risk (thin margin) |
| R11 | Mass as towed, tank and seal pot drained | 499 kg (633 kg full; 437 kg without the hoods) | 500 kg or less | At risk (was met) |
| R11 | Overall width | 1.48 m | 1.5 m or less | At risk (thin margin) |
| R1 | Soil at 70 °C for 20 to 30 min at 15 cm over 80 % of the footprint | Front to 16.5 cm holds 70 °C at 15 cm for 25 min in the 1D model; skirt leakage and permeability not quantified | 70 °C, 20 to 30 min | Not verifiable at TRL 3 |
| R3 | Steam output | 30 kg/h with firebox gas at 510 °C and 31.6 kW firing | 30 kg/h or more | Met |
| R5 | Fuel to steam efficiency | 69 % at λ = 1.5 (61 % at λ = 2.0) | 65 % or more | Met on paper, if the dampers hold λ near 1.5 (was not met) |
| R6 | Normal pressure at the header; open vent | 0.033 bar gauge; seal 0.084 bar; vent cannot be isolated | 0.1 bar gauge or less | Met |
| R6 | Normal pressure at the coil inlet (now the bank inlet) | 0.128 bar gauge | 0.15 bar gauge or less | Met |
| R7 | Water in heated section, flooded | 7.3 L | 8 L or less | Met |
| R8 | Steaming per fill | 4.2 h | 3 h or more | Met |
| R9 | Certified relief valve, set pressure and capacity | 15 psi (1.03 bar) set; rated 170 kg/h against a 138 kg/h refeed flash | 15 psi (1.03 bar) or less; capacity for the flash | Met |
| R10 | Chimney outlet, spark arrestor mesh, hood handles | 2.4 m, 6 mm mesh, hood outer skin 23 °C | 2.2 m, 6 mm, 60 °C | Met |
| R12 | Parts cost against the value-engineering target | USD 2,600 | USD 2,200 target | USD 400 over the target |

Summary: none not met; 5 at risk (R4, R2 twice, R11 mass and width); 1 not verifiable at TRL 3 (R1); 8 met (R3, R5, R6 twice, R7, R8, R9, R10); R12 is USD 400 over the value-engineering target. Status changes from version 0.3: R4 not met to at risk, R5 not met to met, R11 mass met to at risk.

## 9. Limits of this note

- The firebox is one well-stirred zone. Real fireboxes have a hot flame zone and cooler corners; the exchange factor F and excess air λ carry most of the uncertainty (Table 6), and R5 now rests on λ near 1.5.
- The bank and economizer are single counterflow exchangers with constant coefficients; their coefficients for this low gas velocity are estimates within about ±30 %.
- The soil model is one-dimensional with a sharp front and no fingering, no lateral loss at the skirt beyond the assumed 10 %, and no change in permeability as condensate wets the soil.
- The two-phase pressure drop uses correlations developed for straight tubes with a curvature factor; the error band is about ±30 %.
- Prices are indicative except where the BOM names a checked listing.
- Nothing here has been tested. Every result needs measurement at TRL 4, which is on hold by Amish's instruction.

> **Safety:** Steam at 100 °C causes deep burns in under a second. The permeability result means steam may jet from under the hood skirt in finer soils, ballasted or not. The dry-coil refeed result means a restart into a hot coil can throw steam at more than four times the design flow, and the overflow's loop seal must be full to keep it from leaving at ground level. The firebox skin reaches about 100 °C, the bank box about the same and the flue about 500 °C at the bank. Carbon monoxide from the fire is lethal in enclosed spaces, and running with less excess air raises the carbon monoxide made. None of these hazards is controlled by this calculation.

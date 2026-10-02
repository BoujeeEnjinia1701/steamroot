---
doc_id: STR-CAL-001
title: SteamRoot sizing calculations
project: SteamRoot
doc_type: Calculation note
version: "0.3"
status: Draft
date: '2026-10-01'
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
---

# SteamRoot sizing calculations

The decided configuration (open-vented stainless monotube coil, economizer, two hoods, fixed-rate feed) makes 30 kg/h of steam at near-atmospheric pressure with little stored water. With the requirements as restated by Amish on 2026-09-25 (STR-DDR-002), it misses two: fuel-to-steam efficiency comes out at about 51 %, not 65 %, because a single coil in the firebox leaves the flue gas at about 450 °C, and wood use is 5.6 kg/m² at 15 cm, not 4. Version 0.3 reruns the note for the constructable design of STR-DDR-003, whose taller firebox loses about 2 points of efficiency through its larger walls. A paper study of the recommended fix (section 4) finds that about 4.3 m of 25.4 mm evaporator tube in the flue, or excess air held near λ = 1.5 with about 1.3 m, would reach 65 %, but R4 needs about 72 %. The treatment rate (1.88 m²/h at 15 cm) and width (1.48 m) meet their targets with thin margins. These are paper estimates; nothing here has been tested.

> **Safety:** This note sizes a fired steam generator. It is a paper calculation, not a design approval. A written ruling from the local boiler authority on whether an open-vented, fired monotube coil is exempt from boiler and pressure vessel rules is an **open prerequisite**. Amish approved getting that ruling before detail work; it has not been obtained. No part of this note may be used to build or operate the machine until that ruling exists and the design has been reviewed against it.

All numbers below are printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root). The script reads geometry from `cad/src/model.py` (`PARAMS`) and prices from `bom/bom.csv`, so the model, the BOM and this note share one source.

## 1. Method and assumptions

The calculation has six parts: soil heat and steam demand, treatment rate, combustion and firebox heat transfer, steam-side pressure, stored energy and relief, and mass and cost. Every assumption is listed in the `A` dictionary at the top of the script. The main ones are in Table 1.

*Table 1. Main assumptions.*

| Quantity | Value | Basis or range |
| --- | --- | --- |
| Design steam output | 30 kg/h saturated at about 1.01 bar | R3 target |
| Feed water, economizer outlet | 15 °C, 85 °C | Outlet held 15 K below boiling |
| Soil | 1,300 kg/m³ dry bulk density, 20 % water (dry basis), 15 °C start | As STR-REQ-001 |
| Specific heats | Soil 0.84, water 4.18 kJ/(kg K) | Handbook values |
| Soil conductivity | 1.2 W/(m K), giving 0.55 mm²/s diffusivity | Moist loam; range 0.8 to 1.6 |
| Soil permeability | 10⁻¹⁰, 10⁻¹¹, 10⁻¹² m² | Sand, sandy loam, loam (textbook ranges, not measured) |
| Hold at 70 °C | 25 min | R1 allows 20 to 30 min |
| Steam lost under the skirt | 10 % | Assumed; range 5 to 25 % |
| Hood | 1 mm aluminum double skin, 40 mm mineral wool | As BOM item 12 |
| Wood | Dry C 50 %, H 6 %, O 43.3 %, N 0.2 %, ash 0.5 %; 20 % moisture (wet basis) | Typical hardwood analysis |
| Excess air ratio λ | 2.0 | Hand-fed batch firebox; range 1.5 to 2.5 |
| Unburned loss | 4 % of fuel energy | CO and char |
| Coil radiative exchange factor F | 0.40 per unit tube area | Range 0.25 to 0.6 |
| Gas to coil convection | 20 W/(m² K) | Low-velocity cross flow |
| Firebox lining | 50 mm ceramic fiber, 0.12 W/(m K) | As BOM item 5 |
| Trailer tare | 160 kg | Used 2.0 x 1.2 m trailer; range 130 to 250 kg |
| Relief valve rated capacity | 375 lb/h (170 kg/h) | Watts Series 315, 3/4 in, 15 psi set, maker's capacity table |
| Evaporator bank coefficient (R5 study only) | 30 W/(m² K) | Bare tube in cross flow, gas side controlled |

## 2. Soil heat and steam demand

**Model.** Steam condenses at a sharp front that moves down through the soil. Soil above the front sits at the steam temperature, 100 °C, and soil below it stays cold. This replaces the TRL 2 model, which heated a uniform layer to 75 °C. When the hose moves to the other hood, the hot layer begins to lose heat to the cold soil below. For two semi-infinite regions at 100 °C and 15 °C the interface drops at once to 57.5 °C, so the front must go deeper than the working depth. Keeping 70 °C at 15 cm through a 25-minute hold needs an overshoot of 2 √(αt) erf⁻¹(0.294) = 1.53 cm, so the front must reach 16.5 cm.

**Energy.** The soil's volumetric heat capacity is 1,300 x (0.84 + 0.20 x 4.18) = 2,179 kJ/(m³ K). Heating 16.5 cm by 85 K takes 30.6 MJ/m². Condensate stays in the soil at 100 °C, so each kilogram of steam gives its latent heat, 2.257 MJ. Hood losses add 1.00 MJ/m² (wall loss of 178 W through U = 0.91 W/(m² K), and 0.80 MJ of stored heat per setting), and 10 % of the steam escapes under the skirt.

*Table 2. Steam demand per square meter.*

| Case | Soil heat | Steam | Hood efficiency | Heat time per 1.2 m² setting |
| --- | --- | --- | --- | --- |
| TRL 2 model (uniform 75 °C, 60 % hood) | 19.6 MJ/m² | 13.8 kg/m² | 60 % (assumed) | Not used |
| 15 cm working depth | 30.6 MJ/m² | 15.6 kg/m² | 87 % | 37.4 min |
| 5 cm working depth | 12.1 MJ/m² | 6.4 kg/m² | 84 % | 15.2 min |

The TRL 2 figure of about 14 kg/m² was close only because its 60 % hood efficiency hid the extra heat needed to bring the top of the layer to 100 °C.

**Soil permeability.** At full flow the steam passes down through the hot layer at 1.16 cm/s. By Darcy's law that takes 236 Pa through 16.5 cm of sand (10⁻¹⁰ m²), 2,362 Pa through a sandy loam (10⁻¹¹ m²) and 23,617 Pa through a loam (10⁻¹² m²). The hood weighs 28.8 kg, so it lifts at 235 Pa. In anything finer than sand the steam will not push through at full flow: it will escape under the skirt, or the front will slow and the heat time will grow. This is the largest unquantified risk to R1 and R2. Ballast on the hood or a deeper skirt would help, but either raises the steam pressure at the skirt and the burn risk there.

## 3. Treatment rate

Each setting needs the heat time above plus a 25-minute hold and 2 minutes to lift and reset the hood. With two hoods the hose moves between them after steam is diverted to the vent, which wastes about 1 minute of steam per setting. The rate is the lower of the steam limit, 1.2 m² / (heat time + 1 min), and the hood limit, (number of hoods x 1.2 m²) / (heat time + hold + move).

*Table 3. Treatment rate, m²/h.*

| Hoods | 15 cm | 5 cm |
| --- | --- | --- |
| 1 | 1.12 (hood limited) | 1.70 (hood limited) |
| 2 (decided; R2 restated to these values) | 1.88 (steam limited) | 3.41 (hood limited) |
| 3 | 1.88 (steam limited) | 4.43 (steam limited) |

At 15 cm the second hood removes the hold penalty, and the rate is set by steam. At 5 cm even three hoods reach only the steam limit of 4.43 m²/h, below the former 5 m²/h target, because the hold overshoot is the same 1.53 cm at any depth. Amish decided on 2026-09-25 to restate R2 at the two-hood values, about 1.9 m²/h (1.85 or more) at 15 cm and 3.4 m²/h at 5 cm, until soil tests exist. Both are met with margins under 2 %, so they are marked at risk.

## 4. Combustion, heat transfer and efficiency

**Fuel.** The Channiwala and Parikh correlation gives a dry higher heating value of 20.03 MJ/kg for the assumed analysis, a dry lower heating value of 18.72 MJ/kg, and 14.48 MJ/kg at 20 % moisture. The requirements quoted "about 16 MJ/kg" for wood at 20 % moisture; that value is too high by about 10 % and is corrected in STR-REQ-001 v0.3. Stoichiometric air is 4.76 kg per kilogram of wet fuel, so at λ = 2.0 there are 10.5 kg of flue gas per kilogram of wood.

**Duty.** Raising 30 kg/h of water from 15 °C to dry saturated steam takes 21.78 kW. The economizer supplies 2.44 kW (15 to 85 °C) and cannot exceed 2.97 kW before the feed water boils. The coil supplies 19.34 kW.

**Firebox.** The firebox is treated as one well-stirred zone. Heat to the coil is σ F A (T_g⁴ - T_w⁴) + h A (T_g - T_w) with 14.52 m of tube (1.16 m²) and a 110 °C wall. The gas temperature that gives 19.34 kW is 520 °C. An energy balance on the firebox, including 3.5 kW through the 50 mm lining of the 1000 mm tall firebox (3.44 m² of wall), then gives the firing rate. In the constructable design the coil sits above the fire bed rather than around it (STR-DDR-003, C1); the well-stirred model and the exchange factor range of Table 5 cover both layouts, and the measured value is a TRL 4 matter.

*Table 4. Energy balance at the design point (λ = 2.0, F = 0.40).*

| Quantity | Value |
| --- | --- |
| Firing rate | 42.4 kW (10.5 kg/h of wood) |
| Heat to water (coil plus economizer) | 21.78 kW |
| Stack loss (flue gas leaves the economizer at 451 °C) | 15.4 kW |
| Shell loss through the lining | 3.5 kW |
| Unburned loss | 1.7 kW |
| Fuel to steam efficiency | 51.4 % |
| Firebox outer skin temperature | 99 °C |

*Table 5. Sensitivity of fuel-to-steam efficiency (%).*

| λ | F = 0.25 | F = 0.40 | F = 0.60 |
| --- | --- | --- | --- |
| 1.5 | 55.7 | 60.5 | 64.7 |
| 2.0 | 45.6 | 51.4 | 56.4 |
| 2.5 | 35.6 | 42.3 | 48.1 |

The TRL 2 figure of 62 % assumed 55 % for the firebox and coil without a heat transfer model. Reaching 65 % needs a stack temperature of about 262 °C at λ = 2.0; the current layout gives 451 °C. Preheating the combustion air by 135 K with flue heat lifts efficiency to 59.8 % (stack 334 °C, 9.0 kg/h of wood). In Table 5 no corner reaches 65 %; λ = 1.5 with F = 0.60 comes closest at 64.7 %, so R5 needs both tighter air control and better heat transfer to the water (more coil surface in the flue, or better radiant exposure). Amish decided on 2026-09-25 to keep the R5 and R4 targets and to study a convective evaporator bank in the flue with controlled primary and secondary air (STR-DDR-002). The study is below; the baseline design is unchanged until the next paper iteration.

**R5 study: evaporator bank and controlled air.** For a target efficiency the firing rate is fixed (33.5 kW, 8.3 kg/h of wood for 65 %). The firebox balance then sets the gas temperature and the heat the coil in the firebox takes by radiation and convection. The rest of the coil duty must come from a bank of evaporator tube in the flue between the firebox and the economizer, with water boiling at 100 °C inside.

*Table 5a. Evaporator bank needed for 65 % (F = 0.40, U = 30 W/(m² K)).*

| Excess air λ | Firebox gas | Coil in firebox | Bank duty | Gas across the bank | Bank area | 25.4 mm tube | Stack |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.5 | 505 °C | 18.19 kW | 1.15 kW | 505 to 452 °C | 0.10 m² | 1.3 m | 339 °C |
| 2.0 | 475 °C | 16.13 kW | 3.21 kW | 475 to 360 °C | 0.34 m² | 4.3 m | 273 °C |

At λ = 2.0 about 4.3 m of the existing tube size, run as a continuation of the monotube in the flue, reaches 65 %. With air held near λ = 1.5 about 1.3 m is needed, but a hand-fed batch firebox rarely holds that ratio. A bank of about 4 m with a primary and secondary air damper is the likely next paper design. It adds water volume, mass and pressure drop. Flooded, 4.3 m of 22.1 mm bore holds about 1.7 L, which would take the heated section to about 8.6 L, over the 8 L limit in R7, so the next iteration must shorten the firebox coil, use a smaller bank tube or revisit R7, and check R6 and R11 again.

Even at 65 %, wood use is 4.44 kg/m² at 15 cm. R4 (4 kg/m²) needs about 72 % fuel-to-steam efficiency at the current steam demand, so R4 will stay not met unless steam per square meter also falls, for example through less skirt leakage.

**Economizer.** With a log mean temperature difference of 436 K and U = 25 W/(m² K), the economizer needs 0.22 m² of tube; the constructable tube bank, about 7.3 m of 12.7 mm tube bent on a standard 38 mm radius, gives 0.29 m². The flue gas holds 9.6 % water vapor by volume, so its dew point is about 45 °C. The cold end of the economizer, fed at 15 °C, will run wet with acidic condensate, which confirms the stainless tube and the condensate drain.

**Wood per square meter.** With two hoods, 10.5 kg/h of wood treats 1.88 m²/h at 15 cm, which is 5.61 kg/m² against the 4 kg/m² target. At 5 cm it is 3.09 kg/m².

## 5. Steam-side pressure

The coil bore is 22.1 mm. At 30 kg/h the mass flux is 21.7 kg/(m² s) and dry steam would move at 36.3 m/s (Reynolds number 39,033). The two-phase friction gradient comes from the Müller-Steinhagen and Heck correlation, averaged over a quality that rises linearly along the boiling length, times a helical-coil factor of 1.26 (Ito).

*Table 6. Pressure build-up at 30 kg/h.*

| Element | Pressure drop |
| --- | --- |
| Coil friction (two-phase mean 358 Pa/m, all-vapor 401 Pa/m) | 6,398 Pa |
| Coil acceleration | 789 Pa |
| Coil gravity | 18 Pa |
| Outlet riser to the header | 352 Pa |
| **Coil total** | **7,557 Pa** |
| Hose, 6 m at 28.4 m/s, with fittings | 2,546 Pa |
| Hood manifold (assumed) | 500 Pa |
| Hood, at most its lift pressure | 235 Pa |
| **Header pressure** | **3,281 Pa (0.033 bar gauge)** |
| **Coil inlet pressure** | **10,838 Pa (0.108 bar gauge)** |

The 1 m water seal (hot water, 958 kg/m³) opens at 9,402 Pa (0.094 bar gauge), which leaves 6,121 Pa of margin at the header, so steam goes to the hood in normal use and vents only if the hose or hood blocks. Amish decided on 2026-09-25 to redefine R6 as 0.1 bar gauge at the header, where the vent limit applies, and 0.15 bar gauge at the coil inlet. Both are met: 0.033 bar at the header and 0.108 bar at the coil inlet.

**Seal geometry.** When the header pressure pushes water down the dip leg, the same volume rises in the annulus between the dip leg and the pot wall, and that rise adds to the head the steam must overcome. With a 42.2 mm dip leg in a 114.3 mm pot the annulus area is 8.1 times the dip leg bore, so the water outside rises 0.124 mm for each millimetre it falls inside. The constructable design therefore ends the dip leg 890 mm below the static water mark: 890 mm down plus 110 mm up is the 1.0 m effective head, 9,402 Pa, used above (STR-DDR-003, C6). A dip leg a full 1 m deep would have let the header reach about 0.11 bar and would have pushed water up into the vent.

**Flow stability.** A single coil fed by a positive-displacement diaphragm pump is not prone to the parallel-channel or Ledinegg instabilities of multi-tube boilers, and 15 K of inlet subcooling helps. At this low mass flux the flow will be stratified or wavy in the helix, so the top of the tube will dry out before the outlet and run hotter than the 110 °C wall assumed. At 0.07 MPa hoop stress this does not threaten the tube, but it will speed scaling.

## 6. Stored water, dry coil and relief valve

**Stored water.** Flooded, the coil holds 5.57 L, the economizer 0.61 L and the header 0.75 L: 6.93 L in total, under the 8 L limit.

**Dry coil and refeed.** The coil tube weighs 14.3 kg. If it runs dry it approaches the 520 °C firebox gas temperature and stores 3.00 MJ, enough to flash 1.29 kg of feed water. If the pump restarts and that happens over 30 s, the steam flow is 155 kg/h, 5.2 times the design flow, and the coil drop would scale to about 2.0 bar. The open vent and the 15 psi relief valve are sized for 30 kg/h, not for this event. The tube itself is not at risk from pressure: hoop stress is 0.073 MPa in normal use and 2.0 MPa at the pump's 3 bar shut-off, against a yield strength of roughly 100 MPa for 316 at 700 °C (typical handbook value). The hazard is steam and scalding water thrown from joints and the hose, which is why the coil outlet alarm and the rule never to refeed a hot, dry coil stay essential.

**Relief valve.** Napier's formula, with 10 % accumulation over a 15 psi (1.034 bar) set pressure and a derated coefficient of 0.878, needs a 30.2 mm² orifice (6.2 mm) for 30 kg/h and 157 mm² (14.1 mm) for the 155 kg/h refeed flash. The maker's capacity table for the Watts Series 315 gives 375 lb/h (170 kg/h) for the 3/4 in valve at 15 psi, which covers the refeed flash with about 10 % margin. On 2026-09-25 Amish decided to reword R9 to "15 psi (1.03 bar) or less", the lowest standard certified set pressure, and to size the valve for the refeed flash as well as for 30 kg/h (STR-DDR-002). R9 is met on paper; the capacity must be confirmed for the valve actually bought.

## 7. Mass, envelope and cost

*Table 7. Loaded mass with a full tank.*

| Item | Mass |
| --- | --- |
| Trailer (tare, assumed) | 160.0 kg |
| Firebox (shell, fiber lining, grate, door; 1000 mm tall) | 125.2 kg |
| Monotube coil | 14.3 kg |
| Economizer | 18.0 kg |
| Chimney and cap | 4.5 kg |
| Header, seal pot, vent, relief valve | 18.0 kg |
| Seal water | 9.1 kg |
| Tank, empty | 8.0 kg |
| Feed water, full tank | 125.0 kg |
| Pump and battery | 8.0 kg |
| Steam hose | 5.4 kg |
| Hoods, 2 off | 57.5 kg |
| Instruments, alarms, safety kit | 8.0 kg |
| Supports and lines added for construction (skids, header post, pot stay and foot plate, saddles, coil brackets, grate stand, gland plates, damper, feed lines, vent line and discharge, roof frame, unions) | 41.0 kg |
| **Total** | **602 kg** |

The loaded mass is 602 kg with a full tank. Amish decided on 2026-09-25 that R11 applies as towed, with the tank and seal pot drained and filled on site, which gives 468 kg against 500 kg. The parts added for construction weigh 37.4 kg by volume in the model (`python cad/src/model.py --mass`), rounded up to 41 kg for the roof frame and unions. A castable refractory lining would raise the firebox from 125 kg to 406 kg, so the fiber lining is needed for R11. Overall width is 1.48 m against 1.5 m. The chimney outlet is 2.40 m above ground, and one fill of the tank lasts 4.17 h.

The priced BOM (`bom/bom.csv`, 21 lines) totals USD 2,275.00. Value-engineering target: USD 2,200 (`budget_usd`, a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 2,275 (USD 75 over the target). The parts added for construction account for USD 360 of it (STR-DDR-003). Only the relief valve price was checked against a live listing; the rest are indicative.

## 8. Results against requirements

*Table 8. Requirement status, not met items first. Status words: met, not met, at risk, not verifiable at TRL 3.*

| ID | Requirement | Calculated value | Target | Status |
| --- | --- | --- | --- | --- |
| R4 | Wood per m² at 15 cm | 5.6 kg/m² | 4 kg/m² or less | Not met |
| R5 | Fuel to steam efficiency | 51 % | 65 % or more | Not met |
| R2 | Treatment rate at 15 cm, two hoods | 1.88 m²/h | 1.85 m²/h or more (about 1.9) | At risk (thin margin) |
| R2 | Treatment rate at 5 cm, two hoods | 3.41 m²/h | 3.4 m²/h or more | At risk (thin margin) |
| R11 | Overall width | 1.48 m | 1.5 m or less | At risk (thin margin) |
| R1 | Soil at 70 °C for 20 to 30 min at 15 cm over 80 % of the footprint | Front to 16.5 cm holds 70 °C at 15 cm for 25 min in the 1D model; skirt leakage and permeability not quantified | 70 °C, 20 to 30 min | Not verifiable at TRL 3 |
| R3 | Steam output | 30 kg/h with firebox gas at 520 °C and 42.4 kW firing | 30 kg/h or more | Met |
| R6 | Normal pressure at the header; open vent | 0.033 bar gauge; vent cannot be isolated | 0.1 bar gauge or less | Met |
| R6 | Normal pressure at the coil inlet | 0.108 bar gauge | 0.15 bar gauge or less | Met |
| R7 | Water in heated section, flooded | 6.9 L | 8 L or less | Met |
| R8 | Steaming per fill | 4.2 h | 3 h or more | Met |
| R9 | Certified relief valve, set pressure and capacity | 15 psi (1.03 bar) set; rated 170 kg/h against a 155 kg/h refeed flash | 15 psi (1.03 bar) or less; capacity for the flash | Met |
| R10 | Chimney outlet, spark arrestor mesh, hood handles | 2.4 m, 6 mm mesh, hood outer skin 23 °C | 2.2 m, 6 mm, 60 °C | Met |
| R11 | Mass as towed, tank and seal pot drained | 468 kg (602 kg full) | 500 kg or less | Met |
| R12 | Parts cost against the value-engineering target | USD 2,275 | USD 2,200 target | USD 75 over the target |

Summary: 2 not met (R4, R5), 3 at risk (R2 twice, R11 width), 1 not verifiable at TRL 3 (R1), 8 met (R3, R6 twice, R7, R8, R9, R10, R11 mass); R12 is USD 75 over the value-engineering target. The constructable design (version 0.3) changed no status; R4 and R5 moved further from their targets. In version 0.1, against the earlier targets, 7 were not met, 2 at risk, 1 not verifiable and 4 met.

## 9. Limits of this note

- The firebox is one well-stirred zone. Real fireboxes have a hot flame zone and cooler corners; the exchange factor F and excess air λ carry most of the uncertainty (Table 5).
- The soil model is one-dimensional with a sharp front and no fingering, no lateral loss at the skirt beyond the assumed 10 %, and no change in permeability as condensate wets the soil.
- The two-phase pressure drop uses correlations developed for straight tubes with a curvature factor; the error band is about ±30 %.
- Prices are indicative except where the BOM names a checked listing.
- Nothing here has been tested. Every result needs measurement at TRL 4, which is on hold by Amish's instruction.

> **Safety:** Steam at 100 °C causes deep burns in under a second. The permeability result means steam may jet from under the hood skirt in finer soils. The dry-coil refeed result means a restart into a hot coil can throw steam at five times the design flow. The firebox skin reaches about 100 °C and the flue about 450 °C. Carbon monoxide from the fire is lethal in enclosed spaces. None of these hazards is controlled by this calculation.

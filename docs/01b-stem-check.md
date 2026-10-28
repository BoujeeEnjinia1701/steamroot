---
doc_id: STR-STM-001
title: SteamRoot STEM check
project: SteamRoot
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First STEM check (kit 1.9.1 upgrade): 37 claims for the design (option A) and 7 for option B; S6, S7, S12, E2 and C5 fixed under the standing instruction of 2026-10-23 (STR-DEC-001 S1, S3, S4); S11 and B4 sent to Amish; independent review recorded"
---

# SteamRoot STEM check

Verdict: the working principle of SteamRoot (a once-through, open-vented coil fired with wood, delivering steam to hoods on the soil) sits within known science, and no claim fails outright. Four details failed and were fixed in this session under Amish's standing instruction of 2026-10-23, keeping the principle:

- **Gas side of the bank and economizer (S6, S7).** The calculation had assumed 30 and 25 W/(m2 K). The flue gas creeps through those boxes at about 0.1 m/s, where a tube-bank correlation gives about 11. Gas-pass baffles make it cross the tubes at about 1 m/s (STR-DEC-001 S1).
- **Draft (S12).** Once the fuel bed is counted, the 2.4 m chimney leaves almost no draft for the dampers. The outlet is raised to 3.2 m (S3).
- **Dry-coil control (E2).** A stalled pump could restart by itself into a hot, dry coil. The alarm now latches the pump off until it is reset by hand (S4).
- **Baffle material (C5).** The economizer baffles are 316L for the acid condensate (S1).

Two claims fail with fixes that change how the machine is used, so they go to Amish: steam passing through finer soils under the hood (S11, DEC #18) and one person lifting a hood (B4, DEC S2). Six claims are plausible and stay open until TRL 4 measurements or decisions: firebox heat exchange (S5), the refeed flash basis (S15 to S17, DEC #20), the net treatment rate (M2) and the battery (E3). So `stem_check: open`. With every fix in, fuel-to-steam efficiency is 66.1 % at λ = 1.5 against the 65 % target, a margin smaller than several of its uncertainties (STR-CAL-001 v0.5, Table 6a). Option B has one row that fails with a fix (OB5).

Method: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which imports STR-CAL-001 v0.5 (`docs/04-calcs/sizing.py`) and writes `stem_results.csv` and `options_results.csv`.

> **Safety:** This check screens the science; it does not make SteamRoot safe or legal to build. The written ruling from the Texas Department of Licensing and Regulation's boiler program is an open prerequisite for any build (STR-REG-001, R1).

## Claims checked

Table 1. Claims, governing science and verdicts for the design (option A), from `stem_results.csv`.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Raising 30 kg/h of feed water at 15 °C to dry saturated steam takes 21.78 kW | Physics | Thermodynamics | Steady-flow energy equation; latent heat 2.257 MJ/kg | 21.78 against 21.8 kW | Within known science | STR-CAL-001 v0.5 section 4 |
| S2 | Fuel energy 32.9 kW equals heat to water plus stack, shell and unburned losses | Physics | Thermodynamics | First law over firebox, bank, economizer and chimney | In 32.9 kW, out 32.9 kW (closes by construction: an arithmetic check) | Within known science | STR-CAL-001 v0.5 Table 5 |
| S3 | Fuel-to-steam efficiency 66.1 % stays below the first-law ceiling set by the unburned loss alone | Physics | Thermodynamics | Efficiency at most 1 minus the unburned fraction | 66.1 % against 96 % (a bound, not evidence the value is right) | Within known science | STR-CAL-001 v0.5 section 4 |
| S4 | The coil takes 17.5 kW (16.6 kW/m2) from firebox gas at 519 °C | Physics | Heat transfer | Radiant exchange σF(Tg⁴ - Tw⁴) with F = 0.40 plus convection at 20 W/(m2 K), bounded by black-body exchange at the same gas temperature | 16.6 against 29.3 kW/m2 | Within known science | STR-CAL-001 v0.5 section 4 |
| S5 | Exchange factor F = 0.40 and coil convection 20 W/(m2 K) in a hand-fed firebox | Physics | Heat transfer | Single-zone firebox model; F and h set by flame luminosity and plume velocity | PR-005 met for F = 0.40 to 0.60, missed at 0.25 (63.8 %); the correlation at the mean firebox velocity gives about 9 W/(m2 K), which costs 2.6 points | Plausible, to confirm at TRL 3 | Open: flue temperature and oxygen at TRL 4 |
| S6 | Bank gas-side coefficient 24.0 W/(m2 K) clean, 22.4 with fouling, gas crossing the tubes at 1.0 to 1.1 m/s with 10 % edge bypass | Physics | Heat transfer | Zukauskas in-line tube-bank correlation, row factor per pass, gas radiation (emissivity 0.06), fouling 0.003 m2 K/W; checked against Hilpert's correlation | 24.0 against 26.2 W/(m2 K) (ratio 0.92). **Failed before the fix:** v0.4 assumed 30 W/(m2 K) where the gas, unbaffled, gives about 10 | Within known science (was Fails, fix proposed) | STR-DEC-001 S1 (gas-pass baffles) |
| S7 | Economizer gas-side coefficient 23.0 W/(m2 K) clean, 21.5 with fouling, three baffled passes at 0.7 to 1.0 m/s | Physics | Heat transfer | As S6 | 23.0 against 28.2 W/(m2 K) (ratio 0.81). **Failed before the fix:** v0.4 assumed 25 where the gas, unbaffled, gives 12 | Within known science (was Fails, fix proposed) | STR-DEC-001 S1 |
| S8 | Firebox outer skin 99 °C behind 50 mm of ceramic fibre (about 135 °C where the hot face nears 700 °C) | Physics | Heat transfer | Series conduction (k 0.12 W/(m K)) and a 12 W/(m2 K) outside film | 99 °C against 519 °C gas; a contact-burn hazard no requirement yet limits | Within known science | STR-CAL-001 v0.5 Table 5; skin limit proposed (DEC #21) |
| S9 | The steam front must reach 16.5 cm so that 15 cm stays at 70 °C through a 25 min hold | Physics | Heat transfer | Two semi-infinite bodies in contact, erf profile | 1.53 against 1.53 cm overshoot (1.25 to 1.77 cm for k 0.8 to 1.6) | Within known science | STR-CAL-001 v0.5 section 2 |
| S10 | Heating 16.5 cm of moist soil by 85 K takes 30.6 MJ/m2 | Physics | Thermodynamics | Q = ρc ΔT V | 30.6 against 30.6 MJ/m2 (conduction ahead of the front adds about 4 %) | Within known science | STR-CAL-001 v0.5 section 2 |
| S11 | Steam passes down through 16.5 cm of soil at full flow without lifting the 256 Pa hood | Physics | Fluid mechanics | Darcy's law at 1.16 cm/s; permeability 10⁻¹⁰ (sand) to 10⁻¹² m2 (loam), textbook ranges | Needs 236 Pa in sand (92 % of the lift), 2,362 Pa in sandy loam, 23,617 Pa in loam against 256 Pa (583 Pa with 40 kg of ballast); moist soil passes gas less well still | Fails, fix proposed | To Amish (STR-DEC-001 #18): bed preparation, stakes or straps, a deeper skirt, a larger hood or a lower steam flux; TRL 4 soil tests decided 2026-10-02 |
| S12 | Natural draft 16.8 Pa covers the gas-side losses (11.4 Pa, fuel bed included) and the damper openings at λ = 1.5 | Physics | Fluid mechanics | Stack effect over 2.50 m at a mean 400 °C; fuel bed (3 Pa, Ergun estimate), holes, baffled passes, chimney and cap; openings at Cd 0.6 | 7,530 mm2 needed against 12,600 mm2. **Failed before the fix:** with the 2.4 m chimney and the fuel bed counted, 0.1 Pa was left | Within known science (was Fails, fix proposed) | STR-DEC-001 S3 (chimney outlet 3.2 m) |
| S13 | Normal pressure at the bank inlet, the highest on the steam side, 0.129 bar | Physics | Fluid mechanics | Müller-Steinhagen and Heck two-phase friction over the whole coil from the bank's outlet quality, Ito's coil factor; bank bends at 0.3 velocity heads | 0.129 against 0.15 bar (correlations about ±30 %) | Within known science | STR-CAL-001 v0.5 section 5 |
| S14 | The water seal blows at 0.084 bar, above the 0.033 bar header pressure | Physics | Fluid mechanics | Hydrostatics, 890 mm dip leg in water at 100 °C | 8,365 against 3,301 Pa; diverted steam goes up the vent pipe above the pot, not through the seal | Within known science | STR-CAL-001 v0.5 section 5 |
| S15 | The 350 mm overflow loop seal holds against the head-space back pressure of a refeed flash | Physics | Fluid mechanics | Hydrostatics against vent friction and exit loss | 3,291 against 2,453 Pa (about 16 % on flow) for a flash basis that is not bounded | Plausible, to confirm at TRL 3 | Open: to Amish (DEC #20) |
| S16 | The 3/4 in, 15 psi certified valve passes the 141 kg/h dry-coil refeed flash | Physics | Fluid mechanics | Napier's formula; maker's capacity table, 375 lb/h (Watts Series 315) | 170 against 141 kg/h (21 %); the valve and seal sit at the header, downstream of the coil where a flash builds about 1.5 bar | Plausible, to confirm at TRL 3 | Open: to Amish (DEC #20) |
| S17 | A dry coil at 519 °C stores 2.73 MJ and flashes 1.17 kg of refeed water | Physics | Thermodynamics | Stored heat of 13 kg of 316 tube against the feed's latent and sensible heat | 1.17 against 1.13 kg; but a dry coil no longer cools the gas and may reach 700 to 800 °C (about 2 kg) | Plausible, to confirm at TRL 3 | Open: to Amish (DEC #20) |
| S18 | Coil hoop stress at the 3 bar pump shut-off stays far below the yield of 316 at 700 °C | Physics | Strength of materials | pD/2t; 316 hot yield about 100 MPa | 2.0 against 100 MPa | Within known science | STR-CAL-001 v0.5 section 6 |
| S19 | Hood handle bar with half of 40 kg of ballast at mid-span and a load factor of 2 stays below yield | Physics | Strength of materials | M = FL/4 on 30 x 30 x 2.5 SHS; S235 | 33.7 against 235 MPa (the skin, block and backing plate are not checked) | Within known science | STR-CAL-001 v0.5 section 7 |
| C1 | Wood at 20 % moisture (wet basis) gives 14.48 MJ/kg lower heating value | Chemistry | Physical chemistry (thermochemistry) | Channiwala and Parikh correlation, less latent heat of product and fuel water | 14.48 against 14.7 MJ/kg; efficiencies are on this LHV basis (about 61 % on HHV) | Within known science | STR-CAL-001 v0.5 section 4 |
| C2 | Stoichiometric air 4.76 kg per kg of wet fuel | Chemistry | Physical chemistry (stoichiometry) | Combustion of C and H less fuel oxygen | 4.76 against 4.76 kg/kg | Within known science | STR-CAL-001 v0.5 section 4 |
| C3 | Flue gas at λ = 1.5 holds 12.5 % water vapour; dew point 51 °C, so the cold end of the economizer runs wet | Chemistry | Environmental and atmospheric chemistry | Dalton's law and the Antoine equation (air humidity adds about 1.5 K) | 51 °C against a 15 to 20 °C tube wall | Within known science | STR-CAL-001 v0.5 section 4 |
| C4 | Wood fires make carbon monoxide, and less excess air raises the CO made | Chemistry | Physical chemistry (kinetics) | Incomplete combustion where mixing or temperature is poor | Firebox and chimney outdoors only; personal CO alarm; the 4 % unburned loss is an assumption (6 % costs 1.8 points) | Within known science | STR-PRC-001 Safety; STR-RSK-001 H5 |
| C5 | 316 stainless coil, bank and economizer tube; 304 bank baffle; 316L economizer baffles for the acid condensate | Chemistry | Materials and polymer chemistry | Passive chromium oxide film; wood condensate carries organic acids and some chloride; welded 316 sensitizes at 450 to 850 °C | Economizer baffles changed from 304 to 316L after the review; low-carbon filler for coil welds | Within known science | STR-DEC-001 S1 |
| B1 | Holding soil at 70 °C or more for 20 to 30 min kills most weed seeds and soil-borne pathogens | Biology | Microbiology and ecology | 71 to 82 °C (160 to 180 °F) for 30 min (MSU Extension P4033); 60 to 82 °C for 30 min (NCAT 2022) | In the model 15 cm spends about 29 min at 70 °C or more after cooling from 100 °C, inside both | Within known science | PR-001 target; cited sources |
| B2 | Soil behind the steam front reaches 100 °C for most of the hold, above the 82 °C ceiling extension guidance gives | Biology | Ecology and agronomy | MSU P4033: above 82 °C can harm soil structure; NCAT 2022: overheating kills nitrifying bacteria | Known side effect of saturated steam, accepted and carried as a risk | Within known science | STR-RSK-001 H9 |
| B3 | Condensing steam on skin causes deep burns within about a second | Biology | Human physiology | Latent heat of 2.26 MJ/kg released on contact | Divert to the vent before lifting a hood; PPE; 5 m exclusion | Within known science | STR-RSK-001 H1, H2 |
| B4 | One operator lifts and resets a 31.3 kg hood, 1.2 x 1.0 m, by its two side handles 1.12 m apart | Biology | Ergonomics | Revised NIOSH lifting equation: load constant 23 kg in ideal conditions; with the horizontal multiplier for a load held 40 to 60 cm out, about 10 to 14 kg | 31.3 against 23 kg; a two-person share of 15.6 kg is borderline | Fails, fix proposed | To Amish (STR-DEC-001 S2; PR-016): a hood wheel kit or lifting aid |
| M1 | 15.6 kg of steam per m2 at 15 cm | Mathematics | Units and dimensional analysis | (soil + hood heat) / latent heat / (1 - skirt leakage) | 15.6 against 15.6 kg/m2 (hose and header losses not counted) | Within known science | STR-CAL-001 v0.5 section 2 |
| M2 | Two hoods treat 1.88 m2/h at 15 cm | Mathematics | Orders of magnitude | Steam-limited rate less one vented minute per changeover | 1.88 against 1.93 m2/h; an unheated 4 cm edge strip, overlap between settings and hose losses would cut it to about 1.5 to 1.6 m2/h | Plausible, to confirm at TRL 3 | Open: TRL 4 |
| M3 | Heated section holds 7.32 L of water flooded | Mathematics | Units and dimensional analysis | Bore area x length of coil, bank, economizer and header (the seal pot's water is not in the heated section) | 7.32 against 8 L | Within known science | STR-CAL-001 v0.5 section 6 |
| M4 | One 125 L fill lasts 4.17 h at 30 kg/h | Mathematics | Orders of magnitude | Volume / flow (gross volume) | 4.17 against 4.17 h | Within known science | STR-CAL-001 v0.5 section 7 |
| M5 | Every efficiency, rate and pressure is a point estimate with a stated band | Mathematics | Statistics and uncertainty | Sensitivity tables for λ, F, unburned loss, moisture, firebox convection and fouling | PR-005's 1.1-point margin is smaller than each of several uncertainties | Within known science | STR-CAL-001 v0.5 Tables 6 and 6a |
| E1 | The steam side can never be isolated from the vent | Engineering and technology | Standards practice | Open-vent principle; Texas Health and Safety Code 755.022(a)(4) asks for two independent means to prevent pressure build-up | Water seal and certified relief valve; whether these satisfy 755.022(a)(4) is for the TDLR ruling (PR-017) | Within known science | STR-PRC-001; STR-REG-001 R1 |
| E2 | A stalled feed pump can never restart by itself into a hot, dry coil | Engineering and technology | Control | A dry coil heats at about 2.6 K/s: about 16 to 20 s to 150 °C | **Failed as first written** (alarm only; "2 to 3 min" was the time constant); fixed by a latching relay that cuts the pump until reset by hand | Within known science (was Fails, fix proposed) | STR-DEC-001 S4 (latching pump trip) |
| E3 | The 12 V 20 Ah lead-acid battery runs the pump and alarms through one 4.2 h fill | Engineering and technology | Power and link budgets | Charge = current x time; pump current ASSUMED 4 A; a 20 h-rated battery gives about 15 to 16 Ah at 4 A | 16.7 Ah per fill: about 100 % depth of discharge | Plausible, to confirm at TRL 3 | Open: pump datasheet; battery size (DEC #16) |
| E4 | The bank serpentine fits inside the lined box with 25 mm at the bends | Engineering and technology | Manufacturing tolerances | Bend apex 290 mm from the box centre, lining face at 323 mm | 25 against 5 mm | Within known science | Model fit checks; `cad/fidelity.json` |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**. The kit's verdict text says "TRL 3"; for a repo already at TRL 3 these rows are confirmed at TRL 4, which is on hold.

Summary for option A: 29 within known science (S6, S7, S12 and E2 after their fixes), 6 plausible and open, 2 fail with a fix proposed to Amish, 0 fail.

### The rows that failed and their fixes

**S6 and S7, gas side.** Version 0.4 assumed overall coefficients of 30 and 25 W/(m2 K) in the evaporator bank and economizer. In the model the flue gas (about 18 g/s, 0.035 m3/s at 400 °C) rises through the whole 646 x 546 mm bank box and the 516 x 456 mm economizer box at about 0.1 m/s. There the Zukauskas correlation gives about 10 W/(m2 K) in the bank and 12 in the economizer, and the design would make 59.8 %.

Fixes weighed (STR-DEC-001 S1):

- (a) Gas-pass baffles, with the flue openings moved so the gas crosses each layer of tubes sideways.
- (b) A longer bank, which would push the heated water past R7.
- (c) A smaller-bore bank, which would push the bank inlet past R6.
- (d) Thicker linings, which would cost about 15 kg against R11.

Option (a) keeps the working principle, the water volume and the steam-side pressures, and was implemented: a 1.5 mm 304 baffle in the bank box and two 1 mm 316L baffles in the economizer. The reviewed coefficients are 22.4 and 21.5 W/(m2 K), counting fouling, 10 % edge bypass and the row factor per pass.

**S12, draft.** Once the reviewer counted the fuel bed and grate (about 3 Pa by an Ergun estimate), the gas-side losses rose to 11.3 Pa against the 11.4 Pa that a 2.4 m outlet gives, leaving the dampers nothing. Raising the outlet to 3.2 m (STR-DEC-001 S3, about USD 60, 2.4 kg) gives 16.8 Pa and leaves 5.4 Pa. The dampers then need 7,530 of their 12,600 mm2 at λ = 1.5. Wide open they reach about λ = 1.6, so the old "dampers open at λ = 2.0" case is now only a sensitivity. Raising the outlet does not change PR-010, which asks for at least 2.2 m.

**E2, dry-coil control.** The alarm only warned, and a pump that stalls on a weak battery and recovers would refeed a hot coil unattended. A latching relay now cuts the pump on a coil alarm until it is reset by hand (STR-DEC-001 S4, about USD 10).

**C5, condensate.** The economizer baffles changed from 304 to 316L (S1).

### Option B rows

Table 2. Option B (vented fire-tube kettle) claims, from `options_results.csv`.

| # | Claim | Field | Branch | First-order check | Verdict |
| --- | --- | --- | --- | --- | --- |
| OB1 | The kettle holds about 70 L of water at 100 °C (A: 7.3 L heated) | Mathematics | Units | 70 against 68 L | Within known science |
| OB2 | Without an economizer the kettle's efficiency (about 50 %) stays below option A's | Physics | Thermodynamics | 50 against 66.1 % | Within known science |
| OB3 | The pool boils without film boiling on the fired floor | Physics | Heat transfer | 49 kW/m2 against Zuber's critical flux of about 1,100 kW/m2 | Within known science |
| OB4 | A seal blow at 0.084 bar flashes only about 0.3 kg of the pool | Physics | Thermodynamics | 0.28 against 0.29 kg | Within known science |
| OB5 | The flat 3 mm kettle walls hold the relief valve set pressure (1.03 bar) if the water seal freezes or blocks | Physics | Strength of materials | Flat-plate bending about 1,160 MPa against 235 MPa | Fails, fix proposed (a second independent open vent and stiffened walls, if B were chosen) |
| OB6 | Start-up takes about 25 min to bring the pool to the boil at about 16 kW | Mathematics | Orders of magnitude | 24.5 against 24.6 min | Within known science |
| OB7 | A float switch running the pump keeps the pool level | Engineering and technology | Control | Large-capacity on-off level control is stable | Within known science |

## Fields not relevant

- Physics, electromagnetism and circuits: the only circuit is a 12 V pump and alarm; its energy budget is row E3.
- Physics, optics and radiation: thermal radiation is treated under heat transfer (S4 to S7); there is no other optical or ionising radiation.
- Physics, acoustics and vibration: venting steam is loud, which the safety notes cover; no design claim depends on sound or vibration.
- Physics, nuclear and ionising radiation: none.
- Chemistry, electrochemistry and batteries: a sealed lead-acid battery, chosen to avoid lithium beside a fire; no claim beyond capacity (E3).
- Chemistry, analytical and organic: no analysis or organic reaction is claimed beyond the condensate note in C5.
- Biology, toxicology and epidemiology: carbon monoxide is covered under chemistry and safety (C4); no dose or population claim.
- Biology, plant biology: crop response after steaming is not claimed; the beneficial-organism loss is row B2.

## Concept options

- **Option A, monotube coil generator (the design):** no Fails row; S6, S7, S12, E2 and C5 fixed; S11 and B4 to Amish; six plausible rows open. Carried as the current design.
- **Option B, vented fire-tube kettle:** no Fails row; OB5 fails with a fix (a second independent open vent and stiffened kettle walls) that would be needed if B were chosen; it shares A's hood and soil rows (S9 to S11, B1 to B4) and its draft question.

## Independent review

On 2026-10-25 a separate headless Claude session (`claude -p`, no tools) that had not seen the author's reasoning was given only this STEM check, STR-CAL-001, STR-PRS-001 and `sizing.py`. It was asked to refute the headline results and every "Within known science" verdict. A first attempt over all rows returned no usable output (its answer was withheld by a content filter partway through), so the review was rerun in three scoped parts: combustion, heat transfer and draft; steam-side pressure, relief and control; soil, chemistry, biology and arithmetic. It reproduced the arithmetic of almost every row. What it found, and what changed:

Table 3. Independent review findings and responses.

| Finding | Response |
| --- | --- |
| Draft: the fuel bed and grate were not counted; with an Ergun estimate of 2 to 5 Pa the dampers were starved. A code bug reused the λ = 1.5 net draft for the λ = 2.0 opening | Fixed: bed loss added (3 Pa at the design flow, scaling with flow squared); draft worked out for each λ; S12 failed and was closed by raising the chimney outlet to 3.2 m (S3); dampers wide open now reach about λ = 1.6 |
| Gas side optimistic: row factor taken over all rows instead of per pass, gas emissivity 0.08 high (0.05 to 0.06), no fouling, baffle-edge bypass of 15 to 20 % | Fixed in CAL: row factor per pass, emissivity 0.06, fouling 0.003 m2 K/W, 10 % bypass. Efficiency 67.6 % fell to 66.1 % |
| Efficiency is a best case: unburned loss fixed at 4 %, firebox convection 20 W/(m2 K) where the correlation gives about 9, λ hard to hold, transients excluded; the reviewer's estimate is about 61 % (58 to 66 %) | Partly accepted: sensitivities added (CAL Table 6a: 6 % unburned 64.3 %, firebox convection 10 W/(m2 K) 63.5 %, λ = 1.6 64.9 %, 30 % moisture 65.3 %). PR-005 stays at risk, with its margin smaller than each of these; S5 open |
| S8: 98 °C skin is for the exit gas temperature; near the fire bed about 135 °C; no requirement limits it | Recorded in S8; a firebox skin limit and guard proposed (DEC #21) |
| S13: the coil friction used the v0.3 boiling fraction; bank bends were a 10 % allowance | Fixed: whole coil two-phase from the bank's outlet quality; 20 bends at 0.3 velocity heads; bank inlet 0.123 to 0.129 bar |
| S15 to S17: the refeed flash basis (30 s, coil at the loaded gas temperature) is not bounded; a dry coil may reach 700 to 800 °C (about 2 kg); the seal and valve sit downstream of the coil | Accepted: rows moved to plausible and open; vent and relief sizing for a bounded flash, or a relief upstream of the coil, proposed to Amish (DEC #20) |
| S14: diverted steam might pass through the seal and raise the inlet to 0.17 bar | Rebutted: the diverter's vent line joins the DN32 vent pipe above the seal pot, so diverted steam does not pass through the seal (model, `vent_line`) |
| E2: the time to 150 °C is about 16 to 20 s, not 2 to 3 min; a stalled pump could restart into a hot coil | Fixed: wording corrected; latching pump trip with a manual reset (S4) |
| E3: a 20 Ah battery gives only about 15 to 16 Ah at 4 A, so nearly 100 % depth of discharge | Recorded; battery size proposed (DEC #16) |
| S11 should be Fails: only clean sand passes, at 92 % of the lift; the skirt leakage does not depend on permeability | Accepted: S11 is "Fails, fix proposed" to Amish (DEC #18), since the fixes change how the machine is used |
| M2: edge losses, overlap and hose losses cut the net rate to about 1.5 to 1.6 m2/h | Accepted: M2 plausible and open; PR-002 stays at risk with this noted |
| B4: with the horizontal multiplier the one-person limit is 10 to 14 kg, so a two-person lift is borderline | Accepted: recommendation for S2 changed to a wheel kit or lifting aid |
| C5: wood condensate carries acids and chloride; 304 baffles in the wettest zone; 316 sensitizes in a dry-coil excursion | Fixed: economizer baffles 316L (S1); low-carbon filler noted |
| Mass: tare, contingency and residual water make 540 to 600 kg plausible; `status()` called a value over a maximum "at risk" | `status()` fixed (on the wrong side of a target is "not met"); PR-011 now not met at 509 kg; the range is noted in CAL |
| Code: `A_eco_req` used the superseded U; comment said S12 for S6 and S7 | Fixed |

Not checked by the reviewer and still open: the skin, block and backing-plate strength at the hood handles, thermal-shock stress in the coil on refeed, and the stability of a 1.2 m single-wall chimney in wind.

## Sources

- Channiwala, S. A., and P. P. Parikh. 2002. "A Unified Correlation for Estimating HHV of Solid, Liquid and Gaseous Fuels." *Fuel* 81 (8): 1051-63.
- Hilpert, R. 1933. "Wärmeabgabe von geheizten Drähten und Rohren im Luftstrom." *Forschung auf dem Gebiete des Ingenieurwesens* 4: 215-24.
- Hottel, H. C., and A. F. Sarofim. 1967. *Radiative Transfer.* New York: McGraw-Hill.
- Incropera, F. P., D. P. DeWitt, T. L. Bergman, and A. S. Lavine. 2007. *Fundamentals of Heat and Mass Transfer.* 6th ed. Hoboken, NJ: Wiley. (Zukauskas and Hilpert correlations, air properties.)
- Ito, H. 1959. "Friction Factors for Turbulent Flow in Curved Pipes." *Journal of Basic Engineering* 81: 123-34.
- Mississippi State University Extension. n.d. *Soil Steaming 101.* Publication P4033 (POD-08-24), by S. R. Broderick, T.-M. Tseng, C. Coker, M. Cade, B. Breland and E. Sweeten. https://extension.msstate.edu/publications/soil-steaming-101, accessed October 25, 2026.
- Müller-Steinhagen, H., and K. Heck. 1986. "A Simple Friction Pressure Drop Correlation for Two-Phase Flow in Pipes." *Chemical Engineering and Processing* 20 (6): 297-308.
- National Center for Appropriate Technology (NCAT). 2022. "Soil Steaming for Pathogen, Pest, and Weed Control in High Tunnels." April 12, 2022. https://www.ncat.org/blog/soil-steaming-for-pathogen-pest-and-weed-control-in-high-tunnels/, accessed October 25, 2026.
- Texas Health and Safety Code, section 755.022, Exemptions for Certain Boilers. https://texas.public.law/statutes/tex._health_&_safety_code_section_755.022, accessed October 25, 2026.
- Waters, T. R., V. Putz-Anderson, and A. Garg. 1994. *Applications Manual for the Revised NIOSH Lifting Equation.* DHHS (NIOSH) Publication 94-110. Cincinnati: National Institute for Occupational Safety and Health.
- Watts Series 315 steam safety relief valve capacity table, as used in STR-CAL-001 (item 10 of `bom/bom.csv`).
- Young, W. C., and R. G. Budynas. 2002. *Roark's Formulas for Stress and Strain.* 7th ed. New York: McGraw-Hill.
- Zukauskas, A. 1972. "Heat Transfer from Tubes in Crossflow." *Advances in Heat Transfer* 8: 93-160.
- Zuber, N. 1959. *Hydrodynamic Aspects of Boiling Heat Transfer.* AEC Report AECU-4439.

#!/usr/bin/env python3
"""STR-STM-001 SteamRoot STEM check (STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv (option A, the design) and docs/04-calcs/options_results.csv (option B).
Design values come from STR-CAL-001 v0.5 (docs/04-calcs/sizing.py, imported here); each row is a first-order
screen of one claim against a governing law or a cited source, not the sizing itself. Paper checks only;
nothing here is tested. PRELIMINARY, NOT FOR FABRICATION.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs" / "04-calcs"), str(ROOT / "cad" / "src")]
from stem_check import Check, limits, G, SIGMA, LATENT_WATER, WITHIN, PLAUSIBLE, FIX, FAILS  # noqa: E402,F401
import sizing  # noqa: E402

r = sizing.run()
A = sizing.A
P = sizing.GEO
d = r["design"]
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
CAL = "STR-CAL-001 v0.5"

# ------------------------------------------------------------------ Physics: thermodynamics and heat transfer
duty = A["steam_kg_h"] / 3600 * (A["cp_w"] * (100 - A["t_feed"]) + A["h_fg"])
c.order_of_magnitude("S1", f"Raising 30 kg/h of feed water at 15 C to dry saturated steam takes {r['Q_steam']:.2f} kW", "Physics", "Thermodynamics",
                     claimed=r["Q_steam"], estimate=duty, unit="kW", factor=1.02, law="Steady-flow energy equation; latent heat 2.257 MJ/kg at 1.013 bar (steam tables)",
                     closed_by=f"{CAL} section 4")
c.balance("S2", f"Fuel energy {d['Q_in']:.1f} kW = heat to water + stack + shell + unburned losses", "Physics", "Thermodynamics",
          inputs={"fuel": d["Q_in"]}, outputs={"water": r["Q_steam"], "stack": d["Q_stack"], "shell": d["Q_shell"], "unburned": d["Q_unb"]},
          unit="kW", tolerance=0.01, law="First law over the firebox, bank, economizer and chimney", closed_by=f"{CAL} Table 5")
c.claim("S3", f"Fuel-to-steam efficiency {100*d['eta']:.1f} % stays below the first-law ceiling set by the unburned loss alone", "Physics", "Thermodynamics",
        "First law: efficiency <= 1 - unburned fraction (stack at ambient, no shell loss)", 100 * d["eta"], 100 * (1 - A["f_unburned"]), "%",
        closed_by=f"{CAL} section 4")
q_coil = d["qc"] / d["A_c"]
q_bb = SIGMA * ((d["Tg"] + 273.15) ** 4 - (A["t_wall"] + 273.15) ** 4) / 1000 + A["h_conv"] * (d["Tg"] - A["t_wall"]) / 1000
c.claim("S4", f"The coil takes {d['qc']:.1f} kW ({q_coil:.1f} kW/m2) from firebox gas at {d['Tg']:.0f} C", "Physics", "Heat transfer",
        "Radiant exchange sigma F (Tg^4 - Tw^4) with F = 0.40, plus convection at 20 W/(m2 K); the flux may not exceed black-body exchange plus the same convection",
        q_coil, q_bb, "kW/m2", margin=0.0)
c.cited("S5", f"Exchange factor F = 0.40 and coil convection 20 W/(m2 K) in a hand-fed firebox (efficiency {100*min(r['sens_bank'][(1.5,0.25)],1):.1f} to {100*r['sens_bank'][(1.5,0.60)]:.1f} % for F = 0.25 to 0.60)",
        "Physics", "Heat transfer", "Well-stirred zone model of a firebox (Hottel zone method, single zone); F and h set by flame luminosity and plume velocity, not calculable from first principles at TRL 3",
        f"R5 (65 %) is met for F 0.40 to 0.60 at lambda 1.5 and missed at F 0.25 ({CAL} Table 6); the correlation at the mean firebox velocity gives about 9 W/(m2 K), not 20 (independent review), worth about 2.6 points; flue temperature and oxygen to be measured",
        PLAUSIBLE, "")
# bank and economizer gas side: the v0.4 values (30 and 25 W/(m2 K)) failed this row; the gas-pass baffles of STR-DEC-001 S1 close it
gb, ge = d["gas_bank"], d["gas_eco"]
nu, k, pr = sizing.gas_props((d["Tg"] + d["T1"]) / 2)
v1, Re1, _ = gb["passes"][0]
h_hilpert = 0.683 * Re1 ** 0.466 * pr ** (1 / 3) * k / (P["bk_tube_od"] / 1000) * 0.92 + gb["h_rad"]
c.order_of_magnitude("S6", f"Bank gas-side coefficient {gb['h_clean']:.1f} W/(m2 K) clean, {d['U_bank']:.1f} with fouling, gas crossing the tubes at {v1:.2f} m/s (gas-pass baffle, 10 % edge bypass)",
                     "Physics", "Heat transfer", claimed=gb["h_clean"], estimate=h_hilpert, unit="W/(m2 K)", factor=1.3,
                     law="Zukauskas in-line bank correlation with the row factor per pass (CAL) checked against Hilpert's single-cylinder correlation Nu = 0.683 Re^0.466 Pr^1/3 with the same row factor and gas radiation (same correlation family, so a consistency check, not an independent one)",
                     closed_by="STR-DEC-001 S1 (gas-pass baffles, 2026-10-24); " + CAL + " section 4")
nu2, k2, pr2 = sizing.gas_props((d["T1"] + d["T_stack"]) / 2)
v2, Re2, _ = ge["passes"][1]
h_hil2 = 0.683 * Re2 ** 0.466 * pr2 ** (1 / 3) * k2 / (P["eco_tube_od"] / 1000) * 0.95 + ge["h_rad"]
c.order_of_magnitude("S7", f"Economizer gas-side coefficient {ge['h_clean']:.1f} W/(m2 K) clean, {d['U_eco']:.1f} with fouling, three baffled passes at 0.7 to 1.0 m/s",
                     "Physics", "Heat transfer", claimed=ge["h_clean"], estimate=h_hil2, unit="W/(m2 K)", factor=1.3,
                     law="As S6, middle pass", closed_by="STR-DEC-001 S1 (gas-pass baffles, 2026-10-24); " + CAL + " section 4")
r_fg = d["r_fg"]
c.claim("S8", f"Firebox outer skin {d['t_skin']:.0f} C behind 50 mm of ceramic fibre (about 135 C if the hot face near the fire bed is 700 C)", "Physics", "Heat transfer",
        "Series conduction and outside film: k 0.12 W/(m K), h 12 W/(m2 K); the skin must stay below the gas temperature and is a burn hazard above 60 C (no requirement limits it yet; DEC #21)",
        d["t_skin"], d["Tg"], "C", closed_by=f"{CAL} Table 5")
# soil
alpha = r["alpha"]
delta = 2 * math.sqrt(alpha * A["hold_min"] * 60) * sizing.erfinv((A["t_kill"] - (A["t_steam"] + A["t_soil0"]) / 2) / (A["t_steam"] - (A["t_steam"] + A["t_soil0"]) / 2))
c.order_of_magnitude("S9", f"The steam front must reach {100*(0.15 + r['delta']):.1f} cm so that 15 cm stays at 70 C through a 25 min hold", "Physics", "Heat transfer",
                     claimed=100 * r["delta"], estimate=100 * delta, unit="cm of overshoot", factor=1.05,
                     law="Two semi-infinite bodies in contact: the interface sits at the mean temperature and the profile follows erf(x / 2 sqrt(alpha t))",
                     closed_by=f"{CAL} section 2")
E15 = r["C_vol"] * 85 * (0.15 + r["delta"]) / 1000
c.order_of_magnitude("S10", f"Heating 16.5 cm of moist soil by 85 K takes {r['d15']['E_soil']:.1f} MJ/m2", "Physics", "Thermodynamics",
                     claimed=r["d15"]["E_soil"], estimate=E15, unit="MJ/m2", factor=1.02, law="Q = rho c dT V with c = 0.84 + 0.20 x 4.18 kJ/(kg K) for 20 % water",
                     closed_by=f"{CAL} section 2")
# soil permeability against the hood's weight
c.cited("S11", f"Steam passes down through {100*(0.15+r['delta']):.1f} cm of soil at full flow without lifting the {r['p_lift']:.0f} Pa hood",
        "Physics", "Fluid mechanics", "Darcy's law at the superficial steam velocity of 1.16 cm/s; intrinsic permeability 1e-10 (sand) to 1e-12 m2 (loam), textbook ranges, not measured",
        f"needs {r['dp_soil'][1e-10]:,.0f} Pa in sand, {r['dp_soil'][1e-11]:,.0f} Pa in sandy loam, {r['dp_soil'][1e-12]:,.0f} Pa in loam against {r['p_lift']:.0f} Pa (583 Pa with 40 kg of ballast); "
        "holds only in loose sandy soil at full flow (92 % of the lift limit even there); moist soil passes gas less well still, and the 10 % skirt leakage in CAL does not depend on permeability (independent review); fixes (bed preparation, stakes or straps, a deeper skirt, a larger hood or lower steam flux) change how the machine is used, so they go to Amish",
        FIX, "To Amish (STR-DEC-001 #18); TRL 4 soil tests decided 2026-10-02")

# ------------------------------------------------------------------ Physics: fluid mechanics and strength
c.claim("S12", f"Natural draft {r['draft_pa']:.1f} Pa covers the gas-side losses ({r['dp_gas_total']:.1f} Pa, fuel bed included) and the damper openings at lambda 1.5",
        "Physics", "Fluid mechanics", f"Stack effect g H (rho_air - rho_gas) over {r['H_draft']:.2f} m at a mean 400 C; losses at the fuel bed (3 Pa, Ergun estimate), holes, baffled passes, chimney and cap; openings at Cd 0.6. Failed with the 2.4 m chimney once the fuel bed was counted (0.1 Pa left)",
        r["air_need_mm2"][A["lambda_ctl"]], sum(r["air_open_mm2"]), "mm2 of opening needed", margin=0.15, closed_by=f"STR-DEC-001 S3 (chimney outlet 3.2 m); {CAL} section 4")
c.claim("S13", f"Normal pressure at the bank inlet {r['p_inlet']/1e5:.3f} bar, the highest on the steam side, stays within R6", "Physics", "Fluid mechanics",
        "Two-phase friction (Muller-Steinhagen and Heck) with a helical coil factor (Ito), acceleration, gravity, hose and manifold losses", r["p_inlet"] / 1e5, 0.15, "bar gauge",
        margin=0.10, closed_by=f"{CAL} section 5")
c.claim("S14", f"The water seal blows at {r['p_seal']/1e5:.3f} bar, above the {r['p_header']/1e5:.3f} bar header pressure", "Physics", "Fluid mechanics",
        "Hydrostatics: p = rho g h for the 890 mm dip leg in water at 100 C; the overflow at the static mark removes the annulus rise",
        r["p_seal"], r["p_header"], "Pa", rule="above", closed_by=f"{CAL} section 5")
c.claim("S15", f"The 350 mm overflow loop seal ({r['p_trap']:,.0f} Pa) holds against the head-space back pressure of a refeed flash", "Physics", "Fluid mechanics",
        "Hydrostatics against the vent pipe's friction and exit loss at the flash flow; the margin is 34 % on pressure, about 16 % on flow, so a flash faster than about 26 s breaks it", r["p_trap"], r["dp_vent_flash"], "Pa", rule="above")
c.rows[-1]["verdict"] = PLAUSIBLE
c.rows[-1]["check"] += "; the flash basis (30 s, coil at the loaded gas temperature) is not bounded (independent review); to Amish (DEC #20)"
c.claim("S16", f"The 3/4 in, 15 psi certified valve passes the {r['flash_rate']:.0f} kg/h dry-coil refeed flash", "Physics", "Fluid mechanics",
        "Napier's formula (ASME Section IV practice) and the maker's capacity table, 375 lb/h (Watts Series 315); the valve and seal sit at the header, downstream of the coil where a flash builds about 1.5 bar", r["rv_rated_kg_h"], r["flash_rate"], "kg/h",
        rule="above")
c.rows[-1]["verdict"] = PLAUSIBLE
c.rows[-1]["check"] += "; 21 % margin against an unbounded flash basis; a dry coil hotter than the loaded gas (700 to 800 C) could flash about 2 kg (independent review); to Amish (DEC #20)"
E_dry = r["m_tube"] * A["c_ss"] * (r["t_dry"] - 100) / 1000
c.order_of_magnitude("S17", f"A dry coil at {r['t_dry']:.0f} C stores {r['E_dry']:.2f} MJ and flashes {r['m_flash']:.2f} kg of refeed water", "Physics", "Thermodynamics",
                     claimed=r["m_flash"], estimate=E_dry * 1000 / (A["h_fg"] + A["cp_w"] * 35), unit="kg", factor=1.2,
                     law="Stored heat m c dT of 316 tube (c 0.50 kJ/(kg K)) against latent plus sensible heat of the feed")
c.rows[-1]["verdict"] = PLAUSIBLE
c.rows[-1]["check"] += "; arithmetic holds, but a dry coil no longer cools the gas and may reach 700 to 800 C (about 2 kg); to Amish with S15 and S16 (DEC #20)"
c.claim("S18", "Coil hoop stress at the 3 bar pump shut-off stays far below the yield of 316 at 700 C", "Physics", "Strength of materials",
        "Thin-wall hoop stress p D / 2t; 316 yield at 700 C about 100 MPa (hot strength, conservative)", r["hoop_shutoff"] / 1e6, A["sy_316_700C"] / 1e6, "MPa",
        closed_by=f"{CAL} section 6")
c.claim("S19", f"Hood handle bar with half of 40 kg of ballast at mid-span and a load factor of 2 stays below yield", "Physics", "Strength of materials",
        "Simply supported beam M = F L / 4 on a 30 x 30 x 2.5 SHS, Z = 2,330 mm3; S235 yield 235 MPa", r["handle_sigma"] / 1e6, 235, "MPa",
        closed_by=f"{CAL} section 7")

# ------------------------------------------------------------------ Chemistry
C_, H_, O_, N_, ash = A["C"], A["H"], A["O"], A["N"], A["ash"]
lhv_simple = (19.0 * (1 - A["moist"]) - 2.442 * A["moist"])
c.order_of_magnitude("C1", f"Wood at 20 % moisture (wet basis) gives {r['lhv']:.2f} MJ/kg lower heating value", "Chemistry", "Physical chemistry (thermochemistry)",
                     claimed=r["lhv"], estimate=lhv_simple, unit="MJ/kg", factor=1.1,
                     law="Channiwala and Parikh correlation for the dry HHV, less the latent heat of the product and fuel water; checked against 19 MJ/kg dry wood LHV",
                     closed_by=f"{CAL} section 4")
o2 = C_ / 100 * 32 / 12 + H_ / 100 * 8 - O_ / 100
c.order_of_magnitude("C2", f"Stoichiometric air {r['air_st']:.2f} kg per kg of wet fuel", "Chemistry", "Physical chemistry (stoichiometry)",
                     claimed=r["air_st"], estimate=o2 / 0.232 * (1 - A["moist"]), unit="kg/kg", factor=1.02,
                     law="C + O2 -> CO2, 2 H2 + O2 -> 2 H2O, less fuel oxygen; air 23.2 % oxygen by mass", closed_by=f"{CAL} section 4")
c.claim("C3", f"Flue gas at lambda 1.5 holds {100*r['y_h2o']:.1f} % water vapour; dew point {r['t_dew']:.0f} C, so the cold end of the economizer runs wet",
        "Chemistry", "Environmental and atmospheric chemistry", "Dalton's law and the Antoine equation for water", r["t_dew"], A["t_feed"] + 5, "C (dew point above the feed inlet wall)",
        rule="above", closed_by=f"{CAL} section 4; stainless tube and 304 baffles (STR-DEC-001 S1)")
c.cited("C4", "Wood fires make carbon monoxide, and less excess air raises the CO made", "Chemistry", "Physical chemistry (kinetics)",
        "Incomplete combustion of carbon (C + 1/2 O2 -> CO) where mixing or temperature is poor; CO is odourless and toxic",
        "Firebox and chimney outdoors only, personal CO alarm (PRC safety; RSK H5); the 4 % unburned loss in CAL is an assumption", WITHIN, "STR-PRC-001 Safety; STR-RSK-001")
c.cited("C5", "316 stainless coil, bank and economizer resist acidic flue condensate and a dry-fire excursion to about 500 C; 304 for the bank baffle and 316L for the economizer baffles",
        "Chemistry", "Materials and polymer chemistry", "Austenitic stainless steels keep a passive chromium oxide film in mildly acidic, chloride-poor condensate and scale slowly below about 800 C",
        "Design choice decided by Amish 2026-09-25 (coil); economizer baffles changed from 304 to 316L after the independent review, since wood condensate carries organic acids and chloride and drips onto them; welded 316 sensitizes between about 450 and 850 C in a dry-coil excursion (316L or low-carbon filler to be specified)", WITHIN, "STR-DDR-001; STR-DEC-001 S1")

# ------------------------------------------------------------------ Biology
c.cited("B1", "Holding soil at 70 C or more for 20 to 30 min kills most weed seeds and soil-borne pathogens", "Biology", "Microbiology and ecology",
        "Extension guidance: 160 to 180 F (71 to 82 C) for 30 min (Mississippi State University Extension P4033); 140 to 180 F for 30 min for pathogens and weeds (NCAT, 2022)",
        "70 C for 20 to 30 min sits inside both ranges; some hard-seeded weeds survive (accepted in STR-PRS-001 assumptions)", WITHIN, "R1 / PR-001 target; cited sources")
c.cited("B2", "Soil behind the steam front reaches 100 C for most of the hold, more than the 82 C ceiling extension guidance gives",
        "Biology", "Ecology and agronomy", "MSU P4033: exceeding 180 F (82 C) can harm soil structure; NCAT 2022: overheating kills beneficial nitrifying bacteria",
        "Known side effect of steaming with saturated steam; accepted in PRC and carried as risk RSK H9; aerated steam at 70 C to 80 C would avoid it but adds a blower (suggestion in REVIEW)",
        WITHIN, "STR-RSK-001 H9")
c.cited("B3", "Condensing steam on skin causes deep burns within about a second", "Biology", "Human physiology",
        "Latent heat 2.26 MJ/kg released on contact at 100 C, on top of the sensible heat of hot water",
        "Steam diverted to the vent before a hood is lifted; PPE; 5 m exclusion (PRC safety; RSK H1, H2)", WITHIN, "STR-RSK-001")
hood_kg = r["m_hood"]
c.claim("B4", f"One operator lifts and resets a {hood_kg:.1f} kg hood, 1.2 x 1.0 m, by its two side handles 1.12 m apart",
        "Biology", "Ergonomics", "Revised NIOSH lifting equation (NIOSH 94-110): load constant 23 kg for one person under ideal conditions; the handle span is wider than one person's reach",
        hood_kg, 23.0, "kg")
c.rows[-1]["verdict"] = FIX
c.rows[-1]["check"] += "; with the horizontal multiplier for a 1.0 to 1.2 m load the one-person limit is nearer 10 to 14 kg and a two-person share of 15.6 kg is borderline (independent review); fix proposed: a hood wheel kit or lifting aid; changes the one-operator scope, so it goes to Amish (STR-DEC-001 S2)"

# ------------------------------------------------------------------ Mathematics
c.order_of_magnitude("M1", f"{r['d15']['ms']:.1f} kg of steam per m2 at 15 cm", "Mathematics", "Units and dimensional analysis",
                     claimed=r["d15"]["ms"], estimate=(r["d15"]["E_soil"] + r["d15"]["E_hood"]) / 2.257 / (1 - A["edge_leak"]), unit="kg/m2", factor=1.02,
                     law="Steam = (soil + hood heat) / latent heat / (1 - skirt leakage)", closed_by=f"{CAL} section 2")
c.order_of_magnitude("M2", f"Two hoods treat {r['rate15_2']:.2f} m2/h at 15 cm", "Mathematics", "Orders of magnitude",
                     claimed=r["rate15_2"], estimate=A["steam_kg_h"] / r["d15"]["ms"], unit="m2/h", factor=1.1,
                     law="Rate = steam output / steam per m2 (steam limited), less the vented minute per changeover")
c.rows[-1]["verdict"] = PLAUSIBLE
c.rows[-1]["check"] += "; arithmetic holds, but a 4 cm unheated edge strip, overlap between settings and hose and header losses would cut the net rate to about 1.5 to 1.6 m2/h (independent review); to verify at TRL 4"
c.claim("M3", f"Heated section holds {r['V_heated']:.2f} L of water flooded", "Mathematics", "Units and dimensional analysis",
        "Bore area x length for coil, bank, economizer and header", r["V_heated"], 8.0, "L", margin=0.05, closed_by=f"{CAL} section 6")
c.order_of_magnitude("M4", f"One 125 L fill lasts {r['run_h']:.2f} h at 30 kg/h", "Mathematics", "Orders of magnitude",
                     claimed=r["run_h"], estimate=125 / 30, unit="h", factor=1.01, law="Volume / flow", closed_by=f"{CAL} section 7")
c.cited("M5", "Every efficiency, rate and pressure is a point estimate with a stated band", "Mathematics", "Statistics and uncertainty",
        "Sensitivity tables in CAL (lambda 1.5 to 2.5, F 0.25 to 0.60, permeability over two decades); correlations about +/- 30 %",
        "R5 at risk inside the band; R2 margins under 2 %; carried to RSK", WITHIN, f"{CAL} Tables 4 and 6")

# ------------------------------------------------------------------ Engineering and technology
c.cited("E1", "The steam side can never be isolated from the vent: no valve between coil and seal pot, diverter with no closed position",
        "Engineering and technology", "Standards practice", "Open-vent principle of atmospheric boilers; Texas Health and Safety Code 755.022(a)(4) asks for two independent means to prevent pressure build-up",
        "Water seal (first means) and certified relief valve (second means); whether these meet 755.022(a)(4) is for the TDLR ruling (REG R1)", WITHIN, "STR-PRC-001; STR-REG-001 R1")
c.cited("E2", "A stalled feed pump can never restart by itself into a hot, dry coil: the coil outlet alarm (about 150 C) latches the pump off until it is reset by hand",
        "Engineering and technology", "Control", "A dry coil heats at about 17 kW / 6.5 kJ/K = 2.6 K/s, so about 16 to 20 s to 150 C (the 2 to 3 min in the first draft was the time constant); a pump that stalls on low battery and recovers would otherwise refeed it unattended (independent review)",
        "Failed as first written (alarm only, wrong timing); fixed by a latching relay with a manual reset (BOM line 16)", WITHIN, "STR-DEC-001 S4 (latching pump trip)")
pump_a, batt_ah = 4.0, 20.0
c.claim("E3", "The 12 V 20 Ah lead-acid battery runs the feed pump and alarms through one 4.2 h fill", "Engineering and technology", "Power and link budgets",
        "Charge = current x time; a diaphragm pump of this class draws a few amperes (ASSUMED 4 A until the pump is chosen); lead-acid life favours 50 % depth of discharge",
        pump_a * r["run_h"], batt_ah * 0.5, "Ah used against 50 % of capacity")
c.rows[-1]["verdict"] = PLAUSIBLE
c.rows[-1]["check"] += f" ({100*pump_a*r['run_h']/batt_ah:.0f} % depth of discharge per fill at the assumed current; at a 4 A draw a battery rated 20 Ah at the 20 h rate delivers only about 15 to 16 Ah, so nearer 100 %, less in cold weather); to confirm with the pump datasheet, likely a 40 Ah battery with a low-voltage cut-off (proposed, DEC #16)"
c.claim("E4", f"Fabrication tolerance: the bank serpentine fits inside the lined box with {P['fb_l']/2 - P['bk_shell_t'] - P['bk_lining_t'] - P['bk_apex'] - P['bk_tube_od']/2:.0f} mm at the bends",
        "Engineering and technology", "Manufacturing tolerances", "Bend apex at 290 mm from the box centre, lining face at 323 mm; hand-bent tube is typically within a few millimetres",
        P["fb_l"] / 2 - P["bk_shell_t"] - P["bk_lining_t"] - P["bk_apex"] - P["bk_tube_od"] / 2, 5.0, "mm clearance", rule="above",
        closed_by="cad/src/model.py fit checks; cad/fidelity.json (D3, no interference)")

state = c.write()

# ------------------------------------------------------------------ option B (vented fire-tube kettle), first-order
o = Check(ROOT / "docs/04-calcs/options_results.csv")
V_B = 0.594 * 0.494 * 0.250 * 1000 - 7 * math.pi / 4 * 0.0603 ** 2 * 0.250 * 1000      # L of water, 250 mm deep
lam_b = 1.75
q_floor = SIGMA * 0.6 * 0.3 * (1100 ** 4 - 373 ** 4) / 1000                             # kW, fire bed and flame to the 0.3 m2 floor
o.order_of_magnitude("OB1", f"Kettle holds about 70 L of water at 100 C (option A: {r['V_heated']:.1f} L heated)", "Mathematics", "Units and dimensional analysis",
                     claimed=70.0, estimate=V_B, unit="L", factor=1.1, law="Inside floor area x water depth, less the fire tubes", closed_by="STR-OPT-001 Table 2")
o.claim("OB2", "Without an economizer the kettle's efficiency stays below option A's", "Physics", "Thermodynamics",
        "First law with the gas leaving the fire tubes hot (laminar tube flow, Re about 1,700, h about 10 W/(m2 K)); about 16 kW reaches the floor by radiation",
        50.0, 100 * d["eta"], "% (first-order estimate)", closed_by="STR-OPT-001 section 2")
o.claim("OB3", "The pool boils without film boiling on the fired floor", "Physics", "Heat transfer",
        "Zuber critical heat flux for water at 1 bar, about 1.1 MW/m2", q_floor / 0.3, 1100.0, "kW/m2", closed_by="STR-OPT-001 section 2")
flash_b = V_B * 0.958 * (sizing.A["cp_w"] * 2.3) / A["h_fg"]
o.order_of_magnitude("OB4", f"A seal blow at 0.084 bar flashes only about {flash_b:.1f} kg of the pool", "Physics", "Thermodynamics",
                     claimed=flash_b, estimate=V_B * 4.18 * 2.3 / 2257, unit="kg", factor=1.1,
                     law="Saturation temperature 102.3 C at 1.097 bar abs; flash = m c dT / h_fg", closed_by="STR-OPT-001 section 2")
sig_relief = 0.5 * 103e3 * 0.45 ** 2 / 0.003 ** 2 / 1e6
o.claim("OB5", "The flat 3 mm kettle walls hold the relief valve set pressure (1.03 bar) if the water seal freezes or blocks", "Physics", "Strength of materials",
        "Flat plate in bending, sigma = beta q b^2 / t^2 with beta about 0.5 (Roark), b = 450 mm; S235 yield 235 MPa", sig_relief, 235, "MPa")
o.rows[-1]["verdict"] = FIX
o.rows[-1]["check"] += "; fix if B were chosen: a second independent open standpipe vent (Texas 755.022(a)(4) asks for two means) and stiffened walls"
t_boil = V_B * 4.18 * 85 / 16.5 / 60
o.order_of_magnitude("OB6", f"Start-up: about {t_boil:.0f} min to bring the pool to the boil at about 16 kW", "Mathematics", "Orders of magnitude",
                     claimed=t_boil, estimate=V_B * 4.186 * 85 / 16.5 / 60, unit="min", factor=1.05, law="m c dT / heat rate", closed_by="STR-OPT-001 section 2")
o.cited("OB7", "A float switch running the 12 V pump keeps the pool level", "Engineering and technology", "Control",
        "On-off level control of a large-capacity vessel is stable; the pool buffers a pump stop for many minutes", "Common practice in vented kettles and water heaters",
        WITHIN, "STR-OPT-001 section 2")
o.write()
print("option A state:", state)

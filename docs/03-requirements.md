---
doc_id: STR-PRS-001
title: SteamRoot product requirements and specifications
project: SteamRoot
doc_type: Product requirements and specifications
version: "0.8"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, including pressure and safety requirements
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply Amish's 2026-09-25 decisions (two hoods in R2, $1,800 budget in R12); correct the wood heating value in R4; add TRL 3 status from STR-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: TRL 3 status updated for the constructable design (STR-DDR-003, STR-CAL-001 v0.3); R12 reported against the value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R4 to be restated after the evaporator bank study and R5 study to keep R7 (decided 2026-10-02); authority named; no status changed"
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Status from STR-CAL-001 v0.4 (evaporator bank, dampers, seal pot overflow, ballast handles): R4 not met to at risk, R5 not met to met, R11 mass met to at risk; R4 restatement to 4.5 kg/m2 proposed, awaiting Amish"
- version: "0.8"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Migrated from STR-REQ-001 to STR-PRS-001 (kit 1.9.1 upgrade): R1 to R12 become PR-001 to PR-015 with the same targets, each traced to STR-URS-001; status from STR-CAL-001 v0.5 (gas-pass baffles): PR-004 at risk to not met, PR-005 met to at risk, PR-008 met to at risk (battery); PR-016 to PR-018 proposed, awaiting Amish; after the independent review: PR-011 at risk to not met, PR-005 66.1 %, PR-010 at 3.2 m, PR-009 basis open"
---

# SteamRoot product requirements and specifications

What the design must do, each requirement traced to a user need in STR-URS-001. The targets are those of STR-REQ-001 v0.7 as decided by Amish on 2026-09-25 and 2026-10-02, carried over unchanged; R2, R6 and R11, which each held two targets, are split into two rows and the old number is in "Was". Status is from STR-CAL-001 v0.5 (`docs/04-calcs/01-sizing.md`), which carries the gas-pass baffles fitted on 2026-10-24 under Amish's standing instruction of 2026-10-23 (STR-DEC-001 S1), and the 3.2 m chimney outlet and latching pump trip of 2026-10-25 (S3, S4). Targets remain proposals to review with the co-design partners. Of the 18 rows, none is withdrawn; 2 are not met (PR-004, with a restatement proposed, and PR-011, with a basis proposed), 1 is not met for one operator and proposed to Amish (PR-016), 5 are at risk, 1 is over the value-engineering target, 1 is to verify at TRL 4 and 8 are met on paper or by design. Safety requirements (PR-006, PR-007, PR-009, PR-010, PR-013, PR-017) take priority over performance requirements if they conflict. Method: STANDARDS section 22.

> **Safety:** SteamRoot is a fired steam generator. Meeting these requirements on paper does not make it safe or legal to build. A written ruling from the local boiler authority is an open prerequisite for any detail design or build.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Pasteurize soil to working depth | Soil shall reach 70 °C (158 °F) or more for 20 to 30 min at 10 to 15 cm depth across at least 80 % of the hood footprint | 70 for 20 to 30 min, 80 % of footprint | min | °C, min, % | Analysis (CAL-001 section 2), TRL 3; thermocouple probes at 15 cm, TRL 4 | To verify at TRL 4 (1D model holds 70 °C at 15 cm if the front reaches 16.5 cm; STEM S11 fails: in soils finer than sand the steam cannot pass at full flow under the hood; bed preparation and hold-down proposed, DEC #18) | R1 |
| PR-002 | UR-002 | Performance | Treatment rate at 15 cm | Two hoods used alternately shall treat at least 1.85 m2/h (about 1.9) at 15 cm depth (restated by Amish 2026-09-25, STR-DDR-002) | 1.85 | min | m2/h | Analysis (CAL-001 section 3), TRL 3; timed trial, TRL 4 | At risk: 1.88 m2/h; about 1.5 to 1.6 m2/h net of edge strips, overlap and hose losses (STEM M2) | R2 |
| PR-003 | UR-003 | Performance | Steam output | The generator shall make at least 30 kg/h of saturated steam, continuously, from one firebox | 30 | min | kg/h | Analysis (CAL-001 section 4), TRL 3; feed metering, TRL 4 | Met on paper: 30 kg/h at 32.2 kW firing | R3 |
| PR-004 | UR-004 | Performance | Wood per m2 | Wood use shall be at most 4 kg at 20 % moisture (about 14.5 MJ/kg) per m2 at 15 cm (target kept 2026-09-25; to be restated, decided 2026-10-02) | 4.0 | max | kg/m2 | Analysis (CAL-001 section 4), TRL 3; fuel weighing, TRL 4 | Not met: 4.36 kg/m2 with the baffles and dampers set (4.44 with the dampers wide open); restatement to 4.5 kg/m2 proposed, awaiting Amish (DEC #12) | R4 |
| PR-005 | UR-004 | Performance | Fuel-to-steam efficiency | At least 65 % of the fuel energy shall reach the water as steam, with the economizer and evaporator bank | 65 | min | % | Analysis (CAL-001 section 4), TRL 3; flue temperature, oxygen and fuel weighing, TRL 4 | At risk: 66.1 % at λ = 1.5 with the gas-pass baffles, a margin smaller than its uncertainties (62.5 to 66.9 % in CAL Table 6a; 59.8 % without baffles) | R5 |
| PR-006 | UR-005 | Safety | Header pressure and open vent | Normal working pressure at the steam header shall be at most 0.1 bar gauge (1.5 psi), with an open vent to atmosphere that cannot be closed or isolated (redefined by Amish 2026-09-25) | 0.10 | max | bar gauge | Analysis (CAL-001 section 5); design review, TRL 3 | Met on paper: 0.033 bar; seal limit 0.084 bar; vent cannot be isolated | R6 |
| PR-007 | UR-005 | Safety | Stored water | The heated section shall hold at most 8 L of water, with no closed steam drum | 8.0 | max | L | Analysis (CAL-001 section 6), TRL 3 | Met on paper: 7.3 L flooded | R7 |
| PR-008 | UR-006 | Usability | Run between refills | One feed water fill, and one battery charge, shall last at least 3 h of steaming | 3.0 | min | h | Analysis (CAL-001 section 7), TRL 3; timed run, TRL 4 | At risk: water 4.2 h; the 20 Ah battery runs to about 100 % depth of discharge per fill at an assumed 4 A pump (STEM E3; DEC #16) | R8 |
| PR-009 | UR-005 | Safety | Certified relief valve | A certified steam relief valve set at 15 psi (1.03 bar) or less shall pass both the full steam output and the dry-coil refeed flash, as a second line of protection behind PR-006 (reworded by Amish 2026-09-25) | 15 psi set; capacity at least the refeed flash | max set, min capacity | psi, kg/h | Valve rating and capacity check (CAL-001 section 6), TRL 3 | Met on paper: rated 170 kg/h against a 141 kg/h flash on a 30 s basis; the flash basis is open (STEM S16, DEC #20); confirm on the valve bought | R9 |
| PR-010 | UR-007, UR-013 | Safety | Operator and site protection | The chimney outlet shall be at least 2.2 m above ground with a spark arrestor of 6 mm mesh or finer; the fire shall be outdoors only; steam shall be diverted to the vent before a hood is lifted; hood handles shall stay at 60 °C or cooler | 2.2 m; 6 mm; 60 °C | min; max; max | m, mm, °C | Design review, TRL 3; surface temperature check, TRL 4 | Met by design: 3.2 m (raised for draft, DEC S3), 6 mm mesh, hood skin 23 °C | R10 |
| PR-011 | UR-008 | Packaging and transport | Towed mass | The machine as towed, with the feed tank and seal pot drained, shall weigh at most 500 kg (restated by Amish 2026-09-25) | 500 | max | kg | Analysis (CAL-001 section 7 and the model), TRL 3; weighbridge, TRL 4 | Not met: 509 kg with both hoods aboard (643 kg full; 447 kg without the hoods, which ride on a second vehicle for the prototype; basis proposed in DEC #13) | R11 |
| PR-012 | UR-009 | Packaging and transport | Parts cost | Parts cost shall be at or under the USD 2,200 value-engineering target, a hypothetical control target, not a limit (Amish 2026-10-01) | 2,200 | max | USD | Priced BOM, TRL 3 | Over target: USD 2,720 (USD 520 over; the overrun to USD 2,600 was accepted by Amish on 2026-10-03, the USD 120 of STEM fixes is new) | R12 |
| PR-013 | UR-005 | Safety | Coil inlet pressure | Normal working pressure at the coil inlet (now the evaporator bank inlet) shall be at most 0.15 bar gauge (2.2 psi) | 0.15 | max | bar gauge | Analysis (CAL-001 section 5), TRL 3 | Met on paper: 0.129 bar | R6 |
| PR-014 | UR-002 | Performance | Treatment rate at 5 cm | Two hoods used alternately shall treat at least 3.4 m2/h at 5 cm depth (weed seed bank only) | 3.4 | min | m2/h | Analysis (CAL-001 section 3), TRL 3 | At risk: 3.41 m2/h | R2 |
| PR-015 | UR-008 | Packaging and transport | Overall width | Overall width as towed shall be at most 1.5 m | 1.5 | max | m | Model and drawing STR-DWG-002, TRL 3 | At risk: 1.48 m | R11 |
| PR-016 | UR-010 | Usability | Hood handling | No person shall lift more than 23 kg when a hood is moved between settings (revised NIOSH lifting equation load constant), ballast weights lifted off first | 23 | max | kg per person | Analysis (STEM B4), TRL 3; handling trial, TRL 4 | Not met for one person: 31.3 kg hood, handles 1.12 m apart; a two-person share of 15.6 kg is borderline once the reach is counted. Wheel kit recommended; proposed, awaiting Amish (DEC S2) | New |
| PR-017 | UR-011 | Safety | Two independent means against pressure | The steam side shall be designed for operation only at atmospheric pressure and carry two independent means to prevent the build-up of pressure (Texas Health and Safety Code 755.022(a)(4)), subject to the authority's written ruling | 2 | min | independent means | Design review, TRL 3; written ruling from TDLR before any build | Met by design (water seal and certified relief valve); ruling not yet obtained. Proposed, awaiting Amish (DEC #17) | New |
| PR-018 | UR-012, UR-014 | Physical architecture | Workshop build | The machine shall be built from stock steel sections, stock stainless tube and catalogue safety parts with the tools of a farm workshop and a competent welder, following STR-BLD-001 | Stock and catalogue parts only | none | none | Inspection of the model, BOM and build plan, TRL 3 | Met by design (STR-BLD-001; `cad/fidelity.json` D3). Proposed, awaiting Amish (DEC #17) | New |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Soil to 15 cm depth: bulk density 1,300 kg/m³, gravimetric water content 20 % (dry basis), starting temperature 15 °C. The soil is modelled with a condensation front: soil above the front reaches 100 °C, and the front must reach 16.5 cm so that 15 cm stays at 70 °C or more through a 25-minute hold (STR-CAL-001, section 2).
- Specific heat of dry mineral soil 0.84 kJ/(kg K), of water 4.18 kJ/(kg K).
- 70 °C for 20 to 30 minutes sits inside the extension guidance for weed seeds and soil-borne pathogens (STR-STM-001, B1). Some hard-seeded weeds and heat-tolerant viruses need higher temperatures; this is accepted.
- Wood at 20 % moisture (wet basis) has a lower heating value of about 14.5 MJ/kg for a typical hardwood analysis.
- Pressure thresholds for boiler and pressure vessel rules vary by jurisdiction. PR-006, PR-009 and PR-017 are set to stay within the Texas exemption for boilers designed for operation only at atmospheric pressure, but compliance must be confirmed: the written ruling from the Texas Department of Licensing and Regulation's boiler program is an open prerequisite.
- PR-011 assumes the machine is towed with the feed tank and seal pot drained and filled from a water supply at the site.
- The PR-009 capacity check uses the maker's published capacity for the Watts Series 315, 3/4 in, 15 psi valve (375 lb/h); it must be confirmed for the valve actually bought.
- PR-002 and PR-014 assume two hoods used alternately, a 25-minute hold, 2 minutes to reset a hood and 1 minute of vented steam each time the hose is moved.
- PR-008 assumes a pump current of 4 A until a pump is chosen; the datasheet value replaces it.

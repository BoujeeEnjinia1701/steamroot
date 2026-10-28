---
doc_id: STR-PLN-001
title: SteamRoot project plan
project: SteamRoot
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade): workstreams, resources, stage gates (P4 to P6 on hold), decisions requested, reference list"
---

# SteamRoot project plan

SteamRoot is at TRL 3 and pipeline stage P3 (design outputs) since the kit 1.9.1 upgrade of 2026-10-25. The next gate, P4 verification, is on hold while the portfolio is capped at TRL 3, and could not start in any case before the written ruling from the Texas boiler authority. Decisions requested from Amish: the concept choice (#14, A and B within 10 %), hood handling (S2), and the open items #12, #13 and #16 to #21 in STR-DEC-001. Method: STANDARDS sections 19 and 23.

> **Safety:** No workstream below includes buying, building or firing anything. The ruling gates all physical work.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Regulatory ruling | Project lead (Amish) | Written ruling from TDLR's boiler program on the open-vented, fired monotube coil (STR-REG-001, R1) | Open prerequisite; not yet requested in writing |
| Co-design partners | Project lead | One market garden and one nursery near Irving via Texas A&M AgriLife Extension (decided 2026-10-02) | Not yet named |
| Design (P3) | Design lead | D3 model of both options, drawings, priced BOM, build plan, CAL, STEM check, requirements and traceability | Done 2026-10-25; decisions open in STR-DEC-001 |
| Renders | Coordinator | Options picture (`media/options.png`) and product renders from `cad/src/product_model.py` (hero, studio, exploded) on Amish's workstation | Scenes ready; renders pending |
| Verification (P4) | Design lead with partners | Soil tests (permeability, skirt leakage, ballast), flue oxygen and temperature, fuel weighing, alarm response, handling trial | On hold (TRL cap 3) |
| Validation (P5) | Partners | Season of use on a market garden and a nursery | On hold |
| Commercialization (P6) | None | Only with a named deployment partner | On hold |

## Resources needed

Table 2. Resources (all for later stages; nothing is committed while the cap is P3).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Boiler inspector or consultant | Review of the design against Texas Health and Safety Code chapter 755 and the ruling | To assess | To assess |
| Workshop with welder, tube bender and coil former | Prototype built to STR-BLD-001 (P4) | About 2 to 3 weeks of workshop time (estimate, not planned in detail) | 2,720 in parts (BOM) |
| Soil test plot and partner time | P4 soil and steaming tests | To assess with the partners | To assess |
| Instruments | Flue oxygen analyser, type K probes, scale | Borrowed or bought at P4 | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Met (2026-10-25) |
| P1 Definition | URS, PRS, RSK with hazard analysis, MKT | Met (2026-10-25) |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check closed, feasibility | Met except the STEM check, which stays open on six plausible rows and two failed rows sent to Amish (S11, B4) |
| P3 Design outputs | Model, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability | Met (2026-10-25): D3 model, `cad/fidelity.json`, STR-DWG-002 and 101 to 128, STR-BLD-001, STR-RSK-001 |
| P4 Verification | Test plans and reports, verification report | On hold: TRL cap 3 and the ruling |
| P5 Validation | Field trials with a partner | On hold |
| P6 Commercialization | Named deployment partner | On hold |

## Next steps and decision requested

1. Amish decides #14 (concept: A or B), S2 (hood handling), #12 (restate PR-004 to 4.5 kg/m2), #13 (PR-011 without the hoods), #16 (battery), #17 (PR-016 to PR-018), #18 (bed preparation and hood hold-down), #19 (render site scene), #20 (refeed flash basis) and #21 (firebox skin limit). He may also reverse S1, S3 or S4.
2. The coordinator renders the options picture and the product renders.
3. When Amish chooses, request the written ruling from TDLR (the gate for everything physical).
4. TRL 4 work waits for his go.

## References

Every source cited in this repo's documents, Chicago style.

- Channiwala, S. A., and P. P. Parikh. 2002. "A Unified Correlation for Estimating HHV of Solid, Liquid and Gaseous Fuels." *Fuel* 81 (8): 1051-63.
- Elliott, Marianne. n.d. "Heat Treatment Techniques, Equipment, and Costs." Washington State University Puyallup Research and Extension Center. https://wpcdn.web.wsu.edu/wp-puyallup/uploads/sites/687/2016/04/03-steam-costs-equipment.pdf, accessed October 25, 2026.
- Farm Show Magazine. 2020. "Soil Steamer Helps Grower Control Weeds, Pathogens." Vol. 44, no. 4: 40. https://www.farmshow.com/a_article.php?aid=36229, accessed October 25, 2026.
- Hilpert, R. 1933. "Wärmeabgabe von geheizten Drähten und Rohren im Luftstrom." *Forschung auf dem Gebiete des Ingenieurwesens* 4: 215-24.
- Hottel, H. C., and A. F. Sarofim. 1967. *Radiative Transfer.* New York: McGraw-Hill.
- Incropera, F. P., D. P. DeWitt, T. L. Bergman, and A. S. Lavine. 2007. *Fundamentals of Heat and Mass Transfer.* 6th ed. Hoboken, NJ: Wiley.
- Ito, H. 1959. "Friction Factors for Turbulent Flow in Curved Pipes." *Journal of Basic Engineering* 81: 123-34.
- Lent, Chris, and Andy Pressman. 2022. "Soil Steaming for Pathogen, Pest, and Weed Control in High Tunnels." National Center for Appropriate Technology, April 12, 2022. https://www.ncat.org/blog/soil-steaming-for-pathogen-pest-and-weed-control-in-high-tunnels/, accessed October 25, 2026.
- Mississippi State University Extension. n.d. *Soil Steaming 101.* Publication P4033 (POD-08-24). https://extension.msstate.edu/publications/soil-steaming-101, accessed October 25, 2026.
- Müller-Steinhagen, H., and K. Heck. 1986. "A Simple Friction Pressure Drop Correlation for Two-Phase Flow in Pipes." *Chemical Engineering and Processing* 20 (6): 297-308.
- North Central Region SARE. n.d. "SARE Shared Steamer User Guide," Farmer Rancher Grant FNC25-1479. https://projects.sare.org/media/pdf/S/A/R/SARE-Shared-Steamer-user-guide-June-2026.pdf, accessed October 25, 2026.
- SupplyHouse.com. "Watts 0342629 315M2-015 3/4 Steam Safety Relief Valve 15 psi." https://www.supplyhouse.com/Watts-0342629-315M2-015-3-4-Steam-Safety-Relief-Valve-15-psi, accessed September 25 and October 25, 2026.
- Texas Administrative Code, title 30, chapter 111, subchapter B, Outdoor Burning. https://www.law.cornell.edu/regulations/texas/title-30/part-1/chapter-111/subchapter-B, accessed October 25, 2026.
- Texas Department of Licensing and Regulation. 2025. "SB 1185: Exemption of Sterilizers with Integrated Boilers from State Boiler Regulation." August 12, 2025. https://www.tdlr.texas.gov/news/2025/08/12/sb-1185-exemption-of-sterilizers-with-integrated-boilers-from-state-boiler-regulation, accessed October 25, 2026.
- Texas Health and Safety Code, sections 755.001 and 755.022. https://texas.public.law/statutes/tex._health_&_safety_code_section_755.022, accessed October 25, 2026.
- Texas Local Government Code, section 352.081. https://texas.public.law/statutes/tex._local_gov't_code_section_352.081, accessed October 25, 2026.
- UNEP Ozone Secretariat. 2014. *Phasing-out Methyl Bromide in Developing Countries.* https://ozone.unep.org/system/files/documents/Phasing-out%20Methyl%20Bromide%20in%20developing%20countries%20FINAL%20low%20version.pdf.
- US Code of Federal Regulations, 7 CFR 205.206. https://www.law.cornell.edu/cfr/text/7/205.206, accessed October 25, 2026.
- Waters, T. R., V. Putz-Anderson, and A. Garg. 1994. *Applications Manual for the Revised NIOSH Lifting Equation.* DHHS (NIOSH) Publication 94-110.
- Watts Series 315 steam safety relief valve capacity table (as used in STR-CAL-001).
- Young, W. C., and R. G. Budynas. 2002. *Roark's Formulas for Stress and Strain.* 7th ed. New York: McGraw-Hill.
- Zukauskas, A. 1972. "Heat Transfer from Tubes in Crossflow." *Advances in Heat Transfer* 8: 93-160.
- Zuber, N. 1959. *Hydrodynamic Aspects of Boiling Heat Transfer.* AEC Report AECU-4439.

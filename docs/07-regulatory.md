---
doc_id: STR-REG-001
title: SteamRoot regulatory and standards register
project: SteamRoot
doc_type: Regulatory register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade); Texas as the first jurisdiction (decided by Amish 2026-10-02); agriculture rows A1 to A3 cited from GGD-REG-001"
---

# SteamRoot regulatory and standards register

Which laws and standards would apply to SteamRoot, where, and what is needed. Not legal advice; anything marked "to assess" needs the authority or a qualified reviewer before any build or product claim. The first jurisdiction is Texas (decided by Amish on 2026-10-02). One row decides whether SteamRoot can be built at all: Texas Health and Safety Code chapter 755 regulates boilers, and section 755.022(a)(4) exempts "boilers that are designed for operation only at atmospheric pressure and that are equipped with two independent means to prevent the buildup of pressure". SteamRoot is designed to that wording (water seal and certified relief valve, PR-017), but whether a water seal that holds 0.084 bar and a relief valve set at 1.03 bar meet it is for the Texas Department of Licensing and Regulation (TDLR) to rule. The written ruling is an open prerequisite for any build (decided 2026-09-25 and 2026-10-02). No certification is pursued while the portfolio is capped at TRL 3. Method: STANDARDS section 23.

> **Safety:** A fired steam generator that is treated as unregulated when it is not, or that is altered so it can hold pressure, can injure or kill. The ruling overrides this register and every other document if it is stricter.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Texas Health and Safety Code chapter 755 (Boilers), section 755.022(a)(4) | Texas | Exempts boilers designed for operation only at atmospheric pressure with two independent means to prevent the build-up of pressure | SteamRoot is designed to this wording: a water seal at 0.084 bar (first means) and a certified relief valve at 1.03 bar (second means), no isolating valve (PR-006, PR-009, PR-017). Whether these count is the TDLR ruling | Project lead (Amish) | To assess: written ruling from TDLR, an open prerequisite |
| R2 | Texas Health and Safety Code 755.001: definitions of "boiler", "portable boiler" (primarily for use at a temporary location), "steam heating boiler" (up to 15 psi) and "power boiler" (above 15 psi) | Texas | Which class a regulated boiler falls in | If R1 does not exempt it, a towed generator used at temporary sites reads as a portable boiler under 15 psi; inspection and registration would then follow | Project lead | To assess (only if R1 is refused) |
| R3 | ASME Boiler and Pressure Vessel Code, Section IV (heating boilers) and Section I (power boilers) | United States, as adopted by states | Design, fabrication and stamping of boilers | SteamRoot is not built to either code; it relies on R1. A code-stamped boiler would change the design and the pitch | Project lead | Does not apply if R1 is granted; certification needed later if not |
| R4 | ASME Section IV steam safety valve (bought part) | United States | Certified relief capacity at 15 psi | Watts 315M2-015, 3/4 in, 15 psi, listed as ASME Section IV at 15 psi (SupplyHouse.com, 2026-10-25); capacity 375 lb/h from the maker's table (PR-009) | Design lead | Met by design (bought rating), to confirm on the valve bought |
| R5 | Texas Local Government Code 352.081 (county regulation of outdoor burning) | Texas counties | A commissioners court may prohibit or restrict outdoor burning in drought or when burning would worsen a public safety hazard, for up to 90 days | Firing SteamRoot outdoors in a county under a burn ban may be prohibited; whether a contained firebox counts as outdoor burning is not stated | Operator | Applies in practice (check before each use); scope to assess with the county |
| R6 | Texas Administrative Code title 30, chapter 111, subchapter B (Outdoor Burning), 111.201 general prohibition and its exceptions (111.205 to 111.215) | Texas | General prohibition of outdoor burning with listed exceptions (fire training, recreation, ceremony, cooking and warmth, disposal, prescribed burns, hydrocarbons, approval by the executive director) | None of the listed exceptions names firing wood in an enclosed firebox to raise steam | Project lead with TCEQ | To assess |
| R7 | 7 CFR 205.206(c)(5), USDA National Organic Program | United States | Weed problems may be controlled through "flame, heat, or electrical means" | Steaming is a heat method a certified organic grower can use; it is the grower's organic system plan, not the device | Grower with their certifier | Does not apply to the device; supports the use case |
| R8 | Montreal Protocol phase-out of methyl bromide | International | Removal of methyl bromide soil fumigation | Context for the problem (STR-PRB-001); steam is the cited best technical alternative in protected agriculture | None | Does not apply (context) |
| R9 | 49 CFR 571.108, FMVSS No. 108 (lamps and reflective devices), and Texas towing rules for light trailers | United States; Texas | Lights, reflectors and safety equipment on trailers on public roads | The used trailer (BOM line 1) must carry working lights and its coupling and chains in order; the towed mass is about 507 kg (PR-011) | Operator | To assess when the trailer is chosen |
| R10 | NFPA 211, Standard for Chimneys, Fireplaces, Vents, and Solid Fuel-Burning Appliances | United States (adopted locally) | Clearances, chimneys and spark arresting for solid-fuel appliances | Written for buildings; its practice can inform the chimney, spark arrestor and clearances of an outdoor firebox | Design lead | To assess (reference practice) |
| A1 | OSHA 29 CFR 1910.272, grain handling facilities (agriculture focus-area row, GGD-REG-001 A1) | United States | Grain dust and bin entry | No grain handling | None | Does not apply |
| A2 | NFPA 70, Articles 500 and 502, Class II locations (GGD-REG-001 A2) | United States | Electrical equipment where combustible dust is present | No combustible dust; 12 V circuit outdoors | None | Does not apply |
| A3 | NFPA 70, local electrical code for mains wiring (GGD-REG-001 A3) | United States | Mains wiring and equipment | SteamRoot has no mains supply; 12 V battery only | None | Does not apply |

Status: to assess, applies, does not apply, met by design, certification needed later.

Option B (vented fire-tube kettle, STR-OPT-001) meets the same rows, but a 70 L pool behind flat walls that cannot hold the relief set pressure would need a second independent open vent before R1's "two independent means" could be argued (STEM OB5).

## Sources

- Texas Health and Safety Code, section 755.001, Definitions. Public.Law. https://texas.public.law/statutes/tex._health_&_safety_code_section_755.001, accessed October 25, 2026.
- Texas Health and Safety Code, section 755.022, Exemptions for Certain Boilers (text verified by Public.Law on May 26, 2025, with amendments through 2017). https://texas.public.law/statutes/tex._health_&_safety_code_section_755.022, accessed October 25, 2026.
- Texas Department of Licensing and Regulation. 2025. "SB 1185: Exemption of Sterilizers with Integrated Boilers from State Boiler Regulation." August 12, 2025 (effective September 1, 2025; medical sterilizers only). https://www.tdlr.texas.gov/news/2025/08/12/sb-1185-exemption-of-sterilizers-with-integrated-boilers-from-state-boiler-regulation, accessed October 25, 2026.
- Texas Local Government Code, section 352.081, Regulation of Outdoor Burning. Public.Law. https://texas.public.law/statutes/tex._local_gov't_code_section_352.081, accessed October 25, 2026.
- Texas Administrative Code, title 30, part 1, chapter 111, subchapter B, Outdoor Burning (section list). Legal Information Institute. https://www.law.cornell.edu/regulations/texas/title-30/part-1/chapter-111/subchapter-B, accessed October 25, 2026.
- 7 CFR 205.206, Crop pest, weed, and disease management practice standard. Legal Information Institute. https://www.law.cornell.edu/cfr/text/7/205.206, accessed October 25, 2026.
- SupplyHouse.com. "Watts 0342629 315M2-015 3/4 Steam Safety Relief Valve 15 psi." https://www.supplyhouse.com/Watts-0342629-315M2-015-3-4-Steam-Safety-Relief-Valve-15-psi, accessed October 25, 2026 (USD 68.19; ASME Section IV at 15 psi).
- GrainGuard regulatory register GGD-REG-001, rows A1 to A3 (agriculture focus-area research, 2026-10-24).
- Rows R3, R8, R9 and R10 are listed from the codes' and laws' own titles; their applicability is "to assess" or context and needs the authority or a qualified reviewer before any claim.

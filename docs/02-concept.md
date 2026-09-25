---
doc_id: STR-PRC-001
title: SteamRoot design precis
project: SteamRoot
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-24'
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, media)
---

# SteamRoot design precis

SteamRoot is a towable, wood-fired steam generator that never holds pressure. A pump pushes water once through a large-bore stainless coil in a firebox, the steam flows at close to atmospheric pressure through a hose to an insulated hood pressed onto the soil, and a flue-gas economizer preheats the feed water with heat that would otherwise leave the chimney. First-order numbers suggest about 30 kg/h of steam from about 8 kg/h of wood, enough to pasteurize about 2 m² per hour to 15 cm depth, for about $1,500 in parts. The fuel efficiency target is narrowly missed, and the budget has no contingency.

> **Safety:** SteamRoot is a concept for review, not a design to build. It combines open fire, carbon monoxide, and steam that causes severe burns in under a second. Local boiler and pressure vessel rules may apply even at low pressure. See the Safety section before any further work.

![Hero render](../media/hero.png)

*Figure 1. Massing model on its trailer with the hood set on a bed, next to a 1.75 m person.*

## How it works

1. **Feed.** A 12 V diaphragm pump draws water from a 125 L tank and meters about 0.5 L/min (30 kg/h) into the economizer.
2. **Preheat.** The economizer coil sits in the flue gas above the firebox and warms the feed water from about 15 °C to about 85 °C, recovering heat that would otherwise leave the chimney.
3. **Boil.** The warm water enters the bottom of a monotube coil wound inside the refractory-lined firebox. It boils as it rises through the coil. The coil holds less than 6 L of water, so there is little stored energy.
4. **Vent and separate.** The coil discharges into a steam header that is open to the atmosphere through a vent standpipe with a 1 m water seal. The seal limits header pressure to about 0.1 bar gauge. It cannot stick or be adjusted, and it is never valved off. A certified relief valve on the header is the second line of protection. Water carried over with the steam drains from the header.
5. **Deliver.** Steam flows through a 6 m, 25 mm steam hose to the hood. A diverter valve at the header sends steam either to the hood or up the vent, so the hood can be lifted without steam at the hood.
6. **Pasteurize.** The hood, a 1.2 x 1.0 m insulated open-bottom pan with a soil skirt, sits on the bed. Steam from a perforated manifold condenses in the soil and heats it. After the soil at 15 cm reaches 70 °C and has been held for 20 to 30 minutes, the operator diverts steam to the vent, lifts the hood with its side handles and moves it to the next position.

![Energy flow](../media/flow.png)

*Figure 2. Energy flow at the design point of 30 kg/h of steam. All values are estimates.*

## Main components

Item numbers match the exploded view and `bom/bom.csv`. Items 13 to 15 are not drawn.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Trailer frame and drawbar | Used single-axle garden or utility trailer, deck about 2.0 x 1.2 m | Rated 750 kg or more |
| 2 | Wheels | Trailer wheels, about 460 mm diameter | Included with the trailer |
| 3 | Feed water tank | 125 L HDPE drum with strainer and sight tube | About 4 h of steaming |
| 4 | Feed pump | 12 V diaphragm pump with needle valve and flow meter | Its 3 bar shut-off pressure also caps coil inlet pressure if the coil blocks |
| 5 | Firebox | 700 x 600 x 650 mm steel box, refractory lined, grate, latched door, air damper | Batch-fed with split wood or chips, about 35 kW firing |
| 6 | Monotube steam coil | 316 stainless tube, 25.4 mm OD, about 15 m | Large bore keeps steam velocity and pressure drop low. Proposed, awaiting Amish |
| 7 | Flue-gas economizer | Stainless coil, about 8 m, in a box above the firebox, with condensate drain | Stainless because flue condensate is acidic |
| 8 | Chimney and spark arrestor | 150 mm flue, outlet about 2.4 m above ground | Keeps flue gas above head height |
| 9 | Steam header and vent standpipe | 50 mm header and separator, 1 m open water-seal vent, diverter valve | Primary pressure limit. Proposed, awaiting Amish |
| 10 | Certified relief valve | Code-stamped steam safety valve, set 1 bar (15 psi) or lower | Secondary protection only |
| 11 | Steam hose | EPDM saturated-steam hose, 25 mm bore, 6 m, with whip check | Steam rated, not hot-water rated |
| 12 | Steam hood | 1.2 x 1.0 x 0.25 m insulated pan with soil skirt and handles | Covers 1.2 m² per setting |
| 13 | Battery | 12 V 20 Ah for the feed pump | Not drawn |
| 14 | Instruments | Steam gauge, four type K thermocouples and reader | Soil probes at 15 cm; not drawn |
| 15 | Safety kit | Personal CO alarm, fire extinguisher, gloves, face shield | Not drawn |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with item numbers matching the BOM.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

**Assumptions.** Soil to 15 cm: bulk density 1,300 kg/m³, so 195 kg of dry soil per m²; water content 20 % by dry mass, so 39 kg of water per m². Specific heat 0.84 kJ/(kg K) for dry soil and 4.18 kJ/(kg K) for water. Soil heated from 15 °C to 75 °C (60 K) so the coldest point reaches 70 °C. Latent heat of steam 2.26 MJ/kg. Condensate leaves the soil at about 75 °C, so each kilogram of steam gives about 2.36 MJ to the soil. Hood transfer efficiency 60 % (edge leakage, surface losses, heat conducted below 15 cm and heat stored in the hood). Feed water at 15 °C. Air-dry wood at 16 MJ/kg (range 15 to 18 MJ/kg). Firebox and coil efficiency 55 % without the economizer.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Heat to raise 1 m² of soil to 75 °C at 15 cm | about 19.6 MJ/m² | (195 x 0.84 + 39 x 4.18) kJ/K x 60 K | |
| Steam needed per m² at 15 cm | about 14 kg/m² | 19.6 MJ / (0.60 x 2.36 MJ/kg) | |
| Steam needed per m² at 5 cm | about 4.6 kg/m² | One third of the 15 cm value | |
| Steam output | 30 kg/h | Design point | R3 met by design, unverified |
| Heat into the water | about 21.8 kW | 30 kg/h x (0.36 + 2.26) MJ/kg | |
| Economizer duty | about 2.4 kW | Feed water 15 to 85 °C at 30 kg/h | |
| Fuel power without economizer | about 39.6 kW | 21.8 kW / 0.55 | |
| Fuel power with economizer | about 35.1 kW | (21.8 - 2.4) kW / 0.55 | |
| Fuel to steam efficiency | about 62 % with, 55 % without | 21.8 kW / fuel power | R5 (65 %) **not met** |
| Wood use | about 7.9 kg/h (8.9 kg/h without economizer) | 35.1 kW at 16 MJ/kg | |
| Treatment rate at 15 cm | about 2.2 m²/h | 30 kg/h / 13.8 kg/m² | R2 met, thin margin |
| Treatment rate at 5 cm | about 6.5 m²/h | 30 kg/h / 4.6 kg/m² | R2 met |
| Wood per m² at 15 cm | about 3.6 kg/m² | 7.9 kg/h / 2.2 m²/h | R4 met, thin margin |
| Hood cycle, one setting | about 60 min for 1.2 m² | About 33 min to heat, 25 min hold, 2 min to move | One hood alone gives about 1.2 m²/h; see design choices |
| Steam-side pressure drop | about 0.05 bar in the coil, about 0.01 bar in the hose | Saturated steam, 0.6 kg/m³, 36 m/s in the coil, 28 m/s in the hose | R6 met by design |
| Vent standpipe limit | about 0.1 bar gauge | 1 m water seal | R6 met |
| Water in the heated section | under 6 L | 15 m of 22 mm bore tube, full | R7 met |
| Steaming time per fill | about 4.2 h | 125 L / 30 kg/h | R8 met |
| Loaded mass | about 490 kg | Trailer 150, firebox 100, tank and water 135, other 105 kg | R11 met, thin margin |
| Overall width | about 1.48 m | 1.2 m deck plus wheels | R11 met |
| Parts cost | about $1,500 | Indicative prices, see `bom/bom.csv` | R12 met, no contingency |

The economizer gain is limited by the feed water, not the flue gas. Only about 2.4 kW can go into 30 kg/h of water before it nears boiling, which lifts efficiency from about 55 % to about 62 %. Reaching 65 % would need a better firebox and coil (about 58 % on their own), a combustion air preheater, or both. This is the main performance gap.

![Cutaway](../media/cutaway.png)

*Figure 4. Cutaway showing the coil inside the refractory-lined firebox and the open-bottom hood.*

## Key design choices

- **Open-vented, never sealed.** The steam side is always open to the atmosphere through the vent standpipe. There is no isolating valve between the coil and the vent, and the diverter valve can only switch steam between the hood and the vent, never close both. This is the core safety idea and the reason the concept may stay out of boiler and pressure vessel rules. Proposed, awaiting Amish.
- **Monotube coil instead of a drum boiler.** A once-through coil holds under 6 L of water, so a failure releases little stored energy. The cost is careful feed control: too little water dries the coil. Proposed, awaiting Amish.
- **Large-bore coil (25.4 mm).** A 12.7 mm coil would push steam through at about 170 m/s and need more than 2 bar at the inlet, which defeats the low-pressure idea. A 25.4 mm coil keeps the whole steam side under about 0.1 bar. Alternative: several 12.7 mm circuits in parallel. Proposed: single 25.4 mm coil, awaiting Amish.
- **Stainless steel coil.** 316 stainless tolerates a dry-fire event far better than soft copper, which anneals and weakens. Copper would save about $100. Proposed: stainless, awaiting Amish.
- **Hood steaming, not sheet steaming.** A rigid insulated hood gives better soil contact, repeatable settings and a clear lift procedure. Proposed, awaiting Amish.
- **Treatment rate options.** With one hood, the 25-minute hold leaves the generator venting steam for part of each cycle, so the real rate is about 1.2 m²/h. Options: (a) two hoods used alternately, which reaches about 2 m²/h; (b) one hood plus an insulated blanket laid over treated soil for the hold; (c) accept about 1.2 m²/h. Proposed: option (a), awaiting Amish.
- **Wood only.** Split wood or chips at 20 % moisture or drier, batch-fed by hand. No liquid fuel backup. Proposed, awaiting Amish.

## Safety

SteamRoot is the highest-risk concept in the portfolio. Every later stage must keep this section and extend it.

> **Safety: never sealed.** The steam side must always be open to the atmosphere through the vent standpipe. Never fit a valve, cap or plug that can isolate the coil or header from the vent. Never plug, adjust or remove the relief valve. A sealed coil or tank over a fire can rupture violently.

> **Safety: certified relief valve.** Fit only a certified, code-stamped steam safety valve sized for the full steam output. It is a second line of protection behind the open vent, not a replacement for it. Test it by its lever as the maker directs.

> **Safety: local boiler rules.** Many jurisdictions regulate steam generators by pressure, heating surface, water volume or firing rate, and some regulate all fired steam equipment. The low-pressure design is intended to stay below common thresholds, but this is unconfirmed. Confirm with the local boiler inspector or authority before any build, and follow their ruling even if it is stricter than this document.

> **Safety: steam burns.** Steam at 100 °C releases its latent heat on skin and causes deep burns within a second. Divert steam to the vent before lifting or moving the hood. Keep hands and feet clear of the hood skirt and the vent outlet. Wear heat-resistant gloves, a face shield, long sleeves and closed boots. Keep bystanders, children and animals at least 5 m away. Use a steam-rated hose with a whip check, and inspect it before every use.

> **Safety: dry coil.** If the feed pump stops or the tank runs dry, the coil overheats while the fire keeps burning. Never restart the feed into a hot, dry coil: sudden flashing can burst fittings and throw steam and scalding water. Close the air damper, let the fire die and let the coil cool first. A coil outlet thermocouple with an alarm and a low-level tank alarm are proposed for TRL 3.

> **Safety: fire.** Operate only on bare ground or gravel, clear of dry vegetation, with a fire extinguisher and water at hand. The spark arrestor must be fitted. Do not operate during fire bans or in high wind. Never leave a lit firebox unattended, and let it burn out fully before towing.

> **Safety: carbon monoxide.** Wood fires produce carbon monoxide, which is odorless and deadly. The firebox and chimney must stay outdoors. Steam may be piped into a greenhouse or polytunnel, but the generator may not. The operator wears a personal CO alarm. Never refuel or tend the fire from downwind in the smoke.

> **Safety: hot surfaces and water quality.** The firebox, chimney, economizer, header and hood reach burn temperatures. Use rain water or softened water to limit scale in the coil; scale raises tube temperature and can block the coil.

- **Soil biology.** Steaming kills beneficial organisms as well as pests, and overheating soil well past 70 °C can release manganese and ammonium that harm seedlings. Hold near 70 °C and do not steam longer than needed.
- **Towing.** Tow only with the fire out, the tank drained or secured, and the hood strapped down.

## Open questions for TRL 3

- Confirm the regulatory status of an open-vented, low-pressure fired coil in the first target jurisdiction. This gates all further work.
- Verify firebox and coil efficiency. Is 55 % realistic for a batch-fed wood firebox and a single coil, and can a combustion air preheater close the gap to R5?
- Check two-phase pressure drop in the coil and whether flow stays stable (no slugging or flow reversal) at 30 kg/h.
- Choose feed control: fixed pump rate with manual firing, or a coil outlet thermostat that adjusts pump speed. Proposed: fixed rate with a coil temperature alarm, awaiting Amish.
- Hood transfer efficiency (60 % assumed) drives every rate and fuel number. What does published hood steaming data suggest?
- Where does the hood ride during towing? The deck behind the firebox is too short for it.
- How much does starting soil moisture change steam demand? Wet soil needs more energy but conducts heat better.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).

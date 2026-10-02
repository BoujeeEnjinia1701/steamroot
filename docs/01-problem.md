---
doc_id: STR-PRB-001
title: SteamRoot problem statement
project: SteamRoot
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work, safety)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on first users, first jurisdiction and budget; regulatory ruling marked as an open prerequisite
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Partners and authority answered by Amish's 2026-10-02 decisions"
---

# SteamRoot problem statement

Steaming soil kills weed seeds and soil-borne pathogens without herbicides or fumigants, but the equipment that does it is sized, priced and fueled for large greenhouse operations, so small organic growers who need it most rarely have access to it.

## The problem

Organic and low-input growers fight weeds and soil-borne disease (damping-off, Fusarium, Pythium, Rhizoctonia, root-knot nematodes) with hand weeding, cultivation, rotation and, where allowed, fumigants. Hand weeding is often the largest labor cost on a market garden. Chemical soil fumigants are restricted or banned for organic growers, and methyl bromide has been phased out for most uses under the Montreal Protocol.

Heating soil to about 70 °C (158 °F) for 20 to 30 minutes kills most weed seeds and pathogens while sparing some of the heat-tolerant beneficial organisms. Steam is the traditional way to deliver that heat because condensing steam releases a large amount of energy (about 2.26 MJ per kilogram) right where it condenses. The barriers are equipment and energy:

- Commercial soil steamers are built around diesel, oil or gas boilers sized for greenhouse ranges and nurseries. They are costly to buy and to fuel.
- Many small growers have surplus woody biomass (prunings, hedgerow wood, pallets) but no safe way to turn it into steam.
- Improvised rigs built from pressure cookers, water heaters or sealed tanks are dangerous. A sealed vessel with a fire under it can fail violently.
- Energy per square meter is high, so an inefficient boiler makes the method too slow and too fuel-hungry to be practical.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Small organic farm or market garden | Clear weed seed bank and disease from high-value beds without herbicides | Outdoor beds and polytunnels, 0.1 to 2 ha, beds about 0.75 to 1.2 m wide |
| Nursery or seedling grower | Pasteurize potting media and propagation beds | Sheds and greenhouses; generator must stay outside |
| Community garden or farm cooperative | A shared, towable machine that several growers can use | Shared equipment, varied operator experience |
| Extension educator or researcher | An open, documented reference design to demonstrate and study | Field days, trials, university farms |
| Open hardware community | A buildable, inspectable low-pressure steam design | Farm workshops, makerspaces |

## Constraints

- Garage-buildable prototype within $2,200 USD (raised from $1,500 to $1,800 and then to $2,200 by Amish on 2026-09-25 to allow about 15 % contingency over the priced BOM), using stock steel, stainless tube and off-the-shelf safety parts.
- Near-atmospheric operation: open-vented, never sealed, with a normal working pressure well below the thresholds that bring a boiler under pressure vessel and boiler codes. Thresholds, exemptions and registration rules differ by country, state and province and must be confirmed with the local authority before any build.
- Fired with locally available dry woody biomass; no diesel or propane burner.
- Towable by a small tractor, utility vehicle or car with a hitch; 500 kg or less as towed, with the feed tank and seal pot drained and filled on site.
- Operable by one trained adult, with a second person nearby during steaming.
- Outdoor operation only for the fire. Steam may be piped into a greenhouse or polytunnel; the firebox and chimney may not.

> **Safety:** This project handles open fire, flue gas containing carbon monoxide, and steam that causes severe burns. It is a concept, not a buildable or approved design. Steam generators are regulated equipment in many jurisdictions even at low pressure.

## Out of scope

- Any pressurized boiler or sealed vessel. SteamRoot will not operate as a pressure boiler under any configuration.
- Deep steaming beyond 15 cm and field-scale broadacre treatment.
- Negative-pressure (buried pipe) steaming systems.
- Automatic fire control, remote operation or unattended running.
- Chemical additives mixed with steam.

## Prior work

Steam soil disinfestation is established practice. Greenhouse growers have steamed soil since the late nineteenth century, and it remains common in greenhouse horticulture and nurseries. The main methods are:

- **Sheet steaming:** steam is released under a heavy sheet laid on the soil. Simple, but slow and hard to control at depth.
- **Hood steaming:** a rigid open-bottom hood is pressed onto the bed and moved in steps. Better contact and control than sheets. SteamRoot uses this method.
- **Negative-pressure steaming:** steam is drawn down through the soil by suction through buried perforated pipes. Reaches deeper, but needs a permanent installation.
- **Band steaming:** research machines steam only a narrow band where the crop row will be, cutting energy per hectare.

Soil solarization (clear plastic in hot weather) and anaerobic soil disinfestation are lower-energy alternatives, but they depend on climate and take weeks. Steam works in hours and in any season. A 2014 UNEP review of the methyl bromide phase-out called steam "probably the best technical alternative to MB in protected agriculture", but noted that deep in-ground steaming needs long boiler use, labor and fuel that can make it uneconomic ([UNEP Ozone Secretariat, *Phasing-out Methyl Bromide in Developing Countries*, 2014](https://ozone.unep.org/system/files/documents/Phasing-out%20Methyl%20Bromide%20in%20developing%20countries%20FINAL%20low%20version.pdf)). Energy per square meter is therefore the main limit on adoption, which is why SteamRoot focuses on a biomass fire and a flue-gas economizer. The other prior-work statements above are general practice and are not yet individually cited.

## Decisions and open questions

- First users: one market garden and one nursery. Decided by Amish, 2026-09-25 (STR-DDR-001). Decided by Amish, 2026-10-02: one market garden and one nursery within driving distance of Irving that already steam, solarize or chemically treat soil, found through Texas A&M AgriLife Extension's horticulture contacts. None is named or agreed yet.
- First jurisdiction for the regulatory check: Amish's home jurisdiction. Decided by Amish, 2026-09-25. Decided by Amish, 2026-10-02: Texas; the ruling is asked of the Texas Department of Licensing and Regulation's boiler program.
- **Open prerequisite:** a written ruling from the local boiler authority on whether an open-vented, fired monotube coil is exempt from boiler and pressure vessel rules. Amish approved getting it before TRL 3 detail work. It has not been obtained, so TRL 3 was limited to paper calculations and preliminary drawings.

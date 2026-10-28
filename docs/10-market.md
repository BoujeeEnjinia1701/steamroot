---
doc_id: STR-MKT-001
title: SteamRoot market and viability
project: SteamRoot
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade): segments, cited benchmarks (checked 2026-10-25), cost from the priced BOM, open route"
---

# SteamRoot market and viability

Small organic growers, nurseries and cooperatives that want herbicide-free weed and disease control but cannot justify a diesel or oil-fired steam generator costing USD 7,500 to USD 45,000 (cited below) are the users; SteamRoot offers a wood-fired, open-vented machine at an estimated USD 2,720 in parts that runs on wood they already have. It is small (30 kg/h of steam, about a sixth of the smallest commercial generator found) and slow (1.9 m2/h at 15 cm), so it competes on fuel, price and openness, not on rate. An open design matters because the safety case (open vent, small water inventory) has to be inspectable by growers, educators and the authority. Prices and benchmarks are cited with the date checked. Method: STANDARDS section 23.

> **Safety:** Commercial soil steamers are code boilers with certified controls. SteamRoot is a concept that relies on an exemption not yet ruled on (STR-REG-001, R1); nothing here suggests it may be built or sold before that ruling.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Small organic farm or market garden | Growers on 0.1 to 2 ha, first in Texas within reach of Irving (decided 2026-10-02) | Siebring SG12 steam generator, 400 lb/h (181 kg/h), USD 7,500; Siebring SG15, 500 lb/h, USD 10,000 (Elliott, WSU Puyallup, n.d.); a used 1970s diesel soil steamer at USD 4,000 with USD 2,500 of repairs, hoses and tarps, new "USD 20,000 or more" (Farm Show, 2020) | 2,720 parts (BOM); labour and tools extra | Wood from the farm instead of diesel (a diesel steamer used about 4 gal/h in NCAT's 2022 case); open vent, 7.3 L of heated water; parts cost a third to a quarter of the cheapest new generator found |
| Nursery or seedling grower | Propagation beds and media; generator parked outside a tunnel | Sioux SF11, 385 lb/h (175 kg/h), USD 30,000; Sioux SF20, 680 lb/h (308 kg/h), USD 45,000 (Elliott, WSU Puyallup, n.d.) | 2,720 | Steam piped into the tunnel with the fire outside; small enough for bench and bed work |
| Community garden or farm cooperative | Shared towable machine | Shared steamers bought with farmer grants (NCR-SARE project FNC25-1479, "SARE Shared Steamer"; price not published) | 2,720, shared | One machine towed between members by car |
| Extension and research | Field days, trials, teaching | Proprietary equipment that cannot be opened up | 2,720 | A documented, open reference design (CERN-OHL-S-2.0) |

Benchmark per unit of steam: SteamRoot's USD 2,720 for 30 kg/h is about USD 91 per kg/h; the Siebring SG12 is about USD 41 per kg/h at six times the output. SteamRoot is not cheaper per kilogram of steam; it is cheaper to own, runs on free fuel, and fits a grower who needs a few hundred square metres a season rather than a greenhouse range.

Fuel: at 8.2 kg of wood an hour (STR-CAL-001 v0.5), a day of steaming burns about 65 kg of dry prunings or pallet wood, where a diesel steamer of NCAT's example burns about 4 gallons (15 L) an hour.

## Open route

Who builds it: a farm workshop or makerspace with a competent welder, a tube bender and a coil former, following STR-BLD-001 and the 128 making sketches; safety parts (relief valve, steam hose, diverter) are bought certified. How it spreads: through extension field days (Texas A&M AgriLife Extension, the route to the first partners decided on 2026-10-02), farmer-grant shared equipment programmes like NCR-SARE's, and university farms that can host the TRL 4 soil tests. What keeps it open: the hardware is licensed CERN-OHL-S-2.0 and the scripts MIT (`REUSE.toml`); the regulatory ruling, once obtained, should be published with the design so other jurisdictions can see the argument. No commercial route is planned while the portfolio is capped at TRL 3.

## Sources

- Elliott, Marianne. n.d. "Heat Treatment Techniques, Equipment, and Costs." Best Management Practices Workshop for Nurseries: Steam Sanitation and Disease Identification. Washington State University Puyallup Research and Extension Center (file posted April 2016). https://wpcdn.web.wsu.edu/wp-puyallup/uploads/sites/687/2016/04/03-steam-costs-equipment.pdf, accessed October 25, 2026.
- Farm Show Magazine. 2020. "Soil Steamer Helps Grower Control Weeds, Pathogens." Vol. 44, no. 4: 40. https://www.farmshow.com/a_article.php?aid=36229, accessed October 25, 2026.
- Lent, Chris, and Andy Pressman. 2022. "Soil Steaming for Pathogen, Pest, and Weed Control in High Tunnels." National Center for Appropriate Technology, April 12, 2022. https://www.ncat.org/blog/soil-steaming-for-pathogen-pest-and-weed-control-in-high-tunnels/, accessed October 25, 2026.
- North Central Region SARE. n.d. "SARE Shared Steamer User Guide," Farmer Rancher Grant FNC25-1479. https://projects.sare.org/media/pdf/S/A/R/SARE-Shared-Steamer-user-guide-June-2026.pdf, accessed October 25, 2026.
- SteamRoot priced BOM, `bom/bom.csv` (USD 2,720; one line checked live on 2026-10-25).

# BOM notes

Prices were reviewed at TRL 3 (2026-09-25). They are indicative estimates except item 10, which was checked against a live listing (SupplyHouse.com, Watts 315M2-015, $68.19 on 2026-09-25). The item 10 capacity, 375 lb/h (170 kg/h) at 3/4 in and 15 psi, is from the Watts Series 315 capacity table; it covers the dry-coil refeed flash as Amish decided on 2026-09-25. Item numbers match the callouts in `media/exploded.png` and the general arrangement drawing `cad/drawings/STR-DWG-002`. Items 13 to 16 are not drawn in the model.

- **Total $1,915.00 against the $2,200 budget** (`budget_usd`, raised from $1,500 to $1,800 and then to $2,200 by Amish on 2026-09-25, STR-DDR-002). That leaves $285, about 15 %, as contingency. The TRL 2 total of $1,500 rose because of the second hood (item 12, decided by Amish), the feed and coil alarms (item 16, decided by Amish), the water-seal pot, sight tube and three-way diverter (item 9), and a more realistic firebox lining and hose. The total is computed by `docs/04-calcs/sizing.py`.
- The largest cost risks are the stainless coil (item 6), the steam hose (item 11) and the header and seal assembly (item 9). None of these should be substituted with uncertified or hot-water-rated parts to save money.
- The trailer price assumes a used unit. A new trailer would add about $400 to $700.
- Tools, welding consumables, shipping and wood fuel are not included.
- This is a priced bill of materials for TRL 3 evidence, not a purchasing list. Nothing should be bought before the regulatory ruling (see `docs/REVIEW.md`).

> **Safety:** Items 9, 10, 11, 15 and 16 are safety parts. Buy them new, rated for saturated steam where relevant, and keep the receipts and ratings with the design records.

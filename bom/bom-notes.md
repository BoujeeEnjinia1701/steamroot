# BOM notes

Prices were reviewed at TRL 3 (2026-09-25). They are indicative estimates except item 10, which was checked against a live listing (SupplyHouse.com, Watts 315M2-015, $68.19 on 2026-09-25). The item 10 capacity, 375 lb/h (170 kg/h) at 3/4 in and 15 psi, is from the Watts Series 315 capacity table; it covers the dry-coil refeed flash as Amish decided on 2026-09-25. Item numbers match the callouts in `media/exploded.png` and the general arrangement drawing `cad/drawings/STR-DWG-002`. Items 13 to 16 are not drawn in the model. Item 22, the evaporator bank, is drawn and appears in the exploded view.

- **Total $2,600.00.** Value-engineering target: USD 2,200 (`budget_usd`, a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 2,600 (USD 400 over the target). The 2026-10-02 decisions added line 22 (evaporator bank, $190) and repriced lines 5, 6, 9, 12, 19 and 21: the secondary air damper, one coil turn fewer, the seal pot overflow and loop seal, ballast-rated hood handles, the bank link and reducing unions, and longer and extra fixings. Each new price states its basis in the notes column of `bom.csv`; all are indicative. The total is computed by `docs/04-calcs/sizing.py`.
- The largest cost risks are the stainless coil (item 6), the evaporator bank tube (item 22), the steam hose (item 11) and the header and seal assembly (item 9). None of these should be substituted with uncertified or hot-water-rated parts to save money.
- The trailer price assumes a used unit. A new trailer would add about $400 to $700.
- Tools, welding consumables, shipping and wood fuel are not included.
- This is a priced bill of materials for TRL 3 evidence, not a purchasing list. Nothing should be bought before the regulatory ruling (see `docs/REVIEW.md`).

Mass: the made parts are weighed from the model volumes (`python cad/src/model.py --mass`): 42.5 kg of supports and lines and 26.0 kg of evaporator bank. The machine weighs about 499 kg as towed with the drum and seal pot drained and both hoods aboard, 633 kg full (STR-CAL-001 v0.4).

> **Safety:** Items 9, 10, 11, 15 and 16 are safety parts. Buy them new, rated for saturated steam where relevant, and keep the receipts and ratings with the design records.

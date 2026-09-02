# OpDB Architecture — Interfaces & Data Sources

Load this reference when asked where a data category/field in OpDB originates, how OpDB syncs, or what other systems consume OpDB data.

## Input sources (feed into OpDB)

| Source | Data supplied |
| --- | --- |
| SAP R3 COBALT / S4 HANA | Production Masterdata (~200 tables), Real Estate Masterdata |
| SAP Business Warehouse (BW) | Cost Information (COINS), Product Costing (GPC), Capital Expenditures (FORCE), Earnings & Sales (OCEAN) |
| Asset Effectiveness (GAP) | Asset Masterdata and Reporting |
| Operational Excellence (OpEx) | Reporting Data |
| EHS & Sustainability (tbd) | Calculation Data (STArS, SCOTT), EHS Data (REHSA) |
| Enterprise Data Lake (EDL) | Exchange & Inflation Rates, Price Indices, Forecasts |
| Communication Directory (GCD) | Persons / Orgs |
| Finance (CF) | IFAS Companies |
| Phase Gate | Projects |
| Other sources (offline/historical) | RESIS (Real Estate Sites), ZZS/Advance (former SiteDB), InPla (InvestPlanningDB), CA PPM, CEDAR/WHG, beneFITool, BSB Plant-definition LU, BSB ICA (NSP-Qs/PEI) |

## Data usage (consumers of OpDB)

- **Manufacturing Dashboard** — full range of production, cost, and sustainability-related data; the main reporting front-end for OpDB (all legacy front-end reports are deprecated/removed in favor of it). Operates with the same access rights as OpDB.
- **Cluster/Plant Structure (incl. Cost Center assignment)** — consumed by AE/GAP, REHSA, SAP BW (COINS, TAPAS), RSA Archer, GANS DB, VAMOS, SCOTT, STArS, CO2 Calc App, AuditDB, Stature, ServiceNow.
- **OpEx Measures** — consumed by Phase Gate.
- **SAP Masterdata** — consumed by AE/GAP, MES-i Pro, AMSID (GE). This is the **Global BASF Cluster/Plant Structure and SAP Cost Center assignment**, i.e. SAP masterdata.
- **Enterprise Data Lake** — Trusted Structures (TRS).
- **BASF Data Catalog (Collibra)** — documentation of OpDB (metadata, TRS).
- **OD-specific Dashboards** — full range of OpDB data for dozens of other dashboards.
- **Access Rights Management and Row-Level Security** — dynamic, enforced down to Plant level.

## Statistics

- ~10,000 dedicated roles (for confidential data only).
- Row-level security: direct read access to internal data for all BASF employees, no dedicated role required.
- ~500,000 lines of code across the OpDB application.
- Several dozen other dashboards and data users beyond the Manufacturing Dashboard.

## Data categories, sources, and maintenance workload

| Data category | Based on | Maintenance | Workload |
| --- | --- | --- | --- |
| Global BASF Cluster/Plant Structure | Real Estate (Sites), HR GCD, IFAS, SAP Org | Mainly manual | Low — basic definition, no link to transactional data, detached from source systems |
| (SAP) Masterdata | SAP Cobalt, AE GAP, and other systems | Automated, complex logic | Severe — meeting the full relational data structure needs requires complex business logic |
| Transactional Data | SAP BW, AE GAP, OpEx-Plan | Automated, complex sync | Medium — sync based on Masterdata; business logic depends on scope/granularity |

## Notes

- OpDB drives highly automated syncs 24 hours a day, mainly (but not only) from SAP.
- Strict relations ensure high data integrity, at the cost of complex sync business logic (small team maintains this).

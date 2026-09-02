# OpDB Data Model — Cluster/Plant/Area Hierarchy

Use this reference when interpreting hierarchy keys/columns from OpDB queries (e.g. `Analysis.Plantmaster`) or explaining what a level in the structure means.

## Core entity definitions

| Entity | Definition |
| --- | --- |
| **Production Site** | Site with at least one production or utility asset (chemical or physical manufacturing). |
| **Plant Cluster** | One or a group of Plants that represent an organizational unit, headed by one manager (per "find.me"). A "Single Plant" not grouped into a cluster is counted as both Cluster and Plant. |
| **Production Plant** | A group of Production Assets that manufacture a product or type of products (e.g. one step of a value chain). |
| **Production Asset** | A group of Production Units with the capacity to produce a type of product using defined manufacturing technologies. See also Asset Effectiveness (GAP-Tool) definitions. |
| **Production Unit** | Includes all equipment required for an independent production step on a flow of material. |
| **Equipment** | An individual physical object; installed in, or part of, a technical system. |

## Area levels (geographical/organizational structure, levels 0–15)

| Level | Name | Notes |
| --- | --- | --- |
| 0 | Global | |
| 1 | Region | E/A, A/P, NA, SA, and LU. **`LU` (Ludwigshafen) is a special case to make numbers/measures comparable to other regions — it is NOT part of any Sub Region or Country.** |
| 2 | Sub Region | Per COPA Hierarchy (Corporate Finance). |
| 3 | Country | ISO 3166 alpha-2 code. Some exceptions use alpha-3 (`LUX`, `SAU`). Some codes differ from common reporting, e.g. `GB`<>`UK` or `GR`<>`EL`. |
| 4 | Statoid | Province/County/State — optional; basis was Real Estate (used for CN, JP, US). |
| 5 | Site Cluster | Optional grouping of Sites; key/name analogous to Sites. |
| 6 | Site | Per Real Estate definition (key mainly 3 letters). |
| 7 | Site Part | Sub-Site, mainly to group legal entities at a Site — optional, not defined by Real Estate. |
| 8 | Plant Cluster | Responsibility of a dedicated Plant Manager (per "find.me"). "Single Plants" may also be defined at this level (counted as Cluster **and** Plant). Key always starts with the Site key, followed by `_` and a short name. |
| 9 | Plant | Group of assets to manufacture a product/type of products; part of a Cluster with more than one Plant. Optional — not every Cluster has an attached Plant ("Single Plant"). Same key/naming convention as Cluster. |
| 10–15 | Plant part, Asset group, Asset, Unit, PM Unit, Equipment | Defined in Asset Effectiveness (GAP-Tool). Only **Assets/Units** from GAP are available in OpDB — other levels are not exposed. Assets use the Plant key as a prefix, followed by a short name. |

Non-production Cluster/Plant entries are also possible (e.g. Utility, Lab, PHL Cluster).

## Definition of "Site" (Real Estate)

Tools of record: SAP RE-FX and BuildingMinds (former tool: RESIS).

- **Regional dimension**: regional/related facilities pursuing BASF Group business purposes, located within one country.
- **Functional relationship**: parts of a site form an operational and functional relationship.
- **Organizational unit**: independent administration/site manager; operated by at least one BASF Group company.
- **Production Sites** are sites with at least one production or utility asset — sub-categories: Chemical Manufacturing (Verbund Site, Multi OD Site, Single OD Site) or Physical Manufacturing.

### Special cases

- Joint Venture site with ≥50% BASF share (BASF management) → counted as a **BASF production site**.
- BASF plant(s) including a piece of real estate at a non-BASF site → counted as a **BASF production site**.
- Plant owned by a JV company at a BASF site with ≥50% BASF share (BASF management) → counted as a **BASF production plant**.

### Site-level definition rules

- **Site**: within a 50km diameter, business relationship, one management (2 of 3 criteria).
- Every site with production is a production site, even if production is only a smaller part of it.
- Exception: very small production sites (e.g. a mixing facility at a customer site) are excluded.
- Exception: Joint Ventures with ≤50% and no BASF management are excluded.
- **Asset**: a facility to manufacture a product or group of products with no side outlet (see Asset Effectiveness / GAP-Tool definition).

## Example hierarchy (illustrative, not exhaustive)

```text
World (Global)
└─ North America (Region)
   └─ USA (Country)
      └─ Peekskill (Site, Prod. Site)
         ├─ Infra (Cluster, Single Utility)
         ├─ Labs (Cluster, Lab Unit)
         └─ Prod (Cluster, Plant Cluster)
            ├─ OCM (Plant in Cluster) → Assets: Reactors etc.
            └─ Specialty (Plant in Cluster)
└─ Asia Pacific (Region)
   └─ Malaysia (Country)
      └─ Kuantan (Site, Prod. Site)
         └─ BPC (Sub Site)
            ├─ BDO Cl. (Cluster, Plant Cluster)
            │  ├─ BDO (Plant in Cluster) → Assets: BDO, THF, GBL, ...
            │  └─ MAN (3rd Party Plant)
            └─ TBPR (Single Plant)
```

## Correlation to SAP

| OpDB concept | SAP concept |
| --- | --- |
| Production Plant / Production Asset | **Cost center** — an organizational unit within a controlling area representing a defined location of cost incurrence. |
| Production Plant / Production Asset | **Business process** — uses resources across departments; can consume the output of multiple cost centers in a controlling area. |
| Production Asset | **Resource** — an individual machine, a production resource/tool, an employee, or group of employees. |
| Production Unit | **Functional location** — an element of a technical structure. |
| Equipment | **Equipment** — an individual physical object, installed in or part of a technical system. |

A single Plant is typically assigned a single cost center, or a group of cost centers.

## Organizational structure ("Orgs") — for context when Org keys/associations appear

Levels: **Enterprise → Segment → Division → Level 3 (BU) → Level 4 → Level 5+**

- Example chain: BASF (Enterprise) → Performance Products (Segment) → Nutrition & Health `EN` (Division) → Gl. Op. & Tech. `ENO` (Level 3/BU) → Op. Human Nutrition `ENO/H` (Level 4) → N&H Prod. Ballerup `ENO/HB` (Level 5+).
- Orgs are linked to Areas via **Associated Areas** (e.g. an org at Level 5+ associated with a specific Site or Plant).
- **Additional Reportings** are secondary org relations (e.g. for Security) — treat these like additional reporting lines, not the primary hierarchy.

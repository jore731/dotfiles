---
name: operations-database
description: 'Connect to and query the BASF Operations Database (OpDB) — the SQL Server system of record for the global BASF Cluster/Plant structure, cost center assignments, and production KPIs. Use when asked to connect to OpDB, build/populate a Python (pyodbc) connection script for operations-database.basf.net, run or execute a query against OpDB, query the Analysis schema (e.g. Analysis.Plantmaster, SiteDB.Sites), interpret Site/Cluster/Plant/Asset hierarchy keys (RegionKey, CountryKey, SiteKey, ClusterKey, PlantKey), or explain OpDB row-level security and data sources. Not for PIMS/IP.21 historian data (use sql-plus or pyfetchr-pims-query), LIMS lab data (use edl-lims-database), Dataverse (use basf-dataverse), or ADX/KQL production data (use process-data).'
author: Eric Dixon
metadata:
  category: manufacturing-data
  version: "1.0.0"
---

# BASF Operations Database (OpDB)

## Overview

OpDB is BASF's single source of truth for the global Cluster/Plant structure defined below Real Estate Sites, and hosts production KPIs consolidated from SAP, Asset Effectiveness (GAP), OpEx, and other sources. It is a SQL Server database at `operations-database.basf.net` (database `OperationsDB`), used by the Manufacturing Dashboard and several dozen other apps/dashboards.

## Connecting from Python

Default to `pyodbc` with **Windows Authentication** — never hardcode a username or password. The query runs under the caller's own Windows/AD identity, which is also how OpDB's row-level security is enforced.

Use [scripts/query_opdb.py](scripts/query_opdb.py) to connect and run a query. From this skill's root (`skills/operations-database`):

```bash
python scripts/query_opdb.py "SELECT * FROM Analysis.Plantmaster ORDER BY RegionKey, CountryKey, SiteKey, ClusterKey, PlantKey"
python scripts/query_opdb.py --file my_query.sql --out results.csv
```

```python
from scripts.query_opdb import run_query
df = run_query("SELECT SiteId, SiteKey, SiteName, ODOrgKey FROM SiteDB.Sites")
```

Key connection facts:
- **Server**: `operations-database.basf.net`
- **Database**: `OperationsDB`
- **Auth**: `Trusted_Connection=Yes` requests Windows Authentication for the current Windows user; do not pass explicit credentials in `pyodbc` code.
- **Driver**: try `{ODBC Driver 17 for SQL Server}` first; fall back to `{SQL Server}` only when the first attempt fails with ODBC SQLSTATE `IM002` (driver not found).
- Requires `pip install pyodbc pandas` and a domain-joined Windows machine with network access to OpDB (same requirement as any BASF-internal SQL Server).
- **Windows only, in practice**: `Trusted_Connection=Yes` relies on Windows Authentication via the current AD session. Confirmed working from a domain-joined Windows machine with the default ODBC driver. On Linux (including WSL2), this only has a chance of working with the Microsoft ODBC Driver for Linux (`msodbcsql17`/`18`) plus a valid Kerberos ticket for the BASF AD domain (`kinit`) and correct `krb5.conf`/SPN setup — this is unverified and not documented in the source material, so don't promise it works without testing.
- `pd.read_sql(query, conn)` with a raw `pyodbc` connection emits a harmless `UserWarning` about SQLAlchemy support — this is expected, not an error.
- To import `run_query`, run Python from this skill's root and use `from scripts.query_opdb import run_query`.

## Which schema/tables to query

- Prefer views in the **`Analysis`** schema — they are purpose-built and optimized for self-service BI/reporting (e.g. `Analysis.Plantmaster`).
- `SiteDB.Sites` exposes site master data: `SiteId`, `SiteKey`, `SiteName`, `ODOrgKey`.
- `Analysis.Plantmaster` exposes the full cluster/plant hierarchy in one row per plant; sort by `RegionKey, CountryKey, SiteKey, ClusterKey, PlantKey` to read it in hierarchical order.
- Don't invent table/column names beyond what's documented here or confirmed by the user — ask, or query `Analysis.Plantmaster` / `SiteDB.Sites` first to discover real column names before assuming others exist.

## Loading references

- Load [references/data-model.md](references/data-model.md) before interpreting hierarchy keys/levels (Region, Country, Site, Plant Cluster, Plant, Asset, Unit, Equipment) or explaining what a level or key naming convention means.
- Load [references/architecture.md](references/architecture.md) when asked where a data category originates (SAP, GAP, OpEx, EDL, etc.), how OpDB syncs, or what other systems consume OpDB data.
- Load [references/other-connection-methods.md](references/other-connection-methods.md) if the user wants Power Platform, Excel, Access, or a generic BI-tool (OLEDB) connection instead of Python.

## Access & security

- Row-level security is dynamic down to Plant level and tied to the caller's Windows/AD identity — every BASF employee can read internal (non-confidential) data with **no dedicated role**.
- Confidential data requires one of ~10,000 dedicated roles, assigned according to job/scope/need.
- Because access is identity-based, always run queries under the requesting user's own Windows account — never share or hardcode another user's credentials, and never suggest a shared service account as a shortcut around row-level security.

## Gotchas

- `LU` (Ludwigshafen) is a Region-level code used for reporting comparability only — it is **not** part of any Sub Region or Country. Don't treat it as a normal region when writing filters.
- Country codes are ISO 3166 alpha-2, with exceptions (`LUX`, `SAU` use alpha-3); some codes differ from common reporting (`GB`<>`UK`, `GR`<>`EL`).
- A Plant Cluster key always starts with the Site key, followed by `_` and a short name; Plant keys follow the same convention. A "Single Plant" (a cluster with only one plant) counts as both Cluster and Plant.
- Not every Plant Cluster has a Plant beneath it; non-production Cluster/Plant entries also exist (e.g. Utility, Lab, PHL Cluster).
- Only Assets/Units defined in Asset Effectiveness (GAP) are available in OpDB — deeper GAP levels (Plant part, Asset group, PM Unit, Equipment) are not exposed.

## If the connection fails

- **Driver not found** (`IM002`/similar): the ODBC driver name doesn't match what's installed — try the other driver value (`{ODBC Driver 17 for SQL Server}` vs `{SQL Server}`), or list installed drivers with `pyodbc.drivers()`.
- **Login/timeout failures**: usually means no network path to `operations-database.basf.net` (VPN/on-site network required) rather than a credential problem, since auth is Windows-integrated.
- **A query on a schema/table returns zero rows or an unexpected permission error**: this is almost always row-level security, not a bad query — confirm the requesting user actually has visibility into that Plant/Site, or holds the dedicated role required for confidential data, before assuming the SQL is wrong.
- **Results look stale or incomplete**: OpDB syncs continuously from SAP and other sources on a schedule it doesn't expose per-table — don't assume real-time consistency with the source system for very recent changes.

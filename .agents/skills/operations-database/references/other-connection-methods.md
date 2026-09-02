# OpDB — Non-Python Connection Methods

Load this reference only when the user wants to connect to OpDB from a tool other than Python (Power Platform, Excel, Access, or a generic BI tool). All methods connect using the individual user's own access rights (Windows/Trusted Authentication) — there is no separate service account.

Common connection facts across all tools:

- Server: `operations-database.basf.net`
- Database: `OperationsDB`
- Auth: Windows/Trusted Authentication (`Trusted_Connection=Yes`)

## Power Platform

- Add a new connection.
- Connection type: `SQL Server`.
- Authentication: `Windows Authenticate`.
- Server: `operations-database.basf.net`.
- User name: `UserAccount@basfad.basf.net` (the caller's own AD account).
- Password: the Windows user's own password.
- Gateway: `BASF_Central_Managed_Gateway`.
- Requires a Power Platform **Premium** license to add a SQL Server connection.

## Excel tables (via ODBC DSN file)

1. Save the following as `OperationsDB.dsn` in the user's Data Sources folder (under Documents):

   ```ini
   [ODBC]
   DRIVER=SQL Server
   DATABASE=OperationsDB
   APP=Microsoft Office 2010
   Trusted_Connection=Yes
   SERVER=operations-database.basf.net
   ```

2. In the Data ribbon, click **Existing Connections**.
3. Select the `OperationsDB` data source and pick the table to show.
4. For complex/filtered queries, enter a SQL query directly in the connection's property dialog.

## Access — linked tables

1. Save the same `OperationsDB.dsn` file as above.
2. In **External Data**, click **New Data Source → From Other Sources → ODBC Database**.
3. Choose **"Link to the data source by creating a linked table"**.
4. Select the DSN file and the tables needed.
5. When Access asks for a unique key, select the `...Key` field (except for `...History` tables).
6. **Always close linked tables overnight** — leaving them open can block server operations.
7. If content looks stale/odd after a view change, use **Refresh Link** (Access does not auto-refresh view definitions).

## Access — ODBC pass-through queries

1. Create a new query and define it as **pass-through**.
2. Set the ODBC Connect String to:

   ```text
   ODBC;DRIVER=SQL Server;SERVER=operations-database.basf.net;Trusted_Connection=Yes;DATABASE=OperationsDB
   ```

3. Enter valid Microsoft SQL Server `SELECT` syntax.

## Generic BI tools (OLEDB)

Example — retrieving the site list:

```sql
OLEDB CONNECT TO 'Provider=sqloledb;Server=operations-database.basf.net;Database=OperationsDB;Trusted_Connection=yes;';
SQL SELECT SiteId, SiteKey, SiteName, ODOrgKey FROM SiteDB.Sites;
```

The views in schema `Analysis` are optimized for self-service BI usage — prefer them over raw base tables when building reports.

## Office Data Connection (ODC) example seen in practice

Some existing ODC configs use a named user + trusted connection together (the `UID` is effectively unused when `Trusted_Connection=Yes`, since the connection always authenticates as the current Windows user):

Connection string:

```text
DRIVER=SQL Server;SERVER=operations-database.basf.net;UID=SorgM;Trusted_Connection=Yes;APP=Microsoft Office 2010;WSID=H95X7KC2;DATABASE=OperationsDB
```

Command text:

```sql
SELECT *
FROM Analysis.Plantmaster
ORDER BY RegionKey, CountryKey, SiteKey, ClusterKey, PlantKey;
```

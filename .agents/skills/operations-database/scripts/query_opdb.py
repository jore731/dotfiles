#!/usr/bin/env python3
"""
Query the BASF Operations Database (OpDB) via SQL Server / pyodbc.

Connects using Windows Authentication under the caller's own
Windows/AD identity - no username or password is embedded here, and OpDB's
row-level security is enforced automatically based on that identity.

Requires: pip install pyodbc pandas
Requires an ODBC driver for SQL Server (e.g. "ODBC Driver 17 for SQL Server",
falling back to "SQL Server" only when the preferred driver is not installed).

Run from the operations-database skill root:
    python scripts/query_opdb.py "SELECT * FROM Analysis.Plantmaster ORDER BY RegionKey, CountryKey, SiteKey, ClusterKey, PlantKey"
    python scripts/query_opdb.py --file my_query.sql --out results.csv
"""
import argparse

import pandas as pd
import pyodbc

SERVER = "operations-database.basf.net"
DATABASE = "OperationsDB"
DEFAULT_DRIVER = "{ODBC Driver 17 for SQL Server}"
FALLBACK_DRIVER = "{SQL Server}"


def _is_driver_not_found(error: pyodbc.Error) -> bool:
    """Return whether an ODBC error reports an unavailable driver."""
    return bool(error.args) and error.args[0] == "IM002"


def get_connection(driver: str = DEFAULT_DRIVER) -> pyodbc.Connection:
    """Open a Windows Authentication connection to OpDB."""
    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=Yes;"
    )
    try:
        return pyodbc.connect(conn_str)
    except pyodbc.Error as error:
        if driver == FALLBACK_DRIVER or not _is_driver_not_found(error):
            raise
        fallback_str = (
            f"DRIVER={FALLBACK_DRIVER};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            "Trusted_Connection=Yes;"
        )
        return pyodbc.connect(fallback_str)


def run_query(query: str, driver: str = DEFAULT_DRIVER) -> pd.DataFrame:
    """Run a SQL query against OpDB and return the result as a DataFrame."""
    with get_connection(driver) as conn:
        return pd.read_sql(query, conn)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a SQL query against OpDB")
    parser.add_argument("query", nargs="?", help="SQL query string")
    parser.add_argument("--file", help="Path to a .sql file containing the query")
    parser.add_argument("--out", help="Optional CSV output path")
    parser.add_argument(
        "--driver", default=DEFAULT_DRIVER, help="ODBC driver name, e.g. '{SQL Server}'"
    )
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            query = f.read()
    elif args.query:
        query = args.query
    else:
        parser.error("Provide a query string or --file path")

    df = run_query(query, args.driver)
    if args.out:
        df.to_csv(args.out, index=False)
        print(f"Wrote {len(df)} rows to {args.out}")
    else:
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()

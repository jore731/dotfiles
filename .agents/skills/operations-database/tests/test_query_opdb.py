import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "query_opdb.py"


class FakeOdbcError(Exception):
    pass


@pytest.fixture
def query_opdb(monkeypatch):
    fake_pyodbc = SimpleNamespace(
        Connection=object,
        Error=FakeOdbcError,
        connect=Mock(),
    )
    monkeypatch.setitem(sys.modules, "pyodbc", fake_pyodbc)
    monkeypatch.setitem(sys.modules, "pandas", SimpleNamespace(DataFrame=object))

    spec = importlib.util.spec_from_file_location("query_opdb_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_get_connection_retries_with_fallback_for_driver_not_found(query_opdb):
    expected_connection = object()
    query_opdb.pyodbc.connect.side_effect = [
        FakeOdbcError("IM002", "driver not found"),
        expected_connection,
    ]

    connection = query_opdb.get_connection()

    assert connection is expected_connection
    assert query_opdb.pyodbc.connect.call_count == 2
    assert "DRIVER={SQL Server}" in query_opdb.pyodbc.connect.call_args.args[0]


def test_get_connection_does_not_retry_non_driver_error(query_opdb):
    query_opdb.pyodbc.connect.side_effect = FakeOdbcError("28000", "login failed")

    with pytest.raises(FakeOdbcError, match="login failed"):
        query_opdb.get_connection()

    assert query_opdb.pyodbc.connect.call_count == 1
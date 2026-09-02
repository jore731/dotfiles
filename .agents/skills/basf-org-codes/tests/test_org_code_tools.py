from __future__ import annotations

import importlib.util
import json
import runpy
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "org_code_tools.py"
SPEC = importlib.util.spec_from_file_location("org_code_tools", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_normalize_org_code_removes_spaces_and_upcases() -> None:
    assert MODULE.normalize_org_code(" gdb / e ") == "GDB/E"


def test_split_org_code_uses_only_known_regional_prefixes() -> None:
    assert MODULE.split_org_code("A-CPA") == ("A", "CPA", None)
    assert MODULE.split_org_code("CC-E") == (None, "CC-E", None)


def test_extract_division_handles_regional_and_exception_patterns() -> None:
    assert MODULE.extract_division("A-CPA") == "CP"
    assert MODULE.extract_division("CC-E") == "CC-E"
    assert MODULE.extract_division("CHEM") == "CHEM"
    assert MODULE.extract_division("G/ECO/OSAI/L") == "EC"
    assert MODULE.extract_division("G/ECO-DAF") == "EC"
    assert MODULE.extract_division("GECO-DD") == "GEC"


def test_extract_division_covers_empty_slash_before_dash_and_long_codes() -> None:
    assert MODULE.extract_division("   ") == ""
    assert MODULE.extract_division("AB/C-D") == "AB"
    assert MODULE.extract_division("LONG") == "LONG"


def test_split_org_code_rejects_invalid_values() -> None:
    with pytest.raises(ValueError, match="Could not parse org code"):
        MODULE.split_org_code("")


@pytest.mark.parametrize(
    ("main", "tail", "expected_level", "expected_confidence"),
    [
        ("RES", None, "Board or ressort family", "medium"),
        ("I", None, "Board or ressort", "medium"),
        ("EC", None, "President or division head", "high"),
        ("GBM", None, "Senior Vice President or unit head", "high"),
        ("GBM", "E", "Vice President or direct executive report", "medium"),
        ("GBM", "TEAM", "Group, team, or local continuation", "medium"),
        ("CC-E", None, "Exception or special business family", "low"),
        ("LONG", None, "Uncertain", "low"),
    ],
)
def test_infer_level_covers_all_branches(
    main: str,
    tail: str | None,
    expected_level: str,
    expected_confidence: str,
) -> None:
    level, confidence, _ = MODULE.infer_level(main, tail)
    assert (level, confidence) == (expected_level, expected_confidence)


def test_lookup_org_name_prefers_exact_matches() -> None:
    assert MODULE.lookup_org_name("GBM") == ("GBM", "Global Consulting Services")
    assert MODULE.lookup_org_name("CM") == ("CM", "Monomers")
    assert MODULE.lookup_org_name("RES") == ("RES", "Board / ressort family")


def test_lookup_org_name_falls_back_to_nearest_higher_code() -> None:
    assert MODULE.lookup_org_name("GDB/E") == ("GDB", "Digitalization of Research & Development")
    assert MODULE.lookup_org_name("COE") == ("CO", "Corporate Center family")


def test_candidate_lookup_codes_and_unknown_name_paths() -> None:
    assert MODULE.candidate_lookup_codes("A-CC-E/X") == ["A-CC-E/X", "A-CC-E", "CC-E", "CC-", "CC"]
    assert MODULE.lookup_org_name("ZZZ/TEAM") == (None, None)


def test_explain_org_code_includes_name_and_fallback_caveat() -> None:
    interpretation = MODULE.explain_org_code("GDB/E")
    assert interpretation.matched_code == "GDB"
    assert interpretation.matched_name == "Digitalization of Research & Development"
    assert "Known name: Digitalization of Research & Development (GDB)." in interpretation.explanation
    assert any("nearest higher mapped code GDB" in caveat for caveat in interpretation.caveats)


def test_parse_output_fields_are_present() -> None:
    interpretation = MODULE.explain_org_code("CC-E")
    assert interpretation.division == "CC-E"
    assert interpretation.matched_name == "Environmental Catalyst & Metal Solutions (ECMS)"


def test_explain_org_code_includes_prefix_and_unknown_name_behavior() -> None:
    interpretation = MODULE.explain_org_code("A-ZZZ")
    assert interpretation.matched_code is None
    assert interpretation.matched_name is None
    assert "A- is likely a regional or scope prefix." in interpretation.explanation
    assert any("Prefix A- usually indicates regional or scope context" in caveat for caveat in interpretation.caveats)


def test_main_extract_division_command_outputs_tab_separated_values(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["org_code_tools.py", "extract-division", "A-CPA", "CHEM"])
    assert MODULE.main() == 0
    assert capsys.readouterr().out.splitlines() == ["A-CPA\tCP", "CHEM\tCHEM"]


def test_main_lookup_name_command_outputs_json(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["org_code_tools.py", "lookup-name", "GBM", "ZZZ"])
    assert MODULE.main() == 0
    records = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert records == [
        {
            "original": "GBM",
            "normalized": "GBM",
            "matched_code": "GBM",
            "matched_name": "Global Consulting Services",
        },
        {
            "original": "ZZZ",
            "normalized": "ZZZ",
            "matched_code": None,
            "matched_name": None,
        },
    ]


def test_main_parse_command_outputs_json(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["org_code_tools.py", "parse", "GDB/E"])
    assert MODULE.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["normalized"] == "GDB/E"
    assert payload[0]["matched_code"] == "GDB"


def test_main_explain_command_outputs_human_readable_text(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["org_code_tools.py", "explain", "A-CPA"])
    assert MODULE.main() == 0
    output = capsys.readouterr().out
    assert "A-CPA maps most closely to division/root CP." in output
    assert "confidence:" in output
    assert "caveats:" in output


def test_running_as_main_exits_cleanly(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", [str(MODULE_PATH), "parse", "GBM"])
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(MODULE_PATH), run_name="__main__")

    assert exc_info.value.code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["matched_name"] == "Global Consulting Services"

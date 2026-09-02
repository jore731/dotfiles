#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass


STRUCTURE_RE = re.compile(r"^(?:(?P<prefix>[AENSG])\-)?(?P<main>[^/]+?)(?:/(?P<tail>.+))?$")
SPECIAL_DIVISION_CODES = {"BNB", "BVC", "CHEM"}
KNOWN_ORG_NAMES = {
    "RES": "Board / ressort family",
    "CD": "Corporate Development",
    "CL": "Corporate Legal, Compliance, Insurance & Security",
    "CF": "Corporate Finance",
    "COR": "Corporate Environmental Protection, Health & Safety & Quality",
    "COH": "Corporate Human Resources",
    "COM": "Corporate Communications & Government Relations",
    "COI": "Corporate Investor Relations",
    "COA": "Corporate Audit",
    "COT": "Corporate Taxes & Duties",
    "CO": "Corporate Center family",
    "CDE": "Economic Evaluations",
    "CDS": "Corporate Strategy",
    "CDT": "Corporate Technology",
    "CDM": "Senior Project NGBA Core Businesses",
    "CLC": "Corporate Compliance",
    "CLS": "Legal & Compliance Services",
    "CLI": "Insurance",
    "CLN": "Legal North America",
    "CFM": "Corporate Mergers & Acquisitions",
    "CFP": "Group Reporting & Performance Management",
    "CFT": "Corporate Treasury",
    "GB": "Global Business Services",
    "GBT": "Portfolio & Technology Steering",
    "GBE": "Regional Business Services EMEA",
    "GBA": "Regional Business Services Asia Pacific",
    "GBW": "Regional Business Services Americas",
    "GBI": "Global Intellectual Property & Regulatory Services",
    "GBM": "Global Consulting Services",
    "GD": "Global Digital Services",
    "GDS": "Cyber Security",
    "GDB": "Digitalization of Research & Development",
    "GDF": "Digitalization of Businesses",
    "GDD": "Digitalization of Production & Technology",
    "GDE": "Digitalization of Services & ERP Platforms",
    "GDA": "Digitalization of Workspace & Infrastructure",
    "GP": "Global Procurement",
    "GPD": "Global Direct & Logistics Procurement",
    "GPI": "Global Indirect Procurement",
    "GPT": "Global Traded Products Procurement",
    "GE": "Global Engineering Services",
    "GEC": "Global Customized Chemicals & Engineering Services North America",
    "GEM": "Global Make Chemicals & Engineering Services Europe",
    "GEA": "Global High Value Engineering Centers & Engineering Services Asia Pacific",
    "RG": "Group Research",
    "RGC": "Catalysts Research and Testing",
    "RGR": "Process Research and Chemical Engineering",
    "RGQ": "Digitalization, Automation and Innovation Management",
    "RGS": "Chemical, Material and Regulatory Science",
    "CP": "Petrochemicals",
    "CPK": "BASF PETRONAS Chemicals Sdn. Bhd., Kuantan Verbund Site",
    "CPM": "Global Strategic Business Development",
    "CI": "Intermediates",
    "CIP": "Operations Europe, Global EHSQ and Asset Management",
    "CIS": "Technology and Strategic Marketing",
    "PM": "Performance Materials",
    "PMD": "R&D Performance Materials",
    "CM": "Monomers",
    "CMS": "Strategy",
    "CMT": "Technology",
    "ED": "Dispersions & Resins",
    "EDG": "Global Technology, Investments and Supply Chain",
    "EDI": "Colloidal System R&D Platform",
    "EV": "Performance Chemicals",
    "EVM": "Manufacturing & Technology",
    "BM": "Battery Materials",
    "BMD": "Strategic Development",
    "BMO": "Operations, Investments & Technology",
    "BMS": "BASF Shanshan Battery Materials",
    "CC-E": "Environmental Catalyst & Metal Solutions (ECMS)",
    "CC": "Environmental Catalyst & Metal Solutions family",
    "EC": "Coatings",
    "ECP": "Global Operations Paints & Resins",
    "EM": "Care Chemicals",
    "EMX": "Global Operations",
    "EN": "Nutrition & Health",
    "ENT": "Technology",
    "AP": "Agricultural Solutions",
    "APD": "Regulatory, Sustainability & Public Affairs",
    "APR": "R&D Crop Protection",
    "APP": "R&D Seeds & Traits",
    "APB": "Global Controlling and Business Enablers",
    "APM": "Global Strategic Marketing & Sustainability",
    "APT": "Global Operations",
    "ES": "European Site & Verbund Management",
    "ESG": "Corporate Health Management",
    "ESH": "Human Resources",
    "ESE": "Environmental & Safety Services Ludwigshafen",
    "ESI": "Infrastructure & Plant Services Ludwigshafen",
    "ESO": "Technical Services Ludwigshafen",
    "ESL": "European Site Logistics Operations",
    "ESM": "Site Management Ludwigshafen",
    "NA": "BASF Corporation",
    "AC": "Greater China",
    "AM": "Mega Projects Asia",
}


@dataclass(frozen=True)
class OrgCodeInterpretation:
    original: str
    normalized: str
    prefix: str | None
    main: str
    tail: str | None
    division: str
    matched_code: str | None
    matched_name: str | None
    probable_level: str
    confidence: str
    explanation: str
    caveats: list[str]


def normalize_org_code(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().upper())


def split_org_code(value: str) -> tuple[str | None, str, str | None]:
    normalized = normalize_org_code(value)
    match = STRUCTURE_RE.match(normalized)
    if not match:
        raise ValueError(f"Could not parse org code: {value}")
    return match.group("prefix"), match.group("main"), match.group("tail")


def extract_division(value: str) -> str:
    normalized = normalize_org_code(value)
    if not normalized:
        return ""
    if normalized in SPECIAL_DIVISION_CODES:
        return normalized
    if normalized.startswith("CC-"):
        return "CC-E" if normalized.startswith("CC-E") else "CC"
    if normalized.startswith("GECO-"):
        return "GEC"
    if len(normalized) >= 4 and normalized[0] in "AENSG" and normalized[1] == "/":
        return normalized[2:4]
    if "-" in normalized:
        dash_index = normalized.index("-")
        if "/" in normalized and normalized.index("/") < dash_index:
            return normalized[:2]
        return normalized[dash_index + 1 : dash_index + 3]
    if "/" in normalized:
        return normalized[:2]
    if len(normalized) > 3:
        return normalized
    return normalized[:2]


def infer_level(main: str, tail: str | None) -> tuple[str, str, str]:
    if main == "RES":
        return "Board or ressort family", "medium", "RES is treated as a board-related exception provided by current BASF practice"
    if main == "I":
        return "Board or ressort", "medium", "single-letter board notation is not fully systematic"
    if len(main) == 2 and not tail:
        return "President or division head", "high", "two-letter stem usually marks a division-level root"
    if len(main) == 3 and not tail:
        return "Senior Vice President or unit head", "high", "three-letter stem usually marks a unit-level executive root"
    if tail and len(tail) == 1:
        return "Vice President or direct executive report", "medium", "single-character slash tail often signals a level-4 executive unit"
    if tail:
        return "Group, team, or local continuation", "medium", "tail after slash usually indicates locally extended lower-level coding"
    if main.startswith("CC-") or main == "CC-E":
        return "Exception or special business family", "low", "CC- patterns are real but do not follow the common decoding rules cleanly"
    return "Uncertain", "low", "pattern does not map cleanly to the common executive heuristics"


def candidate_lookup_codes(value: str) -> list[str]:
    normalized = normalize_org_code(value)
    prefix, main, tail = split_org_code(normalized)
    candidates: list[str] = []

    def add(candidate: str | None) -> None:
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    add(normalized)
    if tail:
        add(f"{prefix}-{main}" if prefix else main)
    add(main)

    if prefix and main.startswith("CC-"):
        add(main)

    if len(main) > 3:
        for length in range(len(main) - 1, 1, -1):
            add(main[:length])
    elif len(main) == 3:
        add(main[:2])

    if prefix and len(main) >= 2:
        add(main[:2])

    if main.startswith("CC-"):
        add("CC")

    return candidates


def lookup_org_name(value: str) -> tuple[str | None, str | None]:
    for candidate in candidate_lookup_codes(value):
        if candidate in KNOWN_ORG_NAMES:
            return candidate, KNOWN_ORG_NAMES[candidate]
    return None, None


def explain_org_code(value: str) -> OrgCodeInterpretation:
    normalized = normalize_org_code(value)
    prefix, main, tail = split_org_code(normalized)
    division = extract_division(normalized)
    matched_code, matched_name = lookup_org_name(normalized)
    probable_level, confidence, heuristic_note = infer_level(main, tail)

    caveats = [
        heuristic_note,
        "Org codes describe units, not people.",
        "Titles should be checked before asserting an exact rank.",
    ]
    if prefix:
        caveats.append(f"Prefix {prefix}- usually indicates regional or scope context, not a different core hierarchy.")
    if normalized.startswith("CC-"):
        caveats.append("CC- patterns are known exceptions and should be interpreted cautiously.")
    if division in {"CO", "CC", "CC-E"} or main in {"COH", "COR", "COM", "COI"}:
        caveats.append("Corporate Center and CC- families can bypass the normal division-root logic.")
    if matched_code and matched_code != normalized:
        caveats.append(f"No exact name match was found; using nearest higher mapped code {matched_code}.")

    parts = [f"{normalized} maps most closely to division/root {division}."]
    if matched_name:
        parts.append(f"Known name: {matched_name} ({matched_code}).")
    if prefix:
        parts.append(f"{prefix}- is likely a regional or scope prefix.")
    parts.append(f"{main} is the core org stem.")
    if tail:
        parts.append(f"{tail} is the continuation after the slash.")
    parts.append(f"Most likely reading: {probable_level}.")

    return OrgCodeInterpretation(
        original=value,
        normalized=normalized,
        prefix=prefix,
        main=main,
        tail=tail,
        division=division,
        matched_code=matched_code,
        matched_name=matched_name,
        probable_level=probable_level,
        confidence=confidence,
        explanation=" ".join(parts),
        caveats=caveats,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse and explain BASF org codes.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("parse", "extract-division", "explain", "lookup-name"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("codes", nargs="+", help="One or more BASF org codes")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "extract-division":
        for code in args.codes:
            print(f"{normalize_org_code(code)}\t{extract_division(code)}")
        return 0

    if args.command == "lookup-name":
        for code in args.codes:
            matched_code, matched_name = lookup_org_name(code)
            print(
                json.dumps(
                    {
                        "original": code,
                        "normalized": normalize_org_code(code),
                        "matched_code": matched_code,
                        "matched_name": matched_name,
                    }
                )
            )
        return 0

    interpretations = [explain_org_code(code) for code in args.codes]
    if args.command == "parse":
        print(json.dumps([asdict(item) for item in interpretations], indent=2))
        return 0

    for item in interpretations:
        print(item.explanation)
        print(f"confidence: {item.confidence}")
        print("caveats:")
        for caveat in item.caveats:
            print(f"- {caveat}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

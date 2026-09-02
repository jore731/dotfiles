# BASF Org Code Reference

This reference file holds the more detailed material that supports the `basf-org-codes` skill.

## Authoritative Source

- The ultimate source of truth is the BASF Group Organization material in SharePoint:
    `https://basf.sharepoint.com/sites/coh-files/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2Fcoh%2Dfiles%2FShared%20Documents%2FBASF%20Group%20Organization&viewid=f343d362%2D70f5%2D4d1b%2Da223%2D690e55f27ae1&csf=1&cid=7e7b16e9%2D5e19%2D4315%2D9314%2D6c395d983bc5&FolderCTID=0x0120004973657A417AAB4AA9B15E58D3C4C708`
- Use the heuristics in this skill for fast interpretation, extraction, and automation.
- If there is any mismatch between the heuristic reading here and the SharePoint material, the SharePoint material wins.

## Core Mental Model

- Org codes are best treated as coordinates for formal units in the BASF hierarchy.
- They do not identify a person by themselves.
- They work well because they compress a large part of the reporting structure into a short, reusable string.
- They are approximate, locally extended, and sometimes inconsistent.

## Practical Heuristics

### Title-aware level matrix

The March 2026 BASF group organization PDF makes the code more interpretable when combined with titles.

| Formal level | Typical title                                 | Typical org-code form               | Notes                                                                    |
| ------------ | --------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------ |
| `1`          | Board or ressort                              | `RES`                                 | Board notation is not fully systematic                                   |
| `2`          | President or division head                    | `CD`, `EM`, `PM`, `EU`, `ES`, `GD`  | Usually a two-letter executive root                                      |
| `3`          | Senior Vice President or unit head            | `COR`, `CDT`, `EMM`, `ROI`, `N-EMN` | Prefix does not count toward the three-letter core                       |
| `4`          | Vice President or direct executive report     | `COH/D`, `EMM/B`, `GD/S`            | Slash can already appear at executive levels                             |
| `5+`         | Head of, manager, group, or team continuation | `COH/DL`, `ESL/WL`, `GBE/SHV-PDD`   | Below the senior executive layers, divisions continue the coding locally |

Two consequences follow from this:

- The code alone cannot identify the holder's exact rank.
- Assistants and non-managerial roles can still carry executive-looking org codes because the code identifies the unit, not the person's role.

### Executive patterns

| Pattern                             | Typical meaning                           | Notes                                              |
| ----------------------------------- | ----------------------------------------- | -------------------------------------------------- |
| `RES`                               | Board or ressort example                  | Board notation is not fully systematic             |
| `CD`, `EM`, `PM`, `EU`, `ES`, `GD`  | Division headed by a President            | Two-letter executive root                          |
| `COR`, `CDT`, `EMM`, `RGR`, `N-EMN` | Unit headed by a Senior Vice President    | Prefix does not count toward the three-letter core |
| `COH/D`, `EMM/B`, `GD/S`            | Vice President or direct executive report | Slash can appear already at executive levels       |

### Regional and scope prefixes from the org chart

The March 2026 PDF confirms these patterns in active use:

| Prefix | Typical meaning | Examples                   |
| ------ | --------------- | -------------------------- |
| `A-`   | Asia Pacific    | `A-CPA`, `A-CIA`, `A-PMA`  |
| `E-`   | Europe          | `E-CPB`, `E-CPI`, `E-CMP`  |
| `N-`   | North America   | `N-CPN`, `N-CMN`, `N-PMN`  |
| `S-`   | South America   | `S-CPS`, `S-PM/S`          |
| `G-`   | Global          | `G-EVC`, `G-ECO`, `G-BM/B` |

### Lower-level continuation

- Below the senior executive layers, divisions can continue the coding locally.
- Codes such as `COH/DL` or `ESL/WL` usually refer to groups or teams led by a `Head of` role.
- Larger areas can extend deeper, for example `GBE/SHV-PDD`.

### Missing layers

- Missing positions in the organigram can be encoded as `0` and are often written as `O` and can also be omitted entirely.
- This is why some chains look irregular but still follow the same logic.

## Examples Explained

### `GDB/E`

- `GD` suggests the division or President layer.
- `B` suggests the Senior Vice President layer.
- `/E` suggests a Vice President reporting into `B`.
- The nearest higher named unit in the 2026 org chart is `GDB` = `Digitalization of Research & Development`.
- Plain-language reading: `E` reports to `B`, which reports to `GD`.

### `GBM`

- `GBM` is listed in the 2026 org chart under service units.
- Clear name: `Global Consulting Services`.
- This is a good example of a three-letter code that should resolve directly to a known name.

### `A-CPA`

- `A-` marks Asia Pacific scope.
- `CPA` is the regional operating branch of `CP`.
- The higher root `CP` is `Petrochemicals`, while `A-CPA` is `Petrochemicals Asia Pacific`.

### `CC-E`

- `CC-E` is explicitly listed in the 2026 org chart.
- Clear name: `Environmental Catalyst & Metal Solutions (ECMS)`.
- This is a real exception family and should not be forced into the normal two-letter division logic.

### `S-APS`

- `S-` is a regional scope marker.
- `APS` remains the core org stem.
- The 2026 name is `Agricultural Solutions Latin America`.

### `RES`

- `RES` is treated as a board-related exception code in current BASF practice.
- It should be handled as a board or ressort family code, not forced into the standard division heuristics.

## High-Level 2026 Code Names

These are the main high-level codes the bundled CLI should resolve directly.

| Code | 2026 name |
| ---- | --------- |
| `AP` | Agricultural Solutions |
| `BM` | Battery Materials |
| `CC-E` | Environmental Catalyst & Metal Solutions (ECMS) |
| `CI` | Intermediates |
| `CM` | Monomers |
| `CP` | Petrochemicals |
| `EC` | Coatings |
| `ED` | Dispersions & Resins |
| `EM` | Care Chemicals |
| `EN` | Nutrition & Health |
| `ES` | European Site & Verbund Management |
| `EV` | Performance Chemicals |
| `GB` | Global Business Services |
| `GD` | Global Digital Services |
| `GE` | Global Engineering Services |
| `GP` | Global Procurement |
| `NA` | BASF Corporation |
| `RG` | Group Research |

## Three-Letter 2026 Code Names

These named units are supported directly by the bundled CLI.

| Code | 2026 name |
| ---- | --------- |
| `APD` | Regulatory, Sustainability & Public Affairs |
| `APM` | Global Strategic Marketing & Sustainability |
| `APP` | R&D Seeds & Traits |
| `APR` | R&D Crop Protection |
| `CDE` | Economic Evaluations |
| `CDS` | Corporate Strategy |
| `CDT` | Corporate Technology |
| `CFM` | Corporate Mergers & Acquisitions |
| `CFP` | Group Reporting & Performance Management |
| `CFT` | Corporate Treasury |
| `CMS` | Strategy |
| `CMT` | Technology |
| `EDG` | Global Technology, Investments and Supply Chain |
| `GBE` | Regional Business Services EMEA |
| `GBI` | Global Intellectual Property & Regulatory Services |
| `GBM` | Global Consulting Services |
| `GBT` | Portfolio & Technology Steering |
| `GDA` | Digitalization of Workspace & Infrastructure |
| `GDB` | Digitalization of Research & Development |
| `GDD` | Digitalization of Production & Technology |
| `GDE` | Digitalization of Services & ERP Platforms |
| `GDF` | Digitalization of Businesses |
| `GDS` | Cyber Security |
| `RGC` | Catalysts Research and Testing |
| `RGQ` | Digitalization, Automation and Innovation Management |
| `RGR` | Process Research and Chemical Engineering |
| `RGS` | Chemical, Material and Regulatory Science |

## Known Exceptions and Caveats

- Asia-specific org codes do not reliably follow the simplified explanation.
- `CC-` patterns are known exceptions with no stable general rule captured yet.
- The March 2026 org chart confirms `CC-E` as a real top-level exception pattern for Environmental Catalyst & Metal Solutions.
- Corporate Center structures such as `COH`, `COR`, and `COM` can skip the division-head concept and report directly to the Board.
- Assistants and non-managerial roles can still carry executive-looking org codes because the code identifies the unit, not the role holder.

## Useful Regexes

### Split prefix, main stem, and tail

Use this when the first task is structural parsing rather than division extraction:

```regex
^(?:(?<prefix>[AENSG])\-)?(?<main>[^/]+?)(?:\/(?<tail>.+))?$
```

Interpretation:

- `prefix`: optional regional or scope marker such as `G`, `S`, `N`, `E`, or `A`
- `main`: the core org stem that usually carries the executive pattern
- `tail`: everything after the slash, usually a lower local continuation

## Division Extraction Regex

The following regex was shared internally for extracting the division-like root from BASF org code strings:

```regex
^(?:[A-Z]-)?(?:([A-S-UZ][A-GI-NP-Z]|[A-Z]O[A-Z])(?:[A-Z ]*(?:\/.*)?$)|([A-Za-z0-9 _\&]{2,})(?:\/.*)?$)
```

Use it as a heuristic, not an authority. It is helpful for parsing mixed datasets where prefixes and slash tails appear inconsistently.

Practical note:

- Use the regex for candidate extraction, not final semantic interpretation.
- Pair it with special-case handling for preserved codes such as `BNB`, `BVC`, `CHEM`, and known exception families such as `CC-`.

## Excel Formula for Division Extraction

The following Excel formula extracts a division code from typical BASF org-code strings such as `G-ABC/DEF`, while preserving exceptions like `BNB`, `BVC`, and `CHEM`.

```excel
=IF(
    [@[Org Code]]="";
    "";
    IF(
        NOT(ISERR(FIND("-";[@[Org Code]])));
        IF(
            NOT(ISERR(FIND("/";[@[Org Code]])));
            IF(
                FIND("/";[@[Org Code]])>FIND("-";[@[Org Code]]);
                MID([@[Org Code]]; FIND("-";[@[Org Code]])+1; 2);
                LEFT([@[Org Code]]; 2)
            );
            MID([@[Org Code]]; FIND("-";[@[Org Code]])+1; 2)
        );
        IF(
            NOT(ISERR(FIND("/";[@[Org Code]])));
            LEFT([@[Org Code]]; 2);
            IF(
                LEN([@[Org Code]])>3;
                [@[Org Code]];
                IF(
                    [@[Org Code]]="BNB";
                    "BNB";
                    IF(
                        [@[Org Code]]="BVC";
                        "BVC";
                        IF(
                            [@[Org Code]]="CHEM";
                            "CHEM";
                            LEFT([@[Org Code]]; 2)
                        )
                    )
                )
            )
        )
    )
)
```

### What the formula does

1. Returns blank for blank input.
2. If a prefix like `G-` exists, it extracts the two characters after the hyphen unless the slash appears earlier.
3. If no prefix exists but a slash does, it takes the leftmost two characters.
4. If neither prefix nor slash exists, it preserves codes longer than three characters as-is.
5. It explicitly preserves `BNB`, `BVC`, and `CHEM`.
6. Otherwise it falls back to the first two characters.

## Bundled Script

The skill includes [org_code_tools.py](../scripts/org_code_tools.py), a small Python CLI that packages the same heuristics for repeatable use.

Examples:

```bash
python scripts/org_code_tools.py explain GDB/E ROI S-APS
python scripts/org_code_tools.py extract-division G-ABC/DEF BNB CHEM
python scripts/org_code_tools.py parse COH/DL GBE/SHV-PDD CC-E
```

## Recommended Response Style

When a user asks what a code means, answer with:

1. The most likely reading.
2. The exact assumptions you used.
3. The confidence level.
4. The key caveat that the title or local org chart may change the interpretation.

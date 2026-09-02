---
name: basf-org-codes
description: Interpret BASF org codes and explain what they reveal about the formal organization. Use when users ask to decode codes such as ROI, GDB/E, G-EVT, or COH/DL; infer division or reporting line; normalize regional prefixes; estimate the formal hierarchy level; or build formulas and regexes to extract division or hierarchy signals from BASF org code data.
author: Daniel Kaesmayr
metadata:
  category: corporate-structure
  version: "1.1.2"
---

# BASF Org Codes

Use this skill to decode BASF org codes as an organizational coordinate system.
The goal is not to claim perfect truth from the code alone. The goal is to turn a code into a practical, explicit approximation of where a unit sits in the formal hierarchy, what division or corporate area it belongs to, and how confident that reading is.

## What the Code Tells You

- Org codes describe formal organizational units, not people.
- They are useful because they give a compact and fairly universal way to place a person, job, or topic in BASF's structure.
- They often expose reporting-line logic better than a free-text org name.
- They are good approximations, not a perfect source of truth.
- Titles still matter. Use the org code together with the job title when the user needs level accuracy.

## Source Of Truth

- The ultimate source of truth is the BASF Group Organization material in SharePoint:
  `https://basf.sharepoint.com/sites/coh-files/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2Fcoh%2Dfiles%2FShared%20Documents%2FBASF%20Group%20Organization&viewid=f343d362%2D70f5%2D4d1b%2Da223%2D690e55f27ae1&csf=1&cid=7e7b16e9%2D5e19%2D4315%2D9314%2D6c395d983bc5&FolderCTID=0x0120004973657A417AAB4AA9B15E58D3C4C708`
- Use this skill to interpret and operationalize org codes quickly, but defer to the SharePoint source when an org name, reporting line, or current structure is disputed.
- If the SharePoint material and the heuristic reading disagree, treat the SharePoint source as authoritative.

## When to Use This Skill

- The user asks what a BASF org code means.
- The user wants to infer the division, unit, or likely reporting chain.
- The user needs a plain-language explanation of a code such as `ROI`, `RAP/OC`, `GDB/E`, `S-APS`, or `COH/DL`.
- The user wants to classify a spreadsheet of org codes.
- The user wants an Excel formula or regex to extract the division from org codes.
- The user wants a script or CLI helper to normalize, parse, or batch-process BASF org codes.
- The user needs caveats and exceptions spelled out instead of overconfident decoding.

## Default Workflow

1. Normalize the code by trimming spaces and preserving any regional prefix such as `G-`, `S-`, or `N-`.
2. Split the code into three possible parts:
   - optional prefix before `-`
   - main hierarchy stem before `/`
   - local team or subgroup tail after `/`
3. Interpret the main stem first. This usually carries the division, unit, and executive reporting-line signal.
4. Interpret the `/...` tail as a lower-level local continuation unless the code clearly reflects a direct executive report pattern.
5. Cross-check the inferred level against the person's title if a title is available.
6. State confidence and caveats explicitly, especially for regional prefixes, Asia-specific patterns, `CC-` forms, and locally extended team codes.

## Reusable Tools

Use the bundled parser when the user needs repeatable logic instead of one-off chat reasoning.

- `scripts/org_code_tools.py parse CODE ...` returns structured JSON with prefix, main stem, tail, probable level, division root, and caveats.
- `scripts/org_code_tools.py extract-division CODE ...` applies the division-extraction heuristics used in the regex and spreadsheet logic.
- `scripts/org_code_tools.py explain CODE ...` prints a short human-readable explanation for quick checks.
- `scripts/org_code_tools.py lookup-name CODE ...` returns the best known exact code name or the nearest higher mapped org name.

Prefer the script for datasets, CSV cleanup, repeated extraction, or downstream automation.

## Interpretation Rules

### 1. Prefixes

- Prefixes such as `G-` or `S-` usually indicate scope or region, not a different core hierarchy.
- The March 2026 BASF group organization PDF confirms common regional and scope prefixes such as `A-`, `E-`, `N-`, `S-`, and `G-` for Asia Pacific, Europe, North America, South America, and global units.
- Example: `S-APS` usually reads as South America scope for an AP business or unit.
- Example: `G-EVT` usually marks a global unit.
- Example patterns from the org chart include `A-CPA`, `E-CPI`, `N-CPN`, `S-CPS`, and `G-EVC`.

### 2. Main Stem Before the Slash

- Two-letter stems often indicate a division headed by a President, for example `GD`, `EM`, `PM`, `EU`, `ES`, `CD`.
- Three-letter stems often indicate a unit headed by a Senior Vice President, for example `ROI`, `COR`, `CDT`, `EMM`.
- Four-character executive forms often indicate a Vice President level or a direct report to a division head, for example `GD/S`, `EMM/B`, `COH/D`.
- Corporate Center has important exceptions: units such as `COH`, `COR`, `COM`, and `COI` can report directly to a Board member without an intermediate division head.
- The March 2026 group org chart also shows `CC-E` as a top-level exception pattern for Environmental Catalyst & Metal Solutions.

### 3. Letter Order as Reporting Chain

- The order of letters usually reflects the reporting line.
- The rightmost newly added letter often marks the current node at the next lower level.
- Earlier letters represent the chain upward.
- Missing hierarchy slots can be represented with `0`, often written as `O`.

### 4. Approximate Level Heuristic

Use this only as a heuristic and say so.

| Heuristic Level | Typical Reading                                  |
| --------------- | ------------------------------------------------ |
| `1`             | Board or ressort level                           |
| `2`             | President or division head                       |
| `3`             | Senior Vice President or unit head               |
| `4`             | Vice President or department head                |
| `5`             | Group or team lead                               |
| `6+`            | Lower local continuation defined by the division |

Important caveat:

- The first letter is not a clean level marker across BASF.
- It often behaves more like a category or top-area marker, for example Research, Chemicals, Global Services, or Corporate.
- After the senior executive levels, divisions can extend the scheme locally.
- The org code identifies the unit, not the role holder, so assistants and other employees can carry the same code as the managerial unit they support.

## Worked Examples

- `ROI`: likely a Senior Vice President unit reporting to Board area `R` through division or line `RO`.
- `GDB/E`: likely a Vice President `E` reporting into Senior Vice President `B`, which sits under President `GD`.
- `RAP/OC`: likely a group or lower unit `OC` under `RAP`; the missing Vice President layer may be skipped in the code.
- `S-APS`: same core stem as `APS`, but with regional scope prefix `S-`.
- `COH/DL`: Corporate Center unit `COH`, then lower continuation `DL` for a group or team under the VP or department layer.
- `GBE/SHV-PDD`: a locally extended code under division `GB`, with additional subordinate coding after the slash and hyphen.
- `CC-E`: a known special case used for Environmental Catalyst & Metal Solutions rather than a normal two-letter division root.

## Output Pattern

When explaining an org code, present the result in this order:

1. Normalized code
2. Probable scope prefix meaning, if present
3. Probable division or corporate root
4. Probable formal level of the main stem
5. Reporting-line explanation in plain language
6. Confidence level: high, medium, or low
7. Caveats or exceptions

Example structure:

```text
Code: GDB/E
Root area: GD
Likely level: Vice President pattern
Interpretation: E likely reports to B, which reports to GD.
Confidence: Medium
Caveat: exact level should be checked against the person's title.
```

## Why These Codes Are Worth Exposing

- They are a compact shared language across BASF.
- They make it easier to route topics, filter spreadsheets, and understand where an issue sits in the company.
- They are often good enough for research, staffing discussions, stakeholder mapping, and internal analytics.
- Hiding them removes a useful organizational index without actually simplifying the underlying structure.

## Boundaries

- Do not claim the code alone proves a person's rank.
- Do not infer personal attributes from the code.
- Do not hide uncertainty. Say when the reading depends on title, region, or local divisional conventions.
- Treat Asia-specific org codes and `CC-` variants as exceptions unless the user provides additional local context.
- Do not bundle confidential source PDFs into the skill. Distill their reusable logic into references and scripts instead.

## References

- Detailed decoding guidance and examples: [org-code-reference.md](./references/org-code-reference.md)
- Reusable parsing CLI: `scripts/org_code_tools.py`

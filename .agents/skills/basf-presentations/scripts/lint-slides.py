#!/usr/bin/env python3
"""lint-slides.py — BASF Quarto presentation content-budget linter.

Parses a .qmd file and estimates the rendered pixel height of each slide's
content using a heuristic model calibrated to the BASF Reveal.js theme at
1920×1080, margin 0.08, padding 80px, root font-size 36px.

Reports each slide as:
  ✅ OK      — fits comfortably (≤ 85 % of budget)
  ⚠️  WARN    — near the limit (86–100 % of budget)
  🔴 OVER    — exceeds the budget (runtime scaler will compensate)

Exit code 1 when at least one slide is OVER budget.
Use --warn-only to always exit 0 (safe for Quarto pre-render hooks).

Usage:
    python3 lint-slides.py presentation.qmd
    python3 lint-slides.py presentation.qmd --canvas 820 --verbose
    python3 lint-slides.py presentation.qmd --warn-only   # for _quarto.yml hook

Tuning:
    Edit the HEIGHTS dict to recalibrate for a different theme or font size.
    The defaults are validated against the BASF Dark Blue 1920×1080 theme.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ── Pixel-height model ─────────────────────────────────────────────────────
#
# Calibrated for:  BASF Dark Blue theme, 1920×1080, margin 0.08, padding 80px
#                  root font-size 36px, line-height 1.7
#
# Derivation:
#   body line = 36px × 1.7 line-height = 61.2px  →  rounded to 52px
#               (10–15 % discount for partial lines / tight wrap)
#   H3        = 36px × 1.3em × 1.4 leading + 8px margin ≈ 73px  →  60px
#   code line = 36px × 0.6em × 1.2 leading           ≈ 26px  →  22px
#
# Adjust these values when the root font size or theme changes.

HEIGHTS: dict[str, int] = {
    "h3":               60,   # ### heading or <h3> tag
    "h3_subtitle":      70,   # first <h3> directly below H2 (heavier visual weight)
    "body_line":        52,   # one wrapped line of paragraph text
    "bullet_item":      52,   # one list item (− or * or 1.)
    "code_overhead":    32,   # fence open/close + block padding
    "code_line":        22,   # one line inside a fenced code block
    "table_header":     50,   # <thead> row
    "table_row":        44,   # <tbody> row
    "blockquote_line":  55,   # one line inside a > blockquote
    "footnote":         42,   # ::: {.footnote} block (one line)
    "raw_html_block":  200,   # {=html} fenced block — opaque, fixed estimate
    "mermaid_diagram": 380,  # {mermaid} block — renders as compact SVG
    "column_gap":       20,  # flex gap between column groups
}

# Characters per line at 36px on BASF 1920-wide canvas
# Effective content width ≈ 1440px; average char ≈ 19px → 75 chars/line
CHARS_PER_LINE_BODY = 75

# Slide classes to skip — intentionally sparse, no budget check needed
SKIP_CLASSES: frozenset[str] = frozenset({"closing-slide", "divider-slide"})


# ── Regex patterns ─────────────────────────────────────────────────────────

_RE_YAML_FRONT = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_RE_SLIDE_HDR  = re.compile(r"^(## .+)$", re.MULTILINE)
_RE_H3_MD      = re.compile(r"^#{3} .+", re.MULTILINE)
_RE_H3_HTML    = re.compile(r"<h3[^>]*>.*?</h3>", re.IGNORECASE | re.DOTALL)
_RE_BULLET     = re.compile(r"^[ \t]*[-*+] .+", re.MULTILINE)
_RE_ORDERED    = re.compile(r"^[ \t]*\d+[.)]\s+.+", re.MULTILINE)
_RE_TABLE_ROW  = re.compile(r"^\|.+\|$", re.MULTILINE)
_RE_TABLE_SEP  = re.compile(r"^\|[\s\-:|]+\|$", re.MULTILINE)
_RE_BLOCKQUOTE = re.compile(r"^> .+", re.MULTILINE)
_RE_FOOTNOTE   = re.compile(r":::\s*\{\.footnote\}.*?:::", re.DOTALL)
_RE_RAW_HTML   = re.compile(r"```\{=html\}.*?```", re.DOTALL)
_RE_CODE_FENCE = re.compile(r"```(?!\{=html\}).*?```", re.DOTALL)
# Column detection: Pandoc multi-colon syntax
# Matches: :::{.column}, ::::{.split-left}, ::::{.split-right}
_RE_COL_OPEN_MD  = re.compile(
    r"^:{2,}\s*\{\.(?:column|split-left|split-right)[^}]*\}",
    re.MULTILINE | re.IGNORECASE,
)
# Column detection: HTML passthrough (<div class="column...">) inside Markdown
_RE_COL_OPEN_HTML = re.compile(r'<div\s+class="column[^"]*"[^>]*>', re.IGNORECASE)
# Storytelling layout: argument-slide cards laid out side-by-side
_RE_ARGUMENT_CARD = re.compile(r'<div\s+class="argument-card[^"]*"[^>]*>', re.IGNORECASE)

# Mermaid diagrams — rendered as SVG, NOT as per-line code text
_RE_MERMAID = re.compile(r"```\{mermaid\}.*?```", re.DOTALL)


# ── Data classes ───────────────────────────────────────────────────────────

@dataclass
class SlideResult:
    index: int
    title: str
    classes: list[str]
    estimated_px: int
    budget_px: int
    pct: int
    status: str           # "OK" | "WARN" | "OVER"
    details: list[str] = field(default_factory=list)


# ── Helpers ────────────────────────────────────────────────────────────────

def extract_slide_classes(header: str) -> list[str]:
    """Return CSS class names from `## Heading {.content-slide .smaller}`."""
    m = re.search(r"\{([^}]+)\}", header)
    if not m:
        return []
    return re.findall(r"\.([a-zA-Z][a-zA-Z0-9-]*)", m.group(1))


def chars_to_lines(text: str, cpl: int = CHARS_PER_LINE_BODY) -> int:
    """Estimate rendered line count from raw character count."""
    n = len(text.strip())
    return max(1, (n + cpl - 1) // cpl) if n else 0


def _strip_counted_elements(text: str) -> str:
    """Remove text elements that are counted elsewhere to avoid double-counting."""
    t = re.sub(r"^#{1,6} .+", "", text, flags=re.MULTILINE)
    t = re.sub(r"^[ \t]*[-*+\d][.)]\s+.+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^> .+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^\|.+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^:::.+", "", t, flags=re.MULTILINE)
    t = re.sub(r"<[^>]+>", "", t)          # strip HTML tags
    return t


def estimate_region(text: str) -> tuple[int, list[str]]:
    """
    Estimate the pixel height of a text region (one column or full body).
    Returns (pixels, detail_lines).
    """
    details: list[str] = []
    total = 0

    # Code fences (non-HTML) ─────────────────────────────────────────────
    code_blocks = _RE_CODE_FENCE.findall(text)
    text = _RE_CODE_FENCE.sub("", text)
    for cb in code_blocks:
        lines = [l for l in cb.splitlines() if not l.startswith("```")]
        n = max(len(lines), 1)
        h = HEIGHTS["code_overhead"] + n * HEIGHTS["code_line"]
        total += h
        details.append(f"code block {n}L → {h}px")

    # H3 headings ────────────────────────────────────────────────────────
    h3_count = len(_RE_H3_MD.findall(text)) + len(_RE_H3_HTML.findall(text))
    if h3_count:
        h = h3_count * HEIGHTS["h3"]
        total += h
        details.append(f"{h3_count}× H3 → {h}px")

    # List items ─────────────────────────────────────────────────────────
    items = _RE_BULLET.findall(text) + _RE_ORDERED.findall(text)
    if items:
        h = len(items) * HEIGHTS["bullet_item"]
        total += h
        details.append(f"{len(items)}× list item → {h}px")

    # Blockquotes ────────────────────────────────────────────────────────
    bq = _RE_BLOCKQUOTE.findall(text)
    if bq:
        h = len(bq) * HEIGHTS["blockquote_line"]
        total += h
        details.append(f"{len(bq)}× blockquote → {h}px")

    # Tables ─────────────────────────────────────────────────────────────
    all_rows = _RE_TABLE_ROW.findall(text)
    sep_rows = _RE_TABLE_SEP.findall(text)
    if all_rows:
        data_rows = max(len(all_rows) - len(sep_rows) - 1, 0)
        h = HEIGHTS["table_header"] + data_rows * HEIGHTS["table_row"]
        total += h
        details.append(f"table {data_rows}r → {h}px")

    # Paragraph body text ────────────────────────────────────────────────
    body = _strip_counted_elements(text)
    para_text = " ".join(l.strip() for l in body.splitlines() if l.strip())
    if para_text:
        n = chars_to_lines(para_text)
        h = n * HEIGHTS["body_line"]
        total += h
        details.append(f"~{n} body lines → {h}px")

    return total, details


def _measure_columns(body: str, opener: re.Pattern) -> tuple[int, list[str]]:
    """
    Split body by column-opener markers, measure each column.
    Returns (pre_col_height + tallest_col + gap, detail_lines).
    """
    details: list[str] = []
    first = opener.search(body)
    if not first:
        return 0, []

    # Content before the first column (subtitle text etc.)
    pre = body[: first.start()]
    pre_h, pre_d = estimate_region(pre) if pre.strip() else (0, [])
    details.extend(pre_d)

    col_parts = opener.split(body)
    col_heights: list[int] = []
    for part in col_parts[1:]:
        cleaned = re.sub(r"^:{2,}\s*$", "", part, flags=re.MULTILINE)
        cleaned = re.sub(r"</div>", "", cleaned, flags=re.IGNORECASE)
        h, col_d = estimate_region(cleaned)
        col_heights.append(h)
        for d in col_d:
            details.append(f"  col: {d}")

    tallest = max(col_heights) if col_heights else 0
    details.append(f"multi-col: tallest {tallest}px / {len(col_heights)} cols")
    return pre_h + tallest + HEIGHTS["column_gap"], details


def estimate_slide(body: str, budget: int) -> tuple[int, list[str]]:
    """
    Estimate pixel height of a full slide body.

    Supports:
    - Raw {=html} fenced blocks (opaque fixed estimate)
    - .footnote blocks
        - Multi-column: Pandoc ::{.column} syntax, HTML <div class="column">,
            and argument-slide <div class="argument-card">
    - Single-column plain content
    """
    details: list[str] = []
    total = 0

    # ── Raw {=html} blocks — opaque, fixed estimate ───────────────────────
    for _ in _RE_RAW_HTML.findall(body):
        total += HEIGHTS["raw_html_block"]
        details.append(f"{{=html}} block → {HEIGHTS['raw_html_block']}px")
    body = _RE_RAW_HTML.sub("", body)

    # ── Mermaid diagrams — renders as compact SVG, not per-line text ──────
    for _ in _RE_MERMAID.findall(body):
        total += HEIGHTS["mermaid_diagram"]
        details.append(f"{{mermaid}} diagram → {HEIGHTS['mermaid_diagram']}px")
    body = _RE_MERMAID.sub("", body)

    # ── Footnote ──────────────────────────────────────────────────────────
    if _RE_FOOTNOTE.search(body):
        total += HEIGHTS["footnote"]
        details.append(f".footnote → {HEIGHTS['footnote']}px")
        body = _RE_FOOTNOTE.sub("", body)

    # ── Column detection: Pandoc syntax first, HTML fallback ─────────────
    if _RE_COL_OPEN_MD.search(body):
        h, d = _measure_columns(body, _RE_COL_OPEN_MD)
        total += h
        details.extend(d)
        return total, details

    if _RE_COL_OPEN_HTML.search(body):
        h, d = _measure_columns(body, _RE_COL_OPEN_HTML)
        total += h
        details.extend(d)
        return total, details

    if _RE_ARGUMENT_CARD.search(body):
        h, d = _measure_columns(body, _RE_ARGUMENT_CARD)
        total += h
        details.extend(d)
        return total, details

    # ── Single-column ─────────────────────────────────────────────────────
    h, d = estimate_region(body)
    total += h
    details.extend(d)
    return total, details


def split_into_slides(content: str) -> list[tuple[str, str]]:
    """
    Split QMD content into (header, body) pairs.

    Uses a line-by-line code-fence tracker so that ``## `` headings inside
    code blocks do NOT create spurious slide boundaries.
    """
    content = _RE_YAML_FRONT.sub("", content, count=1)
    lines = content.splitlines(keepends=True)

    in_fence = False
    boundaries: list[int] = []
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and re.match(r"^## ", line):
            boundaries.append(i)

    slides: list[tuple[str, str]] = []
    for idx, start in enumerate(boundaries):
        end = boundaries[idx + 1] if idx + 1 < len(boundaries) else len(lines)
        header = lines[start].rstrip("\n")
        body = "".join(lines[start + 1 : end])
        slides.append((header, body))
    return slides


# ── Main linter ────────────────────────────────────────────────────────────

def lint(qmd_path: Path, budget: int, warn_only: bool, verbose: bool) -> int:
    content = qmd_path.read_text(encoding="utf-8")
    slides = split_into_slides(content)

    print(f"BASF Slide Budget Linter  ·  {qmd_path.name}  ·  budget {budget}px\n")

    results: list[SlideResult] = []
    over_count = 0

    for idx, (header, body) in enumerate(slides):
        classes = extract_slide_classes(header)
        title = re.sub(r"\{[^}]*\}", "", header).replace("##", "").strip()

        # Sparse slides — skip budget check
        if any(cls in SKIP_CLASSES for cls in classes):
            continue

        # H3 subtitle immediately after H2 carries extra visual weight
        first_content = body.strip()
        has_h3_subtitle = bool(
            re.match(r"<h3", first_content, re.IGNORECASE)
            or re.match(r"### ", first_content)
        )
        subtitle_px = HEIGHTS["h3_subtitle"] if has_h3_subtitle else 0

        est_px, details = estimate_slide(body, budget)
        total_px = est_px + subtitle_px
        pct = round(total_px / budget * 100)

        if total_px > budget:
            status = "OVER"
            over_count += 1
        elif total_px > budget * 0.85:
            status = "WARN"
        else:
            status = "OK"

        results.append(SlideResult(
            index=idx,
            title=title[:50],
            classes=classes,
            estimated_px=total_px,
            budget_px=budget,
            pct=pct,
            status=status,
            details=details,
        ))

    # ── Report ─────────────────────────────────────────────────────────────
    ICONS = {"OK": "✅", "WARN": "⚠️ ", "OVER": "🔴"}
    BAR_W = 28

    for r in results:
        filled = min(int(r.pct / 100 * BAR_W), BAR_W)
        bar = "█" * filled + "░" * (BAR_W - filled)
        print(
            f"{ICONS[r.status]} [{r.index:2d}] {r.title:<48}  "
            f"{r.estimated_px:4d}/{r.budget_px}px  {r.pct:3d}%  |{bar}|"
        )
        if verbose or r.status in ("WARN", "OVER"):
            for d in r.details:
                print(f"            {d}")
            if r.details:
                print()

    n_ok   = sum(1 for r in results if r.status == "OK")
    n_warn = sum(1 for r in results if r.status == "WARN")
    n_over = sum(1 for r in results if r.status == "OVER")
    print(f"\nSummary: {n_ok} ✅ OK  ·  {n_warn} ⚠️  WARN  ·  {n_over} 🔴 OVER")

    if n_over and not warn_only:
        print(f"\nExit 1 — {n_over} slide(s) over budget.")
        print("  Trim content, or the runtime auto-scaler will compensate.")
        print("  Use --warn-only to suppress this exit code.")
        return 1

    if n_over:
        print(f"\n⚠️  {n_over} slide(s) over budget  (warn-only mode — exit 0).")

    return 0


def main() -> None:
    ap = argparse.ArgumentParser(
        description="BASF Quarto slide content-budget linter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("qmd", type=Path, help="Path to the .qmd presentation file")
    ap.add_argument(
        "--canvas", type=int, default=820,
        help="Effective body-area height in px (default: 820 for BASF 1080p theme)",
    )
    ap.add_argument(
        "--warn-only", action="store_true",
        help="Never exit non-zero — safe for Quarto pre-render hooks",
    )
    ap.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show breakdown for every slide, not just WARN / OVER",
    )
    args = ap.parse_args()

    if not args.qmd.exists():
        print(f"Error: {args.qmd} not found", file=sys.stderr)
        sys.exit(2)

    sys.exit(lint(args.qmd, args.canvas, args.warn_only, args.verbose))


if __name__ == "__main__":
    main()

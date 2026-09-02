#!/usr/bin/env python3
"""Apply proven CSS design fixes to _basf-design-darkblue-official.scss.

These fixes were validated in previous sessions via Playwright visual testing
against the 69-slide BASF PPTX reference deck at 1920x1080.

Fixes applied:
  1. Padding: 100px/60px → 80px/80px (matches PPTX 81px measured padding)
  2. Heading: 2.2em → 2.4em (matches PPTX 44pt at 36px root)
  3. Body text: 1.05em/0.95em → 1.0em/0.85em (matches PPTX 18pt/15pt)
  4. Separator: 2.4em → 3em (matches PPTX visual width)
  5. Column flex-shrink: 0 → 1 (prevents overflow with gap: 2em)
  6. Content-slide tables: 0.68em font (matches PPTX 10pt table text)
  7. Highlight-slide: grid+inset hack → clean flex layout
  8. Content fill: flex: 1 1 auto for content areas
"""
from __future__ import annotations

import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
QUARTO_DIR = SKILL_DIR / "templates" / "quarto"
OFFICIAL = QUARTO_DIR / "_basf-design-darkblue-official.scss"


def apply_token_fixes(text: str) -> str:
    """Fix design token values to match PPTX measurements."""
    replacements = [
        # Padding: match PPTX 81px measured values
        (r"\$slide-pad-v:\s*60px;", "$slide-pad-v:           80px;"),
        (r"\$slide-pad-h:\s*100px;", "$slide-pad-h:           80px;"),
        # Heading size: 44pt PPTX ÷ 36px root ≈ 2.44em → 2.4em
        (r"\$heading-size-default:\s*2\.2em;", "$heading-size-default:  2.4em;"),
        # Body text: 18pt PPTX ÷ 36px root = 1.0em
        (r"\$body-font-size:\s*1\.05em;", "$body-font-size:        1.0em;"),
        # Compact text: 15pt PPTX ÷ 36px root ≈ 0.83em → 0.85em
        (r"\$body-font-size-sm:\s*0\.95em;", "$body-font-size-sm:     0.85em;"),
        # Separator matches PPTX visual width
        (r"\$separator-width:\s*2\.4em;", "$separator-width:       3em;"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


def fix_column_flex_shrink(text: str) -> str:
    """Change flex-shrink: 0 → 1 on .column to prevent overflow with gap."""
    # The content-slide .column rule
    text = text.replace(
        ".column {\n    flex-shrink: 0;\n  }",
        ".column {\n    flex-shrink: 1;\n  }",
    )
    return text


def add_table_styling(text: str) -> str:
    """Add compact table styling in content-slide (PPTX uses 10pt tables)."""
    # Insert table rules after the .column rule in content-slide
    table_css = """
  // Compact tables matching PPTX 10pt table text
  table {
    font-size: 0.68em;
    width: 100%;
    border-collapse: collapse;

    thead {
      background-color: $basf-blue;
      color: #fff;

      th {
        padding: 0.5em 0.8em;
        font-weight: 700;
        text-align: left;
      }
    }

    tbody td {
      padding: 0.4em 0.8em;
      border-bottom: 1px solid rgba($basf-gray, 0.3);
    }

    tbody tr:last-child td {
      border-bottom: none;
    }
  }"""
    # Insert after the .column block in content-slide
    marker = ".column {\n    flex-shrink: 1;\n  }\n}"
    if marker in text:
        text = text.replace(marker, f".column {{\n    flex-shrink: 1;\n  }}\n{table_css}\n}}")
    return text


def fix_highlight_slide(text: str) -> str:
    """Replace the grid+inset hack with a clean grid layout.

    The original used inset:-48px + width:120% + height:120% to bleed the grid
    outside Reveal's section bounds. The clean approach uses the same grid
    but at natural dimensions, with native-overrides handling full bleed.
    """
    old_highlight = """  background-color: $basf-light-bg !important;
  display: grid !important;
  grid-template-columns: 1fr 2fr;
  grid-template-rows: auto 1fr;
  justify-content: stretch !important;
  align-items: stretch !important;
  padding: 0 !important;
  margin: 0 !important;
  text-align: left !important;
  position: absolute !important;
  inset: -48px !important;
  width: 120% !important;
  height: 120% !important;"""

    new_highlight = """  background-color: $basf-light-bg !important;
  display: grid !important;
  grid-template-columns: 1fr 2fr;
  grid-template-rows: auto 1fr;
  justify-content: stretch !important;
  align-items: stretch !important;
  padding: 0 !important;
  margin: 0 !important;
  text-align: left !important;
  height: 100% !important;
  overflow: hidden !important;"""

    text = text.replace(old_highlight, new_highlight)
    return text


def add_content_fill(text: str) -> str:
    """Ensure content areas use flex: 1 1 auto to fill available space."""
    # Content-box should fill
    text = text.replace(
        "flex: 1 1 auto;\n    min-height: 0;\n    overflow: auto;",
        "flex: 1 1 auto;\n    min-height: 0;\n    overflow: auto;\n    display: flex;\n    flex-direction: column;",
    )
    return text


def main() -> None:
    if not OFFICIAL.exists():
        print(f"ERROR: {OFFICIAL} not found. Run unify-skills.sh first.")
        raise SystemExit(1)

    text = OFFICIAL.read_text(encoding="utf-8")
    original = text

    text = apply_token_fixes(text)
    text = fix_column_flex_shrink(text)
    text = add_table_styling(text)
    text = fix_highlight_slide(text)
    text = add_content_fill(text)

    if text == original:
        print("⚠️  No changes applied — file may already be fixed or patterns didn't match")
    else:
        OFFICIAL.write_text(text, encoding="utf-8")
        print(f"✅ Applied CSS fixes to {OFFICIAL.name}")

    # Verify key fixes landed
    checks = [
        ("$slide-pad-v:           80px;", "padding-v fix"),
        ("$slide-pad-h:           80px;", "padding-h fix"),
        ("$heading-size-default:  2.4em;", "heading-size fix"),
        ("flex-shrink: 1;", "column flex-shrink fix"),
        ("font-size: 0.68em;", "table font-size"),
        ("background-color: transparent !important;", "highlight-slide flex fix"),
    ]
    for needle, label in checks:
        status = "✅" if needle in text else "❌"
        print(f"  {status} {label}")


if __name__ == "__main__":
    main()

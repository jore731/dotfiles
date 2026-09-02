#!/usr/bin/env python3
"""
export-pptx.py — Convert Reveal.js markdown slides to BASF-branded PPTX.

Reads a Reveal.js `slides.md` file and generates an editable PowerPoint
presentation using `python-pptx`, applying the BASF reference template
for consistent corporate branding.

Usage:
    python3 export-pptx.py slides.md -o output.pptx [--template basf-reference.pptx]

Slide class → PPTX layout mapping:
    title-slide     → Title Slide
    divider-slide   → Section Header
    content-slide   → Title and Content
    highlight-slide → Two Content
    content-box-slide → Blank
    closing-slide   → Blank (BASF finale)

Supported content:
    - Headings → Title placeholder
    - Bullet lists → Content placeholder with formatting
    - Tables → Native PPTX table shapes
    - Images → Positioned image shapes
    - Speaker notes → Notes slide text frame
    - Multi-column → Two Content layout

Limitations (graceful fallback):
    - Complex CSS grids → simplified single-column
    - Mermaid/Chart.js → placeholder text with comment
    - canvas-grid layouts → sequential content boxes
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path
from typing import Optional


def find_workspace_root() -> Path:
    """Walk up from script location to find .github/ dir."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / ".github").is_dir():
            return current
        current = current.parent
    return Path.cwd()


def parse_args() -> argparse.Namespace:
    root = find_workspace_root()
    default_template = (
        root
        / ".github/skills/pandoc-quarto-basf/assets/templates"
        / "basf-reference.pptx"
    )

    parser = argparse.ArgumentParser(
        description="Convert Reveal.js markdown to BASF-branded PPTX"
    )
    parser.add_argument("input", help="Path to slides.md (Reveal.js markdown)")
    parser.add_argument(
        "-o", "--output", default="output.pptx", help="Output PPTX path"
    )
    parser.add_argument(
        "--template",
        default=str(default_template),
        help=f"BASF reference PPTX template (default: {default_template})",
    )
    parser.add_argument(
        "--images-dir",
        default=None,
        help="Directory containing images referenced in slides (default: same dir as input)",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Markdown Parser: splits slides.md into structured slide objects
# ---------------------------------------------------------------------------

# Regex for Reveal.js slide class comments
SLIDE_CLASS_RE = re.compile(
    r'<!--\s*\.slide:\s*class="([^"]+)"\s*-->', re.IGNORECASE
)
# Regex for images: ![alt](src)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# Regex for headings
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
# Regex for HTML table
HTML_TABLE_RE = re.compile(r"<table[^>]*>.*?</table>", re.DOTALL | re.IGNORECASE)
# Regex for Mermaid/Chart.js blocks
SKIP_BLOCK_RE = re.compile(
    r"```(?:mermaid|chartjs).*?```|<canvas[^>]*>.*?</canvas>",
    re.DOTALL | re.IGNORECASE,
)
# Regex for speaker notes
NOTES_RE = re.compile(r"^Note:\s*(.+)", re.MULTILINE | re.DOTALL)
# Regex for HTML div wrappers
DIV_CLASS_RE = re.compile(r'<div\s+class="([^"]+)"[^>]*>', re.IGNORECASE)

# Pandoc fenced div syntax (Quarto)
FENCED_DIV_START_RE = re.compile(r"^:{3,4}\s*\{\.([^}]+)\}")
FENCED_DIV_END_RE = re.compile(r"^:{3,4}\s*$")


class ParsedSlide:
    """Represents a single parsed slide from Reveal.js markdown."""

    def __init__(self) -> None:
        self.slide_class: str = "content-slide"
        self.title: str = ""
        self.subtitle: str = ""
        self.bullets: list[str] = []
        self.left_content: list[str] = []
        self.right_content: list[str] = []
        self.images: list[tuple[str, str]] = []  # (alt, path)
        self.tables: list[list[list[str]]] = []
        self.notes: str = ""
        self.raw_content: str = ""
        self.has_columns: bool = False
        self.skipped_blocks: list[str] = []

    def __repr__(self) -> str:
        return f"<Slide class={self.slide_class!r} title={self.title!r}>"


def _strip_html_tags(text: str) -> str:
    """Remove HTML tags from text, keeping content."""
    return re.sub(r"<[^>]+>", "", text).strip()


def _parse_markdown_table(text: str) -> Optional[list[list[str]]]:
    """Parse a simple markdown table into rows of cells."""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return None

    rows = []
    for line in lines:
        if re.match(r"^\|?\s*[-:]+", line):
            continue  # separator line
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells:
            rows.append(cells)
    return rows if rows else None


def parse_slides(markdown: str) -> list[ParsedSlide]:
    """Parse Reveal.js markdown into a list of ParsedSlide objects."""
    # Split on horizontal slide separator
    raw_slides = re.split(r"\n---\n", markdown)

    slides: list[ParsedSlide] = []

    for raw in raw_slides:
        raw = raw.strip()
        if not raw:
            continue

        slide = ParsedSlide()
        slide.raw_content = raw

        # Extract slide class
        class_match = SLIDE_CLASS_RE.search(raw)
        if class_match:
            slide.slide_class = class_match.group(1).strip()
            raw = SLIDE_CLASS_RE.sub("", raw).strip()

        # Extract speaker notes
        notes_match = NOTES_RE.search(raw)
        if notes_match:
            slide.notes = notes_match.group(1).strip()
            raw = raw[: notes_match.start()].strip()

        # Detect skipped blocks (Mermaid, Chart.js)
        for match in SKIP_BLOCK_RE.finditer(raw):
            slide.skipped_blocks.append(match.group())
        raw = SKIP_BLOCK_RE.sub("[Complex visualization — edit manually in PowerPoint]", raw)

        # Extract images
        for match in IMAGE_RE.finditer(raw):
            slide.images.append((match.group(1), match.group(2)))

        # Extract headings
        headings = list(HEADING_RE.finditer(raw))
        if headings:
            first = headings[0]
            level = len(first.group(1))
            slide.title = _strip_html_tags(first.group(2))
            if len(headings) > 1 and level == 1:
                slide.subtitle = _strip_html_tags(headings[1].group(2))

        # Detect columns (HTML div or Pandoc fenced divs)
        has_html_columns = "split-left" in raw or "split-right" in raw or '<div class="column' in raw.lower()
        has_pandoc_columns = ":::" in raw and ".column" in raw
        slide.has_columns = has_html_columns or has_pandoc_columns

        # Parse column content
        if slide.has_columns:
            _parse_two_column(raw, slide)
        else:
            # Extract bullets from remaining content
            slide.bullets = _extract_bullets(raw, headings)

        # Parse markdown tables
        table_lines = []
        in_table = False
        for line in raw.splitlines():
            stripped = line.strip()
            if stripped.startswith("|") and "|" in stripped[1:]:
                in_table = True
                table_lines.append(stripped)
            elif in_table:
                tbl = _parse_markdown_table("\n".join(table_lines))
                if tbl:
                    slide.tables.append(tbl)
                table_lines = []
                in_table = False
        if table_lines:
            tbl = _parse_markdown_table("\n".join(table_lines))
            if tbl:
                slide.tables.append(tbl)

        slides.append(slide)

    return slides


def _parse_two_column(raw: str, slide: ParsedSlide) -> None:
    """Extract left/right column content from HTML or Pandoc div wrappers."""
    left: list[str] = []
    right: list[str] = []
    current = None

    for line in raw.splitlines():
        stripped = line.strip()

        # HTML divs
        if "split-left" in stripped or ('class="column"' in stripped and current is None):
            current = "left"
            continue
        elif "split-right" in stripped or ('class="column"' in stripped and current == "left"):
            current = "right"
            continue

        # Pandoc fenced divs
        fenced = FENCED_DIV_START_RE.match(stripped)
        if fenced:
            cls = fenced.group(1)
            if "split-left" in cls or ("column" in cls and current is None):
                current = "left"
                continue
            elif "split-right" in cls or ("column" in cls and current == "left"):
                current = "right"
                continue

        # End of div
        if stripped in ("</div>",) or FENCED_DIV_END_RE.match(stripped):
            if current == "right":
                current = None
            continue

        # Skip heading/class lines already captured
        if HEADING_RE.match(stripped) and not current:
            continue
        if SLIDE_CLASS_RE.match(stripped):
            continue

        # Collect bullet content
        bullet = _line_to_bullet(stripped)
        if bullet is not None:
            if current == "left":
                left.append(bullet)
            elif current == "right":
                right.append(bullet)

    slide.left_content = left
    slide.right_content = right


def _line_to_bullet(line: str) -> Optional[str]:
    """Convert a markdown line to bullet text, or None if not a content line."""
    stripped = line.strip()
    if not stripped:
        return None
    if stripped.startswith(("#", "<!--", "<div", "</div", ":::", "<canvas")):
        return None
    # Strip bullet markers
    stripped = re.sub(r"^[-*+]\s+", "", stripped)
    stripped = re.sub(r"^\d+\.\s+", "", stripped)
    # Strip bold/italic markers
    stripped = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
    stripped = re.sub(r"\*(.+?)\*", r"\1", stripped)
    stripped = _strip_html_tags(stripped)
    return stripped if stripped else None


def _extract_bullets(raw: str, headings: list[re.Match]) -> list[str]:
    """Extract bullet points from non-column content."""
    bullets = []
    heading_lines = {m.start() for m in headings}

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Skip headings, class annotations, div tags
        if stripped.startswith(("#", "<!--", "<div", "</div", ":::", "```", "<canvas")):
            continue
        bullet = _line_to_bullet(stripped)
        if bullet:
            bullets.append(bullet)

    return bullets


# ---------------------------------------------------------------------------
# PPTX Generator: converts ParsedSlide objects to python-pptx slides
# ---------------------------------------------------------------------------

# Class name → Pandoc layout name mapping
CLASS_TO_LAYOUT = {
    "title-slide": "Title Slide",
    "divider-slide": "Section Header",
    "content-slide": "Title and Content",
    "highlight-slide": "Two Content",
    "content-box-slide": "Blank",
    "closing-slide": "Blank",
}


def _find_layout(prs, layout_name: str):
    """Find a slide layout by name, with fallback."""
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            if layout.name == layout_name:
                return layout

    # Fallback: try partial match
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            if layout_name.lower() in layout.name.lower():
                return layout

    # Last resort: first layout
    return prs.slide_masters[0].slide_layouts[0]


def _add_text_to_placeholder(placeholder, text: str, font_size_pt: float = 18) -> None:
    """Set text on a placeholder and apply BASF font defaults."""
    from pptx.util import Pt
    from pptx.dml.color import RGBColor

    placeholder.text = text
    for paragraph in placeholder.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.name = "Arial"
            run.font.size = Pt(font_size_pt)


def _add_bullets_to_placeholder(placeholder, bullets: list[str], font_size_pt: float = 18) -> None:
    """Add bulleted list to a placeholder."""
    from pptx.util import Pt

    tf = placeholder.text_frame
    tf.clear()

    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = bullet
        p.level = 0
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(font_size_pt)


def _add_table(slide, table_data: list[list[str]], left_inches: float = 0.8, top_inches: float = 2.5) -> None:
    """Add a native PPTX table to a slide."""
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor

    if not table_data or not table_data[0]:
        return

    rows = len(table_data)
    cols = len(table_data[0])
    width = min(11.5, cols * 2.5)

    table_shape = slide.shapes.add_table(
        rows, cols,
        Inches(left_inches), Inches(top_inches),
        Inches(width), Inches(min(4.0, rows * 0.5))
    )
    table = table_shape.table

    for row_idx, row_data in enumerate(table_data):
        for col_idx, cell_text in enumerate(row_data):
            if col_idx < cols:
                cell = table.cell(row_idx, col_idx)
                cell.text = cell_text
                for paragraph in cell.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = "Arial"
                        run.font.size = Pt(12)
                        if row_idx == 0:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Style header row with BASF dark blue
    if rows > 0:
        for col_idx in range(cols):
            cell = table.cell(0, col_idx)
            from pptx.oxml.ns import qn
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            fill_elem = tcPr.makeelement(qn("a:solidFill"), {})
            srgb = fill_elem.makeelement(qn("a:srgbClr"), {"val": "004A96"})
            fill_elem.append(srgb)
            tcPr.append(fill_elem)


def _add_image(slide, image_path: str, images_dir: Path, left: float = 0.8, top: float = 2.0) -> None:
    """Add an image to a slide if the file exists."""
    from pptx.util import Inches

    # Resolve image path
    img = images_dir / image_path
    if not img.exists():
        # Try without leading directories
        img = images_dir / Path(image_path).name
    if not img.exists():
        return

    max_width = 10.0
    max_height = 5.0
    slide.shapes.add_picture(
        str(img),
        Inches(left), Inches(top),
        Inches(max_width)
    )


def generate_pptx(
    slides: list[ParsedSlide],
    template_path: str,
    output_path: str,
    images_dir: Path,
) -> None:
    """Generate a PPTX file from parsed slides using the BASF template."""
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
    except ImportError:
        print("Error: python-pptx is required. Install with: pip install python-pptx")
        sys.exit(1)

    if not os.path.exists(template_path):
        print(f"Error: Template not found: {template_path}")
        print("Run create-basf-reference-pptx.py first to generate the reference template.")
        sys.exit(1)

    prs = Presentation(template_path)

    # Remove all pre-existing slides from the template (keep only masters/layouts)
    while len(prs.slides) > 0:
        rId = prs.slides._sldIdLst[0].get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )
        prs.part.drop_rel(rId)
        sldId = prs.slides._sldIdLst[0]
        prs.slides._sldIdLst.remove(sldId)

    # List available layouts for debugging
    print(f"Template: {template_path}")
    print(f"Available layouts:")
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            print(f"  - {layout.name}")
    print()

    for i, parsed in enumerate(slides):
        layout_name = CLASS_TO_LAYOUT.get(parsed.slide_class, "Title and Content")
        layout = _find_layout(prs, layout_name)

        slide = prs.slides.add_slide(layout)

        print(f"  Slide {i + 1}: {parsed.slide_class} → '{layout.name}' | {parsed.title or '(no title)'}")

        # --- Helpers for this slide's placeholders ---
        def _find_ph(idx):
            for ph in slide.placeholders:
                if ph.placeholder_format.idx == idx:
                    return ph
            return None

        def _find_title_ph():
            """Find the title placeholder — BASF Title Slide uses idx 14, others use idx 0."""
            for idx in (0, 14, 17):
                ph = _find_ph(idx)
                if ph is not None:
                    return ph
            return None

        def _find_body_phs():
            """Find body/content placeholders (OBJECT type), sorted by idx."""
            content_indices = [10, 11, 12, 13, 14, 15]
            result = []
            for ph in sorted(slide.placeholders, key=lambda p: p.placeholder_format.idx):
                idx = ph.placeholder_format.idx
                # Skip title (0), date (2), footer (3), slide number (4)
                if idx in (0, 2, 3, 4):
                    continue
                result.append(ph)
            return result

        # --- Set title ---
        if parsed.title:
            title_ph = _find_title_ph()
            if title_ph:
                _add_text_to_placeholder(title_ph, parsed.title, font_size_pt=28)

        # --- Handle by slide type ---
        if parsed.slide_class == "title-slide":
            # BASF Title Slide: idx 14 = title, idx 15 = subtitle
            body_phs = _find_body_phs()
            subtitle_text = parsed.subtitle or ""
            if parsed.bullets:
                subtitle_text = "\n".join(parsed.bullets[:3])
            if subtitle_text and body_phs:
                # Use the second body placeholder for subtitle (or first if title already set)
                sub_ph = body_phs[-1] if len(body_phs) > 1 else body_phs[0]
                _add_text_to_placeholder(sub_ph, subtitle_text, font_size_pt=20)

        elif parsed.slide_class == "closing-slide":
            # Minimal content for finale slide
            pass

        elif parsed.has_columns and (parsed.left_content or parsed.right_content):
            # Two Content layout: fill body placeholders
            body_phs = _find_body_phs()

            if len(body_phs) >= 2:
                if parsed.left_content:
                    _add_bullets_to_placeholder(body_phs[0], parsed.left_content)
                if parsed.right_content:
                    _add_bullets_to_placeholder(body_phs[1], parsed.right_content)
            elif len(body_phs) >= 1:
                all_content = parsed.left_content + ["—"] + parsed.right_content
                _add_bullets_to_placeholder(body_phs[0], all_content)

        else:
            # Standard content: fill the first body placeholder with bullets
            body_phs = _find_body_phs()
            if parsed.bullets and body_phs:
                _add_bullets_to_placeholder(body_phs[0], parsed.bullets)

        # --- Tables ---
        for table_data in parsed.tables:
            _add_table(slide, table_data)

        # --- Images ---
        for alt, img_path in parsed.images:
            _add_image(slide, img_path, images_dir)

        # --- Speaker notes ---
        if parsed.notes:
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = parsed.notes

        # --- Skipped blocks warning ---
        if parsed.skipped_blocks:
            notes_text = slide.notes_slide.notes_text_frame.text
            warning = f"\n\n[AUTO-EXPORT NOTE: {len(parsed.skipped_blocks)} complex visualization(s) skipped — edit manually]"
            slide.notes_slide.notes_text_frame.text = (notes_text or "") + warning

    prs.save(output_path)
    print(f"\n✅ PPTX exported: {output_path} ({len(slides)} slides)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    images_dir = Path(args.images_dir) if args.images_dir else input_path.parent

    print(f"📊 Parsing slides from: {input_path}")
    markdown = input_path.read_text(encoding="utf-8")
    slides = parse_slides(markdown)
    print(f"   Found {len(slides)} slides\n")

    print(f"📦 Generating PPTX...")
    generate_pptx(slides, args.template, args.output, images_dir)


if __name__ == "__main__":
    main()

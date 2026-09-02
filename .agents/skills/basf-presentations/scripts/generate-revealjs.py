#!/usr/bin/env python3
"""Generate Reveal.js slides.md from PPTX extraction data.

Reads summary.json produced by extract-pptx-reference.py and generates
a complete Reveal.js markdown file that recreates each slide with the
BASF SCSS design system classes.

Usage:
    python3 generate-revealjs.py pptx-extract/ basf-pptx-source-demo/

Produces:
    basf-pptx-source-demo/slides.md   - Reveal.js markdown
    basf-pptx-source-demo/assets/     - Copied images
"""

from __future__ import annotations

import csv
import html
import json
import re
import shutil
import sys
from pathlib import Path
from textwrap import dedent

# ============================================================
#  CONFIGURATION
# ============================================================

# PPTX layout name → Reveal.js CSS class
LAYOUT_CLASS = {
    "Title page 01": "title-slide",
    "Title light": "divider-slide",
    "Title dark": None,  # skip for now
    "Title white": None,  # skip for now
    "Title and content": "content-slide",
    "Title and content 2-column": "content-slide",
    "Title and content 3-column": "content-slide",
    "Title and content 4-column": "content-slide",
    "BASF_Finale": "closing-slide",
}

# Number of columns per layout
LAYOUT_COLS = {
    "Title and content 2-column": 2,
    "Title and content 3-column": 3,
    "Title and content 4-column": 4,
}

# Column boundaries (in inches) based on PPTX grid positions
# 3-column (most common): title 0.6–4.5in, col2 4.7–8.6in, col3 8.8–12.7in
COL_BOUNDARIES = {
    2: [6.5],
    3: [4.6, 8.7],
    4: [3.4, 6.5, 9.6],
}

# Chart ID counter
_chart_id = 0


def next_chart_id() -> str:
    global _chart_id
    _chart_id += 1
    return f"chart-{_chart_id}"


# ============================================================
#  TEXT EXTRACTION
# ============================================================


def clean_text(raw: str) -> str:
    """Clean text from PPTX: normalise whitespace, strip control chars."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\u200b\u200c\u200d\ufeff\ufffd]", "", raw)
    return " ".join(text.split())


def extract_title(slide: dict) -> str:
    """Get the title from the first title-like placeholder.

    Priority: shapes named 'Titel*' first (explicit title placeholder),
    then any other non-number placeholder, then any shape with text.
    """
    # First: prefer shapes explicitly named "Titel*" (German PPTX title placeholder)
    for d in slide["shape_details"]:
        if not d.get("placeholder"):
            continue
        if not d.get("text"):
            continue
        name = d.get("name", "")
        if not name.startswith("Titel"):
            continue
        txt = clean_text(d["text"][0])
        if txt.isdigit() and len(txt) <= 3:
            continue
        return txt

    # Second: any placeholder with text (excluding slide numbers)
    for d in slide["shape_details"]:
        if not d.get("placeholder"):
            continue
        if not d.get("text"):
            continue
        txt = clean_text(d["text"][0])
        if txt.isdigit() and len(txt) <= 3:
            continue
        if "Foliennummer" in d.get("name", ""):
            continue
        return txt

    # Fallback: first TEXT_BOX or shape with text
    for d in slide["shape_details"]:
        if d.get("text"):
            txt = clean_text(d["text"][0])
            if not txt.isdigit() or len(txt) > 3:
                return txt

    return f"Slide {slide['slide_number']}"


def is_slide_number_shape(d: dict) -> bool:
    """Check if a shape is the slide number placeholder."""
    if "Foliennummer" in d.get("name", ""):
        return True
    if d.get("text") and d["text"][0].strip().isdigit():
        txt = d["text"][0].strip()
        if len(txt) <= 3 and d["box_in"]["top"] > 6.5:
            return True
    return False


def is_offscreen(d: dict) -> bool:
    """Check if a shape is off-screen (decorative group at x < 0)."""
    return d["box_in"]["left"] < 0


def get_column(d: dict, num_cols: int) -> int:
    """Determine which column a shape belongs to based on x-position."""
    x = d["box_in"]["left"]
    boundaries = COL_BOUNDARIES.get(num_cols, [])
    for i, boundary in enumerate(boundaries):
        if x < boundary:
            return i
    return len(boundaries)


def shape_has_content(d: dict) -> bool:
    """Check if shape has meaningful content (text, image, table, chart)."""
    if d.get("text") and clean_text(d["text"][0]):
        return True
    if d.get("image") and d["image"].get("embedded"):
        return True
    if d.get("table"):
        return True
    if d.get("chart"):
        return True
    return False


# ============================================================
#  CONTENT RENDERING
# ============================================================


def render_text_block(d: dict) -> str:
    """Render a text shape as markdown paragraphs."""
    if not d.get("text"):
        return ""
    raw = d["text"][0]
    # Split on all line-break variants (\n, \r, \x0b vertical tab)
    parts = re.split(r"[\n\r\x0b]+", raw)
    lines = [clean_text(line) for line in parts if clean_text(line)]
    return "\n".join(lines)


def render_kpi_card(d: dict) -> str:
    """Parse KPI card text (label | value | delta) and render as .kpi-card."""
    if not d.get("text"):
        return ""
    raw = d["text"][0]
    parts = [p.strip() for p in re.split(r"[\n\r\x0b]+", raw) if p.strip()]
    if len(parts) < 2:
        return f"<p>{html.escape(clean_text(raw))}</p>"

    label = html.escape(clean_text(parts[0]))
    value = html.escape(clean_text(parts[1]))
    delta = ""
    delta_class = "neutral"
    if len(parts) >= 3:
        delta_raw = parts[2]
        delta = html.escape(clean_text(delta_raw))
        if "+" in delta_raw:
            delta_class = "positive"
        elif "-" in delta_raw:
            delta_class = "negative"

    card = f"""<div class="kpi-card">
<div class="kpi-label">{label}</div>
<div class="kpi-value">{value}</div>"""
    if delta:
        card += f'\n<div class="kpi-delta {delta_class}">{delta}</div>'
    card += "\n</div>"
    return card


def resolve_asset_path(stored_path: str, extract_dir: Path) -> Path | None:
    """Resolve an asset path from summary.json to actual filesystem location.

    Paths in summary.json may reference old /tmp locations; we resolve them
    relative to the current extract_dir.
    """
    p = Path(stored_path)
    if p.exists():
        return p
    # Reconstruct: /tmp/pptx-extract/slide-XX/file.ext → extract_dir/slide-XX/file.ext
    parts = p.parts
    # Find "slide-XX" in the path and take from there
    for i, part in enumerate(parts):
        if part.startswith("slide-"):
            relative = Path(*parts[i:])
            candidate = extract_dir / relative
            if candidate.exists():
                return candidate
    # Last resort: search by filename
    name = p.name
    matches = list(extract_dir.rglob(name))
    if matches:
        return matches[0]
    return None


def render_image(d: dict, slide_num: int, extract_dir: Path, assets_dir: Path) -> str:
    """Copy image to assets/ and return an <img> tag."""
    if not d.get("image") or not d["image"].get("embedded"):
        return ""
    src = resolve_asset_path(d["image"]["path"], extract_dir)
    if src is None:
        return '<div class="img-placeholder">Image</div>'

    dest_name = src.name
    dest = assets_dir / dest_name
    shutil.copy2(src, dest)
    return f'<img src="assets/{html.escape(dest_name)}" class="slide-image" alt="">'


def render_table(d: dict, extract_dir: Path) -> str:
    """Render a table from CSV data as an HTML table."""
    if not d.get("table"):
        return ""
    table_info = d["table"]
    csv_resolved = resolve_asset_path(table_info["path"], extract_dir)
    if csv_resolved and csv_resolved.exists():
        with csv_resolved.open("r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
    else:
        # Fallback to inline preview data
        rows = table_info.get("preview", [])

    if not rows:
        return ""

    lines = ['<table>']
    # First row as header
    lines.append("  <thead><tr>")
    for cell in rows[0]:
        lines.append(f"    <th>{html.escape(clean_text(cell))}</th>")
    lines.append("  </tr></thead>")
    # Remaining rows
    lines.append("  <tbody>")
    for row in rows[1:]:
        lines.append("  <tr>")
        for cell in row:
            lines.append(f"    <td>{html.escape(clean_text(cell))}</td>")
        lines.append("  </tr>")
    lines.append("  </tbody>")
    lines.append("</table>")
    return "\n".join(lines)


def render_chart(d: dict, extract_dir: Path) -> str:
    """Render a chart as a Chart.js canvas element."""
    if not d.get("chart"):
        return ""
    chart_info = d["chart"]
    chart_id = next_chart_id()
    chart_type_raw = chart_info.get("type", "")

    # Map PPTX chart type to Chart.js type
    if "COLUMN" in chart_type_raw or "BAR" in chart_type_raw:
        chart_type = "bar"
    elif "DOUGHNUT" in chart_type_raw:
        chart_type = "doughnut"
    elif "PIE" in chart_type_raw:
        chart_type = "pie"
    elif "LINE" in chart_type_raw:
        chart_type = "line"
    else:
        chart_type = "bar"

    categories = chart_info.get("categories", [])
    series = chart_info.get("series", [])

    # Build Chart.js datasets
    basf_colors = [
        "#004a96",  # BASF blue
        "#21a0d2",  # BASF light blue
        "#00793a",  # BASF green
        "#f39c12",  # amber
        "#e74c3c",  # red
        "#8e44ad",  # purple
    ]
    datasets = []
    for i, s in enumerate(series):
        color = basf_colors[i % len(basf_colors)]
        ds = {
            "label": s.get("name", f"Series {i+1}"),
            "data": s.get("values", []),
            "backgroundColor": color,
            "borderColor": color,
        }
        datasets.append(ds)

    config = {
        "type": chart_type,
        "data": {
            "labels": categories,
            "datasets": datasets,
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {"display": len(series) > 1},
            },
        },
    }

    config_json = html.escape(json.dumps(config, ensure_ascii=False))
    return (
        f'<div class="chart-container">'
        f'<canvas id="{chart_id}" data-chart-config=\'{config_json}\'></canvas>'
        f"</div>"
    )


# ============================================================
#  KPI CARD DETECTION
# ============================================================


def is_kpi_card_shape(d: dict) -> bool:
    """Heuristic: AUTO_SHAPE ~3.9×1.9in containing 2-3 text lines with € or %."""
    if d.get("type") != "AUTO_SHAPE":
        return False
    w = d["box_in"]["width"]
    h = d["box_in"]["height"]
    if not (3.0 < w < 5.0 and 1.0 < h < 3.0):
        return False
    if not d.get("text"):
        return False
    txt = d["text"][0]
    return bool(re.search(r"[€%]|\d+\.\d{3}", txt))


def is_stat_shape(d: dict) -> bool:
    """Heuristic: shape with large percentage or currency value."""
    if not d.get("text"):
        return False
    txt = d["text"][0].strip()
    return bool(re.match(r"^\d+%$", txt))


# ============================================================
#  SLIDE GENERATORS
# ============================================================


def generate_title_page(
    slide: dict, extract_dir: Path, assets_dir: Path
) -> str:
    """Title page 01 → .title-slide"""
    title = extract_title(slide)
    lines = ['<!-- .slide: class="title-slide" -->', ""]
    lines.append(f"# {title}")
    lines.append("")

    # Look for subtitle/description text
    for d in slide["shape_details"]:
        if is_slide_number_shape(d) or is_offscreen(d):
            continue
        if d.get("type") == "LINE":
            continue
        if d.get("placeholder"):
            # Already used as title
            txt = clean_text(d.get("text", [""])[0])
            if txt == title:
                continue
        if d.get("text"):
            txt = clean_text(d["text"][0])
            if txt and txt != title and not txt.isdigit():
                if d.get("type") == "TEXT_BOX" and d["box_in"]["top"] < 2.0:
                    # Subtitle position
                    lines.append(f"### {txt}")
                    lines.append("")
                elif len(txt) > 20:
                    lines.append(txt)
                    lines.append("")
        if d.get("image") and d["image"].get("embedded"):
            img = render_image(d, slide["slide_number"], extract_dir, assets_dir)
            if img:
                lines.append(img)
                lines.append("")

    return "\n".join(lines)


def generate_divider_slide(
    slide: dict, extract_dir: Path, assets_dir: Path
) -> str:
    """Title light → .divider-slide (agenda, section break)"""
    title = extract_title(slide)
    lines = ['<!-- .slide: class="divider-slide" -->', ""]
    lines.append(f"## {title}")
    lines.append("")

    # Count GROUP shapes (agenda rows) to generate placeholder items
    groups = [
        d for d in slide["shape_details"]
        if d["type"] == "GROUP" and not is_offscreen(d)
    ]
    if groups:
        # Generate ordered list with highlight on first item
        for i in range(len(groups)):
            bold = "**" if i == 0 else ""
            lines.append(f"{i+1}. {bold}Lorem ipsum agenda item {i+1}{bold}")
        lines.append("")
    else:
        # Fallback: use any available text, splitting multi-line blocks
        for d in slide["shape_details"]:
            if is_slide_number_shape(d) or is_offscreen(d):
                continue
            if d.get("text"):
                raw = d["text"][0]
                txt = clean_text(raw)
                if txt and txt != title and not txt.isdigit():
                    # Split on line breaks to preserve list structure
                    parts = [clean_text(l) for l in re.split(r"[\n\r\x0b]+", raw) if clean_text(l)]
                    if len(parts) > 1:
                        for p in parts:
                            lines.append(f"- {p}")
                    else:
                        lines.append(txt)
                    lines.append("")

    # Handle images
    for d in slide["shape_details"]:
        if d.get("image") and d["image"].get("embedded"):
            img = render_image(d, slide["slide_number"], extract_dir, assets_dir)
            if img:
                lines.append(img)
                lines.append("")

    return "\n".join(lines)


def generate_content_slide_single(
    slide: dict, extract_dir: Path, assets_dir: Path
) -> str:
    """Title and content → .content-slide (single full-width column)"""
    title = extract_title(slide)
    lines = ['<!-- .slide: class="content-slide" -->', ""]
    lines.append(f"## {title}")
    lines.append("")

    # Collect shapes to detect multi-image pattern
    shapes = []
    rect_count = 0
    title_used = False
    for d in slide["shape_details"]:
        if is_slide_number_shape(d) or is_offscreen(d):
            continue
        if d.get("type") in ("LINE", "AUTO_SHAPE") and not d.get("text"):
            rect_count += 1
            continue
        if not title_used and d.get("placeholder") and d.get("text"):
            txt = clean_text(d["text"][0])
            if txt == title:
                title_used = True
                continue
        shapes.append(d)

    # If no content shapes remain, render placeholder boxes
    if not shapes and rect_count > 0:
        lines.append('<div class="template-placeholder">Layout placeholder</div>')
        lines.append("")
        return "\n".join(lines)

    image_count = sum(1 for d in shapes if d.get("image") and d["image"].get("embedded"))
    in_image_grid = False

    for d in shapes:
        if d.get("image") and d["image"].get("embedded"):
            if image_count >= 3 and not in_image_grid:
                lines.append('<div class="image-grid">')
                in_image_grid = True
            lines.append(render_image(d, slide["slide_number"], extract_dir, assets_dir))
            lines.append("")
        else:
            if in_image_grid:
                lines.append("</div>")
                lines.append("")
                in_image_grid = False
            if d.get("table"):
                lines.append(render_table(d, extract_dir))
                lines.append("")
            elif d.get("chart"):
                lines.append(render_chart(d, extract_dir))
                lines.append("")
            elif d.get("text"):
                txt = d["text"][0]
                text_lines = [clean_text(l) for l in re.split(r"[\n\r\x0b]+", txt) if clean_text(l)]
                for tl in text_lines:
                    lines.append(f"- {tl}")
                lines.append("")

    if in_image_grid:
        lines.append("</div>")
        lines.append("")

    return "\n".join(lines)


def generate_content_slide_multi(
    slide: dict, num_cols: int, extract_dir: Path, assets_dir: Path
) -> str:
    """Title and content N-column → .content-slide with .columns"""
    title = extract_title(slide)
    slide_num = slide["slide_number"]

    # Detect whether it's a narrow-title (left-third only) or full-width title
    title_shape = None
    for d in slide["shape_details"]:
        if d.get("placeholder") and d.get("text"):
            txt = clean_text(d["text"][0])
            if txt == title:
                title_shape = d
                break
    narrow_title = title_shape and title_shape["box_in"]["width"] < 5.0

    # Collect content shapes into columns based on x-position
    columns: dict[int, list] = {i: [] for i in range(num_cols)}

    for d in slide["shape_details"]:
        if is_slide_number_shape(d) or is_offscreen(d):
            continue
        if d.get("type") == "LINE":
            continue
        # Skip decorative triangles
        if "Dreieck" in d.get("name", "") or "riangle" in d.get("name", ""):
            continue

        # Skip the title shape
        if d.get("placeholder") and d.get("text"):
            txt = clean_text(d["text"][0])
            if txt == title:
                continue

        if not shape_has_content(d):
            continue

        col = get_column(d, num_cols)
        columns[col].append(d)

    # Check for KPI pattern: narrow title + 2 columns of KPI cards
    kpi_shapes = []
    if narrow_title and num_cols == 3:
        for col_idx in (1, 2):  # columns 2 and 3
            for d in columns.get(col_idx, []):
                if is_kpi_card_shape(d):
                    kpi_shapes.append(d)
    is_kpi_layout = len(kpi_shapes) >= 4

    lines = ['<!-- .slide: class="content-slide" -->', ""]
    lines.append(f"## {title}")
    lines.append("")

    if is_kpi_layout:
        # KPI grid: title on left, cards on right
        # Left column text
        for d in columns.get(0, []):
            if d.get("text"):
                txt = render_text_block(d)
                if txt:
                    lines.append(txt)
                    lines.append("")

        # KPI grid
        grid_cols = 2 if len(kpi_shapes) <= 6 else 3
        lines.append(f'<div class="kpi-grid cols-{grid_cols}">')
        # Sort KPI shapes by position (top to bottom, left to right)
        kpi_shapes.sort(key=lambda d: (d["box_in"]["top"], d["box_in"]["left"]))
        for d in kpi_shapes:
            lines.append(render_kpi_card(d))
        lines.append("</div>")
        lines.append("")
    else:
        # Standard multi-column layout
        col_widths = {
            2: ["col-50", "col-50"],
            3: ["col-33", "col-33", "col-33"],
            4: ["col-25", "col-25", "col-25", "col-25"],
        }
        # Adjust for narrow title
        if narrow_title and num_cols == 3:
            col_widths[3] = ["col-30", "col-35", "col-35"]

        lines.append('<div class="columns">')
        widths = col_widths.get(num_cols, ["col-50"] * num_cols)
        has_any_content = any(columns.get(i, []) for i in range(num_cols))

        # If all columns empty, render placeholder boxes
        if not has_any_content:
            for col_idx in range(num_cols):
                w = widths[col_idx]
                lines.append(f'<div class="column {w}">')
                lines.append('<div class="template-placeholder">Content area</div>')
                lines.append('</div>')
            lines.append('</div>')
            lines.append("")
            return "\n".join(lines)

        for col_idx in range(num_cols):
            col_shapes = columns.get(col_idx, [])
            # Sort by vertical position
            col_shapes.sort(key=lambda d: d["box_in"]["top"])

            # Skip entirely empty columns
            if not col_shapes:
                continue

            w = widths[col_idx]
            lines.append(f'<div class="column {w}">')
            lines.append("")

            for d in col_shapes:
                if d.get("chart"):
                    lines.append(render_chart(d, extract_dir))
                    lines.append("")
                elif d.get("table"):
                    lines.append(render_table(d, extract_dir))
                    lines.append("")
                elif d.get("image") and d["image"].get("embedded"):
                    lines.append(
                        render_image(d, slide_num, extract_dir, assets_dir)
                    )
                    lines.append("")
                elif d.get("text"):
                    txt = d["text"][0]
                    text_lines = [clean_text(l) for l in re.split(r"[\n\r\x0b]+", txt) if clean_text(l)]
                    if is_stat_shape(d):
                        lines.append(
                            f'<div class="kpi-value">{html.escape(text_lines[0])}</div>'
                        )
                    elif is_kpi_card_shape(d):
                        lines.append(render_kpi_card(d))
                    else:
                        for tl in text_lines:
                            lines.append(f"- {tl}")
                    lines.append("")

            lines.append("</div>")
        lines.append("</div>")
        lines.append("")

    return "\n".join(lines)


def generate_closing_slide(slide: dict) -> str:
    """BASF_Finale → .closing-slide"""
    return '<!-- .slide: class="closing-slide" -->\n\n## BASF\n'


# ============================================================
#  MAIN GENERATOR
# ============================================================


def generate_slide(
    slide: dict, extract_dir: Path, assets_dir: Path
) -> str | None:
    """Generate markdown for a single slide."""
    layout = slide["layout_name"]
    css_class = LAYOUT_CLASS.get(layout)

    # Skip unsupported layouts
    if css_class is None:
        return None

    num_cols = LAYOUT_COLS.get(layout, 0)

    if layout == "Title page 01":
        return generate_title_page(slide, extract_dir, assets_dir)
    elif layout == "Title light":
        return generate_divider_slide(slide, extract_dir, assets_dir)
    elif layout == "BASF_Finale":
        return generate_closing_slide(slide)
    elif num_cols >= 2:
        return generate_content_slide_multi(
            slide, num_cols, extract_dir, assets_dir
        )
    else:
        return generate_content_slide_single(slide, extract_dir, assets_dir)


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <extract-dir> <output-dir>")
        sys.exit(1)

    extract_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    summary_path = extract_dir / "summary.json"

    if not summary_path.exists():
        print(f"Error: {summary_path} not found")
        sys.exit(1)

    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    with summary_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    slide_blocks: list[str] = []
    skipped: list[int] = []

    for slide in data["slides"]:
        md = generate_slide(slide, extract_dir, assets_dir)
        if md is None:
            skipped.append(slide["slide_number"])
            continue
        slide_blocks.append(md)

    # Join with Reveal.js horizontal separator
    slides_md = "\n---\n\n".join(slide_blocks)

    output_path = output_dir / "slides.md"
    output_path.write_text(slides_md, encoding="utf-8")

    print(f"Generated {len(slide_blocks)} slides → {output_path}")
    if skipped:
        print(f"Skipped {len(skipped)} slides (unsupported layouts): {skipped}")
    print(f"Assets copied to: {assets_dir}")
    print(f"Total images: {len(list(assets_dir.glob('*')))}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
check-pptx-overflow.py — Detect and fix overflow issues in PPTX presentations.

Checks for:
  1. Shapes extending beyond slide boundaries (left, right, top, bottom)
  2. Text overflow: content that exceeds the text box height
  3. Tables overflowing slide edges
  4. Images positioned or sized beyond the visible area
  5. Negative positioning (off-screen left/top)

Fix modes:
  --check   Report issues only (default)
  --fix     Auto-fix issues and save to output file

Fix strategies:
  - Shapes beyond edges → clamp position/size to slide bounds with padding
  - Text overflow → enable auto-size (shrink text to fit) or reduce font size
  - Tables too wide → shrink to fit slide width
  - Images off-screen → reposition within slide bounds

Usage:
    python3 check-pptx-overflow.py presentation.pptx [--fix] [-o output.pptx]
    python3 check-pptx-overflow.py presentation.pptx --check --verbose
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from pptx import Presentation
    from pptx.util import Inches, Emu, Pt
    from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
    from pptx.dml.color import RGBColor
except ImportError:
    print("Error: python-pptx is required. Install with: pip install python-pptx")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Minimum padding from slide edge (EMU). Shapes touching the edge look wrong.
EDGE_PADDING_EMU = Inches(0.1)

# Font size estimation constants (EMU per point of line height, rough)
# PowerPoint line spacing is typically 1.2x font size
LINE_HEIGHT_FACTOR = 1.2

# Minimum font size we'll shrink to (points)
MIN_FONT_SIZE_PT = 10

# Font size step for shrinking (points)
FONT_SHRINK_STEP_PT = 1


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class OverflowIssue:
    """A single overflow issue detected on a slide."""
    slide_num: int
    shape_name: str
    issue_type: str  # "bounds", "text_overflow", "table_overflow", "negative_pos"
    detail: str
    severity: str = "warning"  # "warning" or "error"
    fixed: bool = False
    fix_detail: str = ""


@dataclass
class SlideReport:
    """Report for a single slide."""
    slide_num: int
    layout_name: str
    issues: list[OverflowIssue] = field(default_factory=list)


@dataclass
class PresentationReport:
    """Full report for a presentation."""
    filepath: str
    slide_width_emu: int = 0
    slide_height_emu: int = 0
    slides: list[SlideReport] = field(default_factory=list)

    @property
    def total_issues(self) -> int:
        return sum(len(s.issues) for s in self.slides)

    @property
    def total_fixed(self) -> int:
        return sum(1 for s in self.slides for i in s.issues if i.fixed)


# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------

def _safe_shape_name(shape) -> str:
    """Get shape name safely."""
    try:
        return shape.name or "(unnamed)"
    except Exception:
        return "(unnamed)"


def _safe_shape_bounds(shape) -> Optional[tuple[int, int, int, int]]:
    """Get shape bounds (left, top, width, height) in EMU, safely."""
    try:
        return shape.left, shape.top, shape.width, shape.height
    except Exception:
        return None


def _safe_has_text_frame(shape) -> bool:
    """Check if shape has a text frame, safely."""
    try:
        return shape.has_text_frame
    except Exception:
        return False


def _safe_has_table(shape) -> bool:
    """Check if shape has a table, safely."""
    try:
        return shape.has_table
    except Exception:
        return False


def _estimate_text_height_emu(text_frame, shape_width_emu: int) -> int:
    """Estimate the rendered height of text in a text frame.

    Uses font size and approximate character-per-line calculations to
    estimate how tall the text would render. This is an approximation —
    exact rendering depends on the PowerPoint layout engine.
    """
    total_height = 0

    for para in text_frame.paragraphs:
        # Determine font size for this paragraph
        font_size_pt = 18  # default
        for run in para.runs:
            if run.font.size:
                font_size_pt = run.font.size.pt
                break
        if para.font and para.font.size:
            font_size_pt = para.font.size.pt

        line_height_pt = font_size_pt * LINE_HEIGHT_FACTOR

        # Estimate characters per line based on shape width
        # Rough: average char width ≈ 0.55 * font_size for Arial
        char_width_pt = font_size_pt * 0.55
        chars_per_line = max(1, int((shape_width_emu / 12700) / char_width_pt))
        text = para.text
        num_lines = max(1, -(-len(text) // chars_per_line))  # ceiling division

        total_height += int(num_lines * line_height_pt * 12700)  # pt to EMU

    # Add internal margins (top + bottom, ~0.05in each)
    total_height += Inches(0.1)
    return total_height


def _get_max_font_size(text_frame) -> Optional[float]:
    """Get the largest font size used in a text frame (in pt)."""
    max_size = None
    for para in text_frame.paragraphs:
        for run in para.runs:
            if run.font.size:
                sz = run.font.size.pt
                if max_size is None or sz > max_size:
                    max_size = sz
    return max_size


def _count_text_lines(text_frame) -> int:
    """Count approximate number of text lines."""
    return len(text_frame.paragraphs)


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_slide(slide, slide_num: int, slide_w: int, slide_h: int,
                verbose: bool = False) -> SlideReport:
    """Check a single slide for overflow issues."""
    layout_name = "unknown"
    try:
        layout_name = slide.slide_layout.name
    except Exception:
        pass

    report = SlideReport(slide_num=slide_num, layout_name=layout_name)

    for shape in slide.shapes:
        bounds = _safe_shape_bounds(shape)
        if bounds is None:
            if verbose:
                report.issues.append(OverflowIssue(
                    slide_num=slide_num,
                    shape_name=_safe_shape_name(shape),
                    issue_type="no_bounds",
                    detail="Shape has no position/size properties (no spPr)",
                    severity="warning",
                ))
            continue

        left, top, width, height = bounds
        right = left + width
        bottom = top + height
        name = _safe_shape_name(shape)

        # --- Check 1: Negative positioning (off-screen left/top) ---
        if left < -EDGE_PADDING_EMU:
            report.issues.append(OverflowIssue(
                slide_num=slide_num,
                shape_name=name,
                issue_type="negative_pos",
                detail=f"Left={Emu(left).inches:.2f}in — off-screen to the left",
                severity="error",
            ))

        if top < -EDGE_PADDING_EMU:
            report.issues.append(OverflowIssue(
                slide_num=slide_num,
                shape_name=name,
                issue_type="negative_pos",
                detail=f"Top={Emu(top).inches:.2f}in — off-screen above",
                severity="error",
            ))

        # --- Check 2: Shape extends beyond right/bottom edge ---
        if right > slide_w + EDGE_PADDING_EMU:
            overflow_in = Emu(right - slide_w).inches
            report.issues.append(OverflowIssue(
                slide_num=slide_num,
                shape_name=name,
                issue_type="bounds",
                detail=f"Right edge at {Emu(right).inches:.2f}in — overflows by {overflow_in:.2f}in",
                severity="error",
            ))

        if bottom > slide_h + EDGE_PADDING_EMU:
            overflow_in = Emu(bottom - slide_h).inches
            report.issues.append(OverflowIssue(
                slide_num=slide_num,
                shape_name=name,
                issue_type="bounds",
                detail=f"Bottom edge at {Emu(bottom).inches:.2f}in — overflows by {overflow_in:.2f}in",
                severity="error",
            ))

        # --- Check 3: Text overflow ---
        if _safe_has_text_frame(shape):
            tf = shape.text_frame
            text_content = tf.text.strip()
            if not text_content:
                continue

            # Skip if auto-size is set to shrink text to fit
            try:
                if tf.auto_size == MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE:
                    continue
            except Exception:
                pass

            est_height = _estimate_text_height_emu(tf, width)
            if est_height > height * 1.05:  # 5% tolerance
                overflow_pct = int((est_height / height - 1) * 100)
                line_count = _count_text_lines(tf)
                max_font = _get_max_font_size(tf)
                font_info = f", font={max_font:.0f}pt" if max_font else ""
                report.issues.append(OverflowIssue(
                    slide_num=slide_num,
                    shape_name=name,
                    issue_type="text_overflow",
                    detail=f"{line_count} paragraphs, ~{overflow_pct}% overflow{font_info} "
                           f"(est {Emu(est_height).inches:.1f}in > {Emu(height).inches:.1f}in box)",
                    severity="warning" if overflow_pct < 30 else "error",
                ))

        # --- Check 4: Table overflow ---
        if _safe_has_table(shape):
            if right > slide_w:
                report.issues.append(OverflowIssue(
                    slide_num=slide_num,
                    shape_name=name,
                    issue_type="table_overflow",
                    detail=f"Table right edge at {Emu(right).inches:.2f}in > slide width {Emu(slide_w).inches:.2f}in",
                    severity="error",
                ))
            if bottom > slide_h:
                report.issues.append(OverflowIssue(
                    slide_num=slide_num,
                    shape_name=name,
                    issue_type="table_overflow",
                    detail=f"Table bottom at {Emu(bottom).inches:.2f}in > slide height {Emu(slide_h).inches:.2f}in",
                    severity="error",
                ))

    return report


def check_presentation(prs_path: str, verbose: bool = False) -> PresentationReport:
    """Check an entire presentation for overflow issues."""
    prs = Presentation(prs_path)
    report = PresentationReport(
        filepath=prs_path,
        slide_width_emu=prs.slide_width,
        slide_height_emu=prs.slide_height,
    )

    for i, slide in enumerate(prs.slides, 1):
        slide_report = check_slide(
            slide, i, prs.slide_width, prs.slide_height, verbose=verbose
        )
        report.slides.append(slide_report)

    return report


# ---------------------------------------------------------------------------
# Fix functions
# ---------------------------------------------------------------------------

def fix_shape_bounds(shape, slide_w: int, slide_h: int, padding: int = EDGE_PADDING_EMU) -> list[str]:
    """Fix a shape that extends beyond slide boundaries. Returns list of fixes applied."""
    bounds = _safe_shape_bounds(shape)
    if bounds is None:
        return []

    fixes = []
    left, top, width, height = bounds

    # Fix negative left
    if left < -padding:
        new_left = padding
        shape.left = new_left
        fixes.append(f"Moved left from {Emu(left).inches:.2f}in to {Emu(new_left).inches:.2f}in")

    # Fix negative top
    if top < -padding:
        new_top = padding
        shape.top = new_top
        fixes.append(f"Moved top from {Emu(top).inches:.2f}in to {Emu(new_top).inches:.2f}in")

    # Refresh bounds after position fix
    left, top = shape.left, shape.top
    right = left + width
    bottom = top + height

    # Fix right overflow: prefer shrinking width, then moving left
    if right > slide_w + padding:
        max_width = slide_w - left - padding
        if max_width > Inches(1):  # don't shrink below 1 inch
            shape.width = max_width
            fixes.append(f"Shrunk width to {Emu(max_width).inches:.2f}in to fit slide")
        else:
            new_left = padding
            shape.left = new_left
            max_width = slide_w - new_left - padding
            shape.width = max(Inches(1), max_width)
            fixes.append(f"Repositioned to left={Emu(new_left).inches:.2f}in, width={Emu(shape.width).inches:.2f}in")

    # Fix bottom overflow: prefer shrinking height, then moving up
    if top + shape.height > slide_h + padding:
        max_height = slide_h - top - padding
        if max_height > Inches(0.5):
            shape.height = max_height
            fixes.append(f"Shrunk height to {Emu(max_height).inches:.2f}in to fit slide")
        else:
            new_top = padding
            shape.top = new_top
            max_height = slide_h - new_top - padding
            shape.height = max(Inches(0.5), max_height)
            fixes.append(f"Repositioned to top={Emu(new_top).inches:.2f}in, height={Emu(shape.height).inches:.2f}in")

    return fixes


def fix_text_overflow(shape, slide_w: int, slide_h: int) -> list[str]:
    """Fix text overflow by enabling auto-size or shrinking font size."""
    if not shape.has_text_frame:
        return []

    tf = shape.text_frame
    text = tf.text.strip()
    if not text:
        return []

    bounds = _safe_shape_bounds(shape)
    if bounds is None:
        return []

    _, _, width, height = bounds
    est_height = _estimate_text_height_emu(tf, width)

    if est_height <= height * 1.05:
        return []  # No overflow

    fixes = []

    # Strategy 1: Enable auto-size (shrink text to fit)
    try:
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        fixes.append("Enabled 'Shrink text on overflow' auto-size")
    except Exception:
        pass

    # Strategy 2: If auto-size isn't enough, progressively shrink font sizes
    max_font = _get_max_font_size(tf)
    if max_font and max_font > MIN_FONT_SIZE_PT:
        overflow_ratio = est_height / height
        # Calculate target font size to fit
        target_font = max(MIN_FONT_SIZE_PT, max_font / overflow_ratio)
        scale_factor = target_font / max_font

        if scale_factor < 0.95:  # only shrink if meaningful
            for para in tf.paragraphs:
                for run in para.runs:
                    if run.font.size:
                        old_pt = run.font.size.pt
                        new_pt = max(MIN_FONT_SIZE_PT, round(old_pt * scale_factor))
                        run.font.size = Pt(new_pt)

            fixes.append(f"Scaled fonts by {scale_factor:.0%} (max {max_font:.0f}pt → {target_font:.0f}pt)")

    return fixes


def fix_table_overflow(shape, slide_w: int, slide_h: int, padding: int = EDGE_PADDING_EMU) -> list[str]:
    """Fix table overflow by shrinking to fit slide bounds."""
    if not shape.has_table:
        return []

    bounds = _safe_shape_bounds(shape)
    if bounds is None:
        return []

    fixes = []
    left, top, width, height = bounds

    # Shrink width to fit
    if left + width > slide_w + padding:
        new_width = slide_w - left - padding
        if new_width > Inches(2):
            shape.width = new_width
            fixes.append(f"Shrunk table width to {Emu(new_width).inches:.2f}in")
        else:
            shape.left = padding
            new_width = slide_w - 2 * padding
            shape.width = new_width
            fixes.append(f"Repositioned table and set width to {Emu(new_width).inches:.2f}in")

    # Shrink height to fit
    if top + shape.height > slide_h + padding:
        new_height = slide_h - top - padding
        if new_height > Inches(1):
            shape.height = new_height
            fixes.append(f"Shrunk table height to {Emu(new_height).inches:.2f}in")

    return fixes


def fix_presentation(prs_path: str, output_path: str, verbose: bool = False) -> PresentationReport:
    """Fix all overflow issues in a presentation and save."""
    prs = Presentation(prs_path)
    slide_w = prs.slide_width
    slide_h = prs.slide_height

    report = PresentationReport(
        filepath=prs_path,
        slide_width_emu=slide_w,
        slide_height_emu=slide_h,
    )

    for i, slide in enumerate(prs.slides, 1):
        # First check for issues
        slide_report = check_slide(slide, i, slide_w, slide_h, verbose=verbose)

        if not slide_report.issues:
            report.slides.append(slide_report)
            continue

        # Apply fixes
        for shape in slide.shapes:
            bounds = _safe_shape_bounds(shape)
            if bounds is None:
                continue

            name = _safe_shape_name(shape)
            left, top, width, height = bounds
            right = left + width
            bottom = top + height

            # Fix bounds issues
            if (left < -EDGE_PADDING_EMU or top < -EDGE_PADDING_EMU or
                    right > slide_w + EDGE_PADDING_EMU or bottom > slide_h + EDGE_PADDING_EMU):
                fixes = fix_shape_bounds(shape, slide_w, slide_h)
                for issue in slide_report.issues:
                    if issue.shape_name == name and issue.issue_type in ("bounds", "negative_pos"):
                        issue.fixed = True
                        issue.fix_detail = "; ".join(fixes)

            # Fix text overflow
            if _safe_has_text_frame(shape) and shape.text_frame.text.strip():
                fixes = fix_text_overflow(shape, slide_w, slide_h)
                if fixes:
                    for issue in slide_report.issues:
                        if issue.shape_name == name and issue.issue_type == "text_overflow":
                            issue.fixed = True
                            issue.fix_detail = "; ".join(fixes)

            # Fix table overflow
            if _safe_has_table(shape):
                fixes = fix_table_overflow(shape, slide_w, slide_h)
                if fixes:
                    for issue in slide_report.issues:
                        if issue.shape_name == name and issue.issue_type == "table_overflow":
                            issue.fixed = True
                            issue.fix_detail = "; ".join(fixes)

        report.slides.append(slide_report)

    prs.save(output_path)
    return report


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

SEVERITY_ICONS = {"error": "❌", "warning": "⚠️"}


def print_report(report: PresentationReport, verbose: bool = False) -> None:
    """Print a human-readable report."""
    w_in = Emu(report.slide_width_emu).inches
    h_in = Emu(report.slide_height_emu).inches
    print(f"📊 {report.filepath}")
    print(f"   Slide size: {w_in:.2f}in × {h_in:.2f}in")
    print()

    if report.total_issues == 0:
        print("   ✅ No overflow issues found!")
        return

    for sr in report.slides:
        if not sr.issues:
            continue

        print(f"   Slide {sr.slide_num} ({sr.layout_name}):")
        for issue in sr.issues:
            icon = SEVERITY_ICONS.get(issue.severity, "ℹ️")
            fix_marker = " → ✅ FIXED" if issue.fixed else ""
            print(f"     {icon} [{issue.issue_type}] {issue.shape_name}: {issue.detail}{fix_marker}")
            if issue.fixed and issue.fix_detail and verbose:
                print(f"        Fix: {issue.fix_detail}")
        print()

    # Summary
    errors = sum(1 for s in report.slides for i in s.issues if i.severity == "error")
    warnings = sum(1 for s in report.slides for i in s.issues if i.severity == "warning")
    fixed = report.total_fixed
    print(f"   Summary: {report.total_issues} issues ({errors} errors, {warnings} warnings)")
    if fixed:
        print(f"   Fixed: {fixed}/{report.total_issues}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check and fix overflow issues in PPTX presentations"
    )
    parser.add_argument("input", help="Path to PPTX file to check")
    parser.add_argument(
        "--fix", action="store_true",
        help="Auto-fix issues (saves to output file)"
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output path for fixed PPTX (default: input-fixed.pptx)"
    )
    parser.add_argument(
        "--check", action="store_true", default=True,
        help="Check only, report issues (default)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed fix information"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input

    if not Path(input_path).exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    if args.fix:
        output_path = args.output
        if not output_path:
            stem = Path(input_path).stem
            output_path = str(Path(input_path).with_name(f"{stem}-fixed.pptx"))

        print(f"🔧 Fixing overflows in: {input_path}")
        print(f"   Output: {output_path}")
        print()

        report = fix_presentation(input_path, output_path, verbose=args.verbose)
        print_report(report, verbose=args.verbose)

        if report.total_fixed > 0:
            print(f"\n   ✅ Saved fixed presentation: {output_path}")
        else:
            print(f"\n   ℹ️  No fixable issues found. Output saved unchanged: {output_path}")
    else:
        report = check_presentation(input_path, verbose=args.verbose)
        print_report(report, verbose=args.verbose)

        if report.total_issues > 0:
            print(f"\n   💡 Run with --fix to auto-fix these issues")
            sys.exit(1)


if __name__ == "__main__":
    main()

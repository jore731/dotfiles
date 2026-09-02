---
project-knowledge: basf-presentations
category: validation
---

# Layout Validation Guide

This guide explains the two-layer validation system for BASF Quarto presentations.
Use it to catch density problems **before presenting**, not during.

## The Problem

A 1920×1080 BASF slide has approximately **820 px of effective body area** after
accounting for top/bottom padding (80 px each) and the H2 heading with blue separator.
The runtime scaler (`basf-runtime-fixes.js`) catches overflow at presentation time by
shrinking the font — but this is a last resort.  Dense slides are better fixed at the
content stage.

The validation toolchain gives you two signals:

| Tool | Stage | Cost | Accuracy |
|---|---|---|---|
| `lint-slides.py` | Pre-render (authoring) | < 1 second, no browser | Heuristic (~±20%) |
| `?dev=1` overlay | Post-render (browser) | Per-slide, exact browser layout | Ground truth |

Use the linter for fast feedback during writing; use the browser overlay to confirm
before finalising.

---

## Layer 1 — Content Budget Linter (`lint-slides.py`)

### Overview

`scripts/lint-slides.py` parses a `.qmd` file, estimates each slide's pixel height
using a calibrated heuristic model, and reports which slides exceed the budget.

### Heuristic Model (BASF Dark Blue, 1920×1080)

| Element | Estimated height |
|---|---|
| H3 heading / `<h3>` | 60 px |
| H3 subtitle (first element after H2) | 70 px |
| Body paragraph line (~75 chars) | 52 px |
| List item | 52 px |
| Code block line (inside fence) | 22 px |
| Code block overhead | 32 px |
| Table header row | 50 px |
| Table data row | 44 px |
| Blockquote line | 55 px |
| `.footnote` block | 42 px |
| `{=html}` raw block | 200 px (fixed) |

Multi-column slides (`::: {.columns}`) take the **tallest column** — same as the browser.

### Usage

```bash
# Basic report
python3 lint-slides.py presentation.qmd

# Verbose: breakdown for every slide
python3 lint-slides.py presentation.qmd --verbose

# For pre-render hooks (always exits 0, render continues)
python3 lint-slides.py presentation.qmd --warn-only

# Custom canvas height (if you changed the BASF theme padding)
python3 lint-slides.py presentation.qmd --canvas 780
```

### Output

```
BASF Slide Budget Linter  ·  presentation.qmd  ·  budget 820px

✅ [ 4] Two Kinds of Code Quality Tools          360/ 820px   44%  |████████████░░░░░░░░░░░░░░░░|
⚠️  [ 8] The Baseline Stack                      740/ 820px   90%  |█████████████████████████░░░|
🔴 [16] beartype — The Runtime Type Defence     1050/ 820px  128%  |████████████████████████████|
...

Summary: 18 ✅ OK  ·  4 ⚠️  WARN  ·  3 🔴 OVER
```

Status levels:
- **✅ OK** — ≤ 85 % of budget — comfortable
- **⚠️ WARN** — 86–100 % — near the limit, likely fine but tight
- **🔴 OVER** — > 100 % — the runtime scaler will compensate; consider trimming

### Tuning

The heuristic model is calibrated for the BASF Dark Blue theme at 36 px root font.
If your theme uses a different root font size, scale `HEIGHTS` proportionally:

```python
# In lint-slides.py, top of file:
HEIGHTS = {
    "body_line": 52,   # ← multiply by (your_font_px / 36) to recalibrate
    ...
}
```

### Wire into Quarto pre-render

Copy `_quarto.yml` from `templates/quarto/` alongside your `presentation.qmd`:

```yaml
# _quarto.yml
project:
  type: default
  pre-render: python3 lint-slides.py --warn-only
```

Copy `lint-slides.py` from `scripts/` into the same folder (or adjust the path).
After this, every `quarto render presentation.qmd` automatically runs the linter.

---

## Layer 2 — Developer Overlay (`?dev=1`)

### Overview

The `basf-runtime-fixes.js` template includes a developer overlay mode.
When enabled, it shows a small badge on every content slide indicating
the runtime scaler's result:

- **✓ 100%** — content fit without scaling (faint green)
- **⚠ 84% | 30px** — scaled to 84 % of original font size (yellow)
- **⚠ 56% | 20px** — scaled to 56 % — very dense, consider trimming (red)

Colour coding:

| Badge colour | Meaning |
|---|---|
| Faint green | Fits at 100 % — no scaling applied |
| Green | Scaled, but ≥ 80 % of original — acceptable |
| Orange | Scaled to 60–79 % — dense, readable but tight |
| Red | Scaled to < 60 % — too dense, trim content |

### Usage

Open your presentation with `?dev=1` appended to the URL:

```
http://localhost:8765/presentation.html?dev=1
```

Navigate through all slides.  The badge updates on each `slidechanged` event.
When the URL has no `?dev=1`, the overlay is invisible — no change to the
production presentation.

### Badge position

The badge appears in the **top-right corner of each slide canvas** (not the
viewport), with `z-index: 100` so it stays above slide content.
It has `pointer-events: none` — it does not interfere with click navigation.

---

## Recommended Authoring Workflow

1. **Write content** in `presentation.qmd`
2. **Lint early** — run the linter after adding each section:
   ```bash
   python3 lint-slides.py presentation.qmd
   ```
3. **Render** when lint shows no 🔴 slides (or when you are ready to check visuals):
   ```bash
   quarto render presentation.qmd
   ```
4. **Check the overlay** — open `presentation.html?dev=1`, navigate all slides.
   Look for red badges (< 60 %).
5. **Trim dense slides** — for red-badge slides, reduce content in `.qmd`.
   Options:
   - Remove one H3 section
   - Shorten bullet items
   - Trim code block to key lines only
   - Move content to a second slide
6. **Re-render and verify** — repeat steps 3–5 until all badges are green or yellow.
7. **Present clean** — open `presentation.html` (no `?dev=1`).  No badges visible.

---

## Known Limitations

### Linter

- **`{=html}` blocks** are treated as a fixed 200 px estimate.  Actual height
  depends on the HTML content.  Use the `?dev=1` overlay for ground truth.
- **`{mermaid}` blocks** are treated as a fixed 380 px estimate (compact SVG
  flowchart).  Complex or tall diagrams may exceed this.
- **Column layouts detected**: `::: {.column}` / `:::: {.column}` (Pandoc),
  `:::: {.split-left}` / `:::: {.split-right}` (highlight-slide panels), and
  `<div class="column">` HTML passthrough.  Nested or `{=html}`-wrapped column
  HTML is not split — the block counts as 200 px.
- **`.footnote` blocks** contribute 42 px to the estimate even though Reveal.js
  renders them absolutely-positioned at the slide bottom.  If a slide is flagged
  OVER only by ~40 px, the footnote may be the cause; inspect with `?dev=1`.
- **Accuracy is ±20 %** — the heuristic cannot know actual browser line-wrap.
  A WARN slide is usually fine; a mild OVER may have the scaler reduce text only
  2–3 px.  The browser overlay gives the exact answer.

### Overlay

- Badges appear only on slides you **navigate to** — the scaler fires per-slide
  on `slidechanged`.  Navigate through all slides at least once to see all badges.
- The badge position is inside the slide canvas, so on `.closing-slide` and
  `.divider-slide` (which are excluded from scaling), no badge appears.

---

## Files Reference

| File | Location | Purpose |
|---|---|---|
| `lint-slides.py` | `scripts/lint-slides.py` | Content budget linter — copy to presentation folder |
| `basf-runtime-fixes.js` | `templates/quarto/basf-runtime-fixes.js` | Runtime fixes including scaler + dev overlay |
| `_quarto.yml` | `templates/quarto/_quarto.yml` | Pre-render hook wiring the linter |

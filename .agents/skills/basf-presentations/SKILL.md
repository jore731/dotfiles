---
name: basf-presentations
description: Create BASF-branded presentations with Quarto or native Reveal.js. Use when building BASF slides, translating PowerPoint layouts into Quarto or Reveal.js, or applying BASF slide patterns such as agenda dividers, impact slides, dashboard grids, comparison slides, image-text splits, multi-column canvases, and finale slides. This is the SINGLE authoritative skill for all BASF presentation work — do NOT use reveal-basf (deprecated, merged here).
metadata:
  version: "2.2.0"
  category: presentations
---

## Purpose

This skill provides BASF-branded presentation guidance for two delivery modes:

- Quarto + Reveal.js when Quarto is available
- Native Reveal.js + Vite when Node.js is available but Quarto is not

The Reveal.js path must follow the same visual system as the Quarto path. Do not improvise slide structure with ad-hoc placeholder classes or large inline-style blobs. The montage references under `references/` are the target layouts.

## Triage: Choose the Rendering Engine

Before starting, check the environment:

1. Check for Quarto: `quarto --version`
2. Check for Node.js: `node -v`

Decision rules:

- If Quarto is installed, use the Quarto `.qmd` pipeline.
- If Node.js is installed but Quarto is not, use the native Reveal.js starter created by `scripts/setup-revealjs.sh`.
- If neither is installed, recommend Node.js first. Do not recommend Quarto, Pandoc, or LaTeX unless the user explicitly wants heavyweight publishing features.

## Brand System

> **Note:** The `reveal-basf` skill is deprecated and fully merged into this skill.
> All official SCSS, scripts, logos, and references now live here.
> The `setup-revealjs.sh` script is self-contained — no external dependencies.

BASF presentation themes support six color variants. Each theme reuses the same structural SCSS classes so the layout guidance stays identical across colors.

| Theme      | Primary Accent | Hex       | Light Background | Hex       |
| ---------- | -------------- | --------- | ---------------- | --------- |
| Dark Blue  | `basf-blue`    | `#004A96` | `basf-light-bg`  | `#E0E9F2` |
| Light Blue | `basf-blue`    | `#21A0D2` | `basf-light-bg`  | `#EFF7FD` |
| Dark Green | `basf-blue`    | `#007A33` | `basf-light-bg`  | `#E6F2EB` |
| Orange     | `basf-blue`    | `#F37021` | `basf-light-bg`  | `#FEF4E5` |
| Red        | `basf-blue`    | `#E4002B` | `basf-light-bg`  | `#FCE5E8` |
| Soft Black | `basf-blue`    | `#212427` | `basf-light-bg`  | `#E9E9E9` |

## Quarto Workflow

Use Quarto when available.

1. Copy the desired SCSS theme from `templates/quarto/` into the presentation folder.
2. Ensure `logos/BASF_Logo.svg` is available relative to the presentation.
3. Start from `templates/quarto/presentation-template.qmd`.

Minimal front matter:

```yaml
---
title: "Presentation Title"
subtitle: "Subtitle"
author: "Author Name"
date: today
date-format: "DD.MM.YYYY"
format:
  revealjs:
    theme: [default, basf-design-darkblue.scss]
    css: basf-theme-switcher.css
    width: 1920
    height: 1080
    margin: 0.08
    transition: slide
    slide-number: c/t
    controls: true
    hash: true
    center: false
    navigation-mode: linear
    logo: logos/BASF_Logo.svg
    include-after-body:
      text: |
        <script src="basf-runtime-fixes.js"></script>
        <script src="basf-theme-switcher.js"></script>
---
```

> **Required:** `slide-number: c/t` must always be included in the YAML front matter. This shows the current slide number and total (e.g., "5 / 23"). Use `true` for just the number, or `c/t` for the "current / total" format.

> **Operational default:** Include `basf-runtime-fixes.js` to auto-fit dense highlight-slide tables and keep recurring layout fixes active at runtime. Include `basf-theme-switcher.css` and `basf-theme-switcher.js` when you want in-browser BASF color switching during review.

Render with:

```bash
quarto render presentation.qmd
```

To switch brand colors, replace `basf-design-darkblue.scss` with any of the other bundled themes.

Prefer Mermaid over plain fenced code blocks for process chains, decision flows, or staged framework stacks. Use monospaced code blocks only for literal code.

## Native Reveal.js Workflow

Use native Reveal.js only when Quarto is not the chosen pipeline. The Reveal.js starter must mirror the Quarto slide grammar.

1. Scaffold the project:

   ```bash
   ./scripts/setup-revealjs.sh /path/to/my-presentation
   cd /path/to/my-presentation
   ```

2. Select a color theme in `index.html`:

   ```html
   <link rel="stylesheet" href="theme/basf-design-orange.css" id="theme" />
   ```

3. Start the preview server:

   ```bash
   npm run dev
   ```

4. Edit `slides.md` using the same class-based layout patterns as Quarto.

Native Reveal rules:

- Use Reveal Markdown comments to assign slide classes: `<!-- .slide: class="content-slide" -->`
- Do not use `data-background-color` for BASF slide colors; the theme classes own the backgrounds.
- `data-background-image` and `data-background-video` are allowed for media-led divider and impact slides.
- In native Reveal.js markdown, use raw HTML wrappers such as `<div class="columns">`, `<div class="column">`, `<div class="content-box">`, `<div class="split-left">`, and `<div class="split-right">`. Do not use Pandoc-style fenced div syntax like `::: {.split-left}` in the native Reveal.js path.
- Prefer `.content-slide` plus HTML `.columns` and `.column` wrappers for 2-, 3-, and 4-column compositions.
- Prefer `.content-box-slide` plus one or more HTML `.content-box` regions for white canvas layouts.
- Prefer `.highlight-slide` with HTML `.split-left` and `.split-right` blocks for text plus image or text plus visual impact slides.
- Keep the first slide as the title slide and the last slide as the BASF finale.

## Montage-Driven Reveal.js Support

The target layouts are documented by these montage files:

- `references/layouts.png` for divider slides
- `references/layouts_2.png` for impact slides
- `references/layouts_3.png` for core content slides
- `references/layouts_4.png` for dense content, canvases, and finale patterns

Use the montage families below when composing Reveal.js slides.

| Montage Family    | Typical Examples                                                                                                  | Reveal.js Pattern                                                               |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Divider           | agenda, active agenda, numbered chapter list, image-led section break, profile divider, full-screen media divider | `divider-slide`, `highlight-slide`, or media slide with `data-background-image` |
| Impact            | hero statement, centered quote, quote plus portrait, text plus image emphasis                                     | `highlight-slide` or `content-slide` with HTML column wrappers                  |
| Content           | KPI cards, comparisons, table plus sidebar, chart plus narrative, image plus copy, map, process diagram           | `content-slide` or `content-box-slide` with HTML column wrappers                |
| Canvas and Finale | 1-, 2-, 3-, 4-panel white placeholders, end card                                                                  | `content-box-slide` plus repeated HTML `content-box`, then `closing-slide`      |

## Core Slide Classes

These are the first-class BASF slide classes shared by Quarto and native Reveal.js.

1. Title slide: automatic first slide, no special class required.
2. Divider slide: `divider-slide` for agendas, chapter breaks, and numbered section lists.
3. Content slide: `content-slide` for general content, comparisons, and dashboards.
4. Content box slide: `content-box-slide` for white canvases and structured content blocks.
5. Highlight slide: `highlight-slide` for left-copy and right-visual slides.
6. Closing slide: `closing-slide` for the BASF finale.

## Reveal.js Composition Patterns

### Agenda Divider

```markdown
<!-- .slide: class="divider-slide" -->

## Agenda

1. Introduction
2. **Current chapter**
3. Operations
4. Outlook
```

### Numbered Chapter Divider

```markdown
<!-- .slide: class="divider-slide" -->

## 1. Lorem ipsum dolor sit amet

1.1 First supporting point
1.2 Second supporting point
1.3 Third supporting point
```

### Text + Visual Impact Slide

```markdown
<!-- .slide: class="highlight-slide" -->

## Key Message

<div class="split-left">

### Why it matters

- Supporting point one
- Supporting point two
- Supporting point three
</div>

<div class="split-right">
![Plant photo](images/plant.jpg)
</div>
```

### 3-Column KPI Grid

```markdown
<!-- .slide: class="content-slide" -->

## KPI Overview

<div class="columns">
<div class="column" style="width: 33%;">

### Metric A

- Value
- Delta
</div>

<div class="column" style="width: 33%;">

### Metric B

- Value
- Delta
</div>

<div class="column" style="width: 33%;">

### Metric C

- Value
- Delta
</div>
</div>
```

### 4-Panel White Canvas

```markdown
<!-- .slide: class="content-box-slide" -->

## Working Session

<div class="canvas-grid columns-4">

<div class="content-box">
Panel 1
</div>

<div class="content-box">
Panel 2
</div>

<div class="content-box">
Panel 3
</div>

<div class="content-box">
Panel 4
</div>

</div>
```

### Finale

```markdown
<!-- .slide: class="closing-slide" -->

##
```

## Anti-Patterns

Avoid these in the native Reveal.js path:

- Placeholder classes such as `highlight-bar`, `highlight-main`, or `contact-info`
- Large inline-style layout scaffolds when a BASF class already exists
- `data-background-color` for standard BASF slide backgrounds
- Generic Reveal examples that do not match the montage families
- Using the deprecated `reveal-basf` skill instead of this one
- Inline `style="width: XX%"` on columns — use `.col-33`, `.col-50`, etc. utility classes
- Inline KPI card styling — use `.kpi-card`, `.kpi-value`, `.kpi-delta`, `.kpi-label`

Avoid these in Quarto QMD files:

- **`# Chapter` (H1) headings for dividers** — In Quarto with `slide-level: 2`, H1 headings create vertical sub-slide parent containers. Every `##` slide that follows becomes a vertical sub-slide under that H1 section, ballooning the total slide count (e.g. 33 content slides → 54 slides). **Always use `## Chapter {.divider-slide}` for ALL slide-level headings, including chapter breaks.** Never use H1 headers in Quarto Reveal.js QMD files.
- `### Heading` inside `::: {.split-left}`, `::: {.split-right}`, or `::: {.content-box}` fenced divs — use `<h3>Heading</h3>` instead. The same applies inside `::: {.column}` fenced divs.
- **Mermaid diagrams in Reveal.js presentations become invisible** when using the LR (left-to-right) flowchart layout because the Quarto `.cell` container is too narrow. The SVG auto-sizes with a very wide, short viewBox (e.g. 1932×149) which collapses to near-zero height. **Fix: replace Mermaid blocks with `{=html}` raw HTML flexbox/grid diagrams that are fully controllable and won't collapse.** The `%%| fig-height` chunk option has no effect for browser-rendered Mermaid in Reveal.js.
- **Nested `<div>` HTML inside Markdown blocks gets escaped** by Pandoc — inner `<div>` tags render as literal text. When your visual requires multiple nested HTML elements (pipeline diagrams, KPI grids), always wrap the entire HTML block in a `{=html}` fenced code block so Pandoc passes it through verbatim without markdown processing.
- `<h3>1. Something</h3>` numbered text in raw HTML headings — Pandoc parses `1.` as an ordered list
- Relying on `justify-content: flex-start` for divider slides with only H2 + P (pattern P16 auto-centers these)
- **Missing `.content-slide` class** on content slides causes content to render at the bottom of the viewport (with large blank space above). Always apply a slide class (`{.content-slide}`, `{.highlight-slide}`, etc.) to every slide — never leave a `##` heading without a class in BASF presentations.

## Runtime Auto-Scaler

The `basf-runtime-fixes.js` file includes a `fitCurrentSlideFont()` function that automatically reduces the font-size of any content slide whose content overflows the 1080px canvas height.

**How it works:**

1. On `slidechanged` and `ready` events, the function targets the `.present` slide.
2. It uses `element.style.setProperty('overflow', 'visible', 'important')` and `height: auto !important` to temporarily lift Reveal.js's clipping constraints so `scrollHeight` returns the true content height.
3. If content height exceeds the canvas, it calculates a proportional font-size reduction and applies it in two passes (the second pass corrects for layout changes caused by the first).
4. The original font-size is stored in `data-basf-orig-font-px` on the slide element so it can be reset on revisit.
5. The minimum font-size floor is 18px. Divider, title, and closing slides are excluded.

**Key constraints:**

- The scaler operates on the **current slide only** — each slide is scaled when navigated to.
- Font-size reduction cascades through `em`-based child elements (code blocks use `0.55em`, so they scale proportionally).
- `max-height: 500px` on code blocks is in `px` and does NOT scale — excessively tall code blocks should be trimmed in the QMD content.
- The `setProperty` with `'important'` approach is required because the BASF theme uses `height: 100% !important` and `overflow: hidden !important` via `%slide-base`.
- This approach causes NO visual flicker because JS layout reads and the subsequent font-size write happen within a single browser frame.

**Adding to a new presentation:**
Include `basf-runtime-fixes.js` in the Quarto front matter:

```yaml
include-after-body:
  text: |
    <script src="basf-runtime-fixes.js"></script>
```

## Layout Validation

> Full reference: `docs/layout-validation.md`

Two tools catch density problems early:

| Tool                     | Stage                     | How                                 |
| ------------------------ | ------------------------- | ----------------------------------- |
| `scripts/lint-slides.py` | Pre-render authoring loop | Static heuristic, < 1 s, no browser |
| `?dev=1` URL overlay     | Post-render visual check  | Ground-truth browser badges         |

### Content Budget Linter

Copy `scripts/lint-slides.py` alongside your `presentation.qmd`. Run it after
writing each section:

```bash
python3 lint-slides.py presentation.qmd
```

Output flags each slide as ✅ OK / ⚠️ WARN / 🔴 OVER against an 820 px body budget
(calibrated for BASF Dark Blue 1920×1080, 36 px root font).

Wire it to fire automatically on every `quarto render` by copying
`templates/quarto/_quarto.yml` alongside the presentation:

```yaml
# _quarto.yml
project:
  type: default
  pre-render: python3 lint-slides.py --warn-only
```

`--warn-only` keeps exit code 0 so the render always proceeds. Remove it to block
renders on over-budget slides.

### Developer Overlay

`basf-runtime-fixes.js` (both the template and the runtime) supports a `?dev=1` URL
mode. Open the rendered HTML with `?dev=1` appended to see per-slide badges:

- **✓ 100%** (faint green) — fits without scaling
- **⚠ 84% | 30px** (green) — scaled, still comfortable
- **⚠ 62% | 22px** (orange) — dense, readable but tight
- **⚠ 54% | 19px** (red) — too dense, trim content

No `?dev=1` = no badges, clean for presenting.

### Recommended Workflow

1. Write content → `python3 lint-slides.py presentation.qmd`
2. Fix any 🔴 slides → render → open `?dev=1` → fix red badges → re-render
3. Present with clean URL (no `?dev=1`)

## PPTX-to-Reveal.js Conversion Workflow

The skill includes a Python generator that converts extracted PPTX data into a complete Reveal.js presentation.

### Prerequisites

1. A PPTX source file extracted with `scripts/extract-pptx-reference.py` to produce `summary.json`
2. Python 3.10+ (uses only stdlib: `json`, `csv`, `re`, `shutil`, `html`, `pathlib`)

### Workflow

```bash
# Step 1: Extract PPTX data (shapes, text, images, layouts)
python3 scripts/extract-pptx-reference.py source.pptx pptx-extract/

# Step 2: Scaffold a Reveal.js project
./scripts/setup-revealjs.sh my-presentation/

# Step 3: Generate slides from extracted data
python3 scripts/generate-revealjs.py pptx-extract/ my-presentation/

# Step 4: Preview
cd my-presentation && npm run dev
```

### Generator Capabilities (`generate-revealjs.py`)

The generator reads `summary.json` and produces `slides.md` + copies image assets. It handles:

- **Layout detection**: Maps PPTX layout names to BASF CSS classes (`title-slide`, `divider-slide`, `content-slide`, `closing-slide`)
- **Multi-column content**: Automatically arranges content into 1–4 column layouts based on PPTX structure
- **Tables**: Renders HTML `<table>` from extracted PPTX table data
- **Charts**: Generates Chart.js `<canvas>` elements with `data-chart-config` JSON attributes
- **KPI cards**: Creates `.kpi-card` / `.kpi-value` / `.kpi-delta` / `.kpi-label` markup
- **Images**: Copies and links extracted images with proper alt text
- **Text cleanup**: Strips `\x0b` vertical tabs, normalizes whitespace, escapes HTML entities
- **Title extraction**: Prioritizes shapes named `Titel*` before falling back to other placeholders

### Skipped Layouts

The generator skips these PPTX layouts by default (dark backgrounds that need special handling):

- `Title dark` — full-bleed dark blue dividers
- `Title white` — minimalist white dividers

These slides can be added manually in `slides.md` after generation.

## VS Code Preview

### Live Preview with Vite

The recommended way to preview presentations during development:

1. Open the project folder in VS Code
2. Open the integrated terminal and run:

   ```bash
   npm run dev
   ```

3. Open `http://localhost:5173` in a browser (Vite's default port)
4. Edits to `slides.md` and SCSS files trigger hot reload automatically

### Useful VS Code Extensions

- **Live Preview** (ms-vscode.live-server) — built-in browser preview
- **Reveal.js** (evilz.vscode-reveal) — slide editing support with preview panel
- **SCSS IntelliSense** — autocomplete for SCSS variables and mixins

### Keyboard Shortcuts in Reveal.js

| Key         | Action                  |
| ----------- | ----------------------- |
| `S`         | Open speaker notes view |
| `O` / `Esc` | Slide overview          |
| `F`         | Fullscreen              |
| `B` / `.`   | Blackout slide          |
| `?`         | Show keyboard shortcuts |

## Build for Production

### Static Build with Vite

```bash
npm run build
```

This produces a `dist/` folder with all assets optimized and bundled. The build:

- Compiles SCSS to CSS (via `prebuild` hook)
- Bundles Reveal.js and plugins
- Copies `slides.md`, images, and logos
- Minifies JS/CSS for production

### Vite Configuration

For Reveal.js Markdown-based slides, add a `vite.config.js` to ensure `slides.md` and assets are included:

```javascript
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    rollupOptions: {
      input: "index.html",
    },
  },
  assetsInclude: ["**/*.md"],
});
```

### Deploy the Build

The `dist/` folder is a fully self-contained static site. Deploy to:

- **GitHub Pages**: Push `dist/` to a `gh-pages` branch
- **Azure Static Web Apps**: Upload `dist/`
- **Any web server**: Copy `dist/` contents to the document root
- **Offline sharing**: Zip the `dist/` folder — recipients only need a browser

## PDF Export

### Method 1: Browser Print (Recommended)

1. Open the presentation with `?print-pdf` in the URL:

   ```
   http://localhost:5173/?print-pdf
   ```

2. Open the browser print dialog (`Ctrl+P` / `Cmd+P`)
3. Set **Destination** to "Save as PDF"
4. Set **Layout** to "Landscape"
5. Set **Margins** to "None"
6. Enable **Background graphics**
7. Click **Save**

> **Note:** This method requires Google Chrome or Chromium.

### Method 2: Decktape (Command Line)

[Decktape](https://github.com/astefanutti/decktape) provides automated PDF export:

```bash
npx decktape reveal http://localhost:5173 output.pdf --size 1920x1080
```

### Speaker Notes in PDF

To include speaker notes in the PDF export, add to `Reveal.initialize()`:

```javascript
showNotes: true; // overlay on slide
// or
showNotes: "separate-page"; // notes on their own page after each slide
```

### Fragment Handling

By default, each fragment step creates a separate PDF page. To collapse fragments:

````javascript
pdfSeparateFragments: false

  version: "2.1.0"

To share a presentation as a single portable package:

1. Build for production: `npm run build`
2. Zip the `dist/` folder
3. Recipients unzip and open `index.html` in any browser

For Chart.js presentations, the CDN script must be replaced with a local copy:

```html
<!-- Replace CDN with local -->
<script src="chart.umd.min.js"></script>
````

Download from: `https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js`

## Design System Architecture

The SCSS follows a 5-layer token architecture:

```
Import order:
  1. _basf-design-darkblue-official.scss  — Layer 1+2: primitive & semantic tokens, slide classes, mixins
  2. _basf-reveal-quarto-compat.scss      — Reveal.js/Quarto base compatibility styles
  3. _basf-utilities.scss                 — Layer 3: reusable component/utility classes
  4. _basf-core-patterns.scss             — Layer 4: 18 layout patterns, overflow guards, image constraints
  5. _basf-design-darkblue-native-overrides.scss — Cascade fixes for native Reveal.js
```

### Design Tokens (Fixed Values)

These tokens were calibrated against the official BASF PowerPoint template at 1920×1080:

```scss
// Primitive tokens (brand values)
$basf-blue: #004a96;
$basf-light-bg: #e0e9f2;
$basf-gray: #8c8c8c;
$basf-dark-gray: #3d3d3d;

// Semantic tokens (layout spacing — calibrated to PPTX measurements)
$slide-pad-v: 80px; // vertical slide padding (PPTX: ~81px)
$slide-pad-h: 80px; // horizontal slide padding (PPTX: ~81px)
$heading-size-title: 3.6em; // title slide h1
$heading-size-divider: 2.4em; // divider slide h2
$heading-size-default: 2.4em; // all other slide h2 (PPTX: 44pt ÷ 36px = 2.44em)
$body-font-size: 1em; // standard body text (PPTX: 18pt ÷ 36px = 1.0em)
$body-font-size-sm: 0.85em; // compact text (PPTX: 15pt ÷ 36px ≈ 0.83em)
$separator-width: 3em; // blue line below headings
```

### Utility Classes (`_basf-utilities.scss`)

These named classes replace inline styles in `slides.md`:

| Class                    | Purpose                                     | Replaces                                                  |
| ------------------------ | ------------------------------------------- | --------------------------------------------------------- |
| `.col-20` … `.col-75`    | Column widths                               | `style="width: XX%"`                                      |
| `.img-placeholder`       | Blue gradient placeholder                   | `style="background: linear-gradient(…)"`                  |
| `.img-placeholder--dark` | Dark variant                                | `style="background: linear-gradient(…rgba(255,…))"`       |
| `.kpi-card`              | White rounded card for KPI metrics          | `style="background:#fff; border-radius:10px; padding:…"`  |
| `.kpi-value`             | Large blue number                           | `style="font-size:2.4em; font-weight:700; color:#004A96"` |
| `.kpi-delta`             | Delta indicator (`.positive` / `.negative`) | `style="color:#007A33"` etc.                              |
| `.kpi-label`             | Muted uppercase label                       | `style="font-size:0.75em; color:#8C8C8C"`                 |
| `.col-divider`           | Vertical column separator                   | `style="border-right:2px solid …"`                        |
| `.timeline-entry`        | Timeline item with dot                      | `style="border-left:3px solid …"`                         |
| `.template-placeholder`  | Dashed empty placeholder                    | `style="border:2px dashed …"`                             |
| `.hero-heading`          | 5rem oversized heading                      | `style="font-size:5rem"`                                  |
| `.centered-content`      | Full-slide centered flex                    | `style="display:flex; align-items:center; …"`             |
| `.footnote`              | Small gray footer text                      | `style="font-size:0.6em; color:#8C8C8C"`                  |
| `.text-small`            | 0.75em text                                 | inline font-size                                          |
| `.text-muted`            | Gray text                                   | inline color                                              |
| `.flex-fill`             | Stretch to fill space                       | `style="flex:1 1 auto"`                                   |

### Usage Examples with Utility Classes

**KPI Dashboard (no inline styles):**

```markdown
<!-- .slide: class="content-slide" -->

## KPI Overview

<div class="columns">
<div class="column col-33">
<div class="kpi-card">
<span class="kpi-value">€2.4B</span>
<span class="kpi-delta positive">+12%</span>
<span class="kpi-label">Revenue</span>
</div>
</div>

<div class="column col-33">
<div class="kpi-card">
<span class="kpi-value">18.5%</span>
<span class="kpi-delta negative">-2.1pp</span>
<span class="kpi-label">EBIT Margin</span>
</div>
</div>

<div class="column col-33">
<div class="kpi-card">
<span class="kpi-value">4,200</span>
<span class="kpi-delta neutral">±0</span>
<span class="kpi-label">Headcount</span>
</div>
</div>
</div>
```

**Image placeholder (no inline styles):**

```markdown
<div class="img-placeholder">Chart placeholder</div>
```

**Timeline slide:**

```markdown
<!-- .slide: class="content-slide" -->

## Roadmap

<div class="timeline-entry">
<strong>Q1 2026</strong>
<p>Launch pilot program</p>
</div>

<div class="timeline-entry">
<strong>Q2 2026</strong>
<p>Scale to 5 markets</p>
</div>
```

## Export Formats

The BASF presentation pipeline supports three output formats from a single source:

| Format   | Engine               | Editable | CSS Fidelity | Best For                                |
| -------- | -------------------- | -------- | ------------ | --------------------------------------- |
| **HTML** | Quarto / Vite        | No       | 100%         | Live presenting, web sharing            |
| **PDF**  | Decktape             | No       | ~98%         | Printing, email sharing, archival       |
| **PPTX** | Pandoc / python-pptx | Yes      | ~80%         | Corporate editing, offline distribution |

### Which Export Method to Use

| Scenario                | Method                                                 |
| ----------------------- | ------------------------------------------------------ |
| Quarto `.qmd` → PPTX    | `quarto render --to pptx` (uses `basf-reference.pptx`) |
| Quarto `.qmd` → PDF     | Render to HTML first, then Decktape                    |
| Native Reveal.js → PDF  | Decktape from live server or built HTML                |
| Native Reveal.js → PPTX | `export-pptx.py` from `slides.md`                      |

### PDF Export (Decktape)

The `export-pdf.sh` script wraps Decktape for pixel-perfect PDF capture:

```bash
# From Quarto HTML output
./scripts/export-pdf.sh presentation.html output.pdf

# From live Reveal.js dev server
./scripts/export-pdf.sh http://localhost:5173 slides.pdf --size 1920x1080

# Skip fragment steps, export only slides 1-10
./scripts/export-pdf.sh presentation.html output.pdf --no-fragments --slides 1-10
```

Prerequisites: `npm install decktape` (local or global).

### PPTX Export (Quarto Path)

Add `pptx` format to the QMD frontmatter:

```yaml
format:
  revealjs:
    theme: [default, basf-design-darkblue.scss]
    # ... existing config ...
  pptx:
    reference-doc: basf-reference.pptx
    slide-level: 2
```

Then render: `quarto render presentation.qmd --to pptx`

The `basf-reference.pptx` template applies BASF layouts, Arial fonts, and the corporate color palette. Generate it with:

```bash
python3 scripts/create-basf-reference-pptx.py
```

### PPTX Export (Native Reveal.js Path)

For presentations built without Quarto, use the `export-pptx.py` script:

```bash
python3 scripts/export-pptx.py slides.md --template basf-reference.pptx -o output.pptx
```

This reads the Reveal.js markdown and generates editable PPTX using `python-pptx`. Slide class mapping:

| Reveal.js Class     | PPTX Layout       |
| ------------------- | ----------------- |
| `title-slide`       | Title Slide       |
| `divider-slide`     | Section Header    |
| `content-slide`     | Title and Content |
| `highlight-slide`   | Two Content       |
| `content-box-slide` | Blank             |
| `closing-slide`     | Blank             |

**Known limitations** (graceful fallback):

- Complex CSS layouts (KPI grids, canvas grids) → simplified single-column with comment
- Mermaid diagrams / Chart.js → placeholder text
- Custom HTML structures → bullet-list approximation

### Multi-Format Build (Makefile)

Copy `templates/Makefile` into your presentation folder:

```bash
make all QMD=presentation.qmd   # HTML + PPTX + PDF
make html                        # Reveal.js only
make pptx                        # PowerPoint only
make pdf                         # PDF via Decktape
make pptx-native                 # PPTX from native slides.md
make pdf-native                  # PDF from running dev server
```

### Troubleshooting Export

| Issue                              | Fix                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------- |
| PPTX has wrong layouts             | Ensure `basf-reference.pptx` was generated with `create-basf-reference-pptx.py` |
| PPTX fonts not Arial               | Install Arial on build system: `sudo apt install ttf-mscorefonts-installer`     |
| PDF missing slides                 | Increase `--pause` (default 1000ms): `--pause 2000`                             |
| PDF has extra pages from fragments | Use `--no-fragments` flag                                                       |
| Images missing in PPTX             | Use `--images-dir` to point to the correct assets folder                        |
| `decktape` not found               | Install: `npm install -g decktape`                                              |

## Quality Checks

The `check-pptx-overflow.py` script detects and auto-fixes overflow issues in PPTX presentations — text boxes overflowing their bounds, shapes positioned off-screen, tables exceeding slide edges.

### Usage

```bash
# Check for issues (exit code 1 if any found)
python3 scripts/check-pptx-overflow.py presentation.pptx

# Verbose mode — includes shapes with no bounds (layout placeholders)
python3 scripts/check-pptx-overflow.py presentation.pptx --verbose

# Auto-fix — saves corrected file
python3 scripts/check-pptx-overflow.py presentation.pptx --fix -v

# Custom output path
python3 scripts/check-pptx-overflow.py presentation.pptx --fix -o corrected.pptx
```

### Makefile Integration

```bash
make check          # Check PPTX for overflow issues
make check-fix      # Auto-fix and save as presentation-fixed.pptx
```

### What It Detects

| Issue Type       | Description                                          | Severity      |
| ---------------- | ---------------------------------------------------- | ------------- |
| `negative_pos`   | Shape positioned off-screen (negative left/top)      | Error         |
| `bounds`         | Shape extends beyond slide right/bottom edge         | Error         |
| `text_overflow`  | Text content exceeds text box height (>5% tolerance) | Warning/Error |
| `table_overflow` | Table exceeds slide boundaries                       | Error         |

### Fix Strategies

| Issue              | Auto-Fix                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------- |
| Off-screen shapes  | Clamped to slide edge with 0.1in padding                                                      |
| Overflowing shapes | Width/height shrunk to fit, or repositioned                                                   |
| Text overflow      | Enables "Shrink text on overflow" auto-size; scales fonts proportionally if needed (min 10pt) |
| Table overflow     | Shrinks width/height to fit slide bounds                                                      |

### Baseline: BASF Template

The official 69-slide BASF template has **173 known overflow issues** — mostly decorative off-canvas groups and slide-number placeholder boxes too small for their content. These are **by design** and should not be fixed. Run the checker on your _exported_ presentations, not the raw template.

## Resources

- `templates/quarto/_basf-design-darkblue-official.scss` — the canonical BASF SCSS with tokens, mixins, and all 6 slide classes
- `templates/quarto/_basf-reveal-quarto-compat.scss` — Reveal.js/Quarto base compatibility
- `templates/quarto/_basf-utilities.scss` — reusable utility classes (column widths, KPI cards, placeholders, etc.)
- `templates/quarto/_basf-core-patterns.scss` — 18 layout patterns with overflow guards (see below)
- `templates/quarto/_basf-design-darkblue-native-overrides.scss` — cascade fixes for native Reveal.js
- `templates/quarto/basf-design-*.scss` — all 6 color theme entry points
- `templates/quarto/basf-runtime-fixes.js` — runtime overflow fixes for dense highlight-slide tables
- `templates/quarto/basf-theme-switcher.css` — theme-aware color overrides for menu, logo banner, and runtime theming
- `templates/quarto/basf-theme-switcher.js` — in-browser BASF theme switcher widget
- `templates/quarto/presentation-template.qmd` for the canonical BASF structure
- `templates/revealjs/slides.md` for the native Reveal.js starter
- `templates/revealjs/index.html` for the Vite-based Reveal.js wrapper
- `templates/revealjs/package.json` — Vite + Reveal.js 5.0.0 + Sass
- `templates/logos/BASF_Logo.svg` for the BASF logo
- `references/branding-guide.md` — brand colors, typography, tokens
- `references/color-book.md` — all 6 color theme specifications
- `references/layouts.md` for the layout taxonomy
- `references/layouts.png`, `references/layouts_2.png`, `references/layouts_3.png`, `references/layouts_4.png` for the visual targets
- `references/Updated PowerPoint Template_lg_March2025.pptx` — the source PPTX template
- `scripts/setup-revealjs.sh` — self-contained scaffold for native Reveal.js projects
- `scripts/generate-revealjs.py` — PPTX→Reveal.js slide generator (reads summary.json, produces slides.md)
- `scripts/extract-pptx-reference.py` — PPTX analysis tool for extracting layout data
- `scripts/apply-css-fixes.py` — applies proven CSS fixes to the official SCSS

## Core Layout Patterns (`_basf-core-patterns.scss`)

The core patterns library was derived from analysis of 62 PPTX slides. Each pattern maps a specific DOM structure to layout rules that guarantee zero-overflow rendering at 1920×1080.

### Pattern Catalog

| Tier      | ID  | Pattern                        | Frequency | Description                                                      |
| --------- | --- | ------------------------------ | --------- | ---------------------------------------------------------------- |
| Primary   | P01 | H2 → `.columns`                | 22×       | Multi-column bullets, tables, charts                             |
| Primary   | P02 | H2 → OL/UL                     | 5×        | Agenda / divider list                                            |
| Primary   | P03 | H2 → IMG                       | 4×        | Hero image divider                                               |
| Primary   | P04 | H2 → KPI grid                  | 4×        | Dashboard metrics                                                |
| Primary   | P05 | H1 → H3                        | 3×        | Title card                                                       |
| Secondary | P06 | H1 → IMG → P                   | 2×        | Title + hero photo                                               |
| Secondary | P07 | H2 → P → IMG                   | 3×        | Divider + subtitle + image                                       |
| Secondary | P08 | H2 → chart+table cols          | 3×        | Data dashboard                                                   |
| Secondary | P09 | H2 → `.image-grid` → UL        | 1×        | Gallery + legend                                                 |
| Secondary | P10 | H2 → P                         | 2×        | Statement divider                                                |
| Niche     | P11 | H1 → P                         | 1×        | Chapter title with date                                          |
| Niche     | P12 | H2 → PLACEHOLDER               | 1×        | Template / workshop                                              |
| Niche     | P13 | H2 → UL                        | 2×        | Simple full-width list                                           |
| Niche     | P14 | H2 → 4-col images              | 1×        | Photo strip                                                      |
| Niche     | P15 | H2 (closing)                   | 1×        | Closing slide, hidden                                            |
| Fix       | P16 | Sparse divider centering       | 7×        | Centers H2+P dividers without lists                              |
| Fix       | P17 | Content growth                 | 2×        | Table growth constrained; code blocks keep natural height        |
| Fix       | P18 | Quarto vertical-slide fallback | 4×        | Suppresses sub-slide behavior for `section` inside layout slides |

### Key Features

- **Flex-based containment**: All patterns use `display: flex; flex-direction: column` to contain content within the slide area
- **Per-context image constraints**: Images are sized differently in columns (100%), .image-grid (350px), and standalone (70vh)
- **Cross-pattern overflow guards**: `overflow: hidden` on sections, `min-height: 0` on flex children
- **Dense content scaling**: Patterns P08 and P01 apply `font-size: 0.92em` for data-heavy slides
- **Responsive column gaps**: `gap: 2em` for standard columns, `gap: 1.5em` for dense dashboards
- **Sparse divider centering** (P16): Dividers with only H2 + P auto-center vertically via `:not(:has(ol)):not(:has(ul))`
- **Content growth** (P17): Tables and code blocks grow to fill slide space via `flex: 1`
- **Quarto vertical-slide fallback** (P18): Nested `<section>` elements inside layout slides are forced visible and laid out as block elements

## Quarto QMD Authoring Guidelines

When creating presentations with Quarto (`.qmd` files), these rules prevent Reveal.js layout breakage:

### H1 Headers Create Vertical Sub-Slide Stacks — NEVER Use Them

**Critical Rule:** With Quarto's default `slide-level: 2`, a `# Chapter` (H1) heading creates a vertical slide parent section. Every `## Slide` that follows (until the next H1) becomes a _vertical sub-slide_, not a horizontal slide. This silently balloons slide counts and breaks linear navigation.

**Fix:** Use `## Chapter Title {.divider-slide}` for ALL slide-level headings — both chapter breaks and content slides. Do not use H1 headers anywhere in a Quarto Reveal.js QMD.

✅ **Correct — H2 for everything:**

```markdown
## Introduction {.divider-slide}

## The Code Quality Challenge {.content-slide}

Content...

## Two Kinds of Tools {.highlight-slide}

Content...
```

❌ **Broken — H1 creates vertical sub-slide stacks:**

```markdown
# Introduction

## The Code Quality Challenge {.content-slide}

Content... ← This becomes a vertical sub-slide of "Introduction"!

## Two Kinds of Tools {.highlight-slide}

Content... ← Also a vertical sub-slide — horizontal navigation broken!
```

**Symptom:** If slide count is 50% higher than expected (e.g., 54 instead of 33), look for `# Heading` H1 headers — each one created a vertical stack.

### Headings Inside Fenced Divs

**Critical Rule:** Never use `###` Markdown headings inside `::: {.split-left}`, `::: {.split-right}`, or `::: {.content-box}` fenced divs. Quarto promotes `###` headings to `<section>` elements, which Reveal.js treats as vertical sub-slides — breaking the parent layout.

✅ **Correct — raw HTML heading:**

```markdown
## Slide Title {.highlight-slide}

::: {.split-left}

<h3>Definition</h3>

Content here...
:::

::: {.split-right}
![Image](image.png)
:::
```

❌ **Broken — Markdown heading creates sub-slide:**

```markdown
## Slide Title {.highlight-slide}

::: {.split-left}

### Definition

Content here...
:::
```

### Numbered Text in Raw HTML Headings

**Critical Rule:** Never start `<h3>` content with a number followed by a period (e.g., `<h3>1. First Step</h3>`). Pandoc interprets `1.` as an ordered list start, which corrupts the fenced div closure — the closing `:::` renders as literal `<p>:::</p>` instead of ending the div.

✅ **Correct — no numbered prefix:**

```markdown
::: {.content-box}

<h3>Start with Cynefin</h3>

Content...
:::
```

❌ **Broken — Pandoc reads "1." as ordered list:**

```markdown
::: {.content-box}

<h3>1. Start with Cynefin</h3>

Content...
:::
```

### Defensive CSS

The SCSS includes fallback rules (P18) that suppress Reveal.js vertical-slide behavior for `<section>` elements inside `highlight-slide` and `content-box-slide`. These are a safety net — always prefer the `<h3>` approach above for reliable rendering.

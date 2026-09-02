## BASF Reveal.js Layout Taxonomy

This reference maps the BASF montage images to the Reveal.js structures that the
skill should generate.

The montages are the visual source of truth:

- `layouts.png`: divider-slide family
- `layouts_2.png`: impact-slide family
- `layouts_3.png`: core content-slide family
- `layouts_4.png`: dense content, canvas, and finale family

## Class-Based Foundation

These classes are the shared BASF presentation grammar across Quarto and native
Reveal.js.

| Class               | Use                                                         |
| ------------------- | ----------------------------------------------------------- |
| `divider-slide`     | agenda, chapter divider, numbered section divider           |
| `content-slide`     | standard content, dashboards, comparisons, text plus image  |
| `content-box-slide` | white canvas layouts, tables, placeholders, workshop frames |
| `highlight-slide`   | impact layouts with left copy and right visual              |
| `closing-slide`     | finale slide                                                |

## 1. Divider Family

Reference: `layouts.png`

Typical divider variants visible in the montage:

- agenda with active item highlight
- agenda with supporting table or structured content
- large numbered chapter slide
- image-led section break
- profile divider with text block and portrait
- full-screen image or video divider

Recommended Reveal.js patterns:

- Use `divider-slide` for list-first chapter slides.
- Use `highlight-slide` when the divider is text plus image.
- Use `data-background-image` or `data-background-video` for full-screen media dividers.

Example:

```markdown
<!-- .slide: class="divider-slide" -->

## Agenda

1. Introduction
2. **Current section**
3. Results
4. Summary
```

## 2. Impact Family

Reference: `layouts_2.png`

Typical impact variants visible in the montage:

- full-image hero with headline
- centered quote over image
- quote with portrait or circular image accent
- left copy plus right portrait
- left quote plus right portrait

Recommended Reveal.js patterns:

- Use `highlight-slide` for the dominant text plus image split.
- Use `content-slide` with HTML column wrappers for quote and portrait compositions.
- Use `data-background-image` when the image fills the whole slide.

Example:

```markdown
<!-- .slide: class="highlight-slide" -->

## Lorem ipsum dolor sit amet

<div class="split-left">

### Key message

- Point one
- Point two
- Point three
</div>

<div class="split-right">
![Portrait](images/portrait.jpg)
</div>
```

## 3. Content Family

Reference: `layouts_3.png`

Typical content variants visible in the montage:

- KPI card grids with 2x3 or 3x2 structure
- side-by-side white cards
- text plus table or chart
- diagram plus explanatory copy
- list plus sidebar image
- image plus text split
- maps and process diagrams
- dense table slides

Recommended Reveal.js patterns:

- Use `content-slide` for most content layouts.
- In native Reveal.js markdown, use HTML `.columns` and `.column` wrappers with width styles such as `50%`, `33%`, or `25%` for 2-, 3-, and 4-column arrangements.
- Use `content-box-slide` when the white regions are the primary visual containers.

Example 3-column grid:

```markdown
<!-- .slide: class="content-slide" -->

## KPI Overview

<div class="columns">
<div class="column" style="width: 33%;">

### Topic A

- Point A1
- Point A2
</div>

<div class="column" style="width: 33%;">

### Topic B

- Point B1
- Point B2
</div>

<div class="column" style="width: 33%;">

### Topic C

- Point C1
- Point C2
</div>
</div>
```

## 4. Canvas and Finale Family

Reference: `layouts_4.png`

Typical variants visible in the montage:

- one large white canvas
- two equal white canvases
- three white canvases
- four white canvases
- BASF finale card

Recommended Reveal.js patterns:

- Use `content-box-slide` with repeated HTML `.content-box` regions for white canvases.
- Use `.closing-slide` for the finale.

Example 2-panel canvas:

```markdown
<!-- .slide: class="content-box-slide" -->

## Working Areas

<div class="canvas-grid columns-2">

<div class="content-box">
Left canvas
</div>

<div class="content-box">
Right canvas
</div>

</div>
```

Example finale:

```markdown
<!-- .slide: class="closing-slide" -->

##
```

## Implementation Notes

- Do not use `data-background-color` for BASF regular slide backgrounds.
- `data-background-image` and `data-background-video` are valid only for media-led divider and impact layouts.
- Native Reveal.js markdown does not parse Pandoc-style fenced div syntax such as `:::`. Use HTML wrappers for BASF layout regions in the native path.
- The native Reveal.js starter should demonstrate montage-derived layouts, not generic Reveal.js defaults.

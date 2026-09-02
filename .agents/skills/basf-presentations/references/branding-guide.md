# BASF Brand Colors & Design Tokens for Presentations

Source: Official BASF Quarto Presentation Template (`basf-design-darkblue.scss`)

## Core Brand Colors

| SCSS Variable     | Hex       | RGB           | Role                                               |
| ----------------- | --------- | ------------- | -------------------------------------------------- |
| `$basf-blue`      | `#004A96` | 0, 74, 150    | Primary accent: headings, separators, active items |
| `$basf-light-bg`  | `#E0E9F2` | 224, 233, 242 | Slide background (all regular slides)              |
| `$basf-gray`      | `#8C8C8C` | 140, 140, 140 | Inactive / secondary text, dimmed list items       |
| `$basf-dark-gray` | `#3D3D3D` | 61, 61, 61    | Primary body text                                  |
| White             | `#FFFFFF` | 255, 255, 255 | Content boxes, highlight right panel, logo         |

> **Important:** The official template does **not** use orange, dark green, or cream. The background is `#E0E9F2` (light blue-gray), not white or cream.

## Typography

- Heading and body: **Arial** (fallback: Helvetica Neue, Helvetica, sans-serif)
- Code: **Courier New** (fallback: Courier, monospace)
- Base font size: `36px` (root)
- Body text: `1.05em` | Compact (boxes/highlight): `0.95em`

## Design Tokens (SCSS variables)

All spacing and sizing is centralized in `_basf-design-darkblue-official.scss`.
Values calibrated against the official BASF PowerPoint template at 1920×1080:

```scss
$slide-pad-v: 80px; // vertical slide padding (PPTX: ~81px measured)
$slide-pad-h: 80px; // horizontal slide padding (PPTX: ~81px measured)
$separator-width: 3em; // blue line below headings
$separator-height: 5px;
$heading-size-title: 3.6em; // title slide h1
$heading-size-divider: 2.4em; // divider slide h2
$heading-size-default: 2.4em; // all other slide h2 (PPTX: 44pt)
$body-font-size: 1em; // standard body text (PPTX: 18pt)
$body-font-size-sm: 0.85em; // compact body text (PPTX: 15pt)
$list-margin-top: 0.8em;
```

## Slide Resolution

All presentations are **1920 × 1080** with `margin: 0.04`.

## Logo Placement

- **Regular slides**: bottom-right corner (`80px` max-height)
- **Title slide**: inside a BASF-blue decorative bar (bottom-right), logo inverted to white
- **Closing slide**: large centered white logo on full-blue background

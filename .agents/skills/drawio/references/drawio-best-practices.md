# Draw.io Best Practices

Source: Zettelkasten notes [20260127T134106767276000], [20260127T134407749582000], [20260127T134407801920000]

## Configuration (Extras > Configuration)

Draw.io uses JSON configuration. Key principle: **use minimal overrides** — only set what must differ from theme defaults, to avoid locking out future improvements.

```json
{
  "defaultVertexStyle": {
    "fontFamily": "Arial"
  },
  "defaultEdgeStyle": {
    "edgeStyle": "orthogonalEdgeStyle",
    "rounded": "1",
    "jettySize": "auto"
  }
}
```

## Arrowheads

| Setting | Default  | Recommended  |
| ------- | -------- | ------------ |
| Style   | option 1 | **option 8** |
| Size    | 6        | **12**       |

Reason: default size 6 is too small; option 8 is clearest shape.

## Line Colors

- **Never use `#000000`** (pure black) — causes eye strain
- Use `#212427` (soft black) for all strokes and text

## Line Curve Styles

| Style              | Use Case                                     |
| ------------------ | -------------------------------------------- |
| Sharp / Orthogonal | Default, technical, easy to edit             |
| Rounded            | Professional, handles line overlaps well     |
| Curved             | Polished presentations (more editing effort) |

### Line Overlaps (crossing lines)

- Enable "Line jumps" → Arc setting
- Arc size: `12` (default 6 is too subtle)
- Best with Sharp or Rounded line type
- Use right-click → "To Front" to control which line shows the arc

## Shape Styling

- All rectangles: `rounded=1` (friendly, approachable)
- Adjust corner rounding manually for very large shapes (default can look too bulky)

## UI Themes

| Theme             | Best for                    |
| ----------------- | --------------------------- |
| Kennedy (Classic) | Full-featured desktop use   |
| Atlas             | Confluence/Jira integration |
| Minimal           | Tablets, mobile             |
| Sketch            | Whiteboard-style            |
| Simple            | Streamlined toolbar         |

Dark mode: `Extras > Appearance > Dark` (background `#2A2A2A`)

## XML Format Notes

- File extension: `.drawio` (XML containing `<mxfile>`)
- Compression: off by default (`compressXml: false`)
- Style strings: semicolon-delimited key=value pairs
- Discover style keys: select element → `Ctrl+E` (Edit Style)

## Configuration Storage

- Browser local storage key: `.configuration`
- User settings key: `.drawio-config`
- Access via Chrome DevTools > Application > Local Storage

## Preset Color Schemes (Style Tab)

Define coordinated palettes using the `styles` array:

```json
{
  "styles": [
    {},
    {
      "commonStyle": {
        "fontColor": "#FFFFFF",
        "strokeColor": "#004A96",
        "fillColor": "#004A96"
      }
    }
  ]
}
```

Empty object `{}` = default colors.

## Font Tips

- Limit custom fonts (each requires client download)
- Custom fonts need CORS headers for cross-domain use
- Quip: max 10 kB configuration size

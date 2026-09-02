---
name: drawio
description: >
  Create, edit, and style draw.io (.drawio) XML diagram files using BASF corporate
  branding colors and visual best practices. Use when asked to create diagrams,
  flowcharts, architecture diagrams, infographics, process maps, evidence maps,
  decision trees, or any draw.io / diagrams.net file. Triggers on: "create a diagram",
  "draw a flowchart", "make a drawio file", "draw.io", ".drawio", "diagrams.net",
  "create a visual", "infographic".
author: Daniel Kaesmayr
metadata:
  version: "1.1.0"
  category: visualization
---

# Draw.io Diagram Skill

## BASF Color Palette

Always use BASF corporate colors (sRGB, source: [ZK note 20260127T133218763144000]):

| Role                  | Name        | Hex       | Usage                                               |
| --------------------- | ----------- | --------- | --------------------------------------------------- |
| **Primary**           | Orange      | `#F39500` | Headers, highlights, call-outs, accent shapes       |
| **Trust / Structure** | Dark Blue   | `#004A96` | Primary structure, node borders, main flow elements |
| **Information**       | Light Blue  | `#21A0D2` | Secondary nodes, informational boxes                |
| **Sustainability**    | Light Green | `#65AC1E` | Positive outcomes, growth nodes                     |
| **Deep Accent**       | Dark Green  | `#00793A` | Confirmed/validated states                          |
| **Alert / Error**     | Red         | `#C50022` | Warnings, errors, contradictions only               |
| **Text / Lines**      | Soft Black  | `#212427` | All text and strokes (never pure `#000000`)         |
| **Background**        | White       | `#FFFFFF` | Canvas/shape fill default                           |
| **Subtle Fill**       | Off-white   | `#F5F5F5` | Grouped background areas                            |

### Accessibility Rules

- Dark Blue `#004A96` on white → WCAG AAA ✓
- Orange `#F39500` on white → WCAG AA ✓
- Never use Light Blue `#21A0D2` for text (insufficient contrast)
- Red `#C50022` only for alerts/errors, not decoration

---

## Default draw.io JSON Configuration

Apply this to new diagrams via `Extras > Configuration`:

```json
{
  "defaultVertexStyle": {
    "fontFamily": "Arial",
    "fontColor": "#212427",
    "strokeColor": "#004A96",
    "fillColor": "#FFFFFF",
    "rounded": "1"
  },
  "defaultEdgeStyle": {
    "fontFamily": "Arial",
    "fontColor": "#212427",
    "strokeColor": "#212427",
    "edgeStyle": "orthogonalEdgeStyle",
    "rounded": "1",
    "jettySize": "auto",
    "orthogonalLoop": "1"
  },
  "presetColors": [
    "F39500",
    "004A96",
    "21A0D2",
    "65AC1E",
    "00793A",
    "C50022",
    "212427",
    "FFFFFF",
    "F5F5F5"
  ],
  "defaultColorSchemes": [
    {
      "commonStyle": {
        "fontColor": "#212427",
        "strokeColor": "#004A96",
        "fillColor": "#F5F5F5"
      }
    },
    {
      "commonStyle": {
        "fontColor": "#FFFFFF",
        "strokeColor": "#004A96",
        "fillColor": "#004A96"
      }
    },
    {
      "commonStyle": {
        "fontColor": "#212427",
        "strokeColor": "#F39500",
        "fillColor": "#FFFFFF"
      }
    }
  ]
}
```

---

## Diagram Construction Rules

### Shapes / Vertices

- Rounded corners on all rectangles (`rounded=1`)
- Fill: `#FFFFFF` default; `#F5F5F5` for background grouping areas
- Stroke: `#004A96` (Dark Blue) for primary elements
- Use `#F39500` (Orange) fill for headers and hero nodes
- Use `#004A96` fill with `fontColor=#FFFFFF` for emphasis boxes

### Connectors / Edges

- Stroke: `#212427` (Soft Black) — never `#000000`
- Arrowhead style: option 8, size 12 (double default)
- Line type default: orthogonal/sharp for clarity
- Complex diagrams with overlapping lines: use Rounded + arc jumps, arc size 12

### Typography

- Font: Arial throughout
- Labels: `#212427` on light backgrounds; `#FFFFFF` on dark fills
- Minimum font size: 11pt

---

## Workflow: Creating a New Diagram

1. **Plan structure** — identify node types, relationships, flow direction
2. **Map BASF colors to roles** — use table above; Orange=highlight, Dark Blue=structure
3. **Write draw.io XML** — produce valid `<mxGraphModel>` XML
4. **Save as `.drawio`** — typically to `assets/diagrams/` or the research output directory
5. **Validate XML** — ensure all tags close correctly; `mxCell` has `id`, `parent`, `vertex`/`edge`

### Minimal XML Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" version="24.0.0">
  <diagram name="Page-1" id="page1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Use NUMERIC IDs only: "2", "3", "4", ... -->
        <!-- Keep mxGraphModel attributes on ONE line -->
        <!-- No unicode (em dash, middle dot, emoji) in value attrs -->
        <!-- Only <b>, <br>, <i> HTML tags in values -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Cell Style Snippets

**Header / Hero node (Orange):**

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#F39500;strokeColor=#C47800;fontColor=#FFFFFF;fontStyle=1;fontSize=13;
```

**Primary node (Dark Blue):**

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#004A96;strokeColor=#003070;fontColor=#FFFFFF;fontSize=11;
```

**Secondary node (Light Blue):**

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#21A0D2;strokeColor=#1580A8;fontColor=#FFFFFF;fontSize=11;
```

**Neutral node (White + Blue border):**

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#004A96;fontColor=#212427;fontSize=11;
```

**Background grouping area:**

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#004A96;fontColor=#212427;opacity=50;
```

**Positive outcome (Green):**

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#65AC1E;strokeColor=#4E8A18;fontColor=#FFFFFF;fontSize=11;
```

**Warning / Alert (Red):**

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#C50022;strokeColor=#9A001A;fontColor=#FFFFFF;fontSize=11;
```

**Connector (default):**

```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;exitX=0.5;exitY=1;entryX=0.5;entryY=0;strokeColor=#212427;strokeWidth=2;endArrow=block;endFill=1;endSize=12;
```

---

## Troubleshooting: Common XML Errors

### XML Character Escaping (CRITICAL)

**Symptom**: "xmlParseEntityRef: no name" or "Cannot read properties of null" errors

**Cause**: Unescaped special characters in `value` attributes

**Required XML Escapes**:

| Character | Must Write As | Example                                     |
| --------- | ------------- | ------------------------------------------- |
| `&`       | `&amp;`       | "R&D" → `value="R&amp;D"`                   |
| `<`       | `&lt;`        | "A<B" → `value="A&lt;B"`                    |
| `>`       | `&gt;`        | "A>B" → `value="A&gt;B"`                    |
| `"`       | `&quot;`      | In attributes: `title="&quot;Test&quot;"`  |
| `'`       | `&apos;`      | In attributes: `name='It&apos;s working'`  |

**Common Culprits**:

- Category names with ampersands: "QA & Testing" → `"QA &amp; Testing"`
- Mathematical expressions: "A > B & C < D" → `"A &gt; B &amp; C &lt; D"`
- Company names: "R&D", "Q&A", "Sales & Marketing"

**How to Fix**:

1. Search for `value="` in the `.drawio` file
2. Within each `value="..."`, replace:
   - Every standalone `&` with `&amp;`
   - Every `<` with `&lt;`
   - Every `>` with `&gt;`

**Example Fix**:

```xml
<!-- ❌ BROKEN (line 69 error) -->
<mxCell id="cat1" value="SYNTHESIS & REPORTING" ...>

<!-- ✅ FIXED -->
<mxCell id="cat1" value="SYNTHESIS &amp; REPORTING" ...>
```

### Validation Before Opening

Run quick XML validation:

```bash
xmllint --noout yourfile.drawio
```

If no output → valid. If errors → check line number and apply escaping rules above.

---

### "d.setId is not a function" Error (CRITICAL)

**Symptom**: draw.io shows `d.setId is not a function` when opening the file

**Causes** (in order of likelihood):

1. **String IDs with underscores or special characters** — draw.io can choke on IDs like `phaseA_bg`, `leg1t`, `e12`. Use **numeric string IDs** only: `"2"`, `"3"`, `"4"`, etc.
2. **`<code>` tags inside `value` attributes** — HTML tags like `&lt;code&gt;` inside cell values can break parsing. Use plain text or only `&lt;b&gt;`, `&lt;br&gt;`, `&lt;i&gt;` tags.
3. **Unicode characters in values** — Em dashes (`—`), middle dots (`·`), emoji (`📋`), and other non-ASCII characters can cause parsing failures. Use ASCII equivalents: `-` instead of `—`, `/` instead of `·`, omit emoji.
4. **Multi-line XML attributes** — `<mxGraphModel>` attributes split across lines may cause parser issues. Keep all attributes on a single line.
5. **XML comments** — `<!-- comment -->` inside `<root>` can sometimes confuse the parser. Avoid XML comments in the cell area.
6. **Self-closing tags** — Use `<mxCell id="0"/>` not `<mxCell id="0" />` (no space before `/>`) for consistency, though both are valid XML.

**How to Fix**:

```xml
<!-- ❌ BROKEN: string IDs, unicode, code tags, comments -->
<mxCell id="phaseA_bg" value="Data — Overview" ...>
<mxCell id="cache" value="&lt;code&gt;field.users[]&lt;/code&gt;" ...>
<!-- This is a section divider -->

<!-- ✅ FIXED: numeric IDs, ASCII text, simple HTML only -->
<mxCell id="3" value="Data - Overview" ...>
<mxCell id="6" value="field.users[] = username" ...>
```

**Prevention Checklist**:
- [ ] All `id` attributes are numeric strings (`"0"`, `"1"`, `"2"`, ...)
- [ ] No `<code>`, `<span>`, `<div>`, or `<p>` tags in values (only `<b>`, `<br>`, `<i>`)
- [ ] No Unicode beyond basic Latin in `value` attributes (no `—`, `·`, `→`, emoji)
- [ ] `<mxGraphModel>` attributes all on one line
- [ ] No XML comments inside `<root>` element
- [ ] IDs `"0"` and `"1"` reserved for root cells only

---

## Reference Files

- See [references/basf-colors.md](references/basf-colors.md) for full color specification including print/CMYK values and accessibility matrix
- See [references/drawio-best-practices.md](references/drawio-best-practices.md) for detailed configuration options, line styling, and theming

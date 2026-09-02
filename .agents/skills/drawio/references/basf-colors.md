# BASF Corporate Color Specifications

Source: BASF BrandWeb (brandweb.basf.com) · Zettelkasten note [20260127T133218763144000]

## Digital / Screen (sRGB)

| Name        | RGB           | Hex       | Role                           |
| ----------- | ------------- | --------- | ------------------------------ |
| Orange      | 243, 149, 0   | `#F39500` | Primary brand, hero elements   |
| Dark Blue   | 0, 74, 150    | `#004A96` | Structural, professional       |
| Light Blue  | 33, 160, 210  | `#21A0D2` | Secondary information          |
| Light Green | 101, 172, 30  | `#65AC1E` | Growth, sustainability         |
| Dark Green  | 0, 121, 58    | `#00793A` | Confirmed, environmental       |
| Red         | 197, 0, 34    | `#C50022` | Alert, error, contradiction    |
| Soft Black  | 33, 36, 39    | `#212427` | Text, lines (never pure black) |
| White       | 255, 255, 255 | `#FFFFFF` | Background, fills              |
| Off-white   | 245, 245, 245 | `#F5F5F5` | Subtle grouping backgrounds    |

## Accessibility Matrix

| Foreground           | Background          | Ratio  | WCAG Level |
| -------------------- | ------------------- | ------ | ---------- |
| `#004A96` Dark Blue  | `#FFFFFF` White     | ~7.5:1 | **AAA** ✓  |
| `#F39500` Orange     | `#FFFFFF` White     | ~3.2:1 | **AA** ✓   |
| `#FFFFFF` White      | `#004A96` Dark Blue | ~7.5:1 | **AAA** ✓  |
| `#FFFFFF` White      | `#C50022` Red       | ~5.8:1 | **AA** ✓   |
| `#212427` Soft Black | `#FFFFFF` White     | ~18:1  | **AAA** ✓  |
| `#21A0D2` Light Blue | `#FFFFFF` White     | ~2.9:1 | **Fail** ✗ |

> **Rule**: Never use Light Blue (`#21A0D2`) as text color on white. Use only as fill with white text.

## Usage Guidelines for draw.io

- **Headers / hero nodes**: `#F39500` fill, `#FFFFFF` text
- **Primary structure nodes**: `#004A96` fill, `#FFFFFF` text — OR `#FFFFFF` fill, `#004A96` stroke
- **Secondary / informational**: `#21A0D2` fill, `#FFFFFF` text
- **Positive/confirmed states**: `#65AC1E` fill, `#FFFFFF` text
- **Warnings / errors**: `#C50022` fill, `#FFFFFF` text
- **All text and connectors**: `#212427` (not `#000000`)
- **Background groupings**: `#F5F5F5` fill, `#004A96` stroke

## Dark Mode

Recommended canvas background: `#2A2A2A`
Text on dark: `#FFFFFF` or `#F39500` for accents

## Source References

- BASF BrandWeb: https://brandweb.basf.com/portal/basf/de/dt.jsp?setCursor=1_712738
- BASF Atoms library: https://gitlab.roqs.basf.net/atoms/atom

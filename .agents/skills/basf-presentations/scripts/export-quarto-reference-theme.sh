#!/bin/bash

set -euo pipefail

if ! command -v quarto >/dev/null 2>&1; then
  echo "Quarto is required but was not found in PATH."
  exit 1
fi

TARGET_DIR=${1:-/tmp/basf-quarto-reference}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REVEAL_BASF_DIR="$(cd "$SKILL_DIR/../reveal-basf" && pwd)"

rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR/logos"

cp "$REVEAL_BASF_DIR/assets/basf-design-darkblue.scss" "$TARGET_DIR/basf-design-darkblue.scss"
cp "$REVEAL_BASF_DIR/assets/logos/BASF_Logo.png" "$TARGET_DIR/logos/BASF_Logo.png"

cat > "$TARGET_DIR/reference.qmd" <<'EOF'
---
title: "BASF Native Parity Reference"
subtitle: "Quarto Render Baseline"
author: "GitHub Copilot"
date: today
date-format: "DD.MM.YYYY"
format:
  revealjs:
    theme: [default, basf-design-darkblue.scss]
    width: 1920
    height: 1080
    margin: 0.08
    transition: slide
    slide-number: true
    controls: true
    hash: true
    center: false
    navigation-mode: linear
    logo: logos/BASF_Logo.png
---

## Agenda {.divider-slide}

1. **Current section**
2. Content slide
3. Highlight slide
4. Closing slide

---

## Content Example {.content-slide}

### Supporting subtitle

- First point
- Second point
  - Nested point

---

## Highlight Example {.highlight-slide}

::: {.split-left}

### Why this matters

- Left rail content
- Used as visual baseline

:::

::: {.split-right}

Right panel content.

:::

---

## {.closing-slide}
EOF

cd "$TARGET_DIR"
quarto render reference.qmd

THEME_CSS=$(find "$TARGET_DIR/reference_files/libs/revealjs/dist/theme" -maxdepth 1 -name 'quarto-*.css' | head -n 1)

if [ -z "$THEME_CSS" ]; then
  echo "Failed to locate generated Quarto theme CSS."
  exit 1
fi

cp "$THEME_CSS" "$TARGET_DIR/quarto-reference-theme.css"

echo "Quarto reference exported to:"
echo "  HTML: $TARGET_DIR/reference.html"
echo "  Theme CSS: $TARGET_DIR/quarto-reference-theme.css"

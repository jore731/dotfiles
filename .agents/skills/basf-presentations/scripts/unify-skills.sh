#!/bin/bash
# script: unify-skills.sh
# Purpose: Merge reveal-basf assets into basf-presentations to eliminate skill duplication
# The official SCSS from reveal-basf becomes _basf-design-darkblue-official.scss
# in the basf-presentations templates/quarto/ directory.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REVEAL_BASF_DIR="$(cd "$SKILL_DIR/../reveal-basf" && pwd)"
QUARTO_DIR="$SKILL_DIR/templates/quarto"

echo "=== Unifying reveal-basf into basf-presentations ==="
echo "Source:      $REVEAL_BASF_DIR"
echo "Destination: $SKILL_DIR"
echo ""

# 1. Copy the official SCSS as the _official partial
SRC="$REVEAL_BASF_DIR/assets/basf-design-darkblue.scss"
DST="$QUARTO_DIR/_basf-design-darkblue-official.scss"

if [ ! -f "$SRC" ]; then
    echo "ERROR: Official SCSS not found at $SRC"
    exit 1
fi

cp "$SRC" "$DST"
echo "✅ Copied official SCSS → _basf-design-darkblue-official.scss"

# 2. Copy the logo if missing
if [ ! -f "$SKILL_DIR/templates/logos/BASF_Logo.png" ] && [ -f "$REVEAL_BASF_DIR/assets/logos/BASF_Logo.png" ]; then
    mkdir -p "$SKILL_DIR/templates/logos"
    cp "$REVEAL_BASF_DIR/assets/logos/BASF_Logo.png" "$SKILL_DIR/templates/logos/"
    echo "✅ Copied BASF_Logo.png"
else
    echo "ℹ️  Logo already present"
fi

# 3. Copy the Quarto template if not present
if [ ! -f "$QUARTO_DIR/presentation-template.qmd" ] && [ -f "$REVEAL_BASF_DIR/assets/basf-template.qmd" ]; then
    cp "$REVEAL_BASF_DIR/assets/basf-template.qmd" "$QUARTO_DIR/presentation-template.qmd"
    echo "✅ Copied Quarto template"
else
    echo "ℹ️  Quarto template already present"
fi

echo ""
echo "=== Done. Next step: apply CSS fixes to the copied official SCSS ==="
echo "Run the Python fix script: python3 scripts/apply-css-fixes.py"

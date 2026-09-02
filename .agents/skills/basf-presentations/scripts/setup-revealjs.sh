#!/bin/bash
# script: setup-revealjs.sh
# Purpose: Scaffolds a new vanilla Reveal.js presentation with BASF Theme
# This script is self-contained — all assets live within basf-presentations.

if [ "$#" -ne 1 ]; then
    echo "Usage: ./setup-revealjs.sh <target-directory>"
    exit 1
fi

TARGET_DIR=$1
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Creating new Reveal.js presentation in $TARGET_DIR..."
mkdir -p "$TARGET_DIR"

# Copy template files
cp "$SKILL_DIR/templates/revealjs/package.json" "$TARGET_DIR/"
cp "$SKILL_DIR/templates/revealjs/index.html" "$TARGET_DIR/"
cp "$SKILL_DIR/templates/revealjs/slides.md" "$TARGET_DIR/"

# Copy themes (the official SCSS is already inside templates/quarto/)
cp -r "$SKILL_DIR/templates/quarto" "$TARGET_DIR/theme"

# Copy logos
mkdir -p "$TARGET_DIR/logos"
if [ -f "$SKILL_DIR/templates/logos/BASF_Logo.png" ]; then
    cp "$SKILL_DIR/templates/logos/BASF_Logo.png" "$TARGET_DIR/logos/"
else
    echo "⚠️  Please place BASF_Logo.png into $TARGET_DIR/logos/"
fi

cd "$TARGET_DIR" || exit

echo "Installing node dependencies: reveal.js, sass, vite..."
npm install

echo "Building theme..."
npm run build:css

echo "---------------------------------------------------------"
echo "Setup complete! Navigate to $TARGET_DIR and run:"
echo "  npm run dev"
echo "to preview your presentation."
echo "---------------------------------------------------------"

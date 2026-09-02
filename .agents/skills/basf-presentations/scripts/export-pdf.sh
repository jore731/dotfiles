#!/bin/bash
# export-pdf.sh — Pixel-perfect PDF export from Reveal.js HTML using Decktape
#
# Usage:
#   ./export-pdf.sh presentation.html [output.pdf] [OPTIONS]
#
# Arguments:
#   presentation.html   Path or URL to the Reveal.js presentation
#   output.pdf          Output PDF path (default: same name as input with .pdf)
#
# Options:
#   --size WxH          Slide size in pixels (default: 1920x1080)
#   --pause MS          Wait time per slide in ms (default: 1000)
#   --no-fragments      Collapse fragment steps into single slides
#   --slides RANGE      Only export specific slides (e.g., "1-5,8,10")
#   --notes             Include speaker notes on separate pages
#
# Prerequisites:
#   npm install decktape   (local) or
#   npm install -g decktape (global)
#
# Examples:
#   ./export-pdf.sh dist/index.html output.pdf
#   ./export-pdf.sh http://localhost:5173 slides.pdf --no-fragments
#   ./export-pdf.sh presentation.html --size 1280x720 --slides 1-10

set -euo pipefail

# --- Defaults ---
SIZE="1920x1080"
PAUSE="1000"
FRAGMENTS="true"
SLIDES=""
NOTES=""

# --- Parse arguments ---
INPUT=""
OUTPUT=""
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --size)
            SIZE="$2"
            shift 2
            ;;
        --pause)
            PAUSE="$2"
            shift 2
            ;;
        --no-fragments)
            FRAGMENTS="false"
            shift
            ;;
        --slides)
            SLIDES="$2"
            shift 2
            ;;
        --notes)
            NOTES="separate-page"
            shift
            ;;
        --help|-h)
            head -25 "$0" | tail -22
            exit 0
            ;;
        -*)
            EXTRA_ARGS+=("$1")
            shift
            ;;
        *)
            if [[ -z "$INPUT" ]]; then
                INPUT="$1"
            elif [[ -z "$OUTPUT" ]]; then
                OUTPUT="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$INPUT" ]]; then
    echo "Error: No input file specified."
    echo "Usage: ./export-pdf.sh presentation.html [output.pdf]"
    exit 1
fi

# Default output: same name with .pdf extension
if [[ -z "$OUTPUT" ]]; then
    OUTPUT="${INPUT%.*}.pdf"
fi

# --- Find decktape ---
DECKTAPE_CMD=()
if command -v decktape &>/dev/null; then
    DECKTAPE_CMD=("decktape")
elif [[ -x "./node_modules/.bin/decktape" ]]; then
    DECKTAPE_CMD=("./node_modules/.bin/decktape")
elif command -v npx &>/dev/null; then
    DECKTAPE_CMD=("npx" "decktape")
else
    echo "Error: decktape not found. Install with: npm install decktape"
    exit 1
fi

# --- Build command ---
CMD=("${DECKTAPE_CMD[@]}" reveal "$INPUT" "$OUTPUT" --size "$SIZE" --pause "$PAUSE")

if [[ "$FRAGMENTS" == "false" ]]; then
    CMD+=(--pdf-separate-fragments=false)
fi

if [[ -n "$SLIDES" ]]; then
    CMD+=(--slides "$SLIDES")
fi

if [[ -n "$NOTES" ]]; then
    # Inject showNotes option via URL query parameter
    if [[ "$INPUT" == *"?"* ]]; then
        INPUT="${INPUT}&showNotes=$NOTES"
    else
        INPUT="${INPUT}?showNotes=$NOTES"
    fi
    # Rebuild command with modified input
    CMD=("${DECKTAPE_CMD[@]}" reveal "$INPUT" "$OUTPUT" --size "$SIZE" --pause "$PAUSE")
    if [[ -n "$SLIDES" ]]; then
        CMD+=(--slides "$SLIDES")
    fi
    if [[ "$FRAGMENTS" == "false" ]]; then
        CMD+=(--pdf-separate-fragments=false)
    fi
fi

CMD+=("${EXTRA_ARGS[@]}")

echo "📄 Exporting PDF..."
echo "   Input:  $INPUT"
echo "   Output: $OUTPUT"
echo "   Size:   $SIZE"
echo "   CMD:    ${CMD[*]}"
echo ""

"${CMD[@]}"

if [[ -f "$OUTPUT" ]]; then
    FILE_SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo ""
    echo "✅ PDF exported: $OUTPUT ($FILE_SIZE)"
else
    echo ""
    echo "❌ PDF export failed"
    exit 1
fi

# BASF Presentation Multi-Format Build
#
# Usage:
#   make html          — Render Reveal.js HTML slides
#   make pptx          — Render PPTX with BASF branding
#   make pdf           — Render HTML then capture PDF via Decktape
#   make all           — Build all formats
#   make clean         — Remove build artifacts
#
# Configuration:
#   Set QMD to your presentation source file.
#   Set SKILL_DIR to the basf-presentations skill path.

# --- Configuration ---
QMD          ?= presentation.qmd
BASENAME     := $(basename $(QMD))
HTML         := $(BASENAME).html
PDF          := $(BASENAME).pdf
PPTX         := $(BASENAME).pptx
SLIDES_MD    ?= slides.md

# Paths to BASF skill assets
SKILL_DIR    ?= $(shell git rev-parse --show-toplevel 2>/dev/null)/.github/skills/basf-presentations
PANDOC_SKILL ?= $(shell git rev-parse --show-toplevel 2>/dev/null)/.github/skills/pandoc-quarto-basf
TEMPLATE     ?= $(PANDOC_SKILL)/assets/templates/basf-reference.pptx

# Decktape settings
PDF_SIZE     ?= 1920x1080
PDF_PAUSE    ?= 1000

# --- Targets ---

.PHONY: all html pptx pdf pdf-native pptx-native check check-fix clean help

all: html pptx pdf ## Build all formats (HTML + PPTX + PDF)

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'

# --- Quarto Targets ---

html: $(HTML) ## Render Reveal.js HTML via Quarto
$(HTML): $(QMD)
	quarto render $(QMD) --to revealjs

pptx: $(PPTX) ## Render PPTX via Quarto + BASF reference template
$(PPTX): $(QMD) $(TEMPLATE)
	quarto render $(QMD) --to pptx

pdf: $(HTML) ## Render PDF via Decktape from Reveal.js HTML
	$(SKILL_DIR)/scripts/export-pdf.sh $(HTML) $(PDF) --size $(PDF_SIZE)

# --- Native Reveal.js Targets ---

pdf-native: ## Export PDF from a live Reveal.js server (needs server running on :5173)
	$(SKILL_DIR)/scripts/export-pdf.sh http://localhost:5173 $(PDF) --size $(PDF_SIZE)

pptx-native: ## Export PPTX from native Reveal.js slides.md
	python3 $(SKILL_DIR)/scripts/export-pptx.py $(SLIDES_MD) \
		--template $(TEMPLATE) \
		-o $(PPTX)

# --- Utilities ---

clean: ## Remove build artifacts
	rm -f $(HTML) $(PDF) $(PPTX)
	rm -rf $(BASENAME)_files/

# --- Quality Checks ---

check: $(PPTX) ## Check PPTX for overflow issues
	python3 $(SKILL_DIR)/scripts/check-pptx-overflow.py $(PPTX)

check-fix: $(PPTX) ## Auto-fix PPTX overflow issues
	python3 $(SKILL_DIR)/scripts/check-pptx-overflow.py $(PPTX) --fix -v

# --- Template Generation ---

reference-pptx: ## (Re)generate basf-reference.pptx from official BASF template
	python3 $(SKILL_DIR)/scripts/create-basf-reference-pptx.py

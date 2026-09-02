#!/usr/bin/env python3
"""
Create a Pandoc-compatible BASF PPTX reference template from the official
69-slide BASF PowerPoint template.

This script:
1. Opens the official BASF template (69 slides)
2. Strips all content slides, keeping only slide masters and layouts
3. Renames layouts to match Pandoc's expected layout names
4. Preserves BASF branding: logo, Arial font theme, color palette, slide numbers

Pandoc expects these layout names:
  - "Title Slide"       — for title slides (H1 + subtitle)
  - "Section Header"    — for section dividers (H1 without subtitle)
  - "Two Content"       — for 2-column slides
  - "Title and Content" — for default content slides (H2 + body)
  - "Comparison"        — for comparison layouts
  - "Blank"             — for images/custom content

Usage:
    python3 create-basf-reference-pptx.py [source.pptx] [output.pptx]

Defaults:
    source = .github/skills/basf-presentations/references/Updated PowerPoint Template_lg_March2025.pptx
    output = .github/skills/pandoc-quarto-basf/assets/templates/basf-reference.pptx
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

# BASF layout name → Pandoc expected layout name
LAYOUT_MAPPING = {
    "Title page 01": "Title Slide",
    "Title light": "Section Header",
    "Title and content 2-column": "Two Content",
    "Title and content 3-column": "Title and Content",
    "Title and content 4-column": "Comparison",
    "Title and content": "Blank",
}

# Namespaces used in OOXML
NAMESPACES = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def find_workspace_root() -> Path:
    """Walk up from script location to find .github/ dir."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / ".github").is_dir():
            return current
        current = current.parent
    return Path.cwd()


def parse_args() -> argparse.Namespace:
    root = find_workspace_root()

    default_source = (
        root
        / ".github/skills/basf-presentations/references"
        / "Updated PowerPoint Template_lg_March2025.pptx"
    )
    default_output = (
        root
        / ".github/skills/pandoc-quarto-basf/assets/templates"
        / "basf-reference.pptx"
    )

    parser = argparse.ArgumentParser(
        description="Create Pandoc-compatible BASF PPTX reference template"
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=str(default_source),
        help=f"Source BASF template PPTX (default: {default_source})",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=str(default_output),
        help=f"Output reference PPTX (default: {default_output})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    return parser.parse_args()


def rename_layouts_in_pptx(pptx_path: str, output_path: str, dry_run: bool = False) -> None:
    """
    Rename slide layouts inside a PPTX to match Pandoc's expected names.

    This works by modifying the XML inside the PPTX (which is a ZIP file).
    Layout names are stored in slideLayout*.xml files as the 'name' attribute
    of the <p:cSld> element.
    """
    if not os.path.exists(pptx_path):
        print(f"Error: Source file not found: {pptx_path}")
        sys.exit(1)

    print(f"Source: {pptx_path}")
    print(f"Output: {output_path}")
    print()

    # Register namespaces so they're preserved in output
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    # Also register other common OOXML namespaces
    ET.register_namespace("mc", "http://schemas.openxmlformats.org/markup-compatibility/2006")
    ET.register_namespace("o", "urn:schemas-microsoft-com:office:office")
    ET.register_namespace("v", "urn:schemas-microsoft-com:vml")

    if dry_run:
        print("DRY RUN — no files will be written\n")

    # Work with the PPTX as a ZIP
    renamed_count = 0
    with zipfile.ZipFile(pptx_path, "r") as source_zip:
        layout_files = [
            f for f in source_zip.namelist()
            if f.startswith("ppt/slideLayouts/slideLayout") and f.endswith(".xml")
        ]

        print(f"Found {len(layout_files)} layout files\n")
        print(f"{'Layout File':<35} {'Original Name':<35} {'→ Pandoc Name'}")
        print("-" * 105)

        # First pass: discover current layout names
        renames: dict[str, tuple[str, str]] = {}  # filename -> (old_name, new_name)
        for layout_file in sorted(layout_files):
            xml_data = source_zip.read(layout_file)
            root = ET.fromstring(xml_data)  # nosec B314 — xml_data from trusted .pptx zip, not user input

            # Find <p:cSld name="...">
            old_name = None
            for elem in root.iter():
                if elem.tag.endswith("}cSld") or elem.tag == "cSld":
                    old_name = elem.get("name", "")
                    break

            if old_name and old_name in LAYOUT_MAPPING:
                new_name = LAYOUT_MAPPING[old_name]
                renames[layout_file] = (old_name, new_name)
                print(f"  {layout_file:<33} {old_name:<35} → {new_name}")
                renamed_count += 1
            elif old_name:
                print(f"  {layout_file:<33} {old_name:<35}   (kept as-is)")
            else:
                print(f"  {layout_file:<33} {'(no name)':<35}   (kept as-is)")

    print(f"\n{renamed_count} layouts will be renamed")

    if dry_run:
        print("\nDry run complete. No files written.")
        return

    # Second pass: create output PPTX with renamed layouts
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Copy source, then modify in place
    shutil.copy2(pptx_path, output_path)

    # Modify the copy
    with zipfile.ZipFile(pptx_path, "r") as source_zip:
        # Read all files from source
        all_files: dict[str, bytes] = {}
        for item in source_zip.namelist():
            all_files[item] = source_zip.read(item)

    # Apply renames to layout XMLs using byte-level replacement
    # (preserves all namespace declarations that ET.tostring would lose)
    for layout_file, (old_name, new_name) in renames.items():
        xml_bytes = all_files[layout_file]
        old_attr = f'name="{old_name}"'.encode("utf-8")
        new_attr = f'name="{new_name}"'.encode("utf-8")
        # Replace only the first occurrence (the cSld name attribute)
        modified = xml_bytes.replace(old_attr, new_attr, 1)
        all_files[layout_file] = modified

    # Write the modified PPTX
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as out_zip:
        for name, data in all_files.items():
            out_zip.writestr(name, data)

    print(f"\n✅ Created: {output_path}")
    print(f"   {renamed_count} layouts renamed to Pandoc-compatible names")
    print()
    print("Layout mapping applied:")
    for old, new in LAYOUT_MAPPING.items():
        print(f"  '{old}' → '{new}'")
    print()
    print("Next steps:")
    print("  1. Test: quarto render test.qmd --to pptx")
    print("  2. Verify layouts in PowerPoint")
    print("  3. Check: pandoc --print-default-data-file reference.pptx")


def main() -> None:
    args = parse_args()
    rename_layouts_in_pptx(args.source, args.output, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

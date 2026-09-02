---
description: Rebuild the Azure and Microsoft Entra Excalidraw libraries from the checked-in SVG sources
---

Run:

```bash
uv run --with svgpathtools python \
  /Users/jorgepulidolopez/.agents/skills/excalidraw-diagram-generator/scripts/import-svg-library.py \
  /Users/jorgepulidolopez/.agents/skills/excalidraw-diagram-generator/libraries/microsoft-azure-cloud-icons/official-svg \
  /Users/jorgepulidolopez/.agents/skills/excalidraw-diagram-generator/libraries/microsoft-azure-cloud-icons/azure-public-service-icons.excalidrawlib

uv run --with svgpathtools python \
  /Users/jorgepulidolopez/.agents/skills/excalidraw-diagram-generator/scripts/import-svg-library.py \
  /Users/jorgepulidolopez/.agents/skills/excalidraw-diagram-generator/libraries/microsoft-azure-cloud-icons/official-entra-svg \
  /Users/jorgepulidolopez/.agents/skills/excalidraw-diagram-generator/libraries/microsoft-azure-cloud-icons/microsoft-entra-icons.excalidrawlib
```

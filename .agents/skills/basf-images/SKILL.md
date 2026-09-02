---
name: basf-images
description: >
  Find and download externally approved, BASF-owned press photos from the BASF multimedia
  library at basf.com/global/en/media/multimedia. Use when searching for BASF corporate images,
  press photos, or downloadable assets for presentations, reports, or communications. Includes
  browser navigation of the photo library, URL pattern decoding for high-resolution downloads,
  and CLI tool references for resizing and format conversion on WSL/Linux and Windows.
  Triggers: "find BASF images", "download BASF press photo", "get BASF photo", "BASF image
  library", "BASF multimedia", "approved BASF images", "BASF copyright image".
author: Daniel Kaesmayr
metadata:
  version: "1.0.0"
  category: media
---

# BASF Image Library

## Overview

BASF publishes press-approved, royalty-free corporate images at:

- **Multimedia hub**: <https://www.basf.com/global/en/media/multimedia>
- **Press photos (main)**: <https://www.basf.com/global/en/media/multimedia/photos>
- **Current press photos**: <https://www.basf.com/global/en/media/multimedia/photos/current-press-photos>
- **Corporate / highlight photos**: <https://www.basf.com/global/en/media/multimedia/photos/highlight-photos>

> **Copyright**: BASF press photos carry the notice **"Print free of charge. Copyright by BASF."**
> Always credit: *© BASF SE* and include the image caption when used in publications.

---

## Step-by-Step Workflow

### 1. Browse the Photo Library

Use the `open_browser_page` tool to open the press photos page:

```
https://www.basf.com/global/en/media/multimedia/photos
```

Filter categories available on the page:

| Category | Notes |
|---|---|
| Board of Executive Directors | Portraits of leadership |
| Region | Location / site photos |
| Industry | Application / product images |
| Research & Development | Lab, science imagery |
| Events | Conference and trade show photos |
| Digitalization | Tech / digital workplace |
| Sustainability | Environmental and CSR topics |

Use the page filter to narrow results (~6,349 images available). Scroll to find relevant images and read captions to confirm topic match.

### 2. Decode the Image URL

BASF serves images through an AEM/JCR imaging API. URLs follow this pattern:

```
https://www.basf.com/api/imaging/focalarea/{aspect}/{width}/dam/jcr%3A{jcr-id}/{filename}.{ext}
```

| Segment | Description | Example values |
|---|---|---|
| `{aspect}` | Crop ratio | `4x3`, `16x9`, `6x3`, `1x1` |
| `{width}` | Rendered width | `414x`, `828x`, `1080x`, `2400x` |
| `{jcr-id}` | JCR node ID (URL-encoded `:`) | `8bf825f2-2537-3833-8079-40e9fca87fdb` |
| `{filename}` | Original asset filename | `1.1`, `methylamines_production` |
| `{ext}` | Image format | `jpg`, `png` |

**To get a higher resolution**, increase the `{width}` value in the URL. The API renders on-the-fly:

```
# Thumbnail (as shown on page)
https://www.basf.com/api/imaging/focalarea/4x3/414x/dam/jcr%3A8bf825f2-2537-3833-8079-40e9fca87fdb/1.1.jpg

# High-res download (swap 414x → 3000x)
https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A8bf825f2-2537-3833-8079-40e9fca87fdb/1.1.jpg
```

See [Image URL Patterns](./references/image-url-patterns.md) for full reference.

### 3. Download the Image

No authentication is required for press photos. Use standard CLI tools:

**WSL / Linux / macOS:**

```bash
# Single image with curl
curl -L -o basf-photo.jpg \
  "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{jcr-id}/{filename}.jpg"

# Or with wget
wget -O basf-photo.jpg \
  "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{jcr-id}/{filename}.jpg"
```

**Windows (PowerShell):**

```powershell
Invoke-WebRequest `
  -Uri "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{jcr-id}/{filename}.jpg" `
  -OutFile "basf-photo.jpg"
```

**Windows (CMD — curl built-in since Windows 10):**

```cmd
curl -L -o basf-photo.jpg "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{jcr-id}/{filename}.jpg"
```

### 4. Resize or Convert (Optional)

See [CLI Tools Reference](./references/cli-tools.md) for full commands. Quick reference:

| Task | WSL/Linux | Windows |
|---|---|---|
| Resize to max width 1920px | `convert input.jpg -resize 1920x output.jpg` | `magick input.jpg -resize 1920x output.jpg` |
| Convert JPG → PNG | `convert input.jpg output.png` | `magick input.jpg output.png` |
| Batch resize all JPGs | `mogrify -resize 1920x *.jpg` | `magick mogrify -resize 1920x *.jpg` |
| Check image dimensions | `identify image.jpg` | `magick identify image.jpg` |

---

## No Public REST API

The BASF website uses **Adobe Experience Manager (AEM)** as its CMS and DAM. There is no publicly documented REST or GraphQL API for programmatic image search. The workflow requires:

1. Browser navigation to find images and captions
2. URL extraction from the page source or browser DevTools
3. Direct HTTP download using the imaging API URL

For bulk or programmatic workflows, use browser DevTools → Network tab → filter by `api/imaging` to capture all image URLs on a page, then download with `curl` or `wget`.

---

## Quality and Format Notes

- **Default aspect ratios on the page**: `4x3` (standard), `16x9` (widescreen)
- **Recommended download width**: `3000x` for print; `1920x` for screen/presentations
- **Native format**: JPEG for photos; occasionally PNG for graphics
- **Color space**: sRGB (suitable for screen); verify before professional print use

---

## Related Resources

- [Image URL Patterns](./references/image-url-patterns.md) — URL anatomy, aspect ratios, resolution guide
- [CLI Tools Reference](./references/cli-tools.md) — ImageMagick, ffmpeg, curl/wget on WSL and Windows
- **Contact for questions**: [Corporate Media Relations](mailto:presse.kontakt@basf.com)

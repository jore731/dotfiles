# CLI Tools Reference — Image Download, Resize, and Conversion

Tools for downloading BASF press images and processing them on WSL/Linux and Windows.

---

## Download Tools

### curl

Available on: WSL/Linux/macOS natively; Windows 10+ natively (cmd and PowerShell).

```bash
# Download single image
curl -L -o basf-photo.jpg "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{id}/{filename}.jpg"

# Download with auto-filename from URL
curl -L -O "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{id}/{filename}.jpg"

# Download multiple images from a list file (one URL per line)
xargs -a urls.txt -I{} curl -L -O "{}"

# Set a custom User-Agent if the server rejects the request
curl -L -A "Mozilla/5.0" -o basf-photo.jpg "https://..."
```

### wget

Available on: WSL/Linux/macOS (may need `brew install wget`); Windows via scoop/choco or WSL.

```bash
# Download single image
wget -O basf-photo.jpg "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{id}/{filename}.jpg"

# Download from list of URLs
wget -i urls.txt

# Retry on failure
wget --tries=3 -O basf-photo.jpg "https://..."
```

### PowerShell (Windows)

```powershell
# Download single image
Invoke-WebRequest `
  -Uri "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{id}/{filename}.jpg" `
  -OutFile "basf-photo.jpg"

# Alias (shorter)
iwr -Uri "https://..." -OutFile "basf-photo.jpg"

# Batch download from array
$urls = @(
  "https://www.basf.com/api/imaging/...1.jpg",
  "https://www.basf.com/api/imaging/...2.jpg"
)
$urls | ForEach-Object {
  $file = Split-Path $_ -Leaf
  Invoke-WebRequest -Uri $_ -OutFile $file
}
```

---

## ImageMagick — Resize and Convert

### Installation

| Platform | Command |
|---|---|
| WSL / Ubuntu/Debian | `sudo apt install imagemagick` |
| WSL / Fedora/RHEL | `sudo dnf install ImageMagick` |
| macOS | `brew install imagemagick` |
| Windows | Download from [imagemagick.org](https://imagemagick.org/script/download.php) — use the **static** installer |

> **WSL vs Windows**: On WSL, use `convert` and `mogrify`. On Windows native, the command is `magick convert` and `magick mogrify` (the `magick` prefix avoids conflicts with Windows' own `convert.exe`).

### Resize

```bash
# WSL / Linux: Resize to max width 1920px (keeps aspect ratio)
convert input.jpg -resize 1920x output.jpg

# Windows: Same with magick prefix
magick input.jpg -resize 1920x output.jpg

# Resize to exact dimensions (may distort)
convert input.jpg -resize 1920x1080! output.jpg

# Resize to fit within box (no distortion, may add whitespace)
convert input.jpg -resize 1920x1080 -background white -gravity center -extent 1920x1080 output.jpg

# Resize only if larger than target (do not upscale)
convert input.jpg -resize "1920x>" output.jpg
```

### Batch Resize

```bash
# WSL/Linux: Resize all JPGs in-place to max width 1920px
mogrify -resize 1920x *.jpg

# Windows
magick mogrify -resize 1920x *.jpg

# Resize and output to a subdirectory
mogrify -resize 1920x -path ./resized *.jpg
```

### Format Conversion

```bash
# JPG → PNG
convert input.jpg output.png

# PNG → JPG at quality 90
convert input.png -quality 90 output.jpg

# Batch: convert all JPGs to PNG
mogrify -format png *.jpg

# Windows batch
magick mogrify -format png *.jpg
```

### Check Image Info

```bash
# WSL/Linux
identify image.jpg
# Output: image.jpg JPEG 3000x2250 3000x2250+0+0 8-bit sRGB 2.4MB

# Windows
magick identify image.jpg
```

---

## ffmpeg — Video and Bulk Image Operations

Available on: WSL/Linux (`sudo apt install ffmpeg`), macOS (`brew install ffmpeg`), Windows (download from [ffmpeg.org](https://ffmpeg.org/download.html) or `winget install ffmpeg`).

```bash
# Convert image formats
ffmpeg -i input.jpg output.png

# Scale image to width 1920 (keep aspect ratio)
ffmpeg -i input.jpg -vf "scale=1920:-1" output.jpg

# Batch convert all JPGs to PNG in current folder (WSL/Linux)
for f in *.jpg; do ffmpeg -i "$f" "${f%.jpg}.png"; done

# Batch resize to max width 1920 (WSL/Linux)
for f in *.jpg; do ffmpeg -i "$f" -vf "scale='min(1920,iw)':-1" "resized_${f}"; done
```

---

## Windows-Native: Built-in Options

### curl.exe (Windows 10+, built-in)

The Windows-native `curl.exe` is available in CMD and PowerShell since Windows 10 build 1803.

```cmd
curl -L -o basf-photo.jpg "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A{id}/{filename}.jpg"
```

### Paint / Photos app

For one-off resizing without CLI tools: open in Paint → Resize → set pixel dimensions.

### PowerShell + .NET (no extra tools required)

```powershell
Add-Type -AssemblyName System.Drawing

$img = [System.Drawing.Image]::FromFile("C:\path\to\input.jpg")
$newWidth = 1920
$newHeight = [int]($img.Height * $newWidth / $img.Width)
$resized = New-Object System.Drawing.Bitmap($newWidth, $newHeight)
$g = [System.Drawing.Graphics]::FromImage($resized)
$g.DrawImage($img, 0, 0, $newWidth, $newHeight)
$resized.Save("C:\path\to\output.jpg", [System.Drawing.Imaging.ImageFormat]::Jpeg)
$g.Dispose(); $img.Dispose(); $resized.Dispose()
```

---

## Quick Reference Card

| Task | WSL/Linux | Windows (cmd/PS) |
|---|---|---|
| Download image | `curl -L -o out.jpg "URL"` | `curl -L -o out.jpg "URL"` |
| Download list | `wget -i urls.txt` | `iwr` loop in PS |
| Resize to 1920px | `convert in.jpg -resize 1920x out.jpg` | `magick in.jpg -resize 1920x out.jpg` |
| Batch resize | `mogrify -resize 1920x *.jpg` | `magick mogrify -resize 1920x *.jpg` |
| JPG→PNG | `convert in.jpg out.png` | `magick in.jpg out.png` |
| Batch JPG→PNG | `mogrify -format png *.jpg` | `magick mogrify -format png *.jpg` |
| Check dimensions | `identify image.jpg` | `magick identify image.jpg` |
| Scale with ffmpeg | `ffmpeg -i in.jpg -vf scale=1920:-1 out.jpg` | `ffmpeg -i in.jpg -vf scale=1920:-1 out.jpg` |

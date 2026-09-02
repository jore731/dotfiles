# BASF Image URL Patterns

Reference for the BASF AEM/JCR imaging API used at `basf.com`.

## URL Structure

```
https://www.basf.com/api/imaging/focalarea/{aspect}/{width}/dam/jcr%3A{jcr-id}/{filename}.{ext}
```

### Segment Breakdown

| Segment | Required | Notes |
|---|---|---|
| `api/imaging/focalarea` | Yes | Fixed path prefix for the imaging API |
| `{aspect}` | Yes | Crop/focal area ratio (see table below) |
| `{width}` | Yes | Output width; height calculated automatically from aspect ratio |
| `dam/jcr%3A` | Yes | AEM DAM path; `%3A` is URL-encoded `:` |
| `{jcr-id}` | Yes | UUID of the JCR asset node |
| `{filename}.{ext}` | Yes | Original asset name and file extension |

### Aspect Ratios

| Ratio | Common Use |
|---|---|
| `4x3` | Standard photo (most press photos) |
| `16x9` | Widescreen / video-style |
| `6x3` | Wide banner / panoramic |
| `1x1` | Square crop |

### Width Values

| Width | Approximate Output | Recommended For |
|---|---|---|
| `414x` | ~414 px | Mobile thumbnail |
| `828x` | ~828 px | HiDPI mobile / web card |
| `1080x` | ~1080 px | Full HD screen display |
| `1920x` | ~1920 px | Presentations / slides |
| `2400x` | ~2400 px | Large format print |
| `3000x` | ~3000 px | High-res download (recommended) |

> The API renders images on-the-fly. If a width exceeds the native asset resolution, it returns the native resolution without upscaling.

## Example URLs

### Thumbnail (as served on the press photos page)
```
https://www.basf.com/api/imaging/focalarea/4x3/414x/dam/jcr%3A8bf825f2-2537-3833-8079-40e9fca87fdb/1.1.jpg
```

### High-resolution download
```
https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3A8bf825f2-2537-3833-8079-40e9fca87fdb/1.1.jpg
```

### Widescreen crop at 1920px
```
https://www.basf.com/api/imaging/focalarea/16x9/1920x/dam/jcr%3A8bf825f2-2537-3833-8079-40e9fca87fdb/1.1.jpg
```

## How to Find JCR IDs

1. **Browser DevTools**: Open the press photos page → DevTools (F12) → Network tab → filter by `api/imaging` → look at image request URLs
2. **Page source**: Right-click → View Page Source → search for `api/imaging`
3. **Browser inspector**: Hover over image → right-click → Inspect → find the `src` attribute of the `<img>` tag

## Query Parameter: `vid`

Some URLs include a `?vid=...` cache-busting parameter:

```
https://www.basf.com/api/imaging/focalarea/16x9/414x/dam/jcr%3Ac213175a.../stage.jpg?vid=v1.zlJZ2iXdTdaZY1y1YZYhTB6Xu7mXj
```

This is optional for downloading — the URL works without it.

## URL Encoding

The colon in `jcr:` is URL-encoded as `%3A`. When passing URLs in shell scripts, quote them:

```bash
# Correct — quoted
curl -L -o photo.jpg "https://www.basf.com/api/imaging/focalarea/4x3/3000x/dam/jcr%3Aabcd1234.../photo.jpg"

# Wrong — unquoted (shell interprets %3A incorrectly in some contexts)
curl -L -o photo.jpg https://www.basf.com/api/imaging/...
```

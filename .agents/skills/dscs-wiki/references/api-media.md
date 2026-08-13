# Media Operations API Reference

Detailed parameters and response schemas for DokuWiki media file operations.

**Base URL**: `https://wiki.ds.basf.net/lib/exe/jsonrpc.php`

All calls are `POST` with `Content-Type: application/json` and Basic Auth.

---

## core.getMedia

Download a media file's content as base64-encoded string.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `media` | string | Yes | Media file ID (e.g., `dscs:images:logo.png`) |
| `rev` | integer | No | Revision timestamp. Default: `0` (current) |

**Response:** `string` — base64-encoded file content.

**Example — download and decode:**

```bash
# Get base64 content
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getMedia" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"media": "dscs:images:diagram.png"}' | python3 -c "
import json, base64, sys
data = json.load(sys.stdin)
with open('/tmp/diagram.png', 'wb') as f:
    f.write(base64.b64decode(data['result']))
print('Saved to /tmp/diagram.png')
"
```

---

## core.getMediaInfo

Get metadata about a media file. Returns an error if the file doesn't exist.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `media` | string | Yes | Media file ID |
| `rev` | integer | No | Revision timestamp. Default: `0` |
| `author` | boolean | No | Include author info. Default: `false` |
| `hash` | boolean | No | Include MD5 hash. Default: `false` |

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Media ID |
| `revision` | integer | Last modified timestamp |
| `size` | integer | File size in bytes |
| `permission` | integer | Current user's permission level |
| `isimage` | boolean | Whether this is an image file |
| `hash` | string | MD5 hash (if requested) |
| `author` | string | Author (if requested) |

---

## core.saveMedia

Upload a file to the wiki. File data must be base64-encoded.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `media` | string | Yes | Media ID (e.g., `dscs:images:photo.jpg`) |
| `base64` | string | Yes | Base64-encoded file contents |
| `overwrite` | boolean | No | Overwrite existing file. Default: `false` |

**Response:** `boolean` — `true` on success.

**Example — upload a file:**

```bash
# Encode file to base64 and upload
B64=$(base64 < /path/to/image.png)
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.saveMedia" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d "{\"media\": \"dscs:images:image.png\", \"base64\": \"$B64\", \"overwrite\": true}"
```

For large files, use a temp file to avoid shell argument limits:

```bash
python3 -c "
import base64, json
with open('/path/to/image.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
payload = {'media': 'dscs:images:image.png', 'base64': b64, 'overwrite': True}
with open('/tmp/media_payload.json', 'w') as f:
    json.dump(payload, f)
"
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.saveMedia" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d @/tmp/media_payload.json
rm /tmp/media_payload.json
```

---

## core.deleteMedia

Delete a media file from the wiki.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `media` | string | Yes | Media file ID |

**Response:** `boolean` — `true` on success.

**Requirements:** Delete permission for the file. Will fail with error 232 if the media file is still referenced by pages.

---

## core.listMedia

List media files in a namespace.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `namespace` | string | No | Namespace to search. Empty = root. Default: `""` |
| `pattern` | string | No | PHP regex filter (including delimiters, e.g., `/\.png$/`). Default: `""` |
| `depth` | integer | No | Search depth. `0` = all. Default: `1` |
| `hash` | boolean | No | Include MD5 hashes. Default: `false` |

**Response:** Array of media info objects (same fields as `core.getMediaInfo`).

**Example — list all images in a namespace:**

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.listMedia" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "dscs:images", "depth": 0}'
```

---

## core.getMediaHistory

List available revisions of a media file.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `media` | string | Yes | Media file ID |
| `first` | integer | No | Skip first N entries. Default: `0` |

**Response:** Array of change objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Media ID |
| `revision` | integer | Revision timestamp |
| `author` | string | Author of the change |
| `ip` | string | IP address |
| `summary` | string | Change summary |
| `type` | string | Change type |
| `sizechange` | integer | Size change in bytes |

---

## core.getMediaUsage

Find pages that use a given media file.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `media` | string | Yes | Media file ID |

**Response:** `array` — list of page IDs that reference this media file.

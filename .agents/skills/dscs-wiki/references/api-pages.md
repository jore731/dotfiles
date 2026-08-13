# Page Operations API Reference

Detailed parameters and response schemas for DokuWiki page operations.

**Base URL**: `https://wiki.ds.basf.net/lib/exe/jsonrpc.php`

All calls are `POST` with `Content-Type: application/json` and Basic Auth.

---

## core.getPage

Get a wiki page's source syntax (DokuWiki markup).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Wiki page ID (e.g., `dscs:onboarding`) |
| `rev` | integer | No | Revision timestamp for older versions. Default: `0` (current) |

**Response:** `string` — the raw DokuWiki syntax of the page.

A non-existing page returns an empty string (or a template if configured). Use `core.getPageInfo` instead for existence checks.

**Example:**

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getPage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:onboarding"}'
```

---

## core.getPageHTML

Get a wiki page rendered as HTML. Returns only the page content HTML — no headers, footers, or navigation.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page ID |
| `rev` | integer | No | Revision timestamp. Default: `0` (current) |

**Response:** `string` — HTML content of the page.

Returns an error if the page does not exist.

---

## core.getPageInfo

Get metadata about a page. Returns an error if the page does not exist — use this for existence checks.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page ID |
| `rev` | integer | No | Revision timestamp. Default: `0` |
| `author` | boolean | No | Include author info. Default: `false` |
| `hash` | boolean | No | Include MD5 hash. Default: `false` |

**Response:**

```json
{
  "result": {
    "id": "dscs:onboarding",
    "revision": 1698917236,
    "size": 21393,
    "title": "Onboarding Guide",
    "permission": 255,
    "hash": "",
    "author": ""
  },
  "error": { "code": 0, "message": "success" }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Page ID |
| `revision` | integer | Last modified timestamp |
| `size` | integer | Page size in bytes |
| `title` | string | Page title (first heading) |
| `permission` | integer | Current user's permission level |
| `hash` | string | MD5 hash (if requested) |
| `author` | string | Author of this revision (if requested) |

---

## core.getPageHistory

List available revisions of a page.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page ID |
| `first` | integer | No | Skip first N changelog lines. Default: `0` |

**Response:** Array of revision objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Page ID |
| `revision` | integer | Revision timestamp |
| `author` | string | Author of the change |
| `ip` | string | IP address of the change |
| `summary` | string | Edit summary |
| `type` | string | Change type |
| `sizechange` | integer | Size change in bytes |

---

## core.savePage

Create, edit, or delete a wiki page. Saving empty text deletes the page.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page ID |
| `text` | string | Yes | Wiki text (empty string = delete) |
| `summary` | string | No | Edit summary. Default: `""` |
| `isminor` | boolean | No | Minor edit flag. Default: `false` |

**Response:** `boolean` — `true` on success.

**Requirements:** Write permission, page not locked by another user.

**Example — create/edit:**

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.savePage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d @- <<'PAYLOAD'
{
  "page": "dscs:new-page",
  "text": "====== New Page ======\n\nContent here.",
  "summary": "Created via API"
}
PAYLOAD
```

**Example — delete:**

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.savePage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:old-page", "text": "", "summary": "Deleted via API"}'
```

---

## core.appendPage

Append text to the end of a page. Creates the page if it doesn't exist.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page ID |
| `text` | string | Yes | Wiki text to append |
| `summary` | string | No | Edit summary. Default: `""` |
| `isminor` | boolean | No | Minor edit flag. Default: `false` |

**Response:** `boolean` — `true` on success.

---

## core.lockPages

Lock pages for editing. Prevents other users from editing while you hold the lock.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pages` | array | Yes | List of page IDs to lock |

**Response:** `array` — list of pages that were successfully locked.

Compare the returned list against your input to detect failed locks. Locking is not required before `savePage` (it auto-locks), but useful when editing multiple related pages.

---

## core.unlockPages

Unlock previously locked pages.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pages` | array | Yes | List of page IDs to unlock |

**Response:** `array` — list of pages that were successfully unlocked.

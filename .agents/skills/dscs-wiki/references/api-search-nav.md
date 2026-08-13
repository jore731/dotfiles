# Search & Navigation API Reference

Detailed parameters and response schemas for DokuWiki search, listing, and link operations.

**Base URL**: `https://wiki.ds.basf.net/lib/exe/jsonrpc.php`

All calls are `POST` with `Content-Type: application/json` and Basic Auth.

---

## core.searchPages

Full-text search across wiki page content. Uses DokuWiki search syntax.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Yes | Search query (DokuWiki search syntax) |

**Response:** Array of search result objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Page ID |
| `score` | integer | Number of hits |
| `snippet` | string | HTML snippet showing matches (first 15 results only) |
| `revision` | integer | Last modified timestamp |
| `size` | integer | Page size in bytes |
| `title` | string | Page title |
| `permission` | integer | User's permission level |

**Search syntax tips:**
- Simple words: `kubernetes deployment`
- Exact phrase: `"blue green deployment"`
- Namespace filter: `@dscs kubernetes` (search only in `dscs` namespace)
- Exclude: `-deprecated`

**Example:**

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.searchPages" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"query": "kubernetes @dscs"}'
```

---

## core.listPages

List all pages in a namespace (directory browsing). This is **not** a content search — use `core.searchPages` for that.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `namespace` | string | No | Namespace to list. Empty = root. Default: `""` |
| `depth` | integer | No | Depth to recurse. `0` = all levels. Default: `1` |
| `hash` | boolean | No | Include MD5 hashes. Default: `false` |

**Response:** Array of page info objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Page ID |
| `revision` | integer | Last modified timestamp |
| `size` | integer | Page size in bytes |
| `title` | string | Page title |
| `permission` | integer | User's permission level |
| `hash` | string | MD5 hash (if requested) |

> Note: Author info is not available in this call.

**Example — browse a namespace:**

```bash
# List top-level pages
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.listPages" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "", "depth": 1}'

# List all pages in dscs namespace recursively
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.listPages" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "dscs", "depth": 0}'
```

---

## core.getPageLinks

Get all outgoing links from a page (internal, external, and interwiki).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page ID |

**Response:** Array of link objects:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `internal`, `external`, or `interwiki` |
| `page` | string | Target page ID (or same as `href` for external) |
| `href` | string | Full URL to the target |

Duplicate links are returned if they appear multiple times on the page.

---

## core.getPageBackLinks

Get pages that link **to** the given page (backlinks).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page ID |

**Response:** `array` — list of page IDs that contain links to this page.

Only returns links from pages readable by the current user.

---

## core.getRecentPageChanges

Get recently changed pages.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `timestamp` | integer | No | Only changes newer than this Unix timestamp. Default: `0` |

**Response:** Array of change objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Page ID |
| `revision` | integer | Revision timestamp |
| `author` | string | Author |
| `ip` | string | IP address |
| `summary` | string | Edit summary |
| `type` | string | Change type |
| `sizechange` | integer | Size change in bytes |

**Example:**

```bash
# Changes in the last 24 hours
SINCE=$(python3 -c "import time; print(int(time.time()) - 86400)")
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getRecentPageChanges" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d "{\"timestamp\": $SINCE}"
```

---

## core.getRecentMediaChanges

Get recently changed media files. Same parameters and response format as `core.getRecentPageChanges`, but for media files.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `timestamp` | integer | No | Only changes newer than this Unix timestamp. Default: `0` |

**Response:** Array of change objects (same schema as page changes, but `id` is a media ID).

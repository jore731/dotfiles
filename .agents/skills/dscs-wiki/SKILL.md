---
name: dscs-wiki
description: >
  Interact with the DSCS Wiki (DokuWiki) via its JSON-RPC API. Read, search,
  create, edit, and delete wiki pages and media files, check permissions, and
  browse namespaces. Use when the user mentions the DSCS wiki, wiki.ds.basf.net,
  DokuWiki, or needs to look up, update, or publish content on the team wiki.
---

# DSCS Wiki (DokuWiki)

The DSCS Wiki is a DokuWiki instance at **https://wiki.ds.basf.net/**. This skill covers how to interact with it programmatically via the JSON-RPC API.

> **Important**: DokuWiki uses its own markup syntax, **not Markdown**. See [references/dokuwiki-syntax.md](references/dokuwiki-syntax.md) for the syntax reference when creating or editing pages.
>
> If the task is **converting DokuWiki markup to Markdown**, use the **doku-to-md** skill instead of doing it manually.

## Authentication

All API calls require authentication with **BASF UserID and password** via HTTP Basic Auth.

**Credential handling rules:**
- **Never hardcode credentials** — always prompt the user or read from environment variables
- **Never put credentials in URLs** — use the `Authorization` header
- **Never use verbose/debug flags** (`curl -v`, `--trace`) that would expose auth headers in output

```bash
# Prompt the user for credentials once, store in env vars for the session
# Ask the user for their BASF UserID and password before making any API calls
export WIKI_USER="<basf-userid>"
export WIKI_PASS="<password>"
```

## API Basics

### Endpoint

All calls go to a single endpoint via **POST**:

```
POST https://wiki.ds.basf.net/lib/exe/jsonrpc.php/<method>
```

The method name is appended as a path segment (e.g., `/core.getPage`).

### Calling Convention

This is the **simplified JSON-RPC** format — **not** the standard `{"jsonrpc":"2.0","method":...}` envelope. The method is in the URL path, and parameters are in the request body as a plain JSON object:

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getPage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "wiki:welcome"}'
```

### Response Format

Responses are always JSON with two fields:

```json
{
  "result": "...the actual data...",
  "error": { "code": 0, "message": "success" }
}
```

> **Always check the `error.code` field** — errors come back with HTTP 200. A non-zero code means the call failed. Do not rely on HTTP status or `curl` exit code alone.

### Shell-Safe JSON Payloads

For simple parameters, inline JSON works. For multiline wiki text or content with special characters, **use a heredoc or a temp file** to avoid shell quoting issues:

```bash
# Heredoc approach for multiline wiki text
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.savePage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d @- <<'PAYLOAD'
{
  "page": "dscs:my-page",
  "text": "====== My Page ======\n\nThis is the page content.\n\n  * Item one\n  * Item two",
  "summary": "Created page via API"
}
PAYLOAD
```

```bash
# Temp file approach for complex content
cat > /tmp/wiki_payload.json << 'EOF'
{
  "page": "dscs:my-page",
  "text": "====== My Page ======\n\nContent here.",
  "summary": "Updated via API"
}
EOF
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.savePage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d @/tmp/wiki_payload.json
rm /tmp/wiki_payload.json
```

## Bootstrap — Verify Connectivity

Before doing anything else, verify auth and connectivity:

```bash
# Test authentication
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.whoAmI" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{}'

# Check wiki version
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getWikiVersion" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Common Workflows

### Read a Page

Fetch the DokuWiki source syntax of a page:

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getPage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:onboarding"}'
```

To get the rendered HTML instead:

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getPageHTML" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:onboarding"}'
```

### Check if a Page Exists

Use `core.getPageInfo` — not `core.getPage` — for existence checks. A non-existing page returns an error, while `core.getPage` may return an empty string or template content:

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.getPageInfo" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:onboarding"}'
```

### Search for Pages

**Full-text search** (searches page content):

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.searchPages" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"query": "kubernetes deployment"}'
```

**List pages in a namespace** (browse structure):

```bash
# List all pages under the "dscs" namespace, 1 level deep
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.listPages" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "dscs", "depth": 1}'

# List ALL pages recursively (depth 0 = unlimited)
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.listPages" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "", "depth": 0}'
```

### Safe Edit Workflow

When editing an existing page, follow this sequence to avoid accidental data loss:

1. **Check existence and metadata:**
   ```bash
   curl -s -X POST ".../core.getPageInfo" \
     -u "$WIKI_USER:$WIKI_PASS" \
     -H "Content-Type: application/json" \
     -d '{"page": "dscs:my-page"}'
   ```

2. **Fetch current content:**
   ```bash
   curl -s -X POST ".../core.getPage" \
     -u "$WIKI_USER:$WIKI_PASS" \
     -H "Content-Type: application/json" \
     -d '{"page": "dscs:my-page"}'
   ```

3. **Modify the DokuWiki text** (remember: DokuWiki syntax, not Markdown)

4. **Save with a descriptive summary:**
   ```bash
   curl -s -X POST ".../core.savePage" \
     -u "$WIKI_USER:$WIKI_PASS" \
     -H "Content-Type: application/json" \
     -d @/tmp/wiki_payload.json
   ```

5. **Verify the save:**
   ```bash
   curl -s -X POST ".../core.getPageInfo" \
     -u "$WIKI_USER:$WIKI_PASS" \
     -H "Content-Type: application/json" \
     -d '{"page": "dscs:my-page"}'
   ```

> In the workflow above, `...` is shorthand for `https://wiki.ds.basf.net/lib/exe/jsonrpc.php`.

### Create a New Page

Creating a page is the same as saving — `core.savePage` creates the page if it doesn't exist:

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.savePage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:new-page", "text": "====== New Page ======\n\nContent here.", "summary": "Initial creation"}'
```

### Delete a Page

Deleting a page is done by **saving empty text** — there is no separate delete method for pages:

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.savePage" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:old-page", "text": "", "summary": "Deleted page"}'
```

### Check Permissions

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.aclCheck" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:onboarding"}'
```

## API Method Overview

Use **`core.*`** methods only. Avoid `wiki.*` and `dokuwiki.*` — they are legacy XML-RPC compatibility aliases.

| Method | Summary |
|--------|---------|
| **Pages** | |
| `core.getPage` | Get page source (DokuWiki syntax) |
| `core.getPageHTML` | Get page rendered as HTML |
| `core.getPageInfo` | Get page metadata (existence check) |
| `core.getPageHistory` | List page revisions |
| `core.savePage` | Create, edit, or delete (empty text) a page |
| `core.appendPage` | Append text to a page |
| `core.lockPages` | Lock pages for editing |
| `core.unlockPages` | Unlock pages |
| **Media** | |
| `core.getMedia` | Download media file (base64) |
| `core.getMediaInfo` | Get media file metadata |
| `core.saveMedia` | Upload media file (base64) |
| `core.deleteMedia` | Delete a media file |
| `core.listMedia` | List media in a namespace |
| `core.getMediaHistory` | List media revisions |
| `core.getMediaUsage` | Find pages using a media file |
| **Search & Navigation** | |
| `core.searchPages` | Full-text search across page content |
| `core.listPages` | List pages in a namespace (browse) |
| `core.getPageLinks` | Get outgoing links from a page |
| `core.getPageBackLinks` | Get pages linking to a page |
| `core.getRecentPageChanges` | Recent page changes |
| `core.getRecentMediaChanges` | Recent media changes |
| **ACL & System** | |
| `core.aclCheck` | Check permissions for a page/media |
| `core.whoAmI` | Info about authenticated user |
| `core.login` | Login (sets cookie — prefer Basic Auth) |
| `core.logoff` | Log off |
| `core.getWikiVersion` | DokuWiki version |
| `core.getWikiTitle` | Wiki title |
| `core.getAPIVersion` | API version number |

For detailed parameters, response schemas, and examples, see the reference files:
- [references/api-pages.md](references/api-pages.md) — Page operations
- [references/api-media.md](references/api-media.md) — Media operations
- [references/api-search-nav.md](references/api-search-nav.md) — Search and navigation
- [references/api-admin.md](references/api-admin.md) — ACL, auth, and system
- [references/dokuwiki-syntax.md](references/dokuwiki-syntax.md) — DokuWiki markup syntax

## Error Codes

### Framework Errors (all methods)

| Code | Meaning |
|------|---------|
| -32600 | Invalid request |
| -32601 | Method does not exist |
| -32602 | Wrong parameters |
| -32603 | Not authorized (no or invalid credentials) |
| -32604 | Forbidden (valid login, insufficient permissions) |
| -32605 | API not enabled in configuration |
| -32700 | Parse error (malformed JSON) |

### Content Errors (pages)

| Code | Meaning |
|------|---------|
| 111 | Not allowed to read this page |
| 121 | Page/revision does not exist |
| 131 | Empty or invalid page ID |
| 132 | Refusing to write empty new page |
| 133 | Page is locked |
| 134 | Page content was blocked |

### Content Errors (media)

| Code | Meaning |
|------|---------|
| 211 | Not allowed to read media file |
| 212 | Not allowed to delete media file |
| 221 | Media file/revision does not exist |
| 231 | Empty or invalid media ID |
| 232 | Media file still referenced |
| 233 | Failed to delete media file |
| 234 | Invalid base64 data |
| 235 | Empty file |
| 236 | Failed to save media |

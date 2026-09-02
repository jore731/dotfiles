## Public Read Patterns

Use these patterns when the target page or space is likely publicly readable.

## Fetch a Page by ID

Basic page metadata:

```bash
curl -sS -L "https://confluence.basf.net/rest/api/content/391850245"
```

Page body plus common metadata:

```bash
curl -sS -L \
  "https://confluence.basf.net/rest/api/content/391850245?expand=body.storage,space,version,metadata.labels"
```

Use `body.storage` when the user needs full content. Avoid large expansion sets
 unless they are actually needed.

## Browse a Space

List pages in a space:

```bash
curl -sS -L \
  "https://confluence.basf.net/rest/api/space/DSI/content/page?limit=25"
```

Increase `limit` or follow `_links.next` for pagination.

## Browse Page Trees

Child pages:

```bash
curl -sS -L \
  "https://confluence.basf.net/rest/api/content/391850245/child/page"
```

Descendants:

```bash
curl -sS -L \
  "https://confluence.basf.net/rest/api/content/391850245/descendant/page"
```

Use children for direct navigation. Use descendants for broader tree discovery.

## Pagination

Common list endpoints use `limit` and `start`:

```bash
curl -sS -L \
  "https://confluence.basf.net/rest/api/space/DSI/content/page?limit=25&start=25"
```

Prefer `_links.next` when available.

## What to Check in Responses

- `id`, `title`, `type`, `status`
- `_links.webui` for the human page URL
- `body.storage.value` for full page markup
- `metadata.labels.results` for page labels
- `version.number` and `version.when` for freshness
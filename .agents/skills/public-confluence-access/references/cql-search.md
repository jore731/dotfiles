## CQL Search Patterns

Use CQL when the page ID is unknown or when the user wants filtered discovery.

## Search Endpoint

```bash
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=DSI AND type=page'
```

## Common Queries

Find pages by title text:

```bash
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=DSI AND type=page AND title ~ "Azure AD"'
```

Find pages by full-text match:

```bash
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=DSI AND type=page AND text ~ "service desk"'
```

Find pages by label:

```bash
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=DSI AND label = entraid'
```

Find descendants of an ancestor page:

```bash
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=ancestor = 391850245 AND type = page'
```

Find recently modified pages:

```bash
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=DSI AND type=page AND lastmodified >= now("-4w") ORDER BY lastmodified DESC'
```

## Useful Fields

- `space`
- `type`
- `title`
- `text`
- `label`
- `ancestor`
- `created`
- `lastmodified`

## Operator Guidance

- Use `=` for exact matching.
- Use `~` for fuzzy or text matching.
- Use `IN` for multiple values.
- Use `ORDER BY` for stable result ordering.
- Use parentheses when mixing `AND` and `OR`.

## Response Checks

Check:

- `results[]`
- `size`
- `totalSize`
- `_links.self`
- `_links.next` when pagination applies
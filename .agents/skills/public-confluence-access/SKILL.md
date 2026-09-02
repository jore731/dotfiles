---
name: public-confluence-access
description: >
  Use when reading or searching public Confluence content through the Confluence
  REST API. Triggers include requests like "search Confluence", "read this
  Confluence page", "find pages in a space", "use CQL", "browse Confluence
  children or descendants", or "check whether a Confluence page is publicly
  readable". Covers public-first access and an auth-ready transition when public
  access is not enough.
author: Daniel Kaesmayr
metadata:
  category: knowledge-access
  version: "1.0.0"
---

# Public Confluence Access

Read and search publicly accessible Confluence content through the Confluence
Data Center REST API, then switch to authenticated patterns only when the public
path is insufficient.

## When to Use This Skill

- The user wants to fetch a Confluence page by URL or page ID.
- The user wants to search Confluence using CQL.
- The user wants to browse a space, child pages, or descendants.
- The user wants to verify whether Confluence content is publicly readable.
- The user may later need authenticated access, but the first step should stay
  read-only and public-first.

## Default Workflow

1. Identify the task shape: page fetch, space browse, or CQL search.
2. Try the public REST endpoint first.
3. Use the smallest useful `expand` set.
4. If the page is unknown, use CQL to locate it.
5. If the response indicates restricted access, move to the auth-ready
   guidance in [auth-transition.md](./references/auth-transition.md).

## Public-First Rules

- Prefer `GET /rest/api/content/{id}` for known pages.
- Prefer `GET /rest/api/content/search?cql=...` when the page ID is unknown.
- Prefer `expand=body.storage` when the user needs full page content.
- Add `space`, `version`, or `metadata.labels` only when they are needed.
- Treat `401`, `403`, redirects, or anonymous-user responses as signals for an
  authentication check, not as proof the API does not exist.

## References

- Public read patterns:
  [public-read.md](./references/public-read.md)
- CQL search patterns:
  [cql-search.md](./references/cql-search.md)
- Auth-ready escalation:
  [auth-transition.md](./references/auth-transition.md)

## BASF-Verified Pattern

On BASF Confluence Data Center, public endpoints can return JSON directly for
publicly readable content such as:

```text
https://confluence.basf.net/rest/api/content/{pageId}?expand=body.storage,space,version,metadata.labels
https://confluence.basf.net/rest/api/content/search?cql=space=DSI AND type=page
```

Start there before assuming credentials are required.

## Boundaries

- This skill focuses on public read and search access.
- It does not cover content creation, updates, or attachment management.
- It does not assume a PAT or password is available.
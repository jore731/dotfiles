---
name: tech-docs
description: >-
  Navigate and research technical documentation sites, API references, and local
  markdown files with auto-detection of doc frameworks (Docusaurus, ReadTheDocs,
  MkDocs, OpenAPI). Use when asked to look up docs, research an API, find usage
  examples, explain a library feature, or answer questions from technical
  documentation.
---

# Tech Docs

Research assistant for technical documentation. Follows a 3-phase workflow:

1. **Identify & Fetch** — classify source (web/local), auto-detect doc framework, fetch entry page
2. **Map & Navigate** — extract ToC/sidebar, guided-crawl only relevant pages (max 5-10)
3. **Synthesize & Answer** — summarize with code snippets, cite sources, note doc version

## Quick Reference

| Source type | Tool | When |
|-------------|------|------|
| Web doc page | `defuddle` | HTML pages (strips clutter, saves tokens) |
| Raw `.md` URL | `web_fetch` | Already markdown — no conversion needed |
| OpenAPI spec | `web_fetch` | JSON/YAML endpoints |
| Local files | `view`, `grep`, `glob` | Files on disk |

## Doc Framework Detection

See [DOC-TYPES.md](references/DOC-TYPES.md) for detailed per-framework detection and navigation strategies.

## Fallback When Blocked

If a page is inaccessible:
- Try the GitHub source repo (most doc sites publish from a repo)
- Look for raw markdown in the repo
- Check CLI help (`--help`, `man` pages)
- Suggest the user provide a different URL or check auth

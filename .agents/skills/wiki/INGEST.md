# Ingest Workflow

**Trigger:** "ingest", "add to wiki", "process this source", "ingest clippings", "process clippings", or user provides raw content to capture.

> [!IMPORTANT]
> **`_raw/` is immutable.** Never create, edit, rename, or delete files in `_raw/`. The only exception is *moving* files into `_raw/` during initial capture. All wiki output (summaries, cross-references, tags) goes into `wiki/` — never back into the raw source.

## Sources

Ingest can process two kinds of raw material:

### A. On-demand capture

The user provides a URL, paste, or file to ingest. Save verbatim to `_raw/<descriptive-name>.md` with frontmatter:
```yaml
---
created: "YYYY-MM-DD"
tags: [source/article]
source: "URL or origin"
---
```
Once saved, **never modify** the raw file. If the source is a web page, use the `defuddle` skill to extract clean markdown first.

### B. Web Clipper queue

The Obsidian Web Clipper browser extension saves pages to `_raw/` automatically. These files already have frontmatter (`title`, `source`, `created`, `tags: [clippings]`).

**Pre-flight check:** If a `Clippings/` directory exists at the vault root (`~/secondbrain/Clippings/`), the Web Clipper is misconfigured. Stop and tell the user:
> ⚠️ Found `Clippings/` at vault root — the Web Clipper is saving to the wrong location.
> Open the Web Clipper extension → **Settings → Templates → Default → Note location** and change it to `_raw`.

Then move all files from `Clippings/` into `_raw/` and continue with ingestion.

**To ingest clippings:**
1. List unprocessed clippings: files in `_raw/` tagged `clippings` that have **no** corresponding `wiki/sources/` page.
2. Process each clipping using the steps below (starting at step 2). **Do not modify the clipping file itself.**
3. When creating the source summary in `wiki/sources/`, set `source: "[[_raw/<filename>]]"`.

## Steps

1. **Capture raw source** (skip for Web Clipper clippings — already in `_raw/`) → save verbatim to `_raw/<descriptive-name>.md` with frontmatter as described in Source A above.
   Once saved, **never modify** the raw file. If the source is a web page, use the `defuddle` skill to extract clean markdown first.

2. **Discuss with the user** — summarize the key takeaways from the source and confirm which concepts/entities are most relevant before writing wiki pages.

3. **Write source summary** → create `wiki/sources/<descriptive-name>.md`:
   ```yaml
   ---
   created: "YYYY-MM-DD"
   tags: [source/article, concept/relevant-topic]
   source: "[[_raw/descriptive-name]]"
   ---
   ```
   Include: one-paragraph summary, key takeaways as bullet points, `[[wikilinks]]` to related wiki pages.

4. **Update concept and entity pages** — identify 10–15 relevant pages across the wiki:
   - **Existing pages:** append new information with a citation back to the source (`[[source-name]]`)
   - **New pages needed:** create stub pages in the correct directory with proper frontmatter and tags. A stub has a title, one-sentence description, and links to the source that prompted creation.
   - Use judgement — not every mention needs its own page. Create stubs for concepts/tools mentioned substantively.

5. **Update `wiki/index.md`** — add entries for all new pages under the correct sections.

6. **Append to `wiki/log.md`:**
   ```
   ## [YYYY-MM-DD] ingest | <Source Title>
   ```

## Quality Checks

- Every new page has `created`, `tags`, and `source` frontmatter
- All tags follow the hierarchical taxonomy
- All new pages are listed in `wiki/index.md`
- Cross-references use `[[wikilinks]]`, not plain text

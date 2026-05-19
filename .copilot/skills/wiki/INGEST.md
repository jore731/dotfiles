# Ingest Workflow

**Trigger:** "ingest", "add to wiki", "process this source", or user provides raw content to capture.

## Steps

1. **Capture raw source** → save verbatim to `_raw/<descriptive-name>.md` with frontmatter:
   ```yaml
   ---
   created: "YYYY-MM-DD"
   tags: [source/article]
   source: "URL or origin"
   ---
   ```
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

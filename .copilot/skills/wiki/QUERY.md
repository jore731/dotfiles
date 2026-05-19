# Query Workflow

**Trigger:** "query my wiki", "wiki search", "what do I know about X", or knowledge questions that the wiki might answer.

## Steps

1. **Read `wiki/index.md`** to find relevant pages.

2. **Drill into pages** — read the relevant wiki pages, follow `[[wikilinks]]` for context. Read multiple pages in parallel when possible.

3. **Synthesize answer** — combine information with `[[wikilink]]` citations to real wiki pages. Every claim should trace back to a specific page.

4. **Assess filing** — if the answer produced new insight (a comparison, analysis, synthesis, or new connection between concepts), ask the user whether to file it back into the wiki.

5. **File back** (if approved):
   - Save to `wiki/summaries/<descriptive-name>.md` (for cross-cutting answers) or the appropriate `wiki/concepts/` or `wiki/entities/` directory (for topic-specific answers)
   - Frontmatter:
     ```yaml
     ---
     created: "YYYY-MM-DD"
     tags: [concept/relevant-topic]
     source: "query"
     ---
     ```
   - Update `wiki/index.md` with the new entry
   - Append to `wiki/log.md`:
     ```
     ## [YYYY-MM-DD] query | <brief description>
     ```

6. **If the wiki lacks information**, say so honestly. Don't fabricate wiki content. Suggest an ingest if external sources could fill the gap.

## Output Formats

Depending on the question, answers may be:
- Prose summary with citations
- Comparison table
- Bullet-point list of key findings
- Marp slide deck (use `obsidian-markdown` skill for syntax)

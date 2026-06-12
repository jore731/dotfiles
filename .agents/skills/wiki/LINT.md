# Lint Workflow

**Trigger:** "lint the wiki", "wiki health check", "check wiki consistency".

## Steps

1. **Scan for issues** (read all wiki pages and index):

   **Auto-fixable (fix immediately):**
   - Orphan pages — wiki pages not listed in `wiki/index.md`
   - Missing frontmatter — pages lacking `created`, `tags`, or `source` fields
   - Non-hierarchical tags — flat tags that violate the taxonomy
   - Pages in wrong directories — e.g., a tool page in `concepts/` instead of `entities/tools/`
   - Broken wikilinks — `[[target]]` where target doesn't exist (remove or create stub)

   **Report to user (don't auto-fix):**
   - Contradictions — conflicting claims across pages (LLM-judged)
   - Stale claims — information likely superseded by newer sources
   - Data gaps — topics where a web search would fill missing context
   - Ambiguous categorization — pages that could belong in multiple categories

2. **Entity stub detection** — scan for concepts/tools/orgs mentioned ≥3 times across pages that lack their own wiki page. Create stubs with:
   ```yaml
   ---
   created: "YYYY-MM-DD"
   tags: [entity/tool/name]
   source: "lint-stub"
   ---
   ```
   Stubs contain: title, one-sentence description, backlinks to pages that mention the entity.

3. **Apply auto-fixes** — fix all safe issues, add new stubs to `wiki/index.md`.

4. **Report** — present unfixable issues to the user as a checklist.

5. **Append to `wiki/log.md`:**
   ```
   ## [YYYY-MM-DD] lint | <N> fixed, <M> reported for review
   ```

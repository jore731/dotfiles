# Cross-link Workflow

**Trigger:** "cross-link wiki", "link wiki pages", "add wikilinks".

## Steps

1. **Scan wiki pages** for plain-text mentions of other wiki page titles or known aliases.

2. **Insert `[[wikilinks]]`** where plain text references exist — e.g., if a page mentions "ArgoCD" and `wiki/entities/tools/argocd.md` exists, replace with `[[argocd|ArgoCD]]`.

3. **Link to references** — connect wiki concept/entity pages to relevant `wiki/references/dscs-wiki/` pages where the same topic is covered.

4. **Skip already-linked mentions** — don't double-wrap existing wikilinks.

5. **Update `wiki/index.md`** if any new pages were created during the process.

6. **Append to `wiki/log.md`:**
   ```
   ## [YYYY-MM-DD] cross-link | <N> links added across <M> pages
   ```

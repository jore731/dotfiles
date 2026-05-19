---
name: wiki
description: >-
  Maintain the LLM wiki at ~/secondbrain. Use when the user says "ingest",
  "query my wiki", "lint the wiki", "wiki search", "add to wiki",
  "cross-link wiki", or asks to read/write knowledge pages, update the
  index, or process raw sources. Works from any working directory.
---

# Wiki Skill

Operate the three-layer LLM wiki inside the Obsidian vault at `~/secondbrain`.

```
Layer 3  Schema    → this skill, _profile.md, copilot-instructions
Layer 2  Wiki      → wiki/ (LLM-maintained compiled knowledge)
Layer 1  Raw       → _raw/ (immutable source material)
```

Three core operations: **Ingest**, **Query**, **Lint**, **Cross-link**.

---

## Vault Schema

```
~/secondbrain/
├── _raw/                     # Immutable sources (never modify after creation)
├── wiki/
│   ├── index.md              # Master catalog — always read first
│   ├── log.md                # Append-only operation log
│   ├── concepts/             # Technical knowledge (concept/X tags)
│   │   └── <topic>/          # Group by domain (e.g., homelab/, crossplane/)
│   ├── entities/
│   │   ├── tools/            # entity/tool/X
│   │   ├── orgs/             # entity/org/X
│   │   └── persons/          # entity/person/X
│   ├── sources/              # Summaries of ingested raw sources
│   ├── summaries/            # Answers filed back from queries
│   ├── projects/             # Project documentation (project/X)
│   └── references/
│       └── dscs-wiki/        # Synced DSCS wiki mirror
├── daily/                    # Daily notes (daily tag)
├── inbox/                    # Triage area
├── research/                 # Deep research reports
├── templates/                # Note and daily templates
├── _profile.md               # User profile with managed sections
└── CONTEXT.md                # Project context and issue tracker
```

### File Naming

- Lowercase kebab-case: `aks-networking-gotchas.md`
- No spaces, no uppercase
- Wiki pages go in the appropriate subdirectory by type

### Frontmatter (mandatory on every wiki page)

```yaml
---
created: "YYYY-MM-DD"
tags: [concept/kubernetes, project/homelab]   # hierarchical, from taxonomy
source: ""                                     # origin reference if applicable
---
```

---

## Tag Taxonomy

| Prefix | Meaning | Example |
|--------|---------|---------|
| `concept/X` | Technical knowledge, patterns, runbooks | `concept/kubernetes` |
| `entity/tool/X` | Specific tools and frameworks | `entity/tool/argocd` |
| `entity/org/X` | Organizations | `entity/org/basf` |
| `entity/person/X` | People | `entity/person/karpathy` |
| `project/X` | Project documentation | `project/homelab` |
| `source/TYPE` | Raw source classification | `source/article` |
| `daily` | Daily journal entries | `daily` |

**Rules:** Always hierarchical (no flat tags except `daily`). Lowercase kebab-case. Multiple tags allowed. See `wiki/concepts/tag-taxonomy.md` for full reference.

---

## Operation 1: Ingest

**Trigger:** "ingest", "add to wiki", "process this source", or user provides raw content to capture.

**Workflow:**

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

**Quality checks before finishing:**
- Every new page has `created`, `tags`, and `source` frontmatter
- All tags follow the hierarchical taxonomy
- All new pages are listed in `wiki/index.md`
- Cross-references use `[[wikilinks]]`, not plain text

---

## Operation 2: Query

**Trigger:** "query my wiki", "wiki search", "what do I know about X", or knowledge questions that the wiki might answer.

**Workflow:**

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

**Output formats:** Depending on the question, answers may be:
- Prose summary with citations
- Comparison table
- Bullet-point list of key findings
- Marp slide deck (use `obsidian-markdown` skill for syntax)

---

## Operation 3: Lint

**Trigger:** "lint the wiki", "wiki health check", "check wiki consistency".

**Workflow:**

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

---

## Operation 4: Cross-link

**Trigger:** "cross-link wiki", "link wiki pages", "add wikilinks".

**Workflow:**

1. **Scan wiki pages** for plain-text mentions of other wiki page titles or known aliases.

2. **Insert `[[wikilinks]]`** where plain text references exist — e.g., if a page mentions "ArgoCD" and `wiki/entities/tools/argocd.md` exists, replace with `[[argocd|ArgoCD]]`.

3. **Link to references** — connect wiki concept/entity pages to relevant `wiki/references/dscs-wiki/` pages where the same topic is covered.

4. **Skip already-linked mentions** — don't double-wrap existing wikilinks.

5. **Update `wiki/index.md`** if any new pages were created during the process.

6. **Append to `wiki/log.md`:**
   ```
   ## [YYYY-MM-DD] cross-link | <N> links added across <M> pages
   ```

---

## Profile Conventions

The file `~/secondbrain/_profile.md` contains user context with managed sections.

**Reading:** Read `_profile.md` when you need user context (identity, tooling, goals, vetoes).

**Updating:** When you observe new patterns (new tools adopted, goals changed, new vetoes), update the content _inside_ the relevant managed section delimiters:
- `<!-- managed:identity:start -->` ... `<!-- managed:identity:end -->`
- `<!-- managed:tooling:start -->` ... `<!-- managed:tooling:end -->`
- `<!-- managed:goals:start -->` ... `<!-- managed:goals:end -->`
- `<!-- managed:vetoes:start -->` ... `<!-- managed:vetoes:end -->`

**Never modify content outside managed blocks** — that's human-owned.

---

## Conventions

- **Always read `wiki/index.md` first** before any wiki operation
- **Always update both `wiki/index.md` and `wiki/log.md`** after mutations — no exceptions
- **Use `[[wikilinks]]`** for cross-references between pages
- **`_raw/` is immutable** — read but never modify after creation
- **Frontmatter is mandatory** — `created`, `tags`, `source` on every wiki page
- **Tags follow the hierarchy** — see taxonomy table above
- **Start lean** — don't over-engineer pages; add detail as knowledge compounds
- **This skill works from any directory** — always use absolute paths (`~/secondbrain/...`)

---

## Related Skills

| Skill | Use for |
|-------|---------|
| `obsidian-markdown` | Syntax reference for wikilinks, callouts, embeds, and frontmatter when writing wiki pages |
| `obsidian-cli` | Searching and reading vault content via the Obsidian REST API (requires Obsidian running) |
| `defuddle` | Cleaning web page content into markdown before ingesting into `_raw/` |

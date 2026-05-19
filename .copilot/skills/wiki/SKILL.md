---
name: wiki
description: >-
  Maintain the LLM wiki at ~/secondbrain. Use when the user says "ingest",
  "query my wiki", "lint the wiki", "wiki search", "add to wiki", or asks
  to read/write knowledge pages, update the index, or process raw sources.
  Works from any working directory.
---

# Wiki Skill

Operate the three-layer LLM wiki inside the Obsidian vault at `~/secondbrain`.

```
Layer 3  Schema    → this skill, _profile.md, copilot-instructions
Layer 2  Wiki      → wiki/ (LLM-maintained compiled knowledge)
Layer 1  Raw       → _raw/ (immutable source material)
```

Three core operations: **Ingest**, **Query**, **Lint**.

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
   Once saved, **never modify** the raw file.

2. **Create or update wiki pages:**
   - Write a source summary in `wiki/sources/<name>.md`
   - Create or update concept/entity pages in the appropriate directory
   - Use `[[wikilinks]]` to cross-reference related pages

3. **Update `wiki/index.md`** — add entries under the correct section with wikilinks.

4. **Append to `wiki/log.md`:**
   ```
   ## [YYYY-MM-DD] ingest | <brief description>
   ```

---

## Operation 2: Query

**Trigger:** "query my wiki", "wiki search", "what do I know about X", or knowledge questions that the wiki might answer.

**Workflow:**

1. **Read `wiki/index.md`** to find relevant pages.

2. **Drill into pages** — read the relevant wiki pages, follow wikilinks for context.

3. **Synthesize answer** — combine information with `[[wikilink]]` citations to source pages.

4. **File back substantive answers** — if the answer produced new insight or synthesis:
   - Save to `wiki/summaries/<descriptive-name>.md`
   - Update `wiki/index.md` with the new entry
   - Append to `wiki/log.md`:
     ```
     ## [YYYY-MM-DD] query | <brief description>
     ```

5. **If the wiki lacks information**, say so honestly. Don't fabricate wiki content.

---

## Operation 3: Lint

**Trigger:** "lint the wiki", "wiki health check", "check wiki consistency".

**Workflow:**

1. **Scan for issues:**
   - Orphan pages (not in `wiki/index.md`)
   - Broken wikilinks (target doesn't exist)
   - Missing frontmatter or tags
   - Non-hierarchical tags (violates taxonomy)
   - Pages in wrong directories (e.g., a tool page in `concepts/`)
   - Empty sections in `wiki/index.md`

2. **Auto-fix what's safe:**
   - Add missing pages to `wiki/index.md`
   - Fix missing frontmatter fields
   - Correct tag hierarchy violations
   - Move misplaced pages

3. **Report unfixable issues** to the user (e.g., contradictory content, ambiguous categorization).

4. **Append to `wiki/log.md`:**
   ```
   ## [YYYY-MM-DD] lint | <summary of fixes and remaining issues>
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

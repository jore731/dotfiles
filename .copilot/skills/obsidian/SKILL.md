---
name: obsidian
description: Use when the user asks to save notes, document learnings, capture ideas, write journal entries, or manage knowledge. Also use when the user mentions Obsidian, second brain, vault, or knowledge base. Do NOT use exclusively — prefer inline code comments for code-level docs and README files for project docs.
---

# Obsidian Second Brain Skill

Interact with the user's Obsidian vault at `~/secondbrain` — a git-synced knowledge base of plain markdown files.

## Vault Location

```
~/secondbrain
```

## Folder Structure

| Folder | Purpose |
|---|---|
| `wiki/` | LLM-maintained knowledge base — concepts, entities, sources, summaries, projects, references. See the `wiki` skill for full conventions |
| `_raw/` | Immutable source material — never modify after creation |
| `inbox/` | Quick captures — unprocessed thoughts, ideas, raw notes |
| `daily/` | Daily journal entries. Format: `YYYY-MM-DD.md` |
| `research/` | Deep research reports |
| `templates/` | Note and daily templates |
| `_profile.md` | User profile with managed sections (identity, tooling, goals, vetoes) |

## How to Create Notes

1. **Determine the right folder** based on the note type:
   - Knowledge, runbooks, reference → `wiki/` (use the `wiki` skill for placement and conventions)
   - Raw source material → `_raw/` (immutable after creation)
   - Quick capture or unprocessed → `inbox/`
   - Daily log → `daily/YYYY-MM-DD.md`

2. **Use frontmatter** for metadata:
   ```markdown
   ---
   created: "2025-01-15"
   tags: [concept/kubernetes]
   source: ""
   ---
   ```

3. **Use backlinks** to connect related notes: `[[other-note]]`

4. **File naming**: Use lowercase with hyphens (e.g., `aks-networking-gotchas.md`)

## When to Use Obsidian vs Other Documentation

| Use Obsidian for | Use something else for |
|---|---|
| Personal learnings and insights | Project READMEs (keep in the repo) |
| Meeting notes and summaries | Code-level documentation (inline comments, docstrings) |
| Research and investigation notes | API documentation (OpenAPI specs, auto-generated docs) |
| Architecture decision records | Git commit messages |
| Troubleshooting runbooks | Pull request descriptions |
| Ideas and brainstorming | Configuration comments |

## Guidelines

- **Don't duplicate** — if a project has its own docs, link to them rather than copying content into the vault.
- **Tag consistently** — use hierarchical tags from the taxonomy (`concept/X`, `entity/tool/X`, `project/X`, etc.). See `wiki/concepts/tag-taxonomy.md`.
- **Keep notes atomic** — one concept per note in `wiki/`. Use backlinks to connect.
- **Process the inbox** — notes in `inbox/` are temporary. Move them to the right folder once processed.
- **The vault is git-synced** — changes are auto-committed and pushed via the Obsidian Git plugin when Obsidian is running.

## Obsidian Markdown

Use the `obsidian-markdown` skill for syntax reference when creating notes. Obsidian supports wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax.

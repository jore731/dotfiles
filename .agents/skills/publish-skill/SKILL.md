---
name: publish-skill
description: >
  Publish a new skill to the basf-global/skills repository via a GitHub pull
  request. Use when a user wants to contribute a skill they have written (or
  just finished writing) to the shared skills repository. Triggers on phrases
  like "publish this skill", "contribute my skill", "open a PR for this skill",
  "add skill to the skills repo", "submit skill to basf-global/skills".
author: Daniel Kaesmayr
metadata:
  category: meta
  version: "1.0.0"
---

# Publish Skill

End-to-end workflow for contributing a new skill to
[basf-global/skills](https://github.com/basf-global/skills) via GitHub PR.

## Pre-flight Checks

Before starting, confirm:

1. The skill folder exists locally and contains a valid `SKILL.md` with YAML
   frontmatter (`name`, `description`).
2. The skill has been tested in at least one real agent conversation.
3. No credentials, real substance data, or customer data are embedded in any
   skill file.

If any check fails, stop and ask the user to fix it first.

## Workflow

### Step 1 — Determine skill name and category

Read the skill's `SKILL.md` frontmatter to extract the `name`. Ask the user:

> Does this skill contain BASF-specific knowledge (branding, internal tools,
> confidential context), or is it general-purpose?

- BASF-specific → table: **BASF-Specific Skills**
- General-purpose → table: **Generic Skills by BASF Colleagues**

### Step 2 — Create a feature branch

```bash
cd /path/to/skills-repo
git checkout main && git pull
git checkout -b feature/<skill-name>
```

Replace `<skill-name>` with the skill folder name (e.g. `feature/sds-extraction`).

### Step 3 — Copy skill folder into the repo

If the skill was developed elsewhere, copy its folder into the repo root:

```bash
cp -r /path/to/skill-folder /path/to/skills-repo/<skill-name>
```

### Step 4 — Update README.md

Open `README.md` and make two additions:

#### 4a — Add a row to the correct skills table

Add to the appropriate table (BASF-Specific or Generic). Match the three-column
format introduced for `npx` install commands:

```markdown
| [skill-name](skill-name/SKILL.md) | One-line description. | `npx skills add basf-global/skills --skill skill-name` |
```

Use the description from `SKILL.md` frontmatter verbatim.

#### 4b — Add an entry to the Folder Structure section

Add a new entry in alphabetical order:

```markdown
├── skill-name/                ← short phrase describing what it does
│   ├── SKILL.md
│   └── references/            ← optional: reference files
```

### Step 5 — Stage, commit, and push

```bash
git add <skill-name>/ README.md
git commit -m "feat: add <skill-name> skill

<One or two sentences describing what the skill does and why it was added.>"
git push -u origin feature/<skill-name>
```

Commit message conventions:
- `feat:` — new skill
- `fix:` — correction to an existing skill
- `docs:` — documentation-only change

### Step 6 — Open a Pull Request

Use the GitHub MCP tool or the URL printed by `git push` to open the PR.

**With the GitHub MCP tool:**

```
Create a pull request on basf-global/skills:
  base: main
  head: feature/<skill-name>
  title: feat: add <skill-name> skill
  body: <see template below>
```

**PR body template:**

```markdown
## What this adds

<!-- One paragraph describing the skill and its intended use case. -->

## Skill category

- [ ] BASF-Specific Skills
- [ ] Generic Skills by BASF Colleagues

## Testing

<!-- Describe the conversation(s) in which you tested the skill. -->

## Checklist

- [ ] `SKILL.md` has valid YAML frontmatter (`name`, `description`)
- [ ] Tested in at least one real agent conversation
- [ ] README table row added to the correct section
- [ ] Folder Structure entry added to README
- [ ] No credentials, customer data, or substance data embedded
- [ ] Commit message follows `type: description` convention

Closes #<issue-number-if-applicable>
```

## Quality Checklist

Before calling the PR done, ensure all README changes are consistent:

- Table row description matches `SKILL.md` frontmatter `description` exactly.
- `npx` install command uses the correct skill folder name.
- Folder structure entry is in alphabetical order.
- Branch name is `feature/<skill-name>`.
- PR title is `feat: add <skill-name> skill`.

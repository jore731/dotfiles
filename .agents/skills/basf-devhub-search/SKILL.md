---
name: basf-devhub-search
description: >
  Answer questions about BASF DevHub by searching its GitHub-based documentation
  repositories. Covers user guides, AI Gateway, tutorials, platform architecture,
  onboarding, provisioning, CI/CD workflows, and internal team processes.
  Triggers: "how do I on DevHub", "DevHub documentation", "AI Gateway",
  "DevHub tutorial", "DevHub architecture", "create a product", "DevHub
  provisioning", "DevHub workflows", "DevHub troubleshooting", "DevHub modules",
  "DevHub getting started", "DevHub onboarding", "DevHub platform".
author: Daniel Kaesmayr
metadata:
  category: knowledge-access
  version: "1.0.0"
---

# BASF DevHub Search

Answer DevHub questions by searching the official GitHub documentation repos in
the `basf-global` org. Never copy entire repo contents — fetch only the specific
files needed to answer the question.

## Repository Map

Read [references/repo-map.md](references/repo-map.md) to understand which repo
and path to search. The map tells you where each topic lives.

## Workflow

### 1. Classify the Question

| Question type | Start with |
|---------------|------------|
| User how-to, guides, tutorials | `dh-user-docs` |
| AI Gateway (auth, models, access) | `dh-user-docs` → `docs/devhub/aigateway/` |
| Portal UI, Backstage templates | `dh-developer-portal` or `dh-portal-docs` |
| Internal team process, onboarding | `dh-internal-docs` |
| Architecture decisions (ADRs) | `devhub-architecture` → `decisions/` |
| Infrastructure, provisioning | `devhub-architecture`, `dh-provisioning-modules`, `dh-provisioning-stack` |
| CI/CD, GitHub Actions | `dh-workflows` |
| Platform entity registry | `dh-registry-platform-prod` |
| Pricing / tiers | `dh-user-docs` → `docs/devhub/tiers-and-charging/` |

### 2. Search

Use `mcp_github_search_code` to find relevant files:

```
mcp_github_search_code(query="<keywords> repo:basf-global/<repo-name>")
```

Narrow with `path:` when possible:

```
mcp_github_search_code(query="authentication repo:basf-global/dh-user-docs path:aigateway")
```

### 3. Fetch Content

Retrieve file contents via GitHub CLI:

```bash
gh api repos/basf-global/<repo>/contents/<path> --jq '.content' | base64 -d
```

Or use `mcp_github_get_file_contents`:

```
mcp_github_get_file_contents(owner="basf-global", repo="<repo>", path="<path>")
```

### 4. Answer

- Cite the source file path and repo
- Quote relevant sections directly
- Link to the GitHub file URL when helpful
- If the answer spans multiple repos, synthesise across them

## Repository Access Reference

All repos are private under `basf-global`. Requires GitHub authentication with
org access.

### Primary docs (search first)

| Repo | Purpose |
|------|---------|
| `dh-user-docs` | End-user DevHub documentation (Docusaurus, `docs/devhub/`) |
| `dh-internal-docs` | Internal team docs: onboarding, ways-of-working, glossary |
| `dh-portal-docs` | Platform documentation (legacy Docusaurus, `docs/`) |
| `dh-developer-portal` | Backstage portal application code |

### Secondary (infra/platform questions)

| Repo | Purpose |
|------|---------|
| `devhub-architecture` | ADRs, designs, operational docs |
| `dh-provisioning-modules` | Terraform/CDKTF provisioning modules |
| `dh-provisioning-stack` | End-to-end provisioning stack |
| `dh-workflows` | Reusable GitHub Actions workflows |
| `dh-registry-platform-prod` | Production platform entity registry |

## Tips

- `dh-user-docs` and `dh-portal-docs` overlap; prefer `dh-user-docs` as it is
  actively maintained with newer content (AI Gateway, MCP server tutorials).
- For "how do I get access" questions, check `aigateway/guides/managing-access.md`
  or `getting-started/prerequisites.md`.
- ADRs in `devhub-architecture/decisions/` are numbered; use filename search to
  find them by topic keyword.
- Internal processes (sprint ceremonies, team structure) live in
  `dh-internal-docs/ways-of-working/`.

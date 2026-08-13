# GitHub Provider

Instructions for retrieving pending work from GitHub.

## MCP Server Setup

**Server:** [github/github-mcp-server](https://github.com/github/github-mcp-server)

The GitHub MCP server is **available by default in Copilot CLI** — no installation needed. For other agents (Claude Code, etc.), configure it manually:

### Agent configuration (only needed outside Copilot CLI)

**Claude Code** (`claude_desktop_config.json` or project `.mcp.json`):
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Authentication

In Copilot CLI, the server uses the authenticated `gh` session — no extra token needed.

For other agents, a Personal Access Token (PAT) is required. Scopes:
- `repo` — access private repos, PRs, issues
- `read:org` — list org repos
- `workflow` — view workflow run status

For multiple accounts, use `gh auth switch --user <account>` before running queries (Copilot CLI) or configure separate MCP server entries with different tokens (other agents).

## Validation

Verify connectivity by running a lightweight query:

**Via MCP (Copilot CLI — already available):** Call `search_repositories` with `query: "user:<account>"` — should return repos.

**Via CLI:**
```bash
gh auth switch --user <account>
gh api user --jq '.login'
```

**Via API:**
```bash
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user --silent | jq .login
```

If validation fails, check:
- `gh auth status` shows the correct account is active
- Token (if used) is valid and has required scopes
- Account name is correct
- Network/proxy allows access to api.github.com

---

## Authentication

Follow the `login_method` from the config. Common patterns:
- `gh auth switch --user <account>` — switch GitHub CLI identity
- MCP server already authenticated — no action needed

## Method 1: GitHub MCP Server (Preferred)

**Server:** [github/github-mcp-server](https://github.com/github/github-mcp-server)

### PRs authored by me (waiting for review)

Use `search_pull_requests`:
```
query: "author:<account> is:open"
```

### PRs where I'm requested as reviewer

Use `search_pull_requests`:
```
query: "review-requested:<account> is:open"
```

### Issues assigned to me

Use `search_issues`:
```
query: "assignee:<account> is:open"
```

### CI failures on my branches

For each open PR authored by me, use `pull_request_read` with `method: get_check_runs` to get CI status. Filter to failed check runs.

Alternatively, use `actions_list` with `method: list_workflow_runs` filtered by `status: completed` and check for failures on the user's branches.

---

## Method 2: GitHub CLI (`gh`)

### PRs authored

```bash
gh pr list --author <account> --state open --json number,title,repository,createdAt,reviewDecision
```

### PRs to review

```bash
gh pr list --search "review-requested:<account>" --state open --json number,title,repository,author,createdAt
```

### Issues assigned

```bash
gh search issues --assignee <account> --state open --json number,title,repository,labels,createdAt
```

### CI failures

```bash
gh run list --user <account> --status failure --limit 10 --json databaseId,headBranch,name,conclusion,createdAt,url
```

> **Note:** `gh` operates on one repo at a time for `pr list` / `run list`. For cross-repo queries, use `gh search` or iterate over known repos.

---

## Method 3: REST API (Last resort)

### Search PRs

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/issues?q=type:pr+author:<account>+state:open"
```

### Search issues

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/issues?q=type:issue+assignee:<account>+state:open"
```

### Check runs for a ref

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/<owner>/<repo>/commits/<ref>/check-runs"
```

---

## Data mapping

Map API/CLI output to dashboard columns:

| Dashboard field | GitHub source |
|----------------|---------------|
| # | `number` |
| Title | `title` |
| Repo | `repository.nameWithOwner` or `repository` |
| Created | `createdAt` (convert to relative time) |
| Status (PR) | `reviewDecision` + approval count |
| Priority (Issue) | Infer from labels (e.g., `priority/high`) |
| Labels | `labels[].name` |
| CI Error | `check_runs[].name` + `conclusion` |

# GitLab Provider

Instructions for retrieving pending work from GitLab.

## MCP Server Setup

**Server:** [zereight/gitlab-mcp](https://github.com/zereight/gitlab-mcp)
**npm package:** `@zereight/mcp-gitlab` (⚠️ note: the package name is `mcp-gitlab`, NOT `gitlab-mcp`)

### Installation

```bash
# Option 1: npx (no install needed)
npx @zereight/mcp-gitlab

# Option 2: npm global install
npm install -g @zereight/mcp-gitlab
```

### Agent configuration

Add to your agent's MCP config:

**Copilot CLI** (`~/.copilot/mcp-config.json`):

> ⚠️ **Important:** The Copilot CLI has issues resolving env vars for this package. Use CLI args (`--token`, `--api-url`) instead of env vars for reliable operation.

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "npx",
      "args": [
        "-y",
        "@zereight/mcp-gitlab",
        "--token=${YOUR_GITLAB_TOKEN_ENV_VAR}",
        "--api-url=https://gitlab.example.com/api/v4"
      ]
    }
  }
}
```

**Claude Code** (`claude_desktop_config.json` or project `.mcp.json`):
```json
{
  "mcpServers": {
    "gitlab": {
      "command": "npx",
      "args": ["-y", "@zereight/mcp-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "${GITLAB_TOKEN}",
        "GITLAB_API_URL": "https://gitlab.example.com/api/v4"
      }
    }
  }
}
```

### Authentication

The server uses a GitLab Personal Access Token. Required scopes:
- `read_api` — read access to API (MRs, issues, pipelines)
- `read_user` — read user info

**Key env var names** (these differ from what you might expect):
- `GITLAB_PERSONAL_ACCESS_TOKEN` — NOT `GITLAB_TOKEN`
- `GITLAB_API_URL` — NOT `GITLAB_URL`, and must include `/api/v4` suffix

For `gitlab.com`, set `GITLAB_API_URL` to `https://gitlab.com/api/v4`.
For self-hosted instances, set it to `https://<host>/api/v4`.

**CLI args** (recommended for Copilot CLI):
- `--token` — GitLab PAT (alternative to `GITLAB_PERSONAL_ACCESS_TOKEN`)
- `--api-url` — GitLab API URL with `/api/v4` (alternative to `GITLAB_API_URL`)
- `--read-only=true` — enable read-only mode
- `--use-wiki=true` — enable Wiki API
- `--use-pipeline=true` — enable Pipeline API

## Validation

After setup, verify connectivity:

**Via MCP:** Call a tool to list projects or user info — should return results.

**Via CLI:**
```bash
glab auth status
```

**Via API:**
```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "https://<host>/api/v4/user" --silent | jq .username
```

If validation fails, check:
- Token is valid and not expired
- Token has `read_api` scope
- `GITLAB_URL` points to the correct instance (include `https://`)
- Network allows access to the GitLab host

---

## Authentication

Follow the `login_method` from the config. Common patterns:
- GitLab MCP server authenticated via `GITLAB_TOKEN` env var
- `glab auth login` for the CLI
- Direct API token for REST calls

## Method 1: GitLab MCP Server (Preferred)

**Server:** [zereight/gitlab-mcp](https://github.com/zereight/gitlab-mcp)

### Merge Requests authored by me

Use the MCP tool to search for MRs where the current user is the author and state is `opened`.

### Merge Requests where I'm a reviewer

Use the MCP tool to search for MRs where the current user is listed as a reviewer.

### Issues assigned to me

Use the MCP tool to list issues assigned to the current user with state `opened`.

### Pipeline failures

Use the MCP tool to list pipelines with status `failed` for projects the user contributes to.

---

## Method 2: GitLab CLI (`glab`)

### MRs authored

```bash
glab mr list --author <account> --state opened
```

### MRs to review

```bash
glab mr list --reviewer <account> --state opened
```

### Issues assigned

```bash
glab issue list --assignee <account> --state opened
```

### Pipeline failures

```bash
glab ci list --status failed
```

> **Note:** `glab` operates on the current repo by default. Use `--repo` flag or iterate over repos for cross-project queries.

---

## Method 3: REST API (Last resort)

Base URL: `https://<host>/api/v4` (use `gitlab.com` if no custom host).

### MRs authored

```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://<host>/api/v4/merge_requests?author_username=<account>&state=opened&scope=all"
```

### MRs to review

```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://<host>/api/v4/merge_requests?reviewer_username=<account>&state=opened&scope=all"
```

### Issues assigned

```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://<host>/api/v4/issues?assignee_username=<account>&state=opened&scope=all"
```

### Pipeline failures

```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://<host>/api/v4/projects/<project_id>/pipelines?status=failed&per_page=5&order_by=updated_at"
```

---

## Data mapping

| Dashboard field | GitLab source |
|----------------|---------------|
| # | `iid` |
| Title | `title` |
| Repo | `project_id` → resolve via `/projects/:id` or `web_url` |
| Created | `created_at` (convert to relative time) |
| Status (MR) | `merge_status` + approvals count |
| Priority (Issue) | `labels` (look for priority labels) |
| Labels | `labels[]` |
| CI Error | `pipelines[].status` + stage/job name |

## GitLab-specific notes

- GitLab uses "Merge Requests" instead of "Pull Requests" — map both to the same dashboard section.
- The `scope=all` parameter is needed to search across all projects the user has access to.
- For self-hosted instances, replace `gitlab.com` with the configured `host` value.

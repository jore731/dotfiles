# Azure DevOps Provider

Instructions for retrieving pending work from Azure DevOps.

## MCP Server Setup

**Server:** [microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp)
**npm package:** `@azure-devops/mcp` (⚠️ note: package is `@azure-devops/mcp`, NOT `@microsoft/azure-devops-mcp`)

### Installation

```bash
# Option 1: npx (no install needed)
npx @azure-devops/mcp

# Option 2: Clone and run
git clone https://github.com/microsoft/azure-devops-mcp.git
cd azure-devops-mcp
npm install && npm run build
```

### Agent configuration

Add to your agent's MCP config:

> ⚠️ **Key differences from typical MCP configs:**
> - The org name is passed as a **positional argument** (just `"myorg"`, NOT a full URL)
> - Auth method is selected via `--authentication <method>` CLI flag
> - PAT auth expects `PERSONAL_ACCESS_TOKEN` env var containing **base64 of `email:pat`**

**Copilot CLI** (`~/.copilot/mcp-config.json`):
```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "npx",
      "args": [
        "-y",
        "@azure-devops/mcp",
        "myorg",
        "--authentication",
        "pat"
      ],
      "env": {
        "PERSONAL_ACCESS_TOKEN": "${MY_AZDO_PAT_B64}"
      }
    }
  }
}
```

**Claude Code** (`claude_desktop_config.json` or project `.mcp.json`):
```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "myorg", "--authentication", "pat"],
      "env": {
        "PERSONAL_ACCESS_TOKEN": "${MY_AZDO_PAT_B64}"
      }
    }
  }
}
```

### Authentication methods

The server supports multiple auth methods via `--authentication <method>`:

| Method | Flag | Env var | Notes |
|--------|------|---------|-------|
| **Interactive** (default) | `--authentication interactive` | none | Opens browser, device code flow |
| **Azure CLI** | `--authentication azcli` | none | Reuses `az login` session |
| **PAT** | `--authentication pat` | `PERSONAL_ACCESS_TOKEN` | base64 of `email:pat` |
| **Env var (Bearer)** | `--authentication envvar` | `PERSONAL_ACCESS_TOKEN` | Raw bearer token |

**PAT auth setup:**
1. Create a PAT at: `https://dev.azure.com/<org>/_usersSettings/tokens`
2. Encode as base64: `echo -n "your-email@example.com:your-pat" | base64`
3. Set the base64 string as `PERSONAL_ACCESS_TOKEN` env var

Required PAT scopes:
- **Work Items** — Read
- **Code** — Read (for PRs)
- **Build** — Read (for pipelines)
- **Project and Team** — Read

### Domain filtering (optional)

Limit which tool categories are loaded with `--domains`:
```
--domains core,work,repositories,pipelines
```

Available domains: `core`, `work`, `work-items`, `search`, `test-plans`, `repositories`, `wiki`, `pipelines`, `advanced-security`

## Validation

After setup, verify connectivity:

**Via MCP:** Call a tool to list projects in the org — should return results.

**Via CLI:**
```bash
az devops project list --org https://dev.azure.com/<org> --output table
```

**Via API:**
```bash
curl -u ":<PAT>" "https://dev.azure.com/<org>/_apis/projects?api-version=7.1" --silent | jq '.value[].name'
```

If validation fails, check:
- PAT is valid and not expired
- PAT has the required scopes listed above
- Organization URL is correct (include `https://dev.azure.com/`)
- User has access to the organization
- Network/proxy allows access to dev.azure.com

---

## Authentication

Follow the `login_method` from the config. Common patterns:
- Azure DevOps MCP server authenticated via PAT
- `az login` + `az devops configure --defaults organization=https://dev.azure.com/<org>`
- Direct PAT for REST calls

## Method 1: Azure DevOps MCP Server (Preferred)

**Server:** [microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp)

### Pull Requests authored by me

Use the MCP tool to query PRs created by the current user with status `active`.

### Pull Requests where I'm a reviewer

Use the MCP tool to query PRs where the current user is a required reviewer.

### Work Items assigned to me

Use the MCP tool to run a WIQL query:
```wiql
SELECT [System.Id], [System.Title], [System.State], [System.IterationPath]
FROM WorkItems
WHERE [System.AssignedTo] = @Me
  AND [System.State] <> 'Closed'
  AND [System.State] <> 'Done'
  AND [System.State] <> 'Removed'
ORDER BY [System.ChangedDate] DESC
```

### Pipeline failures

Use the MCP tool to list recent pipeline runs with result `failed`.

---

## Method 2: Azure CLI (`az`)

### PRs authored

```bash
az repos pr list --creator <account> --status active --org https://dev.azure.com/<org> --project <project> --output json
```

### PRs to review

```bash
az repos pr list --reviewer <account> --status active --org https://dev.azure.com/<org> --project <project> --output json
```

### Work Items assigned (via WIQL)

```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.IterationPath], [System.WorkItemType] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed' AND [System.State] <> 'Done' AND [System.State] <> 'Removed' ORDER BY [System.ChangedDate] DESC" --org https://dev.azure.com/<org> --project <project> --output json
```

### Pipeline failures

```bash
az pipelines runs list --pipeline-ids <id> --result failed --top 10 --org https://dev.azure.com/<org> --project <project> --output json
```

> **Note:** `az devops` commands require `--org` and `--project` flags unless defaults are configured.

---

## Method 3: REST API (Last resort)

Base URL: `https://dev.azure.com/<org>/<project>/_apis`

### PRs authored

```bash
curl -u ":<PAT>" \
  "https://dev.azure.com/<org>/<project>/_apis/git/pullrequests?searchCriteria.creatorId=<userId>&searchCriteria.status=active&api-version=7.1"
```

### Work Items (WIQL)

```bash
curl -X POST -u ":<PAT>" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT [System.Id] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> '\''Closed'\''"}' \
  "https://dev.azure.com/<org>/<project>/_apis/wit/wiql?api-version=7.1"
```

Then fetch details:
```bash
curl -u ":<PAT>" \
  "https://dev.azure.com/<org>/_apis/wit/workitems?ids=<id1>,<id2>&fields=System.Id,System.Title,System.State,System.IterationPath,System.WorkItemType&api-version=7.1"
```

### Pipeline runs

```bash
curl -u ":<PAT>" \
  "https://dev.azure.com/<org>/<project>/_apis/pipelines/runs?result=failed&$top=10&api-version=7.1"
```

---

## Data mapping

| Dashboard field | Azure DevOps source |
|----------------|---------------------|
| ID | `pullRequestId` / `System.Id` |
| Title | `title` / `System.Title` |
| Project | `project.name` |
| Created | `creationDate` / `System.CreatedDate` |
| State (Work Item) | `System.State` |
| Iteration | `System.IterationPath` (last segment) |
| Type | `System.WorkItemType` (Bug, Task, User Story) |
| Pipeline error | `run.name` + `result` + `finishedDate` |

## Azure DevOps-specific notes

- Azure DevOps has "Projects" within an "Organization". The config should specify both `org` and optionally `project`.
- If `project` is omitted, iterate over all projects in the org (use `az devops project list`).
- Work items use WIQL (Work Item Query Language) — a SQL-like syntax specific to Azure DevOps.
- PRs in Azure DevOps can have "required reviewers" and "optional reviewers" — surface required ones in the dashboard.

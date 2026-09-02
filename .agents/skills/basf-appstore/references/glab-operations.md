# glab CLI Operations for BASF App Store

Complete reference for managing App Store applications via the `glab` CLI.
All operations assume you're in the app's Git repository directory.

## Prerequisites

```bash
# Verify glab is installed
glab --version

# Authenticate with BASF GitLab
glab auth login --hostname gitlab.roqs.basf.net

# Verify authentication
glab auth status
```

## Pipeline Operations

### Watch & Monitor

```bash
# Interactive CI status view
glab ci status

# List recent development pipelines
glab ci list --ref development --per-page=10

# View pipeline in browser
glab ci view --web
```

### Trigger & Control

```bash
# Trigger new pipeline on development branch
glab pipeline run --branch development

# Trigger with variable override
glab pipeline run --branch development --variable "FORCE_REDEPLOY=true"

# Retry failed pipeline
glab ci retry

# Lint CI config before pushing
glab ci lint
```

### Read Job Logs

```bash
# Get latest pipeline ID
PIPELINE_ID=$(glab api "projects/:id/pipelines?ref=development&per_page=1" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")

# List all jobs in a pipeline
glab api "projects/:id/pipelines/${PIPELINE_ID}/jobs" | \
  python3 -c "
import json, sys
for j in json.load(sys.stdin):
    print(f'{j[\"id\"]:>10} | {j[\"name\"]:20} | {j[\"status\"]}')
"

# Read specific job trace (logs)
glab api "projects/:id/jobs/<JOB_ID>/trace"
```

## Environment Variable Management

### List Variables

```bash
# All K8S_ variables (formatted)
glab api "projects/:id/variables?per_page=100" | \
  python3 -c "
import json, sys
vars = json.load(sys.stdin)
k8s = [v for v in vars if v['key'].startswith('K8S_')]
for v in sorted(k8s, key=lambda x: x['key']):
    masked = '[MASKED]' if v['masked'] else v['value']
    print(f'{v[\"key\"]:50s} = {masked}')
"

# All variables (including non-K8S)
glab api "projects/:id/variables?per_page=100" | \
  python3 -c "
import json, sys
for v in sorted(json.load(sys.stdin), key=lambda x: x['key']):
    masked = '[MASKED]' if v['masked'] else v['value']
    scope = v.get('environment_scope', '*')
    print(f'{v[\"key\"]:50s} [{scope:>5}] = {masked}')
"
```

### Create Variable

```bash
# Add variable for all environments
glab api --method POST "projects/:id/variables" \
  --field key="K8S_ALL_MY_SETTING" \
  --field value="my-value" \
  --field masked="false" \
  --field protected="false"

# Add masked variable (for secrets)
glab api --method POST "projects/:id/variables" \
  --field key="K8S_ALL_API_TOKEN" \
  --field value="secret-token-value" \
  --field masked="true" \
  --field protected="false"

# Add dev-only variable
glab api --method POST "projects/:id/variables" \
  --field key="K8S_DEV_DEBUG" \
  --field value="true" \
  --field masked="false" \
  --field protected="false"
```

### Update Variable

```bash
glab api --method PUT "projects/:id/variables/K8S_DEV_MY_SETTING" \
  --field value="new-value"
```

### Delete Variable

```bash
glab api --method DELETE "projects/:id/variables/K8S_ALL_OLD_SETTING"
```

### Variable Naming Convention

```
K8S_<TIER>_<variable_name>
     │       │
     │       └── becomes the pod env var name (lowercased)
     └── ALL = all tiers, DEV/QUAL/PROD = specific tier
```

## Deploy Operations

### Force Restart (No Code Change)

```bash
git commit --allow-empty -m "chore: force pod restart"
git push origin development
```

### Undeploy (Manual Gate)

```bash
# Find and trigger undeploy job
PIPELINE_ID=$(glab api "projects/:id/pipelines?ref=development&per_page=1" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")

UNDEPLOY_JOB=$(glab api "projects/:id/pipelines/${PIPELINE_ID}/jobs" | \
  python3 -c "import json,sys; \
    [print(j['id']) for j in json.load(sys.stdin) if j['name'] == 'undeploy']")

glab api --method POST "projects/:id/jobs/${UNDEPLOY_JOB}/play"
```

### Rollback

```bash
# Quick rollback: revert commit
git revert HEAD
git push origin development

# Re-deploy from specific pipeline (replay deploy job)
JOB_ID=$(glab api "projects/:id/pipelines/<old_pipeline_id>/jobs" | \
  python3 -c "import json,sys; \
    [print(j['id']) for j in json.load(sys.stdin) if j['name'] == 'deploy']")

glab api --method POST "projects/:id/jobs/${JOB_ID}/retry"
```

## Debugging

### Check Deploy Job Output

```bash
# Stream the most recent deploy job log
PIPELINE_ID=$(glab api "projects/:id/pipelines?ref=development&per_page=1" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")

DEPLOY_JOB=$(glab api "projects/:id/pipelines/${PIPELINE_ID}/jobs" | \
  python3 -c "import json,sys; \
    [print(j['id']) for j in json.load(sys.stdin) if j['name'] == 'deploy']")

glab api "projects/:id/jobs/${DEPLOY_JOB}/trace"
```

### Diagnose Failed Pipelines

```bash
# List recent pipelines with status
glab api "projects/:id/pipelines?per_page=5" | \
  python3 -c "
import json, sys
for p in json.load(sys.stdin):
    print(f'{p[\"id\"]:>10} | {p[\"ref\"]:20} | {p[\"status\"]:12} | {p[\"created_at\"][:16]}')
"

# Find failed jobs in a pipeline
glab api "projects/:id/pipelines/<PIPELINE_ID>/jobs" | \
  python3 -c "
import json, sys
for j in json.load(sys.stdin):
    if j['status'] == 'failed':
        print(f'FAILED: {j[\"name\"]} (job {j[\"id\"]})')
"
```

### Check Container Registry

```bash
# List image tags for a service
glab api "projects/:id/registry/repositories" | \
  python3 -c "
import json, sys
for r in json.load(sys.stdin):
    print(f'{r[\"id\"]:>5} | {r[\"path\"]}')
"

# List tags for a specific repository
glab api "projects/:id/registry/repositories/<REPO_ID>/tags?per_page=10" | \
  python3 -c "
import json, sys
for t in json.load(sys.stdin):
    print(f'{t[\"name\"]:30} | {t[\"created_at\"][:16]}')
"
```

## Merge Request Workflow

### Create MR from Feature Branch

```bash
# Push feature branch
git push -u origin feature/my-change

# Create MR targeting development
glab mr create \
  --title "feat: add new endpoint" \
  --description "Adds /api/v2/new-endpoint for ..." \
  --target-branch development

# With reviewers and labels
glab mr create \
  --title "fix: resolve OOM issue" \
  --reviewer=colleague_id \
  --label="bug,infrastructure"
```

### Review MRs

```bash
# MRs assigned to you
glab mr list --assignee=@me

# MRs for you to review
glab mr list --reviewer=@me

# Checkout MR locally
glab mr checkout <mr-number>

# Approve
glab mr approve <mr-number>
```

## Issue Management

```bash
# Create issue
glab issue create --title "Bug: API returns 500" --label=bug

# List open issues
glab issue list

# Close issue
glab issue close <number>
```

## API Pagination

When results exceed one page, use `--paginate`:

```bash
# Auto-fetch all pages
glab api --paginate "projects/:id/pipelines?per_page=100"
```

**Important**: Pagination parameters go in the URL, not as flags:
```bash
# ✅ Correct
glab api "projects/:id/jobs?per_page=100"

# ❌ Wrong
glab api --per-page=100 projects/:id/jobs
```

## Quick Reference

| Action             | Command                                                                             |
| ------------------ | ----------------------------------------------------------------------------------- |
| Watch pipeline     | `glab ci status`                                                                    |
| List dev pipelines | `glab ci list --ref development`                                                    |
| Trigger deploy     | `glab pipeline run --branch development`                                            |
| Retry failed       | `glab ci retry`                                                                     |
| Lint CI config     | `glab ci lint`                                                                      |
| List K8S vars      | `glab api "projects/:id/variables?per_page=100"`                                    |
| Add variable       | `glab api --method POST "projects/:id/variables" --field key=... --field value=...` |
| Read job log       | `glab api "projects/:id/jobs/<id>/trace"`                                           |
| Force restart      | `git commit --allow-empty -m "chore: restart" && git push`                          |
| Create MR          | `glab mr create --title "..." --target-branch development`                          |
| Open in browser    | `glab repo view --web`                                                              |

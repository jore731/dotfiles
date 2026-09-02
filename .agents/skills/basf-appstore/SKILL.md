---
name: basf-appstore
description: >
  Create, deploy, and manage applications on the BASF App Store (ROQS) platform.
  Covers the full lifecycle: creating apps via the Happy Potter wizard, configuring
  the .appstore/ directory (deployment.yml, egress.yml, portal.md), GitLab CI/CD
  pipelines, environment variable management via K8S_ prefix convention, pod
  operations via glab CLI, three-tier deployment (dev/qa/prod), container
  configuration, and observability without kubectl.
  Use when asked to "create an app on the App Store", "deploy to ROQS",
  "configure .appstore/deployment.yml", "add egress rules", "manage K8S variables",
  "restart my app", "check pipeline status", "debug a failing deploy",
  "set up CI/CD for App Store", "add a container to my pod", "update resource limits",
  "configure environment variables", "Happy Potter wizard", "App Store portal".
author: Daniel Kaesmayr
metadata:
  category: platform-deployment
  version: "1.1.1"
---

# BASF App Store (ROQS) Platform

End-to-end workflow for creating, deploying, and operating applications on the
BASF App Store platform (app.roqs.basf.net). The App Store is a PaaS layer on
top of Kubernetes — developers have **no kubectl or SSH access**. All control
happens through **GitLab CI pipelines**, the **`.appstore/` config directory**,
and the **`glab` CLI**.

## Related Skills & Resources

| Resource                                                                                | Purpose                                                      |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `basf-devhub-search` skill                                                              | Search DevHub documentation for platform details             |
| `glab` CLI                                                                              | All pod operations, pipeline management, variable management |
| [DevHub Documentation](https://devhub.intranet.basf.com/documentation/)                 | Official platform docs                                       |
| [AppStore Blog](https://appstore.docs.basf.net/portal/app-store-blog/)                  | Platform updates and guides                                  |
| [AppStore Help](https://devhub.intranet.basf.com/documentation/appstore/add_or_create/) | Happy Potter wizard documentation                            |

> **DevHub Integration**: For detailed platform documentation beyond this skill,
> invoke the `basf-devhub-search` skill with your question. It searches the
> official DevHub repositories (`dh-user-docs`, `dh-portal-docs`, etc.) for
> authoritative answers.

## Platform Overview

| URL                              | Purpose                         |
| -------------------------------- | ------------------------------- |
| `https://app.roqs.basf.net`      | Production portal and app store |
| `https://app-qa.roqs.basf.net`   | QA / staging tier               |
| `https://app-dev.roqs.basf.net`  | Development tier                |
| `https://gitlab.roqs.basf.net`   | Source code and CI/CD           |
| `https://registry.roqs.basf.net` | Private container registry      |

## Architecture

```
Developer ──git push──► GitLab CI ──deploy job──► AppStore kubectl_wrapper
                                                        │
                                          .appstore/deployment.yml
                                          .appstore/egress.yml
                                          K8S_* CI variables
                                                        │
                                              Kubernetes Namespace
                                        ┌───────────────────────────┐
                                        │  Pod: <app-name>          │
                                        │  ┌──────┐  ┌───────────┐ │
                                        │  │svc A │  │  nginx    │ │
                                        │  └──────┘  └───────────┘ │
                                        │  ┌──────┐  ┌────────────┐│
                                        │  │svc B │  │  worker   ││
                                        │  └──────┘  └────────────┘│
                                        └───────────────────────────┘
```

**Key Constraints:**

- No `kubectl` access — all deploys run inside the CI `deploy` job
- No SSH/exec into pods — use health endpoints and CI job traces for logs
- No Kubernetes Dashboard — use `glab api` to query deployment history
- The AppStore's `kubectl_wrapper.py` handles kubeconfig, secrets, digest tracking

## Workflow

### Step 1 — Create the App (Happy Potter Wizard)

1. Open `https://app.roqs.basf.net/portal/add`
2. Click **"Create new application"**
3. The **Happy Potter 3.0** wizard has three steps:

#### Step 1: Info

- **GitLab Namespace**: Select your team or personal namespace (only namespaces you have access to are shown)
- **Application name**: Enter a "pretty name" — the wizard auto-generates:
  - GitLab repo: `https://gitlab.roqs.basf.net/<namespace>/<app-name>`
  - App Store URL: `https://app.roqs.basf.net/<app_name>`

#### Step 2: Modules

Select from **45+ pre-configured templates**:

| Category           | Templates                                                     |
| ------------------ | ------------------------------------------------------------- |
| **Python Web**     | FastAPI, Flask, Django, Flask-RESTX, Dash, Streamlit          |
| **JS/TS Web**      | React, Angular, Vue.js, Svelte, Nuxt 3, Express               |
| **Java/.NET**      | Spring Boot, ASP.NET                                          |
| **Data Science**   | Jupyter, JupyterLab, MLFlow, Gradio, TensorFlow Model Server  |
| **R**              | Shiny, Plumber, Shinypackage                                  |
| **Databases**      | PostgreSQL, MongoDB, Redis, Neo4j, MariaDB, ArangoDB, CouchDB |
| **Workflow**       | Airflow, Dagster                                              |
| **Publishing**     | Quarto Presentation, Quarto Report, VitePress Blog            |
| **Dev Tools**      | Code Server, pgAdmin, Python Library                          |
| **Graph/Semantic** | GraphExplorer, Fuseki, Virtuoso, Kuzu                         |

Use filters: **Name search**, **Team favorites** (recommended), **Hide unmaintained**

#### Step 3: Configuration

- **Kubernetes Persistent Volume**: Enable for stateful storage (databases, file uploads)
- **CCSP credentials**: Enable for GPU compute + global storage access
- **Nexus credentials**: Enable for publishing packages to Sonatype Nexus
- Module-specific configuration (varies by template)

4. Click **"Create application"** — this generates:
   - GitLab repository with scaffolded code
   - `.gitlab-ci.yml` with CI/CD pipeline
   - `.appstore/` directory with deployment manifests
   - App Store portal registration

### Step 2 — Clone and Develop

```bash
# Clone the generated repository
glab repo clone <namespace>/<app-name> --hostname gitlab.roqs.basf.net
cd <app-name>

# Or with git directly
git clone git@gitlab.roqs.basf.net:<namespace>/<app-name>.git
```

### Step 3 — Deploy

Push to the correct branch for your target tier:

```
git branch        → deployed tier          → URL
──────────────────────────────────────────────────────────────
development       → Development (dev)      → app-dev.roqs.basf.net/<app>/
main              → Quality Assurance (qa) → app-qa.roqs.basf.net/<app>/
release/x.y.z     → Production            → app.roqs.basf.net/<app>/
```

```bash
# Deploy to dev
git push origin development

# Watch pipeline
glab ci status
glab pipeline ci view
```

## The `.appstore/` Directory

This is your primary control surface for Kubernetes configuration.

| File             | Purpose                                                  | Edit?            |
| ---------------- | -------------------------------------------------------- | ---------------- |
| `deployment.yml` | Pod spec: containers, resources, ports, env vars, images | ✅ Yes           |
| `egress.yml`     | Outbound firewall rules (public + private hosts)         | ✅ Yes           |
| `portal.md`      | App description shown in the App Store portal            | ✅ Yes           |
| `README.md`      | AppStore documentation                                   | ❌ Do not modify |

### deployment.yml — Container Configuration

This is a standard Kubernetes Deployment manifest. Key sections:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: api
          image: registry.roqs.basf.net/<namespace>/<app>_backend
          ports:
            - containerPort: 5000
          env:
            - name: REQUESTS_CA_BUNDLE
              value: /etc/ssl/certs/ca-certificates.crt
            - name: SSL_CERT_FILE
              value: /etc/ssl/certs/ca-certificates.crt
          resources:
            limits:
              memory: "2500Mi" # Pod killed if exceeded (OOMKilled)
            requests:
              memory: "1500Mi" # Affects pod scheduling
          securityContext:
            runAsUser: 1000
            runAsGroup: 1000
```

**Image naming convention**: `registry.roqs.basf.net/<namespace>/<app>_<service>`

**Common patterns** (see [references/deployment-patterns.md](./references/deployment-patterns.md)):

- Multi-container pod (nginx + api + worker + redis)
- Sidecar pattern (redis cache alongside API)
- Resource tuning for OOMKilled prevention

### egress.yml — Firewall Rules

```yaml
# Public internet / cloud services
public:
  - host: api.example.com
    port: 443

# BASF intranet / private network
private:
  - host: 10.99.195.24
    port: 8080
```

Changes take effect on next deploy.

### portal.md — App Store Description

Markdown content displayed on the app's detail page in the App Store portal.
Update this to describe what your app does for users browsing the portal.

## Environment Variable Management (K8S\_ Convention)

The AppStore injects CI/CD variables prefixed with `K8S_` into pods as
environment variables. The prefix and tier suffix are stripped automatically.

| CI/CD Variable       | Pod Env Var | Scope     |
| -------------------- | ----------- | --------- |
| `K8S_ALL_REDIS_URL`  | `REDIS_URL` | All tiers |
| `K8S_DEV_API_TOKEN`  | `API_TOKEN` | Dev only  |
| `K8S_QUAL_API_TOKEN` | `API_TOKEN` | QA only   |
| `K8S_PROD_API_TOKEN` | `API_TOKEN` | Prod only |

Variables are stored in a Kubernetes Secret `envvars---<app>---<tier>` and
mounted into **all containers** automatically.

### Manage Variables with glab CLI

```bash
# List all K8S variables
glab api "projects/:id/variables?per_page=100" | \
  python3 -c "
import json, sys
vars = json.load(sys.stdin)
k8s = [v for v in vars if v['key'].startswith('K8S_')]
for v in sorted(k8s, key=lambda x: x['key']):
    masked = '[MASKED]' if v['masked'] else v['value']
    print(f'{v[\"key\"]:50s} = {masked}')
"

# Add new variable
glab api --method POST "projects/:id/variables" \
  --field key="K8S_ALL_MY_SETTING" \
  --field value="my-value" \
  --field masked="false" \
  --field protected="false"

# Update existing variable
glab api --method PUT "projects/:id/variables/K8S_DEV_MY_SETTING" \
  --field value="new-value"

# Delete a variable
glab api --method DELETE "projects/:id/variables/K8S_ALL_OLD_SETTING"
```

After changing variables, **trigger a new deploy pipeline** to apply them.

## CI/CD Pipeline

### Pipeline Structure

The pipeline includes remote templates from the AppStore CI/CD repo:

```yaml
include:
  - remote: https://gitlab.roqs.basf.net/appstore/cicd/deploy/-/raw/main/.gitlab-ci.yml
  - remote: https://gitlab.roqs.basf.net/appstore/cicd/security/-/raw/main/.gitlab-ci.yml
```

| Stage      | Purpose                                     | Notes                         |
| ---------- | ------------------------------------------- | ----------------------------- |
| `compile`  | Compilation (from template)                 | Optional                      |
| `build`    | Docker build + push to registry             | Parallel per service          |
| `test`     | Run tests inside built images               | `allow_failure: true` typical |
| `quality`  | Lint, dependency checks                     | `allow_failure: true` typical |
| `security` | Trivy container scan                        | `allow_failure: true` typical |
| `deploy`   | `kubectl apply -f .appstore/deployment.yml` | Automatic on push             |
| `undeploy` | Remove from cluster                         | **Manual gate**               |

### Example .gitlab-ci.yml (FastAPI + Worker + Nginx)

```yaml
include:
  - remote: https://gitlab.roqs.basf.net/appstore/cicd/deploy/-/raw/main/.gitlab-ci.yml
  - remote: https://gitlab.roqs.basf.net/appstore/cicd/security/-/raw/main/.gitlab-ci.yml

variables:
  DEPLOYMENT_NAME: my-app
  IMAGE_NAME: my-app
  CI_REGISTRY: registry.roqs.basf.net
  IMAGE_API: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_backend:${CI_PIPELINE_ID}
  IMAGE_API_LATEST: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_backend:latest
  IMAGE_NG: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_frontend:${CI_PIPELINE_ID}
  IMAGE_NG_LATEST: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_frontend:latest

stages:
  - build
  - test
  - quality
  - security
  - deploy
  - undeploy

build_backend:
  stage: build
  tags: [docker]
  script:
    - docker login -u ${CI_REGISTRY_USER} -p ${CI_REGISTRY_TOKEN} ${CI_REGISTRY}
    - cd backend
    - docker build -t $IMAGE_API .
    - docker push $IMAGE_API
    - docker tag $IMAGE_API $IMAGE_API_LATEST
    - docker push $IMAGE_API_LATEST

build_frontend:
  stage: build
  tags: [docker]
  script:
    - docker login -u ${CI_REGISTRY_USER} -p ${CI_REGISTRY_TOKEN} ${CI_REGISTRY}
    - cd frontend
    - docker build -t $IMAGE_NG .
    - docker push $IMAGE_NG
    - docker tag $IMAGE_NG $IMAGE_NG_LATEST
    - docker push $IMAGE_NG_LATEST

test_backend:
  stage: test
  tags: [docker]
  image: $IMAGE_API
  script:
    - cd backend && python3 -m pytest -v
  allow_failure: true
```

### Docker Image Conventions

```
registry.roqs.basf.net/<namespace>/<app>_backend     # API container
registry.roqs.basf.net/<namespace>/<app>_frontend     # Nginx/UI container
registry.roqs.basf.net/<namespace>/<app>_worker       # Background worker
registry.roqs.basf.net/base-images/redis:7            # Shared base images
registry.roqs.basf.net/base-images/nginx:latest       # Shared Nginx base
```

## Pod Operations via glab CLI

Since there's no kubectl access, all operations go through GitLab pipelines
and the `glab` CLI.

### Deploy / Restart

```bash
# Trigger a new pipeline (deploys latest images)
glab pipeline run --branch development

# Force restart without code change
git commit --allow-empty -m "chore: force pod restart"
git push origin development
```

### Check Pipeline Status

```bash
glab ci status                                      # Interactive view
glab ci list --ref development --per-page=5         # Last 5 dev pipelines
```

### Read Deploy Logs

```bash
# Get latest pipeline → deploy job → trace
PIPELINE_ID=$(glab api "projects/:id/pipelines?ref=development&per_page=1" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")

JOB_ID=$(glab api "projects/:id/pipelines/${PIPELINE_ID}/jobs" | \
  python3 -c "import json,sys; \
    [print(j['id']) for j in json.load(sys.stdin) if j['name'] == 'deploy']")

glab api "projects/:id/jobs/${JOB_ID}/trace"
```

### Undeploy (Manual Gate)

```bash
# Find undeploy job ID from latest pipeline
PIPELINE_ID=$(glab api "projects/:id/pipelines?ref=development&per_page=1" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")

UNDEPLOY_JOB=$(glab api "projects/:id/pipelines/${PIPELINE_ID}/jobs" | \
  python3 -c "import json,sys; \
    [print(j['id']) for j in json.load(sys.stdin) if j['name'] == 'undeploy']")

# Trigger undeploy
glab api --method POST "projects/:id/jobs/${UNDEPLOY_JOB}/play"
```

### Rollback

```bash
# Quickest rollback: revert the bad commit
git revert HEAD
git push origin development
```

## Debugging Failing Deploys

| Symptom            | Likely Cause               | Fix                                              |
| ------------------ | -------------------------- | ------------------------------------------------ |
| `OOMKilled`        | Memory limit too low       | Increase `limits.memory` in `deployment.yml`     |
| `ImagePullBackOff` | Wrong image name/tag       | Check image names in `deployment.yml`            |
| `CrashLoopBackOff` | App crash on startup       | Check `K8S_*` variables; read test job logs      |
| `Pending`          | Resource requests too high | Lower `requests.memory` or contact platform team |
| `ErrImagePull`     | Registry auth failure      | Check `CI_REGISTRY_TOKEN` variable               |

```bash
# Read deploy job trace for error details
glab api "projects/:id/jobs/<job_id>/trace"
```

## FastAPI App Pattern (Reference Implementation)

For a production-ready FastAPI app on the App Store, see
[references/fastapi-pattern.md](./references/fastapi-pattern.md) which documents
the proven structure from the ideator2phasegate project.

Key patterns:

- **Dockerfile**: Base image from `registry.roqs.basf.net`, `uv export` for deps, gunicorn + uvicorn
- **Nginx reverse proxy**: Strips app prefix from URL path, proxies to FastAPI
- **Multi-container pod**: nginx + api + worker + redis in one pod
- **Gunicorn config**: Production-ready with K8s optimizations (preload, max_requests, `/dev/shm`)
- **SSL certificates**: `REQUESTS_CA_BUNDLE` and `SSL_CERT_FILE` for BASF CA chain

## Checklist: New App Store Application

- [ ] Create app via Happy Potter wizard at `app.roqs.basf.net/portal/add`
- [ ] Clone the generated GitLab repository
- [ ] Review `.appstore/deployment.yml` — adjust resource limits
- [ ] Review `.appstore/egress.yml` — add external service dependencies
- [ ] Update `.appstore/portal.md` — describe your app for the portal
- [ ] Configure `.gitlab-ci.yml` — add build/test/quality jobs
- [ ] Write `Dockerfile` for each service container
- [ ] Set `K8S_*` CI/CD variables for secrets and config
- [ ] Push to `development` branch → verify deploy on `app-dev.roqs.basf.net`
- [ ] Test on dev tier, merge to `main` → verify on `app-qa.roqs.basf.net`
- [ ] Cut `release/x.y.z` branch → production deploy on `app.roqs.basf.net`

## Accessing Application Logs via Portal API

The AppStore Portal exposes a REST API for programmatic log access. This is the
only way to read container logs without kubectl — essential for debugging deployed
apps.

**API base URL:** `https://app.roqs.basf.net/appstore_portal_back_end/api/`

**OpenAPI spec** (no auth required):
`https://app.roqs.basf.net/appstore_portal_back_end/api/openapi.json`

### Generating an Access Token

The Portal API requires an **Azure AD MSAL Bearer token**. Two common approaches
that do NOT work:

- **Azure CLI (`az account get-access-token`)** — fails with AADSTS650057/AADSTS65001
  because the CLI app registration lacks the Portal's API resource permission
- **BASF federation cookie (`basf_federation_access_token`)** — returns 401; the
  Portal backend only accepts MSAL tokens, not federation JWE cookies

**Working approach — extract from Portal browser session:**

The Portal SPA acquires an MSAL token during login and stores it in `sessionStorage`.
Extract it from any authenticated Portal page:

```javascript
// Run in browser console on any app.roqs.basf.net/portal/* page:
const keys = [];
for (let i = 0; i < sessionStorage.length; i++) {
  const key = sessionStorage.key(i);
  if (key.includes("accesstoken")) keys.push(key);
}
const tokenData = JSON.parse(sessionStorage.getItem(keys[0]));
console.log(tokenData.secret); // Bearer token (JWT, ~2200 chars)
```

The token is stored under a sessionStorage key matching the pattern:
`*-accesstoken-*-api://<portal-client-id>/*--`

> **Note:** The Portal's MSAL client ID and tenant ID can be discovered from the
> OpenAPI spec or the Portal SPA's network requests. They are not secrets — they
> are public Azure AD app registration identifiers.

### Calling the Logs API

```bash
# GET /apps/{project_id}/logs
# Replace {PROJECT_ID} with your app's numeric AppStore ID (visible in the portal URL)
curl -s "https://app.roqs.basf.net/appstore_portal_back_end/api/apps/{PROJECT_ID}/logs?\
start_date=2026-01-01T00:00:00.000Z&\
end_date=2026-01-01T01:00:00.000Z&\
env=DEV&page_num=1&page_count=500" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN"
```

**Parameters:**

| Param        | Type       | Description                                               |
| ------------ | ---------- | --------------------------------------------------------- |
| `project_id` | int (path) | AppStore project ID (from portal URL: `/portal/app/{id}`) |
| `start_date` | datetime   | ISO 8601 start timestamp                                  |
| `end_date`   | datetime   | ISO 8601 end timestamp                                    |
| `env`        | enum       | `DEV`, `QUAL`, or `PROD`                                  |
| `page_num`   | int        | Page number (1-based)                                     |
| `page_count` | int        | Logs per page (max 500)                                   |
| `search`     | string     | Optional text filter                                      |

**Response structure:**

```json
{
  "worker": { "pod-name-xxx": [ { "id": "...", "timestamp": "...", "message": "..." } ] },
  "api":    { "pod-name-xxx": [ ... ] },
  "redis":  { "pod-name-xxx": [ ... ] },
  "nginx":  { "pod-name-xxx": [ ... ] },
  "POD":    { "pod-name-xxx": [ ... ] }
}
```

Logs are grouped by container name, then by pod name. Log `message` values are
JSON-encoded strings containing structured logs (typically ECS format). Parse with:

```python
import json
log_entry = json.loads(raw_message)
timestamp = log_entry.get("@timestamp")
level = log_entry.get("log.level")
message = log_entry.get("message")
logger = log_entry.get("log.logger")
```

### Authentication Model Summary

| Method                 | Works for Portal UI | Works for API | Notes                              |
| ---------------------- | ------------------: | :------------ | ---------------------------------- |
| BASF federation cookie |       Yes (browser) | **No** (401)  | JWE token; API rejects it          |
| Azure AD MSAL token    |                 N/A | **Yes** (200) | Extract from Portal sessionStorage |
| Azure CLI (`az`)       |                 N/A | **No**        | CLI app lacks resource permission  |

### Using Playwright / Browser Automation for Log Access

When an authenticated Portal browser page is available (e.g. via Playwright or
VS Code browser tools), extract the token and call the API in one step:

```javascript
// In page.evaluate() on an authenticated portal page:
const key = Object.keys(sessionStorage).find((k) => k.includes("accesstoken"));
const token = JSON.parse(sessionStorage.getItem(key)).secret;
const resp = await fetch(
  `https://app.roqs.basf.net/appstore_portal_back_end/api/apps/${projectId}/logs?` +
    `start_date=${startDate}&end_date=${endDate}&env=DEV&page_num=1&page_count=500`,
  { headers: { Authorization: "Bearer " + token, accept: "application/json" } },
);
return await resp.json();
```

## Progressive Disclosure

For detailed references, load these files:

- [references/deployment-patterns.md](./references/deployment-patterns.md) — Multi-container pods, resource tuning, volumes, nginx config
- [references/fastapi-pattern.md](./references/fastapi-pattern.md) — Production FastAPI app structure (Dockerfile, gunicorn, middleware)
- [references/ci-cd-patterns.md](./references/ci-cd-patterns.md) — Pipeline stages, parallel builds, test jobs, security scanning
- [references/glab-operations.md](./references/glab-operations.md) — Complete glab CLI reference for App Store operations

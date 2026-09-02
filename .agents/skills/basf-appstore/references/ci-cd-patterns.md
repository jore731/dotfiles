# CI/CD Patterns for BASF App Store

## Pipeline Architecture

Every App Store app uses remote CI/CD templates that handle the deploy and
security stages. Your `.gitlab-ci.yml` extends these with custom build, test,
and quality jobs.

```yaml
include:
  # Deploy template: handles kubectl apply, tier routing, undeploy
  - remote: https://gitlab.roqs.basf.net/appstore/cicd/deploy/-/raw/main/.gitlab-ci.yml
  # Security template: Trivy container scanning
  - remote: https://gitlab.roqs.basf.net/appstore/cicd/security/-/raw/main/.gitlab-ci.yml
```

## Required Variables

```yaml
variables:
  DEPLOYMENT_NAME: my-app              # Must match .appstore/deployment.yml metadata.name
  IMAGE_NAME: my-app                   # Base name for image tags
  CI_REGISTRY: registry.roqs.basf.net  # BASF container registry
```

## Image Tag Convention

```yaml
variables:
  # Tagged with pipeline ID (unique per build) + latest for deploy
  IMAGE_API: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_backend:${CI_PIPELINE_ID}
  IMAGE_API_LATEST: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_backend:latest
  IMAGE_NG: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_frontend:${CI_PIPELINE_ID}
  IMAGE_NG_LATEST: ${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}/${IMAGE_NAME}_frontend:latest
```

The `latest` tag is what `.appstore/deployment.yml` references. Each build pushes
both the pipeline-specific tag (for audit trail) and `latest` (for deployment).

## Stage Order

```yaml
stages:
  - compile     # Optional: compilation step
  - build       # Docker build + push (parallel per service)
  - test        # Run tests inside built images
  - quality     # Lint, dependency checks
  - security    # Trivy container scan (from remote template)
  - deploy      # kubectl apply (from remote template)
  - undeploy    # Manual gate (from remote template)
```

## Build Jobs

### Parallel Docker Builds

Build multiple services in parallel:

```yaml
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

build_worker:
  stage: build
  tags: [docker]
  script:
    - docker login -u ${CI_REGISTRY_USER} -p ${CI_REGISTRY_TOKEN} ${CI_REGISTRY}
    - export DOCKER_BUILDKIT=1
    - docker build -f worker/Dockerfile -t $IMAGE_WO .
    - docker push $IMAGE_WO
    - docker tag $IMAGE_WO $IMAGE_WO_LATEST
    - docker push $IMAGE_WO_LATEST
```

### BuildKit for Faster Builds

```yaml
script:
  - export DOCKER_BUILDKIT=1
  - docker build --progress=plain -t $IMAGE .
```

## Test Jobs

### Test Inside Built Image

Run tests using the production image — ensures the test environment matches prod:

```yaml
test_backend:
  stage: test
  tags: [docker]
  image: $IMAGE_API            # Use the image we just built
  timeout: 15 minutes
  variables:
    # Test-only env vars
    API_TOKEN: "test_token"
    DATABASE_URL: "sqlite:///test.db"
  before_script:
    # Install test tools (not in production image)
    - python3 -m pip install --quiet --user \
        'pytest>=8.3' 'pytest-asyncio>=0.25' 'pytest-cov>=6.0'
  script:
    - cd backend && python3 -m pytest -v --timeout=300
  allow_failure: true
```

### Import Verification (Lightweight Test)

For workers or services without a full test suite:

```yaml
test_worker:
  stage: test
  tags: [docker]
  image: $IMAGE_WO
  timeout: 5 minutes
  script:
    - cd /app
    - python3 -c "from worker.main import run; print('✅ main')"
    - python3 -c "from worker.config import get_settings; print('✅ config')"
  allow_failure: true
```

## Quality Jobs

### Ruff Linting

```yaml
lint:
  stage: quality
  tags: [docker]
  image: registry.roqs.basf.net/base-images/python:3.12
  before_script:
    - python3 -m pip install --quiet --user 'ruff>=0.9'
  script:
    - python3 -m ruff format --check --diff .
    - python3 -m ruff check --output-format=concise .
  allow_failure: true
```

### Dependency Footprint Check

Verify a service doesn't pull in unexpected heavy dependencies:

```yaml
dependency_check:
  stage: quality
  tags: [docker]
  image: registry.roqs.basf.net/base-images/python:3.12
  script:
    - pip3 install -r requirements.txt
    - pip3 list | grep -E "(torch|tensorflow)" && \
        echo "❌ Unexpected ML dependencies" && exit 1 || \
        echo "✅ Clean dependency set"
  allow_failure: true
```

## Security Override

The remote Trivy job sometimes fails on transient image-pull issues. Override
to prevent blocking:

```yaml
trivy:
  retry: 2
  allow_failure: true
```

## Branch-Based Deployment

The remote deploy template maps branches to tiers automatically:

| Branch        | Tier | URL                            |
| ------------- | ---- | ------------------------------ |
| `development` | dev  | `app-dev.roqs.basf.net/<app>/` |
| `main`        | qa   | `app-qa.roqs.basf.net/<app>/`  |
| `release/*`   | prod | `app.roqs.basf.net/<app>/`     |

No need to configure this — it's handled by the remote template.

## Pipeline Management via glab CLI

```bash
# Watch current pipeline
glab ci status

# List recent development pipelines
glab ci list --ref development --per-page=5

# Trigger a new pipeline
glab pipeline run --branch development

# Retry a failed pipeline
glab ci retry

# Lint your CI config before pushing
glab ci lint

# View pipeline in browser
glab ci view --web
```

## Tips

1. **Always push both `:<pipeline_id>` and `:latest` tags** — the pipeline tag
   provides audit trail, latest provides deploy target
2. **Use `allow_failure: true`** on test/quality/security jobs during development
   to avoid blocking deploys
3. **Use `tags: [docker]`** for all build jobs — the Docker runner is required
4. **Install test tools in `before_script`** rather than including them in the
   production image
5. **Use `timeout`** on test jobs to prevent stuck pipelines

# DevSpace Advanced Configuration

This document covers advanced DevSpace features: deployments, pipelines, variables, profiles, patches, and common patterns.

## Deployments

### Kubectl / Raw Manifests

```yaml
deployments:
  my-app:
    kubectl:
      manifests:
        - k8s/                    # directory of YAML files
        - k8s/special.yaml        # specific file

  inline-resources:
    kubectl:
      inlineManifest: |
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: my-deployment
        spec:
          replicas: 1
          ...
        ---
        apiVersion: v1
        kind: Service
        ...
```

### Helm Charts

```yaml
deployments:
  backend:
    helm:
      chart:
        name: my-chart
        repo: https://charts.example.com
        version: "1.2.3"
      values:
        replicaCount: 1
        image:
          repository: my-registry/my-image
      valuesFiles:
        - values-dev.yaml
```

### Kustomize

```yaml
deployments:
  app:
    kubectl:
      manifests:
        - kustomize/overlay/dev
      kustomize: true
```

## Pipelines

Pipelines define execution logic in POSIX shell syntax with special built-in functions:

```yaml
pipelines:
  dev: |-
    run_dependencies --all
    create_deployments --all
    start_dev app
  deploy: |-
    run_dependencies --all
    build_images --all -t $(git describe --always)
    create_deployments --all
  purge: |-
    stop_dev --all
    purge_deployments --all
```

### Built-in Pipeline Functions

| Function | Purpose |
|----------|---------|
| `build_images [name...]` | Build specified images (or `--all`) |
| `create_deployments [name...]` | Deploy specified deployments (or `--all`) |
| `start_dev [name...]` | Start dev mode for specified dev configs (or `--all`) |
| `stop_dev [name...]` | Stop dev mode |
| `purge_deployments [name...]` | Remove deployments |
| `run_dependencies [name...]` | Run dependency pipelines |
| `run_pipelines [name...]` | Run other pipelines (in parallel) |
| `ensure_pull_secrets [name...]` | Create image pull secrets |
| `get_flag <name>` | Get custom flag value |
| `is_empty <var>` | Check if variable is empty |
| `select_pod <selector>` | Select a pod interactively |
| `wait_pod <selector>` | Wait for a pod to be ready |

### Custom Pipelines

```yaml
pipelines:
  seed-data: |-
    create_deployments temp-db
    wait_pod --label-selector app=temp-postgres
    exec_container --label-selector app=backend -- python manage.py loaddata seed.json
```

Run with: `devspace run-pipeline seed-data`.

## Variables

```yaml
vars:
  # Static value
  MY_VAR: "some-value"

  # From environment (with default)
  DB_HOST:
    source: env
    default: localhost

  # From command
  GIT_SHA: $(git rev-parse --short HEAD)

  # Interactive prompt
  ENVIRONMENT:
    question: "Which environment?"
    options:
      - dev
      - staging
      - production
    default: dev

  # Load .env file
  DEVSPACE_ENV_FILE: ".env"
```

Use variables anywhere in config: `${MY_VAR}` or `$!{MY_VAR}` (force string type).

### Built-in Variables

| Variable | Value |
|----------|-------|
| `${DEVSPACE_CONTEXT}` | Current kubeconfig context |
| `${DEVSPACE_NAMESPACE}` | Current namespace |
| `${DEVSPACE_NAME}` | Project name from devspace.yaml |
| `${DEVSPACE_GIT_BRANCH}` | Current git branch |
| `${DEVSPACE_GIT_COMMIT}` | Current git commit SHA |
| `${DEVSPACE_RANDOM}` | Random 6-char string |
| `${DEVSPACE_TIMESTAMP}` | Unix timestamp |

## Profiles

Profiles modify the base config for different environments or use cases:

```yaml
profiles:
  - name: production
    patches:
      - op: replace
        path: images.backend.image
        value: prod-registry/backend

  - name: debug
    merge:
      dev:
        app:
          env:
            - name: DEBUG
              value: "true"

  - name: no-sync
    strategicMerge:
      dev:
        app:
          sync: []
```

Apply: `devspace dev -p production` or combine: `devspace dev -p debug -p extra`.

### Profile Operations

| Operation | Behavior |
|-----------|----------|
| `patches` | JSON Patch (RFC 6902) on the resolved config |
| `merge` | Deep merge (replaces arrays entirely) |
| `strategicMerge` | Kubernetes-style strategic merge (arrays by key) |
| `replace` | Full replacement of specified paths |

### Conditional Activation

```yaml
profiles:
  - name: ci
    activations:
      - env:
          CI: "true"
```

## Patches (Deep Dive)

Patches modify the Kubernetes PodSpec using JSON Patch (RFC 6902) with yaml-jsonpath paths.

### Operations

```yaml
dev:
  app:
    patches:
      - op: replace
        path: spec.terminationGracePeriodSeconds
        value: 3
      - op: remove
        path: spec.securityContext
      - op: add
        path: spec.containers.name=backend.env
        value: { name: MY_VAR, value: "hello" }
```

### Path Selectors for Arrays

| Syntax | Example | Selects |
|--------|---------|---------|
| Index | `spec.containers[0]` | First container |
| Property | `spec.containers.name=main` | Container named "main" |
| Wildcard | `spec.containers.*` | All containers |
| Comparison | `spec.containers[?(@.image=='nginx')]` | Container with image nginx |
| Regex | `spec.containers[?(@.name=~/^app/)]` | Containers starting with "app" |

### Important Rules

- **`op: add`** only works for appending to arrays/lists. To add fields to objects, use `op: replace`.
- **`op: remove`** silently succeeds even if path doesn't exist.
- **Patches are applied to config-level paths** (profiles) or pod-spec paths (dev patches).

## Common Patterns

### Temporary Database for Dev

Deploy a temporary database alongside your app:

```yaml
deployments:
  temp-db:
    kubectl:
      inlineManifest: |
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: temp-postgres
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: temp-postgres
          template:
            metadata:
              labels:
                app: temp-postgres
            spec:
              containers:
                - name: postgres
                  image: postgres:16-alpine
                  ports:
                    - containerPort: 5432
                  env:
                    - name: POSTGRES_DB
                      value: mydb
                    - name: POSTGRES_USER
                      value: dev
                    - name: POSTGRES_PASSWORD
                      value: dev
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: temp-postgres
        spec:
          selector:
            app: temp-postgres
          ports:
            - port: 5432
```

### Override Init Container Env Vars

When init containers get credentials from secrets/configmaps that point to a different DB, override them with patches:

```yaml
dev:
  app:
    patches:
      - op: add
        path: spec.initContainers.*.env
        value: { name: DB_HOST, value: temp-postgres }
      - op: add
        path: spec.initContainers.*.env
        value: { name: DB_PASSWORD, value: dev }
```

### Node Tolerations

If the cluster has tainted nodes, add tolerations to inline manifests:

```yaml
spec:
  tolerations:
    - key: my-taint-key
      operator: Equal
      value: my-taint-value
      effect: NoSchedule
```

### GitOps + DevSpace

DevSpace can attach to pods deployed by ArgoCD, Flux, or any other tool — just use `labelSelector`:

```yaml
dev:
  app:
    labelSelector:
      app.kubernetes.io/name: my-app
    sync:
      - path: ./src:/app/src
    terminal: {}
```

No `deployments` section needed — DevSpace only patches the existing pod.

### Multi-Container Dev

Target a specific container in a multi-container pod:

```yaml
dev:
  backend:
    imageSelector: my-image
    container: backend         # target this container
    sync:
      - path: ./src:/app/src
    terminal: {}

  sidecar:
    imageSelector: my-image
    container: sidecar
    logs: {}                   # stream sidecar logs
```

### Dependencies (Multi-Project)

```yaml
dependencies:
  shared-lib:
    source:
      path: ../shared-lib
    pipeline: deploy

  api-gateway:
    source:
      git: https://github.com/org/api-gateway
      branch: main
    pipeline: deploy
```

Run with: `run_dependencies --all` in your pipeline.

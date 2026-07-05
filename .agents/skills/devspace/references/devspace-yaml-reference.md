# devspace.yaml Full Reference

This is the complete configuration reference for `devspace.yaml` (v2beta1). Load this file on demand when editing `devspace.yaml` configuration.

## Top-Level Structure

```yaml
version: v2beta1          # required, always v2beta1
name: my-project           # project name

vars: {}                   # variables
images: {}                 # image build definitions
deployments: {}            # deployment definitions
dev: {}                    # dev container definitions
pipelines: {}              # pipeline definitions
profiles: []               # profile overrides
dependencies: {}           # project dependencies
imports: []                # config imports
commands: {}               # custom commands
functions: {}              # reusable functions
```

## `deployments` Section

### Kubectl Deployments

```yaml
deployments:
  <name>:
    kubectl:
      manifests: string[]          # list of files or directories
      inlineManifest: string       # inline YAML (multi-doc supported via ---)
      applyArgs: string[]          # extra args for kubectl apply
      createArgs: string[]         # extra args for kubectl create (runs before apply)
      kubectlBinaryPath: string    # custom kubectl binary path
      kustomize: boolean           # use kustomize instead of kubectl (default: false)
      kustomizeArgs: string[]      # extra args for kustomize build
      kustomizeBinaryPath: string  # custom kustomize binary path
      patches:                     # patches to K8s resources after rendering
        - target:
            apiVersion: string     # e.g., apps/v1
            kind: string           # e.g., Deployment
            name: string           # resource name
          op: string               # replace | add | remove
          path: string             # yaml-jsonpath path
          value: any               # value for replace/add
```

### Helm Deployments

```yaml
deployments:
  <name>:
    helm:
      releaseName: string          # Helm release name
      chart:
        # From Helm repo
        name: string               # chart name or OCI URL
        version: string            # chart version
        repo: string               # repo URL
        username: string           # repo auth username
        password: string           # repo auth password
        # From local filesystem
        path: string               # local chart path
        # From git
        git: string                # git repo URL
        subPath: string            # path within repo
        branch: string             # git branch
        tag: string                # git tag
        revision: string           # git revision
      values: object               # inline Helm values
      valuesFiles: string[]        # additional values files
      displayOutput: boolean       # show helm output (default: false)
      upgradeArgs: string[]        # extra args for helm upgrade
      templateArgs: string[]       # extra args for helm template
      disableDependencyUpdate: boolean  # skip helm dep update (default: false)
```

## `dev` Section

### Container Selection

```yaml
dev:
  <name>:
    imageSelector: string          # select by image name
    labelSelector:                 # select by K8s labels
      <label>: <value>
    namespace: string              # target namespace
    container: string              # specific container name
    arch: string                   # amd64 | arm64 (auto-detected)
```

### Container Modifications

```yaml
dev:
  <name>:
    devImage: string               # replace container image
    command: string[]              # override entrypoint
    args: string[]                 # override args
    workingDir: string             # override working directory
    env:                           # add environment variables
      - name: string
        value: string
    resources:                     # override resource limits
      requests:
        cpu: string
        memory: string
      limits:
        cpu: string
        memory: string
```

### Patches

```yaml
dev:
  <name>:
    patches:
      - op: string                 # replace | add | remove
        path: string               # yaml-jsonpath to target
        value: any                 # value (for replace/add)
```

**Path syntax (yaml-jsonpath):**

| Pattern | Example | Description |
|---------|---------|-------------|
| Array index | `spec.containers[0].env` | First container's env |
| Property selector | `spec.containers.name=main.env` | Container named "main" |
| Wildcard | `spec.initContainers.*.env` | All init containers |
| Comparison | `spec.containers[?(@.image=='nginx')].env` | By image |
| Regex | `spec.containers[?(@.name=~/^app/)].env` | By name pattern |

### File Sync

```yaml
dev:
  <name>:
    sync:
      - path: string              # localPath:remotePath (e.g., ./src:/app/src)
        excludePaths: string[]     # gitignore-style patterns to exclude
        excludeFile: string        # load exclude patterns from file
        downloadExcludePaths: string[]
        downloadExcludeFile: string
        uploadExcludePaths: string[]
        uploadExcludeFile: string
        initialSync: string        # mirrorLocal|mirrorRemote|preferLocal|preferRemote|preferNewest|keepAll|disabled
        initialSyncCompareBy: string  # mtime | size
        waitInitialSync: boolean   # wait for initial sync (default: true)
        disableDownload: boolean   # one-way upload only
        disableUpload: boolean     # one-way download only
        noWatch: boolean           # sync once, then stop
        polling: boolean           # use polling instead of inotify
        file: boolean              # sync single file instead of directory
        startContainer: boolean    # start container after initial sync
        bandwidthLimits:
          download: integer        # KB/s
          upload: integer          # KB/s
        onUpload:
          restartContainer: boolean
          exec:
            - name: string
              command: string
              args: string[]
              failOnError: boolean
              local: boolean       # run locally instead of in container
              once: boolean        # run only once per container lifecycle
              onChange: string[]   # file patterns that trigger this exec
```

### Port Forwarding

```yaml
dev:
  <name>:
    ports:
      - port: string              # "localPort:remotePort" or just "port" (same both sides)
        bindAddress: string        # default: localhost
    reversePorts:                  # container -> localhost
      - port: string
        bindAddress: string
```

### Persistent Paths

```yaml
dev:
  <name>:
    persistPaths:
      - path: string              # container path to persist
        volumePath: string         # sub-path on the PVC
        readOnly: boolean
        skipPopulate: boolean      # don't copy existing contents to PVC
        initContainer:
          resources:
            requests: {}
            limits: {}
    persistenceOptions:
      size: string                 # PVC size (e.g., "10Gi")
      storageClassName: string
      accessModes: string[]
      readOnly: boolean
      name: string                 # PVC name override
```

### Terminal / Logs / Attach

```yaml
dev:
  <name>:
    terminal:
      command: string              # shell command to run
      workDir: string              # working directory
      enabled: boolean
      disableReplace: boolean      # don't replace pod for terminal
      disableScreen: boolean       # disable GNU screen
      disableTTY: boolean          # disable TTY
    logs:
      enabled: boolean
      lastLines: integer           # initial log lines to show
    attach:
      enabled: boolean
      disableReplace: boolean
      disableTTY: boolean
```

### Multi-Container Dev

Target multiple containers in the same pod:

```yaml
dev:
  <name>:
    imageSelector: my-image
    containers:
      sidecar:
        container: sidecar-name
        devImage: my-debug-image
        sync:
          - path: ./sidecar:/app
        env:
          - name: DEBUG
            value: "true"
```

## `images` Section

```yaml
images:
  <name>:
    image: string                  # image name (registry/repo:tag)
    tags: string[]                 # additional tags
    dockerfile: string             # Dockerfile path (default: ./Dockerfile)
    context: string                # build context (default: ./)
    buildArgs: object              # Docker build args
    target: string                 # multi-stage build target
    network: string                # Docker build network
    rebuildStrategy: string        # always | default
    # Build tools
    docker: {}                     # use Docker daemon
    buildKit:                      # use BuildKit
      inCluster: {}                # build in-cluster
    kaniko: {}                     # use kaniko (in-cluster)
    custom:                        # custom build command
      command: string
      args: string[]
```

## `pipelines` Section

```yaml
pipelines:
  # Default pipelines (override these)
  dev: |-
    run_dependencies --all
    ensure_pull_secrets --all
    build_images --all
    create_deployments --all
    start_dev --all
  deploy: |-
    run_dependencies --all
    ensure_pull_secrets --all
    build_images --all
    create_deployments --all
  build: |-
    run_dependencies --all --pipeline build
    build_images --all
  purge: |-
    stop_dev --all
    purge_deployments --all
    run_dependencies --all --pipeline purge

  # Custom pipeline
  my-pipeline:
    flags:                         # custom CLI flags
      - name: flag-name
        short: f                   # single-letter alias
        type: string               # bool (default) | string | stringArray | int
        description: string
    run: |-
      echo "Flag value: $(get_flag flag-name)"
      create_deployments my-deployment
      start_dev my-dev
```

### Pipeline Built-in Functions

```
# Image operations
build_images [name...] [--all] [--tag/-t tag] [--force-rebuild] [--sequential]
ensure_pull_secrets [name...] [--all]
get_image <name>                     # returns most recent image:tag

# Deployment operations
create_deployments [name...] [--all] [--except name...]
purge_deployments [name...] [--all]

# Dev operations
start_dev [name...] [--all] [--set key=value]
stop_dev [name...] [--all]

# Dependencies
run_dependencies [name...] [--all] [--pipeline name]
run_dependency_pipelines [name...] [--all]

# Pipeline orchestration
run_pipelines [name...]              # run other pipelines (parallel)

# Utilities
get_flag <name>                      # get custom flag value
is_empty <variable>                  # check if variable is empty
select_pod [--label-selector sel]    # interactive pod selection
wait_pod [--label-selector sel]      # wait for pod readiness

# General (also available outside pipelines)
exec_container [--label-selector sel] -- <command>
```

## `vars` Section

```yaml
vars:
  # Static
  MY_VAR: "value"

  # From environment
  ENV_VAR:
    source: env
    default: "fallback"

  # From command
  CMD_VAR: $(git rev-parse --short HEAD)
  CMD_VAR_LONG:
    command: git
    args: ["rev-parse", "--short", "HEAD"]

  # User prompt
  PROMPTED_VAR:
    question: "Which environment?"
    options: ["dev", "staging", "prod"]
    default: "dev"
    # password: true              # mask input

  # .env file
  DEVSPACE_ENV_FILE: ".env"

  # Default flags
  DEVSPACE_FLAGS: "-n my-namespace"
  DEVSPACE_DEV_FLAGS: "--verbose-dependencies"
```

## `profiles` Section

```yaml
profiles:
  - name: production
    # Strategy 1: Replace entire sections
    replace:
      deployments:
        prod-app:
          helm:
            chart:
              name: my-chart

    # Strategy 2: JSON Merge Patch (RFC 7386)
    merge:
      dev:
        app:
          env:
            - name: ENV
              value: production

    # Strategy 3: JSON Patch (RFC 6902)
    patches:
      - op: replace
        path: images.backend.image
        value: prod-registry/backend
      - op: remove
        path: dev.app.terminal

    # Activation conditions (auto-activate profile)
    activateBy:
      - env:
          MY_ENV: "true"
      - vars:
          MY_VAR: "production"
```

Execution order within a profile: `replace` → `merge` → `patches`.

## `dependencies` Section

```yaml
dependencies:
  auth-service:
    git: https://github.com/org/auth-service.git
    branch: main
    subPath: /                     # optional sub-directory
    pipeline: deploy               # which pipeline to run (default: deploy)
    overwriteVars: true
    vars:
      NAMESPACE: ${DEVSPACE_NAMESPACE}
  local-dep:
    path: ../shared-lib
```

## `commands` Section

Custom commands runnable via `devspace run <name>`:

```yaml
commands:
  migrate:
    command: |-
      devspace enter -- python manage.py migrate
  seed:
    command: |-
      devspace enter -- python manage.py loaddata fixtures/*.json
  test:
    command: |-
      devspace enter -- python manage.py test --no-input -v 2
```

## `imports` Section

Import config from other files or git repos:

```yaml
imports:
  - path: devspace-base.yaml       # local file
  - git: https://github.com/org/devspace-configs.git
    subPath: base/devspace.yaml
    branch: main
```

## Config Expressions

Use `$()` for dynamic values resolved at runtime:

```yaml
deployments:
  app:
    helm:
      values:
        image: $(devspace print -p ${DEVSPACE_PROFILE} | jq -r '.images.app.image')
        tag: $(git describe --always)
```

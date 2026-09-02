# Deployment Patterns Reference

## Multi-Container Pod Pattern

A single pod on the App Store can host multiple containers that share networking
(localhost) and volumes. This is the standard pattern for apps with a frontend
reverse proxy, API backend, background worker, and cache.

### Production Example (4 containers)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        # --- Nginx Reverse Proxy (entry point) ---
        - name: nginx
          image: registry.roqs.basf.net/<namespace>/<app>_frontend
          ports:
            - containerPort: 1080
          resources:
            limits:
              memory: "100Mi"
            requests:
              memory: "50Mi"
          securityContext:
            runAsUser: 100
            runAsGroup: 101

        # --- FastAPI Backend ---
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
              memory: "2500Mi"
            requests:
              memory: "1500Mi"
          securityContext:
            runAsUser: 1000
            runAsGroup: 1000

        # --- Background Worker ---
        - name: worker
          image: registry.roqs.basf.net/<namespace>/<app>_worker
          command: ["python3"]
          args: ["-m", "worker.main"]
          env:
            - name: REQUESTS_CA_BUNDLE
              value: /etc/ssl/certs/ca-certificates.crt
            - name: SSL_CERT_FILE
              value: /etc/ssl/certs/ca-certificates.crt
          resources:
            limits:
              cpu: "1"
              memory: "1000Mi"
            requests:
              cpu: "0.5"
              memory: "250Mi"
          securityContext:
            runAsUser: 1000
            runAsGroup: 1000

        # --- Redis Cache (sidecar) ---
        - name: redis
          image: registry.roqs.basf.net/base-images/redis:7
          command: ["redis-server"]
          args: ["--loglevel", "warning"]
          resources:
            limits:
              memory: "500Mi"
            requests:
              memory: "100Mi"
          securityContext:
            runAsUser: 999
            runAsGroup: 999
          ports:
            - containerPort: 6379
```

### Networking Within the Pod

All containers in a pod share `localhost`. Connections between containers:

```
nginx (port 1080) ──proxy_pass──► api (port 5000)
api ──────────────────────────────► redis (port 6379)
worker ───────────────────────────► redis (port 6379)
```

The App Store API gateway routes external traffic to the nginx container on
port 1080. Nginx then proxies to the API on port 5000.

## Nginx Reverse Proxy Configuration

The nginx container strips the app prefix from URL paths before forwarding
to the FastAPI backend:

```nginx
worker_processes 1;
user nobody nobody;
error_log /tmp/error.log;
pid /tmp/nginx.pid;

events {
  worker_connections 1024;
}

http {
    client_body_temp_path /tmp/client_body;
    fastcgi_temp_path /tmp/fastcgi_temp;
    proxy_temp_path /tmp/proxy_temp;
    scgi_temp_path /tmp/scgi_temp;
    uwsgi_temp_path /tmp/uwsgi_temp;

    log_format timed_combined '[$time_local] $remote_addr '
      '(time: $request_time/$upstream_response_time sec) '
      '"$request" $status $body_bytes_sent '
      '"$http_referer" "$http_user_agent" $pipe';
    access_log /tmp/access.log timed_combined;
    error_log /tmp/error.log;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 1080;
        large_client_header_buffers 4 32k;

        # AppStore: strip app prefix and proxy to backend
        location /<app_name>/ {
            proxy_pass  http://0.0.0.0:5000/;
            proxy_set_header X-Forwarded-Prefix /<app_name>;
            proxy_pass_request_headers on;
        }

        # Direct/local access: no prefix to strip
        location / {
            proxy_pass  http://0.0.0.0:5000/;
            proxy_set_header X-Forwarded-Prefix $http_x_forwarded_prefix;
            proxy_pass_request_headers on;
        }
    }
}
```

**Important**: The nginx container must run as non-root. Use `/tmp/` for all
writable paths (logs, temp, pid).

## Resource Tuning

### Memory

| Container | Requests (scheduling) | Limits (OOMKill threshold) |
|-----------|----------------------|---------------------------|
| nginx | 50Mi | 100Mi |
| API (light) | 256Mi | 512Mi |
| API (heavy/ML) | 1500Mi | 2500Mi |
| worker | 250Mi | 1000Mi |
| redis | 100Mi | 500Mi |

**OOMKilled?** Increase `limits.memory`. The pod is killed when it exceeds the limit.

**Pending/Unschedulable?** Lower `requests.memory`. This value affects which
node the pod is scheduled on.

### CPU

CPU limits are optional but recommended for workers:

```yaml
resources:
  limits:
    cpu: "1"          # Max 1 CPU core
  requests:
    cpu: "0.5"        # Request half a core for scheduling
```

Omitting CPU limits allows burst usage, which is fine for API containers.

## Security Context

All containers must run as non-root:

```yaml
securityContext:
  runAsUser: 1000      # Application user UID
  runAsGroup: 1000     # Application group GID
```

Standard UIDs:
- **API/Worker**: 1000:1000 (custom `app` user)
- **Nginx**: 100:101 (nobody)
- **Redis**: 999:999 (redis user)

## SSL/TLS Configuration

BASF infrastructure uses internal CA certificates. Set these env vars in every
container that makes HTTPS requests:

```yaml
env:
  - name: REQUESTS_CA_BUNDLE
    value: /etc/ssl/certs/ca-certificates.crt
  - name: SSL_CERT_FILE
    value: /etc/ssl/certs/ca-certificates.crt
```

## Persistent Volumes

If the Happy Potter wizard enabled persistent storage:

```yaml
spec:
  template:
    spec:
      containers:
        - name: db
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: <app-name>-pvc
```

The PVC is created automatically by the AppStore platform.

## Adding a New Container

1. Create the Dockerfile and build job in `.gitlab-ci.yml`
2. Add the container spec to `.appstore/deployment.yml`
3. Add any `K8S_*` variables via `glab api`
4. Commit and push to trigger the full pipeline

## Egress Rules

### Format

```yaml
# Public internet / cloud services (through corporate proxy)
public:
  - host: api.openai.com
    port: 443
  - host: huggingface.co
    port: 443

# BASF intranet / private network (direct)
private:
  - host: 10.99.195.24
    port: 8080
  - host: internal-service.basf.net
    port: 443
```

### Common Egress Entries

| Service | Host | Port |
|---------|------|------|
| Wazoku API | `public-api-de.wazoku.com` | 443 |
| BASF Federation | `federation.basf.net` | 443 |
| BASF Nexus | `nexus.roqs.basf.net` | 443 |
| Azure OpenAI | `*.openai.azure.com` | 443 |

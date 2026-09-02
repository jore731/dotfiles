# FastAPI App Store Pattern

Production-ready FastAPI application structure for the BASF App Store, based on
the proven ideator2phasegate reference implementation.

## Project Structure

```
my-app/
├── .appstore/
│   ├── deployment.yml        # K8s pod spec
│   ├── egress.yml            # Firewall rules
│   ├── portal.md             # App Store description
│   └── README.md             # Do not modify
├── backend/
│   ├── api/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config/
│   │   │   └── settings.py   # Pydantic v2 Settings
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic
│   │   ├── middleware/       # Auth, CORS, logging
│   │   └── dependencies.py   # Dependency injection
│   ├── Dockerfile            # Production image
│   ├── gunicorn_conf.py      # WSGI config for K8s
│   ├── pyproject.toml        # Python project config
│   ├── uv.lock               # Frozen dependencies
│   └── tests/                # Test suite
├── frontend/
│   ├── Dockerfile            # Nginx container
│   └── nginx.non-root.conf   # Reverse proxy config
├── worker/                   # Optional background service
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── .gitlab-ci.yml            # CI/CD pipeline
└── docker-compose.yml        # Local development
```

## Dockerfile (Backend)

Uses BASF base image with `uv` for dependency management:

```dockerfile
FROM registry.roqs.basf.net/base-images/python:3.12
USER root

ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV PIP_IGNORE_INSTALLED=1

# Install dependencies via uv export
COPY uv.lock pyproject.toml /app/
WORKDIR /app
RUN pip install uv && \
    uv export --frozen --no-dev --group appstore --no-hashes --native-tls \
      -o /tmp/requirements.txt && \
    pip install --ignore-installed --no-deps -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Create app user
RUN id app 2>/dev/null || useradd -m -s /bin/bash app
RUN mkdir -p /app/logs && touch /app/logs/app.log && \
    chmod 777 /app/logs/app.log && chown -R app:app /app

EXPOSE 5000
USER app
COPY . /app
WORKDIR /app

ENTRYPOINT []
CMD ["python3", "-m", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", \
     "-c", "gunicorn_conf.py", "api.main:app"]
```

### Key Dockerfile Patterns

1. **BASF base image**: Always use `registry.roqs.basf.net/base-images/` or custom
   base images — they include BASF CA certificates
2. **`uv export`**: Generate requirements.txt from `uv.lock` for reproducible builds
3. **`--group appstore`**: Separate dependency group for production-only packages
   (e.g., `uvloop`, `httptools`)
4. **Non-root user**: Create `app` user, `EXPOSE` port, switch to `USER app`
5. **`ENTRYPOINT []`**: Override base image entrypoint to avoid command duplication

## Gunicorn Configuration (gunicorn_conf.py)

Production-ready WSGI server config optimized for Kubernetes:

```python
import multiprocessing
import os

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "5000")
bind = os.getenv("BIND", f"{host}:{port}")

# Worker count: conservative for K8s pods
workers_per_core = float(os.getenv("WORKERS_PER_CORE", "1"))
cores = multiprocessing.cpu_count()

if web_concurrency := os.getenv("WEB_CONCURRENCY"):
    workers = int(web_concurrency)
else:
    workers = max(int(workers_per_core * cores), 2)

loglevel = os.getenv("LOG_LEVEL", "info").lower()

# Production timeouts
keepalive = 480           # 8 min — match K8s ingress timeout
timeout = 180             # 3 min per request
graceful_timeout = 60     # 1 min graceful shutdown

worker_class = "uvicorn.workers.UvicornWorker"

# Disable gunicorn access logs (FastAPI middleware handles this)
accesslog = None
errorlog = "-"            # stderr for container log aggregation

# K8s optimizations
preload_app = True        # Better memory usage
max_requests = 1000       # Prevent memory leaks
max_requests_jitter = 100 # Prevent thundering herd
worker_tmp_dir = "/dev/shm"  # Shared memory for heartbeat
forwarded_allow_ips = "*"    # Behind K8s ingress
```

## pyproject.toml Patterns

### Dependency Groups

```toml
[project]
requires-python = ">=3.12,<3.13"
dependencies = [
    "fastapi>0.110",
    "gunicorn>=23,<24",
    "uvicorn>=0.30,<1",
    "pydantic>=2.9,<3",
    "pydantic-settings>=2.6,<3",
    "httpx>=0.27,<1",
    # ... other runtime dependencies
]

[dependency-groups]
dev = [
    "pytest>=8.3,<9",
    "pytest-asyncio>=0.25,<1",
    "ruff>=0.9,<1",
    # ... dev-only dependencies
]
appstore = [
    "httptools>=0.6.1,<1",   # Fast HTTP parsing (Linux only)
    "uvloop>=0.19,<1",       # Fast event loop (Linux only)
]

[tool.uv]
default-groups = ["dev"]
native-tls = true

[[tool.uv.index]]
name = "basf-nexus"
url = "https://nexus.roqs.basf.net/repository/python/simple"
default = true
```

### BASF Nexus Registry

Internal packages (e.g., `basf-auth`) are hosted on BASF's Nexus:

```toml
[[tool.uv.index]]
name = "basf-nexus"
url = "https://nexus.roqs.basf.net/repository/python/simple"
default = true

[tool.uv.sources]
basf-auth = { index = "basf-nexus" }
```

## Authentication Pattern

BASF apps typically use `basf-auth` for SSO cookie authentication:

```python
from basf_auth import BASFAuth

# FastAPI middleware for BASF SSO
auth = BASFAuth(
    federation_url=settings.basf_auth_federation_url,
    enabled=settings.basf_auth_enabled,
)
```

## Docker Compose (Local Development)

```yaml
services:
  api:
    build:
      context: backend
    ports:
      - 8000:5000
    links:
      - redis
    env_file:
      - .env.docker.local
    networks:
      - app-network

  redis:
    image: registry.roqs.basf.net/base-images/redis:7
    ports:
      - 6379:6379
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Environment Variable Pattern

Use Pydantic Settings for typed, validated configuration:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    environment: str = "DEV"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str = "redis://localhost:6379/0"

    # Authentication
    basf_auth_enabled: bool = True
    basf_auth_federation_url: str = "https://federation.basf.net"

    # SSL (BASF CA chain)
    ssl_cert_file: str = "/etc/ssl/certs/ca-certificates.crt"

    class Config:
        env_file = ".env"
        case_sensitive = False
```

Variables injected by the AppStore `K8S_*` system map directly to these fields
(e.g., `K8S_DEV_REDIS_URL` → `redis_url` in the pod).

## Health Endpoints

Implement health endpoints for Kubernetes probes:

```python
@router.get("/api/v2/health")
async def health():
    return {"status": "ok"}

@router.get("/api/v2/health/detailed")
async def health_detailed():
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": settings.environment,
        "redis": await check_redis(),
        "uptime": get_uptime(),
    }
```

These endpoints are the primary way to verify deployment health since
there's no kubectl access.

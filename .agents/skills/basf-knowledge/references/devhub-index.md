# DevHub Index

BASF **DevHub** is the BASF developer platform ("DevHub Engineering Portal"). It has two
distinct web surfaces, both hosted behind Azure Front Door and protected by **Entra ID (Azure AD) SSO**:

| Surface | Host | Tech | Purpose |
|---------|------|------|---------|
| Landing / Docs | `https://devhub.intranet.basf.com` | Next.js (SPA) | Marketing landing page, platform overview, roadmap, documentation |
| Engineering Portal | `https://portal.devhub.intranet.basf.com` | **Backstage** (SPA) | Software Catalog, Software Templates (scaffolder), TechDocs |

> Although the hosts end in `.com`, they resolve publicly via Azure Front Door
> (`*.azurefd.net`) and are reachable from the internet — but every request without a
> valid token is redirected (HTTP 302) to `login.microsoftonline.com`.

---

## Authentication — `az` as token broker (no secret sharing)

Both surfaces accept an Entra ID **Bearer token** whose audience is the DevHub app
registration. The clean, reproducible way to obtain one is the **Azure CLI** — it performs
the interactive login once and then caches/refreshes the token locally. **Never paste or
share raw tokens.**

```bash
# DevHub app registration (audience / resource)
APPID="074bdf99-9d4c-46db-8395-c8a42baaa6ce"
TENANT="ecaa386b-c8df-4ce0-ad01-740cbdb5ba55"   # BASF tenant

az login                                          # once, interactive (browser)
TOKEN=$(az account get-access-token --resource "$APPID" --query accessToken -o tsv)

curl -sk -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  https://portal.devhub.intranet.basf.com/api/catalog/entity-facets?facet=kind
unset TOKEN
```

Verification: with the token the endpoints return **HTTP 200**; without it they return
**HTTP 302** to `login.microsoftonline.com`.

> If `az account get-access-token --resource <APPID>` is rejected for the DevHub app
> (custom app registrations do not always allow the Azure CLI client), a small
> `DeviceCodeCredential` / `InteractiveBrowserCredential` bridge (`azure-identity`) against
> the same `APPID` + `TENANT` produces an equivalent token. The auth pattern stays the same.

---

## Surface 1 — Landing / Docs (`devhub.intranet.basf.com`)

Next.js app (`__next` root, `/_next/static/...` chunks). Most content is either hardcoded in
the bundle or injected server-side into `__NEXT_DATA__`. Only two real API routes exist:

| Endpoint | Method | Notes |
|----------|--------|-------|
| `/api/health` (aliases `/health`, `/healthz`) | GET | `{"status":"ok"}` |
| `/api/devhub-announcement/announcement` | GET | Proxy to an external announcement API (returns JSON; may 500 when empty) |

- **Roadmap** is embedded in the homepage `__NEXT_DATA__` at
  `props.pageProps.roadmapEntries` (+ `roadmapMeta`). Cached snapshot; live fetch needs a
  separate GitHub "roadmap token" (`basf-global/dh-cross-team`).
- **Documentation** is server-rendered under `/documentation/...`, e.g.
  `/documentation/DevHub/`, `/documentation/argus/`, `/documentation/appstore/`,
  `/documentation/dsp/`.
- **Platforms** advertised on the landing page: DevHub, Argus (frozen), App Store (frozen),
  DSP (frozen).

Extract the embedded roadmap:

```bash
curl -sk -H "Authorization: Bearer $TOKEN" https://devhub.intranet.basf.com/ \
 | grep -oE '<script id="__NEXT_DATA__"[^>]*>.*</script>' \
 | sed -E 's/<[^>]+>//g' \
 | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d['props']['pageProps'].get('roadmapEntries',[]), indent=2)[:2000])"
```

---

## Surface 2 — Engineering Portal (`portal.devhub.intranet.basf.com`)

This is a **Backstage** instance (title: "DevHub Engineering Portal"; bundles
`module-backstage*.js`). It exposes the **standard Backstage backend API** under `/api/<plugin>/...`.
The most useful plugin is the **Software Catalog**.

### Catalog size (snapshot 2026-06, via `/api/catalog/entity-facets?facet=kind`)

| Kind | Count | Kind | Count |
|------|-------|------|-------|
| User | ~6060 | Group | ~5930 |
| Resource | ~5515 | Component | ~2440 |
| System | ~1170 | Location | ~1940 |
| Template | ~25 | API | ~11 |
| Domain | ~4 | | |

### Key Catalog API endpoints (verified)

```bash
B="https://portal.devhub.intranet.basf.com"
H=(-H "Authorization: Bearer $TOKEN" -H "Accept: application/json")

# Counts per kind
curl -sk "${H[@]}" "$B/api/catalog/entity-facets?facet=kind"

# Query entities with filter + field projection (preferred, paginated)
curl -sk "${H[@]}" "$B/api/catalog/entities/by-query?filter=kind=component&limit=20&fields=metadata.name,metadata.title,spec.owner"

# Filter by owner / type
curl -sk "${H[@]}" "$B/api/catalog/entities/by-query?filter=kind=component,spec.type=service&limit=50"

# Fetch a single entity by name: <kind>/<namespace>/<name>
curl -sk "${H[@]}" "$B/api/catalog/entities/by-name/component/default/<name>"

# Software Templates (Backstage scaffolder templates live in the catalog as kind=Template)
curl -sk "${H[@]}" "$B/api/catalog/entities/by-query?filter=kind=template&limit=50&fields=metadata.name,metadata.title"

# Auth discovery / health
curl -sk "${H[@]}" "$B/api/auth/.well-known/openid-configuration"
curl -sk "${H[@]}" "$B/.backstage/health/v1/readiness"
```

> Note: `/api/scaffolder/v2/templates` returns **404** here — templates are exposed as
> catalog entities of `kind=Template`, not via the scaffolder list endpoint.

### Software Templates (examples)

DevHub Workspace · Data Platform Workspace · ExpressJS Web Framework · DevHub DSP ·
RAG API Python · Angular Frontend · FastAPI MCP Service · DevHub Product by Wizard

### Catalog query reference

- Filters: `filter=<key>=<value>` (comma = AND within one filter, repeat `filter=` for OR).
  Common keys: `kind`, `metadata.name`, `metadata.namespace`, `spec.type`, `spec.owner`,
  `relations.ownedBy`.
- Projection: `fields=metadata.name,spec.owner` keeps responses small.
- Pagination: `limit=<n>` + cursor returned in the `by-query` response.
- Free-text search across the portal: `/api/search/query?term=<text>`.

Full Backstage Catalog API reference:
<https://backstage.io/docs/features/software-catalog/software-catalog-api/>

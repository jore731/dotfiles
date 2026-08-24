---
name: basf-knowledge
description: >
  Search BASF internal knowledge from Confluence, Cloud Reference docs, and the
  DevHub developer platform. Covers Azure subscriptions, networking, DNS, cost
  centers, cloud policies, platform guidelines, the DevHub Backstage Software
  Catalog (components, systems, APIs, groups, software templates), and the DevHub
  platform documentation (DSP, APIs, App Store, Argus, developer setup). Use when the
  user asks about BASF-specific cloud procedures, policies, Service4You articles,
  DevHub, the Engineering Portal, or needs to look up how to do something in the
  BASF Azure/cloud environment. Also use when the user mentions Confluence, Cloud
  Reference, cloudreference, DevHub, Backstage, or BASF cloud docs.
---

# BASF Knowledge Search

Search BASF internal documentation across Confluence and Cloud Reference docs.

## BASF Domains: `.net` vs `.com`

BASF uses two top-level domains, and the distinction matters for reachability:

- **`basf.net` → intranet** (BASF Corporate Network / BCN only). Internal tools live
  here: `confluence.basf.net`, RunIP DNS appliances, internal services. Only reachable
  from the corporate network or VPN.
- **`basf.com` → public internet**. Externally resolvable services live here:
  `service4you.intranet.basf.com` (S4Y / Employee Center), `docs.cloudreference.basf.com`
  (SSO-protected), `devhub.intranet.basf.com` and `portal.devhub.intranet.basf.com`
  (DevHub, behind Azure Front Door + Entra ID SSO), `*@basf.com` email addresses.

When advising users where to open a link or why something is/isn't reachable, use this
distinction. A `.net` host failing to resolve usually means the user is off the intranet.

## Quick Start — Confluence Search

Confluence supports **anonymous read access** via REST API (no credentials needed):

```bash
# Full-text search (CQL)
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=text~\"your+search+terms\"&limit=10" | python3 -c "
import json,sys
for r in json.load(sys.stdin).get('results',[]):
    print(f\"{r['id']} | {r['title']} | {r['_links']['webui']}\")"

# Search within a specific space
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=text~\"query\"+AND+space=BASANTCLOUD&limit=10"

# Get full page content by ID
curl -sk "https://confluence.basf.net/rest/api/content/<PAGE_ID>?expand=body.storage"
```

> **`-sk` flags**: `-s` silent, `-k` skip TLS verification (required for BASF corporate CA).

## Key Confluence Spaces

| Space Key | Name | Topics |
|-----------|------|--------|
| `BASANTCLOUD` | BASANT Cloudification | Azure subscriptions, cost centers, cloud setup, security, connectivity |
| `DNSDHCP` | DNS & DHCP | DNS records, subdomains, S4Y articles, DNS policies, external/internal DNS |
| `OPF` | Operations Platform | Azure DevOps, infrastructure, deployment, architecture |

## Workflows

### Find a How-To or Policy

1. **Check the pre-indexed pages** in [references/confluence-index.md](references/confluence-index.md) first — it lists all pages from key spaces with IDs and topics
2. If found, fetch the page content directly:
   ```bash
   curl -sk "https://confluence.basf.net/rest/api/content/<PAGE_ID>?expand=body.storage" | python3 -c "
   import json,sys,html,re
   body = json.load(sys.stdin)['body']['storage']['value']
   text = re.sub(r'<[^>]+>', ' ', body)
   print(html.unescape(text)[:3000])"
   ```
3. If not found, search Confluence with CQL (see Advanced Search below)

### Find a Service4You (S4Y) Article

S4Y articles have GS/GSP numbers. Search by article number or topic:

```bash
# By article number
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=text~\"GS0000291\"&limit=5"

# By topic
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=text~\"CNAME\"+AND+space=DNSDHCP&limit=10"
```

Common S4Y articles are listed in [references/confluence-index.md](references/confluence-index.md).

### Look Up Cloud Reference Docs

`docs.cloudreference.basf.com` requires **Azure AD authentication** (BASF SSO, Azure App Service Auth). It is a DocFX static site (server-rendered HTML). Use [references/cloudref-index.md](references/cloudref-index.md) to find URLs (548 pages indexed across 9 sections).

**Default — Azure CLI token broker** (same `az login` as DevHub, but its own resource ID; never paste raw tokens):

```bash
CRAPP="6b6bc843-3472-4c61-af63-5b99fd17d534"   # Cloud Reference resource ID
TOKEN=$(az account get-access-token --resource "$CRAPP" --query accessToken -o tsv)
curl -sk -H "Authorization: Bearer $TOKEN" "https://docs.cloudreference.basf.com/<PATH>"
unset TOKEN
```

With a valid token the site returns HTTP 200; without it, HTTP 401 with a
`WWW-Authenticate: Bearer` header naming this resource ID.

**Fallback** — if `az` is unavailable, an `AppServiceAuthSession` cookie from browser
DevTools (Application → Cookies) also works:
`curl -sk -b "AppServiceAuthSession=<COOKIE>" "https://docs.cloudreference.basf.com/<PATH>"`.
Otherwise provide direct URLs for the user to open in their browser.

### Search DevHub (Engineering Portal / Backstage)

BASF **DevHub** is the developer platform. It has two SSO-protected surfaces behind Entra ID:
`devhub.intranet.basf.com` (Next.js landing/docs) and `portal.devhub.intranet.basf.com`
(a **Backstage** Engineering Portal with a large Software Catalog). See
[references/devhub-index.md](references/devhub-index.md) for the full API map.

Authenticate with the **Azure CLI as a token broker** — never paste raw tokens:

```bash
APPID="074bdf99-9d4c-46db-8395-c8a42baaa6ce"   # DevHub app registration
az login                                         # once, interactive
TOKEN=$(az account get-access-token --resource "$APPID" --query accessToken -o tsv)

# Backstage Software Catalog — counts per kind
curl -sk -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "https://portal.devhub.intranet.basf.com/api/catalog/entity-facets?facet=kind"

# Query catalog entities (filter + field projection)
curl -sk -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "https://portal.devhub.intranet.basf.com/api/catalog/entities/by-query?filter=kind=component&limit=20&fields=metadata.name,spec.owner"
unset TOKEN
```

With a valid token endpoints return HTTP 200; without it they 302-redirect to
`login.microsoftonline.com`. Software Templates are catalog entities of `kind=Template`.

#### DevHub Platform Documentation

The docs at `devhub.intranet.basf.com/documentation/` are a **Docusaurus** static site
(728 pages across DSP, DevHub, APIs, App Store, Argus, Setup). Use
[references/devhub-docs-index.md](references/devhub-docs-index.md) to map a topic to its
exact page path — far faster than crawling. Then fetch that one page with the same token
and strip the HTML to read it:

```bash
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://devhub.intranet.basf.com/documentation/devhub/getting-started/prerequisites/" \
  | python3 -c "import sys,re,html; h=sys.stdin.read(); m=re.search(r'<main.*?</main>',h,re.S); print(html.unescape(re.sub(r'<[^>]+>',' ',m.group(0) if m else h))[:3000])"
```

The full page list can be refreshed from `/documentation/search-index.json`
(`block[0].documents`).

## Advanced Search (CQL)

```bash
# Search by title
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=title~\"subscription\"&limit=20"

# Combine space + text
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=text~\"cost+center\"+AND+space=BASANTCLOUD"

# Search by label
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=label=\"application-owner\"+AND+space=BASANTCLOUD"

# Recently modified pages in a space
curl -sk "https://confluence.basf.net/rest/api/content/search?cql=space=DNSDHCP+AND+type=page+ORDER+BY+lastModified+DESC&limit=10"
```

## References

- [references/confluence-index.md](references/confluence-index.md) — Pre-indexed Confluence pages from key spaces
- [references/cloudref-index.md](references/cloudref-index.md) — Known Cloud Reference doc URLs
- [references/devhub-index.md](references/devhub-index.md) — DevHub landing site + Backstage Engineering Portal API
- [references/devhub-docs-index.md](references/devhub-docs-index.md) — DevHub platform documentation (Docusaurus, 728 pages: DSP, DevHub, APIs, App Store, Argus, Setup)
- [references/policies.md](references/policies.md) — Key BASF cloud/networking policies

---
name: corporate-rulebase-confluence
description: >
  Navigate the BASF Corporate Rule Base (CRB) on Confluence to find binding corporate policies,
  directives, and governance documents. Use when asked to find BASF corporate policy on a topic,
  check what the BASF rule is for a given activity, look up a CRB directive or guideline, verify
  whether something is covered by corporate governance, or identify which CRB area owns a topic
  (finance, legal, HR, EHSQ, communications, procurement, etc.). Trigger phrases: "find BASF
  corporate policy", "check CRB on X", "what is the BASF rule for", "is there a corporate
  directive on", "which CRB area covers", "look up BASF governance document".
  DO NOT use for product safety data sheets (SDS), site-specific local rules, country-level
  regulations, or non-BASF policy sources.
author: WalzDS
metadata:
  version: "1.1.0"
  category: knowledge-management
---

# Corporate Rule Base Confluence

- Map the request to one CRB area and open that area page first.
- Extract relevant document entries from the area page; if needed, drill down to child pages or run area-scoped CQL.
- Return concise results with direct links and page IDs.

## Start Pages

- CF - Corporate Finance (parent for CFM/CFP/CFT)
  - https://confluence.basf.net/spaces/CRB/pages/341412005
  - Finance governance hub with corporate requirements and related binding documents across accounting, reporting, risk, treasury, and financing.

- CFM - Corporate Mergers and Acquisitions
  - https://confluence.basf.net/spaces/CRB/pages/356096085
  - Focused M&A section covering advisory services and M&A process governance.

- CFP - Group Reporting and Performance Management
  - https://confluence.basf.net/spaces/CRB/pages/356096093
  - Group accounting/reporting, internal controls over financial reporting, and risk/performance related finance reporting standards.

- CFT - Corporate Treasury
  - https://confluence.basf.net/spaces/CRB/pages/356096089
  - Treasury operations including cash and bank management, payment services and fraud prevention, financing, derivatives, and pensions risk.

- CD - Corporate Development
  - https://confluence.basf.net/spaces/CRB/pages/341411975
  - Corporate development and digital governance topics, including commissions, innovation, cyber/information security governance, transfer pricing, and PCF/LCA related rules.

- COR - Corporate EHSQ
  - https://confluence.basf.net/spaces/CRB/pages/341412277
  - Large EHSQ corpus spanning environmental protection, health, occupational and process safety, emergency response, product safety, transport safety, and EHSQ reporting.

- COH - Corporate HR
  - https://confluence.basf.net/spaces/CRB/pages/341412048
  - HR policy area for human resources management, labor standards, talent/leadership, people-related reporting, and pensions-related topics.

- COI - Corporate Investor Relations
  - https://confluence.basf.net/spaces/CRB/pages/341412052
  - Investor relations governance centered on financial market communication, primarily the One Voice Policy.

- CL - Corporate Legal, Compliance and Insurance
  - https://confluence.basf.net/spaces/CRB/pages/341412026
  - Legal/compliance/insurance/security framework including competition law, anti-corruption, data privacy, trade compliance, and security governance documents.

- COM - Corporate Communications and Government Relations
  - https://confluence.basf.net/spaces/CRB/pages/341412054
  - Communications and advocacy rules including brand governance, media/crisis communications, employee communications, and political relations/association management.

- GB - Global Business Services
  - https://confluence.basf.net/spaces/CRB/pages/759075327
  - Focused set of IP-related governance documents, notably innovation and intellectual property topics.

- GP - Global Procurement
  - https://confluence.basf.net/spaces/CRB/pages/759075346
  - Procurement governance including procurement policy/framework, commodity and derivatives governance context, and passive contract manufacturing links.

## REST and CQL Patterns

Use page fetch when the page ID is known.
Use CQL when the ID is unknown or when filtering is needed.

## Fetch by Page ID

```
curl -sS -L \
  "https://confluence.basf.net/rest/api/content/<PAGE_ID>?expand=body.storage,space,version,metadata.labels"
```

## Browse by Hierarchy

Children of a start page:
```
curl -sS -L \
  "https://confluence.basf.net/rest/api/content/<PAGE_ID>/child/page?limit=50"
```

Descendants of a start page:
```
curl -sS -L \
  "https://confluence.basf.net/rest/api/content/<PAGE_ID>/descendant/page?limit=200"
```

## CQL Search Endpoint

```
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=CRB AND type=page'
```

## CQL Templates for CRB

By title text:
```
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=CRB AND type=page AND title ~ "Payment Fraud Prevention"'
```

By full-text content:
```
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=CRB AND type=page AND text ~ "corporate requirement"'
```

Scoped to one area using ancestor page ID (preferred for precision):
```
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=ancestor = 341412026 AND type = page'
```

Recently modified pages:
```
curl -sS -L --get \
  "https://confluence.basf.net/rest/api/content/search" \
  --data-urlencode 'cql=space=CRB AND type=page AND lastmodified >= now("-8w") ORDER BY lastmodified DESC'
```

## CQL Operator Guidance

- Use `=` for exact match.
- Use `~` for text/fuzzy match.
- Use `AND`/`OR` with parentheses for complex logic.
- Use `ORDER BY` for deterministic output ordering.

## Pagination and Response Checks

- Pagination: use `limit` and `start`, or follow `_links.next`.
- Always inspect `results`, `size`, `totalSize`, `_links.next`.
- For each result, capture `id`, `title`, `_links.webui`, and when available:
  `version.when`, `metadata.labels.results`.

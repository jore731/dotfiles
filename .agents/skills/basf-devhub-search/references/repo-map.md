# DevHub Documentation Repository Map

Quick reference for where to find what across the DevHub GitHub documentation landscape.
All repos are under the `basf-global` GitHub org.

## Primary Documentation Repos (search these first)

### dh-user-docs

End-user documentation for DevHub consumers (developers building on DevHub).
Docusaurus site. Path root: `docs/devhub/`.

| Path | Content |
|------|---------|
| `getting-started/` | Prerequisites, product creation, workspace setup, support |
| `guides/` | Apps & services, compute, custom domains, data sources, dev workflow, firewall, secrets, monitoring, routing, security, troubleshooting |
| `modules/` | AI & analytics, ETL tools, messaging, monitoring, storage |
| `tutorials/` | Create a frontend, API, RAG, MCP server, Databricks agent, data/ML pipeline, ask2sql agent |
| `tiers-and-charging/` | Pricing tiers and billing |
| `aigateway/` | **AI Gateway** — sub-sections below |
| `aigateway/getting-started/` | Access overview, prerequisites, first setup, deployment |
| `aigateway/guides/` | Authentication, consuming models, managing access, requesting models, monitoring, troubleshooting |
| `aigateway/references/` | API reference, available models, costs & billing |
| `explanations/` | Conceptual/explanatory content |
| `references/` | Reference material |

### dh-internal-docs

Internal team documentation: onboarding, ways of working, platform architecture.
Not a Docusaurus site — plain Markdown at root level.

| Path | Content |
|------|---------|
| `onboarding/` | New member onboarding (sub-teams: data-ai, runtime, webstore, devhub-general) |
| `ways-of-working/` | Team processes (TSG, data-ai, portal, runtime, webstore, cross-team) |
| `platform/` | Platform instance docs, architecture diagrams (drawio) |
| `glossary/` | Terminology, agile process, who-is-who, ownership matrix |

### dh-portal-docs

Platform documentation (legacy/parallel to dh-user-docs). Docusaurus site.
Path root: `docs/`.

| Path | Content |
|------|---------|
| `getting-started/` | Product creation, workspace, language setup, storage |
| `guides/` | Apps & services, Argus package feeds, compute, data sources, dev workflow, ML pipelines, ML model lifecycle, monitoring, routing, secrets, SSP groups |
| `tutorials/` | Create a frontend, API, data/ML pipeline |
| `explanations/` | Data access, identities |
| `references/` | Reference material |

### dh-developer-portal

Backstage-based self-service portal application (code, not docs).
Useful for: portal UI behaviour, Backstage templates, catalog entities.

## Secondary Repos (search for infra/platform-level questions)

### devhub-architecture

Architecture decisions, designs, operational docs.

| Path | Content |
|------|---------|
| `decisions/` | ADRs (0000–0050+): health checks, CDKTF, JupyterHub, Backstage templates, Envoy, AKS nodepools, workspace concept, product lifecycle, observability, etc. |
| `designs/` | Technical design docs (subnet allocation, BA enforcement) |
| `docs/` | Architecture diagrams, GitHub config, infrastructure, migration, observability, operations, security, services |

### dh-provisioning-modules

Monorepo for DevHub provisioning modules (Terraform/CDKTF).
Useful for: infrastructure module details, what gets provisioned for products.

### dh-provisioning-stack

Cloud infrastructure provisioning at scale.
Useful for: how products are provisioned end-to-end, stack configuration, deployment pipelines.

### dh-workflows

Reusable GitHub Actions workflows for DevHub-managed repositories.
Useful for: CI/CD questions, workflow templates, build/deploy pipelines.

### dh-registry-platform-prod

Production registry/catalog for platform entities.
Useful for: what products exist, platform entity schemas, registry lookups.

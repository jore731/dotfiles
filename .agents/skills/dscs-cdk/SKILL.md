---
name: dscs-cdk
description: >
  Build Azure infrastructure with DSCS CDK — a Python IaC framework on CDKTF with
  Pydantic models, resource constructs, and BASF conventions. Use when creating stacks,
  adding constructs, writing config models, debugging synthesis, or following BASF
  naming/security patterns. Triggers: dscs-cdk, basf constructs, CustomTerraformStack,
  ExcludeNoneModel, AllowPEResourceGroup, PrivateEndpoint, BASF Azure infrastructure.
---

# DSCS CDK

Python IaC framework on CDKTF for Azure infrastructure at BASF. Provides validated, opinionated constructs with Pydantic models, security-by-default mixins, and standardised naming.

## Quick Start

1. Subclass `CustomTerraformStack` and implement: `name_generator`, `project_config`, `stage_config`, `backend`
2. Create resources: `AllowPEResourceGroup` → `StorageAccount` / `KeyVault` / etc.
3. For production, use group constructs with private endpoints (e.g., `PrivateEndpointStorageAccount`)

See [EXAMPLES.md](EXAMPLES.md) for full stack code and resource patterns.

## Key Concepts

- **`~model` operator**: `ExcludeNoneModel.__invert__` → `model_dump(exclude_none=True, by_alias=True)` — bridges Pydantic to Terraform
- **Layered architecture**: Models → Resource Constructs (1:1 Terraform) → Group Constructs → User Stack
- **Generic type resolution**: `CustomResourceConstruct[T]` resolves Terraform type from Generic param
- **Mixin pattern**: `Literal` types lock security defaults; mixin goes **first** in MRO
- **`Microsoft.*` types**: Validate Azure resource names at model construction time
- **All `__init__.py` are EMPTY** — use direct path imports always

See [REFERENCE.md](REFERENCE.md) for architecture details, construct catalog, and development guide.

## Adding a New Resource — Checklist

1. **Provider**: Ensure the Terraform provider is available — check `uv add --dry-run cdktn-provider-<name>`. If unavailable, add to `cdktf.json` `terraformProviders` and run `cdktn get` for local bindings (see [REFERENCE.md](REFERENCE.md#adding-a-new-terraform-provider))
2. **Model**: `src/basf/models/<provider>/resources/<resource>.py` — `ExcludeNoneModel` subclass with `Field(description=...)`
3. **Construct**: `src/basf/terraform/resource_constructs/<provider>/resources/<resource>.py` — `CustomResourceConstruct[TerraformType]`
4. **Group construct** (if PE needed): Extend `PrivateEndpointConstruct`
5. **Tests**: `MockBaseStack` + `get_stack()` + `test_to_be_valid_terraform`
6. **Lint**: `ruff check src/ test/ && ruff format src/ test/`

## Build & Test

```bash
uv sync --all-groups
uv run pytest                    # all tests
uv run pytest <path> -v          # specific test
ruff check src/ test/            # lint
ruff format src/ test/           # format
uvx pre-commit run --all-files   # pre-commit hooks
```

## References

- [REFERENCE.md](REFERENCE.md) — Architecture, construct catalog, core concepts, development guide, Databricks settings & grants
- [EXAMPLES.md](EXAMPLES.md) — Stack examples, PE patterns, best practices, deployment
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Import errors, naming conflicts, DBFS 403, depends_on issues

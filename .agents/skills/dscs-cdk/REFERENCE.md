# DSCS CDK Reference

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Stack Code                         │
│  class MyStack(CustomTerraformStack): ...                   │
├─────────────────────────────────────────────────────────────┤
│               Group Constructs Layer                        │
│  PrivateEndpointStorageAccount, PrivateEndpointKeyVault,    │
│  DatabricksEnvironmentGroup, PrivateKubernetesCluster, ...  │
├─────────────────────────────────────────────────────────────┤
│              Resource Constructs Layer                       │
│  StorageAccount, KeyVault, RoleAssignment, Cluster, ...     │
├─────────────────────────────────────────────────────────────┤
│            Configuration Models Layer                        │
│  Pydantic ExcludeNoneModel subclasses, Microsoft.* types,   │
│  Mixins, ProjectConfig, StageConfig, NameGenerator          │
├─────────────────────────────────────────────────────────────┤
│           CDKTF / Terraform Providers                        │
│  cdktn-provider-azurerm, cdktn-provider-databricks, ...     │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Location | Purpose |
|-------|----------|---------|
| **Configuration Models** | `src/basf/models/` | Pure Pydantic data models with validation. No CDKTF dependency. |
| **Resource Constructs** | `src/basf/terraform/resource_constructs/` | 1:1 wrappers — one construct per Terraform resource/data source. |
| **Group Constructs** | `src/basf/terraform/group_constructs/` | Compose multiple resource constructs into reusable patterns. |
| **Central Services** | `src/basf/terraform/central_services_constructs/` | Data sources referencing shared DSCS infrastructure. |
| **User Stack** | Your `main.py` | Subclass `CustomTerraformStack`, wire constructs together. |

---

## Project Structure

```
dscs-cdk/
├── src/basf/
│   ├── models/                    # Pydantic configuration models
│   │   ├── abstract/              #   Base classes (ExcludeNoneModel)
│   │   ├── azure/                 #   Azure resource configs
│   │   │   ├── globals/           #     Naming constraints (Microsoft.*)
│   │   │   └── resources/         #     Resource-specific models
│   │   ├── azuread/               #   Azure AD models
│   │   ├── databricks/            #   Databricks models
│   │   ├── conventions/           #   Project & subscription conventions
│   │   └── types/                 #   Reusable constrained types
│   ├── terraform/
│   │   ├── resource_constructs/   # Single-resource CDKTF constructs
│   │   ├── group_constructs/      # Multi-resource patterns
│   │   ├── central_services_constructs/  # Shared DSCS infra data sources
│   │   ├── stacks/                # Stack definitions
│   │   ├── backends/              # Terraform backend configs
│   │   └── providers/             # Provider configurations
│   ├── construct/abstract/        # Base construct classes
│   ├── kubernetes/                # cdk8s constructs (ArgoCD)
│   ├── cli/                       # CLI tools (change detection)
│   └── utils/                     # Shared utilities
├── test/                          # Test suite (mirrors src/ structure)
└── examples/                      # Working example projects
```

---

## Core Concepts

### The `~model` Operator

`ExcludeNoneModel.__invert__` returns `model_dump(exclude_none=True, by_alias=True)`. This bridges Pydantic validation and Terraform resource creation:

```python
# In CustomResourceConstruct — the base class auto-creates the resource:
self._resource = resource_type(self.construct, "resource", **~resource_model)
```

Every config model must inherit from `ExcludeNoneModel`.

### Construct Hierarchy

```
App
└── CustomTerraformStack (your application stack)
    ├── AllowPEResourceGroup (logical grouping)
    │   ├── StorageAccount (individual resources)
    │   ├── KeyVault
    │   └── ContainerRegistry
    └── PrivateEndpointConstruct (complex patterns)
        ├── MainResource (e.g., PrivateStorageAccount)
        ├── PrivateEndpoint
        └── RoleAssignments
```

### Generic Type Resolution

`CustomResourceConstruct[T]` resolves its concrete Terraform resource type from the Generic parameter via MRO introspection (`__orig_bases__`). No `resource_factory` class variable is needed:

```python
class StorageAccount(CustomResourceConstruct[AzurermStorageAccount]):
    @property
    def resource_model(self) -> StorageAccountConfig:
        return StorageAccountConfig(name=..., resource_group_name=..., ...)
```

### CustomTerraformStack

Every stack must implement four abstract properties:

```python
class MyStack(CustomTerraformStack):
    @property
    def name_generator(self) -> NameGenerator: ...   # Naming convention instance
    @property
    def project_config(self) -> ProjectConfig: ...    # Global project configuration
    @property
    def stage_config(self) -> StageConfig: ...        # Stage-specific configuration
    @property
    def backend(self) -> TerraformBackend: ...        # State backend configuration
```

Initialize providers in `__init__` via:
- `self.init_azure_provider(subscription_id, default=True)` for Azure
- `self.init_provider(ProviderClass, alias)` for other providers

### Adding a New Terraform Provider

When a construct needs a provider that isn't already a dependency:

1. **Check if a pre-built package exists**:
   ```bash
   uv add --dry-run cdktn-provider-<name>
   ```
   If it resolves, add it to `pyproject.toml` dependencies normally.

2. **If no package exists**, generate local bindings:
   - Add the provider to `cdktf.json` under `terraformProviders` (e.g., `"Azure/azapi@~> 2.0"`)
   - Run `cdktn get` to generate Python bindings into `imports/<provider>/`
   - Import from `imports.<provider>.<resource>` instead of `cdktn_provider_<name>.<resource>`
   - Commit the generated `imports/` directory (check `.gitignore`)

### `depends_on` in Constructs

Both `CustomResourceConstruct` and `CustomDataSourceConstruct` support an optional `depends_on` parameter:

```python
# ✅ Correct — use the constructor parameter
data_source = DataStorageAccount(
    parent=rg, id="default-storage",
    depends_on=[self.main_resource],
)
```

**⚠️ Never use `add_override("depends_on", [...])` with `.fqn`** — it produces `${...}` interpolation syntax which Terraform rejects. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#depends_on-produces-interpolation-syntax).

### Naming Conventions

`Microsoft.*` constrained types validate resource names at model construction time:

```python
Microsoft.Storage.StorageAccountsValidName        # 3-24 chars, ^[a-z0-9]+$
Microsoft.KeyVault.KeyVaultsValidName              # 3-24 chars, ^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]$
Microsoft.Resources.ResourceGroupsValidName        # 1-90 chars
Microsoft.ContainerRegistry.RegistriesValidName    # 5-50 chars, ^[a-zA-Z0-9]+$
Microsoft.Global.AzureLocation                     # Enum: westeurope, northeurope, swedencentral
```

### Mixin Pattern for Policy Enforcement

Mixins use `Literal` types to lock field values and go **first** in MRO:

```python
class PrivateStorageAccountMixin(BaseModel):
    public_network_access_enabled: Literal[False] = False
    network_rules: NetworkRules = Field(default_factory=DenyNonAzureServices)

class PrivateStorageAccountConfig(PrivateStorageAccountMixin, StorageAccountConfig):
    pass
```

Rules:
- Mixins inherit from `BaseModel` (not `ExcludeNoneModel`).
- The mixin goes **FIRST** in MRO for value precedence.
- Use `Literal` types to lock values that should not be overridden.

---

## Available Constructs

### Resource Constructs (55+ total)

| Resource | Class | Import Path |
|----------|-------|-------------|
| Resource Group | `AllowPEResourceGroup` | `basf.terraform.resource_constructs.azure.resources.resource_group` |
| Storage Account | `StorageAccount`, `PrivateStorageAccount` | `basf.terraform.resource_constructs.azure.resources.storage_account` |
| Key Vault | `KeyVault`, `PrivateKeyVault` | `basf.terraform.resource_constructs.azure.resources.key_vault` |
| Key Vault Secret | `KeyVaultSecret`, `ChangeMeKeyVaultSecret` | `basf.terraform.resource_constructs.azure.resources.key_vault_secret` |
| Container Registry | `ContainerRegistry`, `PrivateContainerRegistry` | `basf.terraform.resource_constructs.azure.resources.container_registry` |
| Databricks Workspace | `DatabricksWorkspace`, `PrivateDatabricksWorkspace` | `basf.terraform.resource_constructs.azure.resources.databricks_workspace` |
| Databricks Cluster | `Cluster`, `SharedCluster` | `basf.terraform.resource_constructs.databricks.resources.cluster` |
| PostgreSQL Server | `PostgresFlexibleServer`, `PrivatePostgresFlexibleServer` | `basf.terraform.resource_constructs.azure.resources.postgres_flexible_server` |
| Redis Cache | `RedisCache`, `PrivateRedisCache` | `basf.terraform.resource_constructs.azure.resources.redis_cache` |
| Kubernetes Cluster | `KubernetesCluster`, `PrivateKubernetesCluster` | `basf.terraform.resource_constructs.azure.resources.kubernetes_cluster` |
| Cosmos DB | `CosmosDBAccount`, `PrivateCosmosDBAccount` | `basf.terraform.resource_constructs.azure.resources.cosmosdb` |
| Role Assignment | `RoleAssignment` | `basf.terraform.resource_constructs.azure.resources.role_assignment` |
| User Assigned Identity | `UserAssignedIdentity` | `basf.terraform.resource_constructs.azure.resources.user_assigned_identity` |
| Databricks Grants | `Grants`, `CatalogGrants`, `SchemaGrants`, `ExternalLocationGrants`, `StorageCredentialGrants` | `basf.terraform.resource_constructs.databricks.resources.grants` |
| Databricks Grant | `CatalogGrant`, `SchemaGrant`, `ExternalLocationGrant`, `StorageCredentialGrant` | `basf.terraform.resource_constructs.databricks.resources.grant` |

### Group Constructs (Private Endpoint Patterns)

| Pattern | Class | Import Path |
|---------|-------|-------------|
| Private Storage (File+Blob) | `PrivateEndpointStorageAccount` | `basf.terraform.group_constructs.azure.resources.private_endpoint.storage_account` |
| Private ADLS Gen2 (Blob+DFS) | `PrivateEndpointADLSStorageAccount` | (same module) |
| Private Key Vault | `PrivateEndpointKeyVault` | `basf.terraform.group_constructs.azure.resources.private_endpoint.key_vault` |
| Private Container Registry | `PrivateEndpointContainerRegistry` | `basf.terraform.group_constructs.azure.resources.private_endpoint.container_registry` |
| Private Cosmos DB | `PrivateEndpointCosmosDBAccount` | `basf.terraform.group_constructs.azure.resources.private_endpoint.cosmosdb` |
| Private Databricks | `PrivateEndpointDatabricksWorkspace` | `basf.terraform.group_constructs.azure.resources.private_endpoint.databricks_workspace` |
| Private PostgreSQL | `PrivateEndpointPostgresFlexibleServer` | `basf.terraform.group_constructs.azure.resources.private_endpoint.postgres_flexible_server` |
| Private Redis | `PrivateEndpointRedisCache` | `basf.terraform.group_constructs.azure.resources.private_endpoint.redis_cache` |
| Private AKS | `PrivateKubernetesClusterGroup` | `basf.terraform.group_constructs.azure.resources.private_kubernetes_cluster` |
| Databricks Environment | `DatabricksEnvironmentGroup` | `basf.terraform.group_constructs.databricks.resources.databricks_environment` |

---

## Pydantic Model Conventions

| Rule | Example |
|------|---------|
| Inherit from `ExcludeNoneModel` | `class MyConfig(ExcludeNoneModel):` |
| Every field has `Field(description=...)` | `name: str = Field(description="The name.")` |
| Use `Microsoft.*` types for names | `name: Microsoft.Storage.StorageAccountsValidName` |
| Use `str` enums | `class Tier(str, Enum): standard = "Standard"` |
| Modern Python syntax | `field: str \| None` not `Optional[str]` |
| Module docstring with Terraform URL | `"""...\nDocs: https://registry.terraform.io/..."""` |
| Mixins inherit from `BaseModel` | `class MyMixin(BaseModel):` |
| Mixins go first in MRO | `class Private(Mixin, Base):` |

---

## Development Guide — Adding a New Resource

### Step 1: Create the Configuration Model

**Location**: `src/basf/models/<provider>/resources/<resource>.py`

```python
"""
Widget configuration model.

Official documentation: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/widget
"""

from pydantic import Field
from basf.models.abstract.exclude_none_model import ExcludeNoneModel
from basf.models.azure.globals.naming_constraints import Microsoft

class WidgetConfig(ExcludeNoneModel):
    """Configuration for an Azure Widget."""
    name: Microsoft.SomeService.WidgetValidName = Field(description="The name of the Widget.")
    resource_group_name: str = Field(description="The resource group name.")
    location: str = Field(description="The Azure Region.")
    sku: str | None = Field(default=None, description="The SKU.")
    tags: dict[str, str] | None = Field(default=None, description="Tags to assign.")
```

### Step 2: Create the Resource Construct

**Location**: `src/basf/terraform/resource_constructs/<provider>/resources/<resource>.py`

```python
from typing import TYPE_CHECKING
from cdktn_provider_azurerm.widget import Widget as AzurermWidget
from basf.construct.abstract.custom_resource_construct import CustomResourceConstruct
from basf.models.azure.resources.widget import WidgetConfig

if TYPE_CHECKING:
    from basf.terraform.resource_constructs.azure.resources.resource_group import AllowPEResourceGroup

class Widget(CustomResourceConstruct[AzurermWidget]):
    resource: AzurermWidget
    parent: "AllowPEResourceGroup"

    def __init__(self, parent: "AllowPEResourceGroup", id: str, name: str,
                 custom_resource_model: WidgetConfig | None = None):
        self._name = name
        super().__init__(parent, id, custom_resource_model)

    @property
    def resource_model(self) -> WidgetConfig:
        return WidgetConfig(name=self._name, resource_group_name=self.parent.resource.name,
                            location=self.parent.resource.location)
```

### Step 3: Create the Group Construct (if needed)

For private endpoint patterns, extend `PrivateEndpointConstruct`:

```python
from basf.models.azure.resources.private_endpoint import PrivateEndpointSubresources
from basf.terraform.group_constructs.azure.templates.private_endpoint_construct import PrivateEndpointConstruct
from basf.terraform.resource_constructs.azure.resources.widget import Widget

class PrivateEndpointWidget(PrivateEndpointConstruct):
    main_resource: Widget

    def __init__(self, parent, id, *args, **kwargs):
        super().__init__(parent, id, *args, **kwargs)

    @property
    def private_endpoint_subresources(self):
        return [PrivateEndpointSubresources.Widget_SubResource]

    def init_main_resource(self):
        self.main_resource = Widget(self, "main_resource")
```

### Step 4: Add Tests

**Location**: `test/terraform/resource_constructs/<provider>/resources/test_<resource>.py`

```python
from cdktn import Testing
from test.common import common_tests
from test.common.cdktf_fixtures import full_synth, get_stack, synth
from test.common.mocks.mock_base_stack import MockBaseStack
from basf.terraform.resource_constructs.azure.resources.resource_group import AllowPEResourceGroup
from basf.terraform.resource_constructs.azure.resources.widget import Widget

class MockStack(MockBaseStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)
        self.rg = AllowPEResourceGroup(self, id="test-rg")
        self.widget = Widget(self.rg, id="test-widget", name="my-widget")

stack = get_stack(MockStack)
_ = synth, full_synth

def test_to_be_valid_terraform(full_synth):
    return common_tests.to_be_valid_terraform(full_synth)

def test_to_have_correct_widget_definition(full_synth, synth, stack: MockStack):
    assert Testing.to_have_resource_with_properties(synth, "azurerm_widget", {"name": "my-widget"})
```

### Step 5: Export in `__init__.py`

⚠️ **All `__init__.py` files in dscs-cdk are EMPTY.** Imports are always direct path imports. Do not add exports unless the package already uses them.

---

## Databricks Workspace Settings

Databricks workspace settings control security, compliance, and feature toggles. The library provides `WorkspaceSettingKeys` enum and Pydantic models for type-safe configuration.

### Available Setting Keys

All known keys are in `WorkspaceSettingKeys` (in `basf.models.databricks.resources.workspace_setting`):

| Key | Scope | Notes |
|-----|-------|-------|
| `LLM_PROXY_PARTNER_POWERED` | Workspace | Generic setting, uses `boolean_val` |
| `DEFAULT_NAMESPACE` | Workspace | Dedicated resource |
| `RESTRICT_WORKSPACE_ADMINS` | Workspace | Dedicated resource |
| `COMPLIANCE_SECURITY_PROFILE_WORKSPACE` | Workspace | Dedicated resource |
| `ENHANCED_SECURITY_MONITORING_WORKSPACE` | Workspace | Dedicated resource |
| `AUTOMATIC_CLUSTER_UPDATE_WORKSPACE` | Workspace | Dedicated resource |
| `DISABLE_LEGACY_ACCESS` | Workspace | Dedicated resource, has custom construct |
| `DISABLE_LEGACY_DBFS` | Workspace | Dedicated resource |
| `DISABLE_LEGACY_FEATURES` | **Account** | Account-scoped, not workspace |

### Two Patterns for Settings

**Pattern 1: Generic `WorkspaceSettingV2` with `name=` parameter** — for settings using `boolean_val`, `string_val`, or `integer_val`:

```python
from imports.databricks.workspace_setting_v2 import WorkspaceSettingV2
from basf.models.databricks.resources.workspace_setting import WorkspaceSettingKeys

WorkspaceSettingV2(
    self, "ai-services-setting",
    name=WorkspaceSettingKeys.LLM_PROXY_PARTNER_POWERED.value,
    boolean_val={"value": True},
)
```

**Pattern 2: Dedicated setting resource with custom construct** — for settings with their own Terraform resource:

```python
from basf.terraform.resource_constructs.databricks.resources.disable_legacy_access_setting import (
    DisableLegacyAccessSetting,
)
DisableLegacyAccessSetting(parent=workspace, id="disable-legacy-access")
```

The `PrivateEndpointDatabricksWorkspace` group construct automatically provisions common settings — check its `init_children()` before adding settings manually.

---

## Databricks Grants

Two grant patterns mapping to `databricks_grants` (authoritative, plural) and `databricks_grant` (non-authoritative, singular).

### Authoritative Grants (Preferred)

`databricks_grants` **overwrites ALL existing grants** on a securable object. Only one resource per securable should exist. Typed subclasses auto-populate the securable identifier from the parent:

| Class | Parent Type | Securable |
|-------|-------------|-----------|
| `CatalogGrants` | `Catalog` | `catalog` |
| `SchemaGrants` | `Schema` | `schema` |
| `ExternalLocationGrants` | `ExternalLocation` | `external_location` |
| `StorageCredentialGrants` | `StorageCredential` | `storage_credential` |

```python
from basf.terraform.resource_constructs.databricks.resources.grants import CatalogGrants
from basf.models.databricks.resources.grants import GrantEntryConfig, CatalogPrivilege

catalog_grants = CatalogGrants(
    parent=my_catalog, id="catalog-grants",
    grants=[GrantEntryConfig(principal="my-group",
        privileges=[CatalogPrivilege.USE_CATALOG, CatalogPrivilege.USE_SCHEMA])],
)
```

### Non-Authoritative Grant (Additive)

`databricks_grant` manages a **single principal's grants**. Multiple can coexist for the same securable:

```python
from basf.terraform.resource_constructs.databricks.resources.grant import ExternalLocationGrant
from basf.models.databricks.resources.grants import ExternalLocationPrivilege

grant = ExternalLocationGrant(
    parent=my_external_location, id="user-read",
    principal="my-group",
    privileges=[ExternalLocationPrivilege.READ_FILES, ExternalLocationPrivilege.BROWSE],
)
```

### Privilege Enums

All privilege enums are `str, Enum` subclasses in `basf.models.databricks.resources.grants`:

`MetastorePrivilege`, `CatalogPrivilege`, `SchemaPrivilege`, `TablePrivilege`, `VolumePrivilege`, `RegisteredModelPrivilege`, `FunctionPrivilege`, `CredentialPrivilege`, `StorageCredentialPrivilege`, `ExternalLocationPrivilege`, `ConnectionPrivilege`, `SharePrivilege`

### DatabricksEnvironmentGroup Grants

The `DatabricksEnvironmentGroup` auto-provisions grants for AD groups via cached properties (`catalog_grants`, `external_location_grants`). These are wired automatically via `init_children()`.

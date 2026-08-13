# DSCS CDK Examples

## Quick Start Stack

```python
#!/usr/bin/env python3
from cdktn import App, LocalBackend
from cdktn_provider_time.provider import TimeProvider
from constructs import Construct

from basf.construct.abstract.custom_terraform_stack import CustomTerraformStack
from basf.models.azure.globals.naming_constraints import Microsoft
from basf.models.conventions.azure.subscription import AzureSubscriptionConfig
from basf.models.conventions.constants import SubscriptionNetworkMode
from basf.models.conventions.default_name_generator import DefaultNameGenerator
from basf.models.conventions.project import ProjectConfig, ProjectStage, StageConfig
from basf.terraform.resource_constructs.azure.resources.resource_group import AllowPEResourceGroup
from basf.terraform.resource_constructs.azure.resources.storage_account import StorageAccount


class MyStack(CustomTerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        self.init_azure_provider(
            subscription_id=self.name_generator.subscription_id, default=True
        )
        self.init_provider(TimeProvider, "time")

        rg = AllowPEResourceGroup(self, "rg")
        storage = StorageAccount(parent=rg, id="main-storage", storage_id="001")

    @property
    def name_generator(self) -> DefaultNameGenerator:
        return DefaultNameGenerator(self)

    @property
    def project_config(self) -> ProjectConfig:
        return ProjectConfig(
            name="my-project",
            owner=["your-email@basf.com"],
            azure=AzureSubscriptionConfig(
                location=Microsoft.Global.AzureLocation.north_europe,
                network_mode=SubscriptionNetworkMode.internal,
            ),
            tags={"env": "dev", "project": "my-project"},
        )

    @property
    def stage_config(self) -> StageConfig:
        return StageConfig(stage=ProjectStage.development, base_CN="my-project.basf.net")

    @property
    def backend(self) -> LocalBackend:
        return LocalBackend(self.construct)


app = App()
MyStack(app, "my-stack")
app.synth()
```

---

## Storage Account with Private Endpoint

```python
from basf.terraform.group_constructs.azure.resources.private_endpoint.storage_account import (
    PrivateEndpointStorageAccount,
)
from basf.models.azure.resources.storage_account import (
    StorageAccountConfig, AccountTier, AccountReplicationType,
)

private_storage = PrivateEndpointStorageAccount(
    parent=resource_group,
    id="private-storage",
    storage_id="001",
    config=StorageAccountConfig(
        account_tier=AccountTier.Premium,
        account_replication_type=AccountReplicationType.ZRS,
    ),
)
```

---

## Key Vault with Secrets

```python
from basf.terraform.group_constructs.azure.resources.private_endpoint.key_vault import (
    PrivateEndpointKeyVault,
)
from basf.terraform.group_constructs.azure.resources.key_vault.key_vault_secret import (
    KeyVaultSecret, RandomKeyVaultSecret,
)

vault = PrivateEndpointKeyVault(parent=resource_group, id="main-vault")

# Static secret
db_secret = KeyVaultSecret(
    parent=vault.main_resource, id="database-connection",
    name="db-conn-str", value="Server=myserver;Database=mydb;",
)

# Random secret (auto-generated password)
api_secret = RandomKeyVaultSecret(
    parent=vault.main_resource, id="api-key", name="external-api-key"
)
```

---

## Container Registry with Private Endpoint

```python
from basf.terraform.group_constructs.azure.resources.private_endpoint.container_registry import (
    PrivateEndpointContainerRegistry,
)
from basf.models.azure.resources.container_registry import (
    AzureContainerRegistryConfig, AzureContainerRegistrySKU,
)

registry = PrivateEndpointContainerRegistry(
    parent=resource_group,
    id="main-registry",
    config=AzureContainerRegistryConfig(
        sku=AzureContainerRegistrySKU.premium,
        admin_enabled=False,
        public_network_access_enabled=False,
    ),
)
```

---

## Databricks Shared Cluster (Non-Serverless)

```python
from basf.terraform.resource_constructs.databricks.resources.cluster import SharedCluster
from basf.models.databricks.resources.cluster import (
    SharedClusterConfig, ClusterAutoscaleConfig,
)

# Basic shared cluster (uses defaults: autoscale 1-2, photon, 120min timeout)
cluster = SharedCluster(
    parent=databricks_workspace,  # A CustomConstruct with workspace provider
    id="shared-compute",
    cluster_name="shared-cluster",
    spark_version="15.4.x-scala2.12",
    node_type_id="Standard_D4ds_v5",
    custom_provider=workspace_provider,
)

# Customized shared cluster
cluster = SharedCluster(
    parent=databricks_workspace,
    id="data-engineering",
    cluster_name="data-eng-cluster",
    spark_version="15.4.x-scala2.12",
    node_type_id="Standard_E8ds_v5",
    custom_provider=workspace_provider,
    custom_resource_model=SharedClusterConfig(
        autoscale=ClusterAutoscaleConfig(min_workers=2, max_workers=8),
        autotermination_minutes=60,
        spark_conf={"spark.databricks.delta.preview.enabled": "true"},
        custom_tags={"team": "data-engineering"},
    ),
)
```

---

## Databricks Grants

```python
from basf.terraform.resource_constructs.databricks.resources.grants import CatalogGrants
from basf.models.databricks.resources.grants import GrantEntryConfig, CatalogPrivilege

catalog_grants = CatalogGrants(
    parent=my_catalog,
    id="catalog-grants",
    grants=[
        GrantEntryConfig(
            principal="data-engineers",
            privileges=[CatalogPrivilege.USE_CATALOG, CatalogPrivilege.USE_SCHEMA],
        ),
        GrantEntryConfig(
            principal="data-readers",
            privileges=[CatalogPrivilege.USE_CATALOG],
        ),
    ],
)
```

---

## Best Practices

### Use Group Constructs for Security

```python
# ✅ Good — includes private endpoint
private_storage = PrivateEndpointStorageAccount(parent=rg, id="main", storage_id="001")

# ❌ Avoid in production — public endpoint
storage = StorageAccount(parent=rg, id="main", storage_id="001")
```

### Use Meaningful IDs

```python
# ✅ Good
app_storage = StorageAccount(parent=rg, id="app-data", storage_id="001")
logs_storage = StorageAccount(parent=rg, id="logs", storage_id="002")

# ❌ Avoid
storage1 = StorageAccount(parent=rg, id="s1", storage_id="001")
```

### Use Configuration Objects for Complex Resources

```python
config = StorageAccountConfig(
    account_tier=AccountTier.Premium,
    account_replication_type=AccountReplicationType.ZRS,
)
storage = PrivateEndpointStorageAccount(parent=rg, id="main", storage_id="001", config=config)
```

### Organize by Environment

```python
class ProductionStack(CustomTerraformStack):
    @property
    def stage_config(self):
        return StageConfig(stage=ProjectStage.production, base_CN="myapp.basf.net")

class DevelopmentStack(CustomTerraformStack):
    @property
    def stage_config(self):
        return StageConfig(stage=ProjectStage.development, base_CN="myapp-dev.basf.net")
```

---

## Deployment

```bash
# Install dependencies
uv sync

# Authenticate with Azure
az login

# Synthesize and deploy
uv run cdktf plan
uv run cdktf deploy
```

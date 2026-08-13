# DSCS CDK Troubleshooting

## Module Import Errors

```bash
uv list | grep dscs-cdk
uv add dscs-cdk --index-url https://artifactory.basf.net/artifactory/api/pypi/pypi-python-dscs/simple --upgrade
```

---

## Resource Naming Conflicts

Ensure `id` and semantic IDs (e.g., `storage_id`) are unique within each parent scope:

```python
# ✅ Unique storage_ids
storage_app = StorageAccount(parent=rg, id="app-data", storage_id="001")
storage_logs = StorageAccount(parent=rg, id="logs", storage_id="002")

# ❌ Duplicate storage_id — will cause naming conflict
storage1 = StorageAccount(parent=rg, id="d1", storage_id="001")
storage2 = StorageAccount(parent=rg, id="d2", storage_id="001")
```

---

## Construct ID Disambiguation

When creating multiple instances of the same construct type under the same parent, provide explicit `id=` values:

```python
rg1 = AllowPEResourceGroup(self, id="app-rg")
rg2 = AllowPEResourceGroup(self, id="data-rg")
```

---

## Databricks DBFS 403 After Enabling Private Endpoints

**Symptom**: `dbutils.fs.ls("/Volumes/...")` returns **403 Forbidden**, but direct FUSE-mounted listing works.

**Cause**: The workspace's **default (managed/DBFS) storage account** lacks a private endpoint. `dbutils.fs.ls` routes through the DBFS API → default storage account, which is blocked without a blob PE.

**Fix**: Enable a private endpoint on the Databricks default storage account:
1. Set `custom_parameters.storage_account_name` on the workspace to a custom name (e.g., `f"{resource_prefix}dbksinternal"`).
2. Create a `DataStorageAccount` data source referencing this storage account (with `depends_on` on the workspace).
3. Create a blob private endpoint targeting the data source's ID.

The `PrivateEndpointDatabricksWorkspace` group construct handles this automatically via `default_storage_data` and `default_storage_blob_private_endpoint`.

---

## `depends_on` Produces Interpolation Syntax

**Symptom**: Terraform errors with `Error: Invalid expression` on a `depends_on` block containing `"${azurerm_...}"`.

**Cause**: Using `resource.add_override("depends_on", [other_resource.fqn])`. The `.fqn` property wraps references in `${...}` which is invalid for Terraform's `depends_on` (requires static references).

**Fix**: Use the constructor's `depends_on` parameter instead:

```python
# ✅ Correct
my_data_source = DataStorageAccount(
    parent=rg, id="storage-data",
    depends_on=[self.main_resource],
)

# ❌ Wrong — never do this
my_data_source.resource.add_override("depends_on", [self.main_resource.resource.fqn])
```

---

## Serverless Compute Cannot Be Disabled via Terraform

Serverless compute **cannot** be disabled via Terraform or the Databricks REST API. The API returns:

> "Serverless Compute is not allowed to be disabled for your workspace. Please contact Databricks Support."

To disable serverless compute, open a support ticket with Databricks. Use `SharedCluster` to provision classic (non-serverless) compute instead.

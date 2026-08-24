# DevHub Platform Documentation Index

Base URL: `https://devhub.intranet.basf.com/documentation/`

The DevHub documentation is a **Docusaurus** static site. Pages are server-rendered HTML and require **Azure AD authentication** (BASF SSO) — same token broker as the rest of DevHub:

```bash
TOKEN=$(az account get-access-token --resource 074bdf99-9d4c-46db-8395-c8a42baaa6ce --query accessToken -o tsv)
curl -sk -H "Authorization: Bearer $TOKEN" "https://devhub.intranet.basf.com/documentation/<PATH>/"
unset TOKEN   # never print or share the raw token
```

Paths below are relative to the base URL (omit the leading `documentation/`). Append a trailing `/` when fetching.

## How to use this index

1. Find the topic in the tables below → note its **path**.
2. Fetch that single page (auth header as above) and strip HTML to read the content:

```bash
curl -sk -H "Authorization: Bearer $TOKEN" "https://devhub.intranet.basf.com/documentation/devhub/getting-started/prerequisites/" \
  | python3 -c "import sys,re,html; h=sys.stdin.read(); m=re.search(r'<main.*?</main>',h,re.S); t=re.sub(r'<[^>]+>',' ',m.group(0) if m else h); print(html.unescape(re.sub(r'\s+',' ',t))[:3000])" 
```

Only the exact page paths listed below are fetchable. Bare category/landing
prefixes (e.g. `devhub/getting-started/`) have no own page and return **403** —
always use a full path from the tables.

## Refreshing this index

This file was generated from the Docusaurus local search index (plugin `@easyops-cn/docusaurus-search-local`), which lists every page with title, URL and breadcrumb:

```bash
curl -sk -H "Authorization: Bearer $TOKEN" "https://devhub.intranet.basf.com/documentation/search-index.json" -o search-index.json
# block[0].documents = page list {i:id, t:title, u:url, b:breadcrumb}
```
_Snapshot: 2026-06-18 — 728 pages across 6 sections._

## Site Structure

| Section | Pages | Path Prefix | Description |
|---------|------:|-------------|-------------|
| DataScience Platform | 241 | `dsp/` | ML/AI workspaces, tools & resources, Azure DevOps/GitHub projects, Enterprise Data Lake, monitoring |
| DevHub Platform | 186 | `devhub/` | Onboarding, build & configure, deploy & operate, AI Gateway, guides, references, troubleshooting |
| APIs @ BASF | 156 | `apis/` | API enablement program, API guidelines, knowledge base, large API glossary |
| App Store | 75 | `appstore/` | App templates, lifecycle management, AAD migration, API gateway, analytics |
| Argus | 54 | `argus/` | Argus product docs — getting started, guides, references, tutorials, explanations |
| Developer Setup | 16 | `setup/` | Local dev environment — programming languages, tools, version control, code editors, CA certs |

---

## DataScience Platform (`dsp/`, 241 pages)

### Overview (1)

| Path | Title |
|------|-------|
| `dsp` | DataScience Platform |

### Tools And Resources (146)

| Path | Title |
|------|-------|
| `dsp/tools-and-resources/accessing-on-prem-data-sources` | Accessing On-Prem Data Sources |
| `dsp/tools-and-resources/adf-azure-data-factory/adf-integration-runtime` | What is Integration Runtime? |
| `dsp/tools-and-resources/adf-azure-data-factory/adf-quickstart-guide` | Azure Data Factory Quickstart |
| `dsp/tools-and-resources/adf-azure-data-factory/best-practices-loading-data` | Best Practices Loading Data |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services` | Linking ADF to different Services |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-adls` | Link ADF with ADLS |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-adls/link-adf-with-dedicated-adls` | Dedicated ADLS |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-adls/link-adf-with-edl-storage-layer` | How to connect with the Central ADLS |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-azure-machine-learning` | Linking AzureML |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-databricks` | Link Databricks |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-odbc` | Connecting to an ODBC Database |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-polybase` | Connecting ADF to Polybase |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-repository` | Link Azure DevOps Repository |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-resources-on-prem` | Introduction |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-resources-on-prem/link-adf-with-sqldb-onprem` | 1. Prerequisites |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-resources-on-prem/read-data-from-sap-hana` | Creating a Copy activity |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-resources-on-prem/write-edl-data-into-hana` | Intro |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-sharepoint` | Connecting SharePoint to ADF |
| `dsp/tools-and-resources/adf-azure-data-factory/linking-adf-to-services/link-adf-with-sql-db` | Linked service |
| `dsp/tools-and-resources/adf-azure-data-factory/moving-dev-to-prod-adf` | Process to move data from ADF-DEV to ADF-PROD |
| `dsp/tools-and-resources/adf-azure-data-factory/serverless-compute` | Serverless Compute Guide for ADF |
| `dsp/tools-and-resources/adf-azure-data-factory/use-cases` | index |
| `dsp/tools-and-resources/adf-azure-data-factory/use-cases/copy-activity` | copy-activity |
| `dsp/tools-and-resources/adf-azure-data-factory/use-cases/data-flows` | data-flows |
| `dsp/tools-and-resources/adf-azure-data-factory/use-cases/power-query` | power-query |
| `dsp/tools-and-resources/adf-azure-data-factory/using-alerts-in-adf` | Alerts in Azure Data Factory |
| `dsp/tools-and-resources/adf-azure-data-factory/using-storage-triggers` | Storage Triggers |
| `dsp/tools-and-resources/adf-azure-data-factory/using-triggers-in-adf` | How to use triggers in Azure Data Factory |
| `dsp/tools-and-resources/adls-gen2` | Creating additional Containers |
| `dsp/tools-and-resources/adls-gen2/adls-gen2-link-using-service-principle` | Python Read/Write data from ADLS2 using Service Principal (SP) |
| `dsp/tools-and-resources/adls-gen2/adls-gen2-link-with-storage-explorer` | Storage Explorer |
| `dsp/tools-and-resources/aml-azure-machine-learning/aml-limitations` | Limitations |
| `dsp/tools-and-resources/aml-azure-machine-learning/aml-quickstart-guide` | Azure Machine Learning - Quickstart |
| `dsp/tools-and-resources/aml-azure-machine-learning/auto-ml` | 1. Intro |
| `dsp/tools-and-resources/aml-azure-machine-learning/auto-ml/automl-sdk` | 1. Intro |
| `dsp/tools-and-resources/aml-azure-machine-learning/auto-ml/automl-ui/additional-configurations` | Additional configurations |
| `dsp/tools-and-resources/aml-azure-machine-learning/auto-ml/automl-ui/clasiffication-model` | How to create a regression model |
| `dsp/tools-and-resources/aml-azure-machine-learning/auto-ml/automl-ui/featurization-settings` | Featurization settings |
| `dsp/tools-and-resources/aml-azure-machine-learning/auto-ml/automl-ui/regression-model` | How to create a regression model |
| `dsp/tools-and-resources/aml-azure-machine-learning/auto-ml/clasiffication-vs-regression` | What is the difference between Regression vs Classification |
| `dsp/tools-and-resources/aml-azure-machine-learning/compute` | Compute targets features by use |
| `dsp/tools-and-resources/aml-azure-machine-learning/compute/create-attached-compute` | Attached computes creation |
| `dsp/tools-and-resources/aml-azure-machine-learning/compute/create-compute-cluster` | Compute cluster creation |
| `dsp/tools-and-resources/aml-azure-machine-learning/compute/create-compute-instance` | Compute instance creation |
| `dsp/tools-and-resources/aml-azure-machine-learning/datastore-datasset` | Important to Remind |
| `dsp/tools-and-resources/aml-azure-machine-learning/datastore-datasset/how-to-create-datassets` | Types of Data asset |
| `dsp/tools-and-resources/aml-azure-machine-learning/datastore-datasset/how-to-create-datassets/from_local_file` | How to create a Data asset "From Local File" |
| `dsp/tools-and-resources/aml-azure-machine-learning/datastore-datasset/how-to-create-datassets/mltable` | What is Table(mltable)? |
| `dsp/tools-and-resources/aml-azure-machine-learning/datastore-datasset/how-to-create-datassets/uri_file` | What is File (uri_file)? |
| `dsp/tools-and-resources/aml-azure-machine-learning/datastore-datasset/how-to-create-datassets/uri_folder` | What is Folder(uri_folder)? |
| `dsp/tools-and-resources/aml-azure-machine-learning/datastore-datasset/types-of-datastores` | Datastores Types Overview |
| `dsp/tools-and-resources/aml-azure-machine-learning/endpoints-and-deployments` | What are endpoints and deployments? |
| `dsp/tools-and-resources/aml-azure-machine-learning/endpoints-and-deployments/deploy-model-with-sdk` | Objective |
| `dsp/tools-and-resources/aml-azure-machine-learning/endpoints-and-deployments/test-and-debug-endpoint-locally` | Debugging scoring script with Azure ML inference HTTP server |
| `dsp/tools-and-resources/aml-azure-machine-learning/environments` | Environments |
| `dsp/tools-and-resources/aml-azure-machine-learning/git-flow` | Git Flow |
| `dsp/tools-and-resources/aml-azure-machine-learning/installing-libraries` | Installing Libraries |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-to-vscode` | Connecting AzureML to VSCode |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-adls` | Initial steps |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-adls/read-from-adls` | Reading from Azure Data Lakes |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-adls/write-into-adls-from-notebook` | Writing from AML to ADLS gen2 from a Notebook |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-adls/write-into-adls` | Write Into ADLS gen2 |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-repository` | Link Azure DevOps Repository |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-sql-db/read-from-sql-db` | Read From SQL DB |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-sql-db/write-into-sql-db-via-odbc` | Writing from AML to SQL via PyODBC |
| `dsp/tools-and-resources/aml-azure-machine-learning/link-aml-with-sql-db/write-into-sql-db` | Write Into SQL DB |
| `dsp/tools-and-resources/aml-azure-machine-learning/notebooks` | Notebooks features |
| `dsp/tools-and-resources/aml-azure-machine-learning/notebooks/managed-spark-compute` | Managed Spark Compute |
| `dsp/tools-and-resources/aml-azure-machine-learning/pipeline` | What are Pipelines? |
| `dsp/tools-and-resources/aml-azure-machine-learning/trigger-aml-with-sql-change` | Goal |
| `dsp/tools-and-resources/databricks/accessing-data/access-adls` | Mounting Points |
| `dsp/tools-and-resources/databricks/accessing-data/access-local-metastore` | Access Local Metastore |
| `dsp/tools-and-resources/databricks/accessing-data/access-sql-db` | Connecting to SQL Databases |
| `dsp/tools-and-resources/databricks/accessing-data/access-sql-pool-using-polybase` | Intro |
| `dsp/tools-and-resources/databricks/accessing-data/access-sql-pool-without-polybase` | Databricks Code |
| `dsp/tools-and-resources/databricks/best-practices-loading-data` | Best Practices Loading Data in Databricks |
| `dsp/tools-and-resources/databricks/build-basic-pipeline` | Build a basic Pipeline |
| `dsp/tools-and-resources/databricks/confluent-kafka` | Confluent Kafka |
| `dsp/tools-and-resources/databricks/connect-powerbi` | Use case |
| `dsp/tools-and-resources/databricks/copy-delta-with-adf` | Copy data to and from Azure Databricks Delta Lake using Azure Data Factory |
| `dsp/tools-and-resources/databricks/create-a-cluster` | Cluster Creation: |
| `dsp/tools-and-resources/databricks/create-instance-pool` | What are instance pools: |
| `dsp/tools-and-resources/databricks/create-scheduled-job` | Create a scheduled Job |
| `dsp/tools-and-resources/databricks/databricks-blueprint-dev-and-prod` | Databricks Blueprint |
| `dsp/tools-and-resources/databricks/databricks-in` | Databricks IN |
| `dsp/tools-and-resources/databricks/databricks-sql` | What is Databricks SQL? |
| `dsp/tools-and-resources/databricks/databricks-sql/databricks-sql-alerts` | Databricks SQL Alerts |
| `dsp/tools-and-resources/databricks/databricks-sql/databricks-sql-dashboards` | Databricks SQL Dashboards |
| `dsp/tools-and-resources/databricks/databricks-sql/databricks-sql-permissions` | Databricks SQL Permissions |
| `dsp/tools-and-resources/databricks/databricks-sql/databricks-sql-powerbi` | Databricks SQL PowerBi |
| `dsp/tools-and-resources/databricks/databricks-sql/databricks-sql-query` | Databricks SQL Query |
| `dsp/tools-and-resources/databricks/databricks-sql/databricks-sql-visualization` | Create a visualization |
| `dsp/tools-and-resources/databricks/databricks-sql/quick-create-option` | Quick Create Option |
| `dsp/tools-and-resources/databricks/dnas-databricks-utils-lib` | DNAUtils library |
| `dsp/tools-and-resources/databricks/dsp-delta-utils-lib` | Delta Utils |
| `dsp/tools-and-resources/databricks/init-scripts` | Init scripts |
| `dsp/tools-and-resources/databricks/jobs,-instances-and-pools` | Jobs, instances and Pools |
| `dsp/tools-and-resources/databricks/limit-data-access` | Limit Data Access |
| `dsp/tools-and-resources/databricks/link-to-local-clients` | Link Databricks to local clients |
| `dsp/tools-and-resources/databricks/link-to-local-clients/link-to-pycharm-&-intellij-idea` | Link To PyCharm & IntelliJ IDEA |
| `dsp/tools-and-resources/databricks/link-to-local-clients/link-to-rstudio` | Linking local RStudio IDE to Databricks and Azure DevOps |
| `dsp/tools-and-resources/databricks/link-to-local-clients/link-to-vscode` | Linking Databricks to Visual Studio Code |
| `dsp/tools-and-resources/databricks/rstudio-databricks-guide` | Rstudio Databricks Guid |
| `dsp/tools-and-resources/databricks/rstudio-databricks-guide/local-rstudio-to-databricks-&-azure-devops` | Connecting local RStudio IDE with Databricks and Azure DevOps |
| `dsp/tools-and-resources/databricks/rstudio-databricks-guide/running-rstudio-in-databricks` | Installing RStudio web interface in Databricks |
| `dsp/tools-and-resources/databricks/serverless-compute` | What is Serverless Compute? |
| `dsp/tools-and-resources/databricks/share-folders-and-change-permissions` | Share Databricks Folders and Change User Permissions |
| `dsp/tools-and-resources/databricks/unity-catalog/data-sharing` | Unity Catalog-Based Data Sharing |
| `dsp/tools-and-resources/databricks/unity-catalog/migration-to-uc` | Purpose and Scope |
| `dsp/tools-and-resources/databricks/unity-catalog/monitor-permissions` | How to monitor permissions - Unity Catalog |
| `dsp/tools-and-resources/databricks/unity-catalog/query-data-in-uc` | Querying Data in Databricks within Unity Catalog |
| `dsp/tools-and-resources/databricks/unity-catalog/system_tables_user_guide` | Databricks System Tables - User Guide |
| `dsp/tools-and-resources/databricks/unity-catalog/unity-catalog-best-practices` | Unity Catalog - Best Practices |
| `dsp/tools-and-resources/databricks/versioning-and-ci-cd` | Versioning and CI/CD Index |
| `dsp/tools-and-resources/databricks/versioning-and-ci-cd/ci-cd-setup` | CI-CD in Databricks |
| `dsp/tools-and-resources/databricks/versioning-and-ci-cd/update-databricks-blueprint-dev-and-prod` | Scope |
| `dsp/tools-and-resources/databricks/versioning-and-ci-cd/version-control-in-databricks` | Basic Version Control |
| `dsp/tools-and-resources/event-grid-topic` | Event Grid Topic |
| `dsp/tools-and-resources/events` | 1. Intro |
| `dsp/tools-and-resources/events/events-schemas-used-in-the-edl` | Intro |
| `dsp/tools-and-resources/events/how-to-consume-events` | 1. Intro |
| `dsp/tools-and-resources/how-to-access-individual-resources` | How To Access Individual Resources |
| `dsp/tools-and-resources/keyvault` | Normal Key Vault - KV |
| `dsp/tools-and-resources/keyvault/using-the-keyvault` | Using the Azure Key Vault |
| `dsp/tools-and-resources/logic-app` | index |
| `dsp/tools-and-resources/logic-app/powerbi-refresh` | Refresh multiple datasets with logic apps |
| `dsp/tools-and-resources/monitor/create-action-group` | Create an Action Group through Azure Portal |
| `dsp/tools-and-resources/powerbi` | Use DSP Data in PowerBI |
| `dsp/tools-and-resources/powerbi/change-the-database-table-of-a-dataset-in-power-bi-desktop` | Introduction |
| `dsp/tools-and-resources/powerbi/connect-powerbi-adls2` | Connect ADSL2 to PowerBI/Import Data |
| `dsp/tools-and-resources/request-service-principal-to-access-sharepoint-sites` | Request a Service Principal |
| `dsp/tools-and-resources/sql-db` | SQL Server |
| `dsp/tools-and-resources/sql-db/external-data-source` | External Data Source |
| `dsp/tools-and-resources/sql-db/link-sqldb-with-local-clients` | SQL DB link from local clients |
| `dsp/tools-and-resources/sql-db/link-sqldb-with-local-clients/link-sqldb-with-alteryx` | WORK IN PROGRESS |
| `dsp/tools-and-resources/sql-db/link-sqldb-with-local-clients/link-sqldb-with-local-python` | Connecting a local Python cli to a DSP SQLDB |
| `dsp/tools-and-resources/sql-db/link-sqldb-with-local-clients/link-sqldb-with-powerbi` | Link SQL DB With Power BI |
| `dsp/tools-and-resources/sql-db/link-sqldb-with-local-clients/link-sqldb-with-ssms` | Connect to SQL DB with SQL Server Management Studio |
| `dsp/tools-and-resources/sql-db/link-sqldb-with-local-clients/link-sqldb-with-tableau` | Connecting Tableau to an SQL DB via ODBC Drivers |
| `dsp/tools-and-resources/sql-db/performance-overview` | Performance Overview |
| `dsp/tools-and-resources/sql-db/segregating-dev-and-prod-environments` | 1. Creating/Updating the SQL Dacpac file |
| `dsp/tools-and-resources/sql-db/sql-elastic-pools` | SQL Elastic Pools |
| `dsp/tools-and-resources/synapse-studio` | Linking Synapse Studio to different Services |
| `dsp/tools-and-resources/synapse-studio/spark-pools` | Spark Pools |
| `dsp/tools-and-resources/synapse-studio/sql-pools` | SQL Pools |
| `dsp/tools-and-resources/synapse-studio/synapse-integration-runtime` | What is Integration Runtime? |

### Machine Learning (45)

| Path | Title |
|------|-------|
| `dsp/machine-learning/ai-box` | Introduction |
| `dsp/machine-learning/cognitive-services` | Intro |
| `dsp/machine-learning/cognitive-services/ai-services` | Intro |
| `dsp/machine-learning/cognitive-services/ai-services/content-safety` | Definition |
| `dsp/machine-learning/cognitive-services/ai-services/document-intelligence` | Definition |
| `dsp/machine-learning/cognitive-services/ai-services/language` | Definition |
| `dsp/machine-learning/cognitive-services/ai-services/speech` | Definition |
| `dsp/machine-learning/cognitive-services/ai-services/translator` | Definition |
| `dsp/machine-learning/cognitive-services/ai-services/vision` | Definition |
| `dsp/machine-learning/cognitive-services/azure-cognitive-search` | Intro |
| `dsp/machine-learning/cognitive-services/openai` | Intro |
| `dsp/machine-learning/machine-learning-tools-comparison` | Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/automl` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/automl/automl-databricks-vs-azureml` | AutoML Databricks vs AzureML |
| `dsp/machine-learning/machine-learning-tools-comparison/automl/azureml-automl` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/automl/databricks-automl` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/databricks-vs-azureml-deeply` | Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/databricks-vs-azureml-deeply/capacity-comparison` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/databricks-vs-azureml-deeply/cost-optimization` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/databricks-vs-azureml-deeply/training-time-and-metrics-comparison` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/ml-model-deployment` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/ml-model-deployment/ml-model-deploy-azureml` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/ml-model-deployment/ml-model-deploy-azureml/ml-deploy-as-an-endpoint` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/ml-model-deployment/ml-model-deploy-azureml/ml-deploy-locally` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/ml-model-deployment/ml-model-deploy-databricks` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/ml-model-deployment/ml-model-deploy-databricks/ml-deploy-with-job-cluster` | 1. Intro |
| `dsp/machine-learning/machine-learning-tools-comparison/ml-model-deployment/ml-model-deployment-comparison` | 1. Intro |
| `dsp/machine-learning/migration` | 1. Intro |
| `dsp/machine-learning/migration/mlflow-migration` | 1. Intro |
| `dsp/machine-learning/mlflow` | Introduction |
| `dsp/machine-learning/mlflow/mlflow-resources` | Intro |
| `dsp/machine-learning/mlflow/mlflow-resources/aml-env-mlflow` | Intro |
| `dsp/machine-learning/mlflow/mlflow-resources/databricks-env-mlflow` | Intro |
| `dsp/machine-learning/mlflow/mlflow-resources/local-env-mlflow` | Intro |
| `dsp/machine-learning/mlflow/notebook-code-quickstart` | Intro |
| `dsp/machine-learning/mlflow/ways-to-connect` | Intro |
| `dsp/machine-learning/mlflow/ways-to-connect/aml-connection` | Intro |
| `dsp/machine-learning/mlflow/ways-to-connect/databricks-connection` | Intro |
| `dsp/machine-learning/mlflow/ways-to-connect/local-connection` | Intro |
| `dsp/machine-learning/mlrecipes` | Pre-requisites |
| `dsp/machine-learning/share-ml-models-aml-and-dbks` | 1. Intro |
| `dsp/machine-learning/share-ml-models-aml-and-dbks/share-with-adls2` | 1. Intro |
| `dsp/machine-learning/share-ml-models-aml-and-dbks/share-with-mlflow` | 1. Intro |
| `dsp/machine-learning/understanding-the-costs` | 1. Intro |
| `dsp/machine-learning/understanding-the-costs/aml-costs` | 1. Intro |

### Generally Useful Information (11)

| Path | Title |
|------|-------|
| `dsp/generally-useful-information/azure-cost-reporting` | Azure Cost Reporting: A PowerBI Solution |
| `dsp/generally-useful-information/change-tao-for-cloud-environment-in-webinfo` | Change TAO for Cloud Environment in WebInfo |
| `dsp/generally-useful-information/create-budgets-and-budget-alerts` | Create Budgets and Budget Alerts |
| `dsp/generally-useful-information/create-service-health-alerts` | Create Service Health Alerts |
| `dsp/generally-useful-information/create-shared-dashboards` | Create Shared Dashboards in DSP |
| `dsp/generally-useful-information/dsl-common-acronyms-sheet` | DSL Common Acronyms Sheet |
| `dsp/generally-useful-information/how-to-contribute-to-the-common-wiki` | Prerequisites |
| `dsp/generally-useful-information/how-to-contribute-to-the-common-wiki/creating-indexfiles` | How to automatically delete redundant/outdated images from the Guidelines |
| `dsp/generally-useful-information/lab-cheat-sheet` | DSP Cheat Sheet |
| `dsp/generally-useful-information/learning-material` | Udemy License |
| `dsp/generally-useful-information/learning-material/internal-training-videos` | Git Flow |

### Data Science Platform (10)

| Path | Title |
|------|-------|
| `dsp/data-science-platform/authorization-concept` | Intro |
| `dsp/data-science-platform/consultancies` | Consultancies |
| `dsp/data-science-platform/edl-data-approval-process` | EDL Data Approval Process |
| `dsp/data-science-platform/requests/request-a-firewall-exception-for-your-dsp` | Requesting a new firewall exception for your DSP |
| `dsp/data-science-platform/requests/request-a-new-environment` | Request a new Environment |
| `dsp/data-science-platform/requests/request-ait-roles-for-sql-func-user` | Template EDL Request |
| `dsp/data-science-platform/requests/request-data` | How to request a new source system to be onboarded to EDL |
| `dsp/data-science-platform/requests/request-databricks-assistant-activation` | Requesting Databricks Assistant Activation for your DSP |
| `dsp/data-science-platform/requests/request-firewall-exception-via-tufin` | Request Firewall Exception via Tufin |
| `dsp/data-science-platform/requests/request-general-support` | Requesting general support |

### Azure Devops Project (9)

| Path | Title |
|------|-------|
| `dsp/azure-devops-project` | Azure DevOps Project |
| `dsp/azure-devops-project/best-practices` | Best Practices |
| `dsp/azure-devops-project/branch-policies` | Branch Policies |
| `dsp/azure-devops-project/ci-cd` | CI/CD |
| `dsp/azure-devops-project/create-and-publish-a-lab-wiki` | Create Code Wiki |
| `dsp/azure-devops-project/git-flow` | Git Flow |
| `dsp/azure-devops-project/naming-convention-for-identities-and-users` | Naming convention for Service Principals |
| `dsp/azure-devops-project/request-basic-licence-devops` | Request Basic License DevOps |
| `dsp/azure-devops-project/security-scan` | Introduction |

### Github Project (6)

| Path | Title |
|------|-------|
| `dsp/github-project` | GitHub Project |
| `dsp/github-project/best-practices` | Best Practices |
| `dsp/github-project/branch-policies` | Branch Policies |
| `dsp/github-project/ci-cd` | CI/CD |
| `dsp/github-project/git-flow` | Git Flow |
| `dsp/github-project/naming-convention-for-identities-and-users` | Naming convention for Service Principals |

### Enterprise Data Lake (3)

| Path | Title |
|------|-------|
| `dsp/enterprise-data-lake` | FAQ |
| `dsp/enterprise-data-lake/ingestion-processes` | 1. SAP BW Ingestion |
| `dsp/enterprise-data-lake/table-status-script` | Table status script |

### Monitoring (3)

| Path | Title |
|------|-------|
| `dsp/monitoring` | Monitoring |
| `dsp/monitoring/cost-effective-monitoring` | Introduction |
| `dsp/monitoring/out-of-the-box-monitoring` | Introduction |

### Regulatory Compliance (3)

| Path | Title |
|------|-------|
| `dsp/regulatory-compliance` | DSP Regulatory Compliance |
| `dsp/regulatory-compliance/alerts` | Azure Defender Security Alerts |
| `dsp/regulatory-compliance/baselines` | Cloud Native Security Baselines |

### Basf Data Catalog (2)

| Path | Title |
|------|-------|
| `dsp/basf-data-catalog` | BASF Data Catalog |
| `dsp/basf-data-catalog/data-marketplace` | BASF Data Marketplace |

### Trusted Structures (2)

| Path | Title |
|------|-------|
| `dsp/trusted-structures` | TRS Overview page |
| `dsp/trusted-structures/trs-metadata-views` | Why are metadata views needed? |

---

## DevHub Platform (`devhub/`, 186 pages)

### Overview (1)

| Path | Title |
|------|-------|
| `devhub` | 🚀 DevHub |

### Build Configure (96)

| Path | Title |
|------|-------|
| `devhub/build-configure` | Build & Configure |
| `devhub/build-configure/compute-infrastructure` | Compute Infrastructure |
| `devhub/build-configure/environments-and-secrets` | Environments & Secrets |
| `devhub/build-configure/firewall-configuration` | Firewall Configuration |
| `devhub/build-configure/resources` | Resources |
| `devhub/build-configure/resources/backend` | Backend Resources |
| `devhub/build-configure/resources/backend/expressjs` | Express.js Template |
| `devhub/build-configure/resources/backend/fastapi` | FastAPI Template |
| `devhub/build-configure/resources/backend/spring-boot` | Spring Boot Template |
| `devhub/build-configure/resources/data-and-ai` | Data & AI Resources |
| `devhub/build-configure/resources/data-and-ai/ai-foundry` | Azure AI Foundry |
| `devhub/build-configure/resources/data-and-ai/ai-search` | Azure AI Search |
| `devhub/build-configure/resources/data-and-ai/dagster` | Dagster |
| `devhub/build-configure/resources/data-and-ai/data-factory` | Azure Data Factory (ADF) |
| `devhub/build-configure/resources/data-and-ai/data-factory/adf-role-concept` | ADF Role Concept |
| `devhub/build-configure/resources/data-and-ai/data-factory/best-practices` | Azure Data Factory Best Practices |
| `devhub/build-configure/resources/data-and-ai/data-factory/integration-runtime` | What is Integration Runtime? |
| `devhub/build-configure/resources/data-and-ai/data-factory/linking-services` | Linking ADF to different Services |
| `devhub/build-configure/resources/data-and-ai/data-factory/linking-services/link-with-adls` | Linking ADF with Azure Data Lake Storage (ADLS) |
| `devhub/build-configure/resources/data-and-ai/data-factory/linking-services/link-with-databricks` | Link Azure Data Factory with Databricks |
| `devhub/build-configure/resources/data-and-ai/data-factory/linking-services/link-with-on-prem-resources` | Connecting Azure Data Factory with On-Premises Resources |
| `devhub/build-configure/resources/data-and-ai/data-factory/linking-services/link-with-sharepoint` | Connecting SharePoint to Azure Data Factory |
| `devhub/build-configure/resources/data-and-ai/data-factory/linking-services/link-with-sql-database` | Linking ADF with SQL Database |
| `devhub/build-configure/resources/data-and-ai/data-factory/moving-dev-to-prod` | Azure Data Factory CI/CD |
| `devhub/build-configure/resources/data-and-ai/data-factory/quickstart-guide` | Azure Data Factory Quickstart |
| `devhub/build-configure/resources/data-and-ai/data-factory/use-cases` | Azure Data Factory Use Cases |
| `devhub/build-configure/resources/data-and-ai/data-factory/use-cases/copy-activity` | Copy Activity Use Case |
| `devhub/build-configure/resources/data-and-ai/data-factory/use-cases/data-flows` | Data Flows Use Case |
| `devhub/build-configure/resources/data-and-ai/data-factory/use-cases/power-query` | Power Query Use Case |
| `devhub/build-configure/resources/data-and-ai/data-factory/using-alerts` | Alerts and Monitoring in Azure Data Factory |
| `devhub/build-configure/resources/data-and-ai/data-factory/using-storage-triggers` | Storage Triggers in Azure Data Factory |
| `devhub/build-configure/resources/data-and-ai/data-factory/using-triggers` | Using Triggers in Azure Data Factory |
| `devhub/build-configure/resources/data-and-ai/databricks-agent` | Databricks Agent Template |
| `devhub/build-configure/resources/data-and-ai/databricks` | Azure Databricks |
| `devhub/build-configure/resources/data-and-ai/databricks/getting-started/access-overview` | Add Users to Your Databricks Workspace |
| `devhub/build-configure/resources/data-and-ai/databricks/getting-started/beforeyoustart` | Before You Start |
| `devhub/build-configure/resources/data-and-ai/databricks/getting-started/deployment` | Deploy Your Databricks Workspace |
| `devhub/build-configure/resources/data-and-ai/databricks/getting-started/first-setup` | Run Your First Pipeline |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/connecting-power-bi` | Connecting Power BI |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/copying-delta-with-adf` | Copying Delta Tables with Azure Data Factory |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/deploying-with-ci-cd` | Deploying with CI/CD |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/linking-local-ide` | Linking Your Local IDE |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/loading-data` | Loading Data into SQL Sinks |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/managing-compute` | Managing Compute |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/scheduling-jobs` | Scheduling Jobs |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/streaming-with-kafka` | Streaming with Confluent Kafka |
| `devhub/build-configure/resources/data-and-ai/databricks/guides/using-databricks-in` | Using Databricks IN |
| `devhub/build-configure/resources/data-and-ai/databricks/references/cluster-policies` | Cluster Policies |
| `devhub/build-configure/resources/data-and-ai/databricks/references/cost-and-tagging` | Cost and Tagging |
| `devhub/build-configure/resources/data-and-ai/databricks/references/naming-conventions` | Naming Conventions |
| `devhub/build-configure/resources/data-and-ai/databricks/references/troubleshooting` | Troubleshooting and Escalation |
| `devhub/build-configure/resources/data-and-ai/databricks/unity-catalog/introduction` | Unity Catalog |
| `devhub/build-configure/resources/data-and-ai/databricks/unity-catalog/managing-permissions` | Managing Unity Catalog Permissions |
| `devhub/build-configure/resources/data-and-ai/databricks/unity-catalog/monitoring-permissions` | Monitoring Unity Catalog Permissions |
| `devhub/build-configure/resources/data-and-ai/databricks/unity-catalog/querying-data` | Querying Data in Unity Catalog |
| `devhub/build-configure/resources/data-and-ai/databricks/unity-catalog/sharing-data` | Sharing Data Across Products |
| `devhub/build-configure/resources/data-and-ai/databricks/unity-catalog/using-system-tables` | Using System Tables |
| `devhub/build-configure/resources/data-and-ai/databricks/unity-catalog/using-volumes-and-init-scripts` | Using Volumes and Init Scripts |
| `devhub/build-configure/resources/data-and-ai/jupyterhub` | JupyterHub |
| `devhub/build-configure/resources/data-and-ai/mlflow` | MLflow |
| `devhub/build-configure/resources/data-and-ai/rag-api-python` | RAG API Python Template |
| `devhub/build-configure/resources/frontend` | Frontend Resources |
| `devhub/build-configure/resources/frontend/angular` | Angular Template |
| `devhub/build-configure/resources/frontend/plotly` | Plotly Dash Template |
| `devhub/build-configure/resources/frontend/react` | React Template |
| `devhub/build-configure/resources/frontend/streamlit` | Streamlit Template |
| `devhub/build-configure/resources/frontend/vue` | Vue Template |
| `devhub/build-configure/resources/messaging` | Messaging |
| `devhub/build-configure/resources/messaging/azure-bot-service` | Azure Bot Service |
| `devhub/build-configure/resources/messaging/event-grid` | Event Grid |
| `devhub/build-configure/resources/messaging/rabbitmq` | RabbitMQ |
| `devhub/build-configure/resources/monitoring` | Monitoring |
| `devhub/build-configure/resources/monitoring/log-analytics` | Log Analytics |
| `devhub/build-configure/resources/storage` | Storage Resources |
| `devhub/build-configure/resources/storage/cloudbeaver` | CloudBeaver |
| `devhub/build-configure/resources/storage/memgraph` | Using Memgraph |
| `devhub/build-configure/resources/storage/mongodb-atlas` | MongoDB Atlas |
| `devhub/build-configure/resources/storage/mysql` | Using MySQL |
| `devhub/build-configure/resources/storage/object-store` | Azure Blob Storage |
| `devhub/build-configure/resources/storage/postgresql` | Using PostgreSQL |
| `devhub/build-configure/resources/storage/sql-server` | Using SQL Server |
| `devhub/build-configure/roles-and-access` | DevHub Roles & Access Management |
| `devhub/build-configure/routing-and-authorization` | Routing & Authorization |
| `devhub/build-configure/security` | Security |
| `devhub/build-configure/security/Fortify` | Fortify on DevHub |
| `devhub/build-configure/security/Fortify/implementation` | Pipeline Integration |
| `devhub/build-configure/security/Fortify/remediation` | Remediation Instructions |
| `devhub/build-configure/security/GitGuardian` | GitGuardian |
| `devhub/build-configure/security/GitGuardian/Installation` | GitGuardian CLI (ggshield) |
| `devhub/build-configure/security/GitGuardian/citest` | Detect secrets in CI pipelines |
| `devhub/build-configure/security/GitGuardian/githooks` | Integrate secrets detection in git workflow |
| `devhub/build-configure/security/GitGuardian/prchecks` | GitGuardian GitHub Pull Request Checks |
| `devhub/build-configure/security/GitGuardian/remediate` | How to remediate secret incidents |
| `devhub/build-configure/security/Sonatype` | Sonatype IQ on DevHub |
| `devhub/build-configure/security/Sonatype/implementation` | Pipeline Integration |
| `devhub/build-configure/security/Sonatype/remediation` | Remediation Instructions |

### Deploy Operate (21)

| Path | Title |
|------|-------|
| `devhub/deploy-operate` | Deploy & Operate |
| `devhub/deploy-operate/apps-and-services/backend-applications` | Backend Applications |
| `devhub/deploy-operate/apps-and-services/deploy-apps-and-services` | Deploy Apps & Services on DevHub |
| `devhub/deploy-operate/apps-and-services/frontend-applications` | Frontend Applications |
| `devhub/deploy-operate/cicd-pipelines` | CI/CD Pipelines |
| `devhub/deploy-operate/deployments-and-environments` | Deployments & Environments |
| `devhub/deploy-operate/development-workflow` | Development Workflow |
| `devhub/deploy-operate/development-workflow/code-quality` | Code Quality |
| `devhub/deploy-operate/development-workflow/github-runners` | GitHub Runners |
| `devhub/deploy-operate/development-workflow/python-dependency-management` | Python Dependency Management |
| `devhub/deploy-operate/development-workflow/semantic-release` | Semantic Release |
| `devhub/deploy-operate/monitoring` | Monitoring & Observability |
| `devhub/deploy-operate/monitoring/developer-portal` | Developer Portal |
| `devhub/deploy-operate/monitoring/grafana` | Observability in DevHub |
| `devhub/deploy-operate/monitoring/grafana/alerts` | Alerting |
| `devhub/deploy-operate/monitoring/grafana/custom-dashboards` | Custom Dashboards |
| `devhub/deploy-operate/monitoring/grafana/logs-ingestion` | Application Logging |
| `devhub/deploy-operate/monitoring/grafana/metrics-ingestion` | Application Metrics |
| `devhub/deploy-operate/monitoring/grafana/traces` | Distributed Tracing |
| `devhub/deploy-operate/monitoring/k8s-api-access` | Kubernetes API Access |
| `devhub/deploy-operate/monitoring/kubernetes-roles-and-permissions` | Kubernetes API Roles & Permissions |

### Aigateway (17)

| Path | Title |
|------|-------|
| `devhub/aigateway/getting-started/access-overview` | Adding Users to Your AI Gateway |
| `devhub/aigateway/getting-started/beforeyoustart` | Before You Start |
| `devhub/aigateway/getting-started/deployment` | Deploy the AI Gateway |
| `devhub/aigateway/getting-started/first-setup` | First Setup |
| `devhub/aigateway/guides/authentication` | Authentication |
| `devhub/aigateway/guides/consuming-ai-services` | Consuming AI Services |
| `devhub/aigateway/guides/consuming-models` | Consuming Models |
| `devhub/aigateway/guides/managing-access` | Managing Access |
| `devhub/aigateway/guides/modify-ai-gw` | Modify AI Gateway Configuration |
| `devhub/aigateway/guides/monitoring` | AI Gateway Monitoring |
| `devhub/aigateway/guides/requesting-models` | Requesting Additional Models |
| `devhub/aigateway/guides/troubleshooting` | Troubleshooting |
| `devhub/aigateway/introduction` | AI Gateway |
| `devhub/aigateway/references/api-reference` | API Reference |
| `devhub/aigateway/references/available-models` | Available Models |
| `devhub/aigateway/references/costs-billing` | Costs & Billing |
| `devhub/aigateway/references/model-lifecycle` | Model Lifecycle |

### Guides (12)

| Path | Title |
|------|-------|
| `devhub/guides/background-workers` | Background Workers |
| `devhub/guides/custom-domains` | Configure Custom Domains for DMZ Products |
| `devhub/guides/data-sources/databricks-aks` | Connecting Your Application to Azure Data Services at BASF |
| `devhub/guides/data-sources/databricks-aks/azure_cli_setup` | Azure CLI Setup for Local Development |
| `devhub/guides/data-sources/databricks-aks/connect_to_blob_storage` | Connect to Azure Blob Storage with Python |
| `devhub/guides/data-sources/databricks-aks/connect_to_delta_sharing` | Connect to Delta Sharing |
| `devhub/guides/data-sources/databricks-aks/connect_to_sql_warehouse` | Connect to Databricks SQL Warehouse |
| `devhub/guides/data-sources/enterprise-data-lake` | Enterprise Data Lake |
| `devhub/guides/data-sources/sharepoint` | Sharepoint |
| `devhub/guides/data-sources/storage` | DevHub Storage |
| `devhub/guides/sending-emails` | Sending Emails via SMTP |
| `devhub/guides/software-catalog` | Software Catalog |

### References (11)

| Path | Title |
|------|-------|
| `devhub/references` | Reference |
| `devhub/references/auth_flows` | Introduction |
| `devhub/references/data-access-patterns` | Accessing internal and external data sources |
| `devhub/references/data-access` | Data Access |
| `devhub/references/devhub-tech-and-processes` | DevHub technology and processes |
| `devhub/references/identities` | Product Identities |
| `devhub/references/infrastructure-details` | Infrastructure Details |
| `devhub/references/limits-and-quotas` | Limits & Quotas |
| `devhub/references/networking-reference` | Networking Reference |
| `devhub/references/platform-architecture` | Platform Architecture |
| `devhub/references/security-reference` | Security Reference |

### Tutorials (7)

| Path | Title |
|------|-------|
| `devhub/tutorials/create-a-data-ml-pipeline` | Data/ML Pipeline |
| `devhub/tutorials/create-a-databricks-agent` | Create a Talk2Data Databricks Agent |
| `devhub/tutorials/create-a-frontend` | Frontend Application |
| `devhub/tutorials/create-a-mcp-server` | MCP Server |
| `devhub/tutorials/create-a-rag` | Retrieval Augmented Generation (RAG) API |
| `devhub/tutorials/create-an-api` | API Service |
| `devhub/tutorials/create-ask2sql-agent` | Ask2SQL: Natural Language to SQL Agent |

### Troubleshooting (6)

| Path | Title |
|------|-------|
| `devhub/troubleshooting` | Troubleshooting |
| `devhub/troubleshooting/access-and-permissions` | Access & Permission Issues |
| `devhub/troubleshooting/access-network` | Troubleshooting Access & Network |
| `devhub/troubleshooting/common-issues` | Common Issues |
| `devhub/troubleshooting/deployment-failures` | Deployment Failures |
| `devhub/troubleshooting/kubernetes` | Troubleshooting Kubernetes workloads |

### Getting Started (5)

| Path | Title |
|------|-------|
| `devhub/getting-started/creating-your-first-application` | Creating your first application |
| `devhub/getting-started/delete-your-product-and-workspace` | Delete your Product and Workspace |
| `devhub/getting-started/governance` | Governance & Compliance |
| `devhub/getting-started/prerequisites` | Prerequisites |
| `devhub/getting-started/request-support` | Requesting support |

### Product Lifecycle (4)

| Path | Title |
|------|-------|
| `devhub/product-lifecycle/creating-a-product` | Creating a Product |
| `devhub/product-lifecycle/deleting-a-product` | Delete your Product |
| `devhub/product-lifecycle/deleting-a-workspace` | Delete your Workspace |
| `devhub/product-lifecycle/modifying-a-product` | Modifying Template Resource & Modules from Your Product |

### Tiers And Charging (4)

| Path | Title |
|------|-------|
| `devhub/tiers-and-charging` | Tiers & Charging |
| `devhub/tiers-and-charging/change-cost-center` | Change Cost Center |
| `devhub/tiers-and-charging/cost-examples` | Cost Examples |
| `devhub/tiers-and-charging/tier-definitions` | Tier Definitions |

### Example Projects (1)

| Path | Title |
|------|-------|
| `devhub/example-projects` | Example Projects |

### Feature Requests (1)

| Path | Title |
|------|-------|
| `devhub/feature-requests` | Feature Requests & Roadmap Prioritization |

---

## APIs @ BASF (`apis/`, 156 pages)

### Overview (1)

| Path | Title |
|------|-------|
| `apis` | APIs @ BASF |

### Glossary (119)

| Path | Title |
|------|-------|
| `apis/glossary` | Glossary |
| `apis/glossary/a/access-token` | Access Token |
| `apis/glossary/a/api-business-hub-enterprise` | API Business Hub Enterprise |
| `apis/glossary/a/api-call` | API Call |
| `apis/glossary/a/api-catalog` | API Catalog |
| `apis/glossary/a/api-community` | API Community |
| `apis/glossary/a/api-consumer` | API Consumer |
| `apis/glossary/a/api-definition` | API Definition |
| `apis/glossary/a/api-design` | API Design |
| `apis/glossary/a/api-documentation` | API Documentation |
| `apis/glossary/a/api-enablement` | API Enablement |
| `apis/glossary/a/api-first` | API First |
| `apis/glossary/a/api-gateway` | API Gateway |
| `apis/glossary/a/api-guidelines` | API Guidelines |
| `apis/glossary/a/api-key` | API Key |
| `apis/glossary/a/api-management` | API Management (APIM) |
| `apis/glossary/a/api-operations-pipeline` | API Operations Pipeline |
| `apis/glossary/a/api-owner` | API Owner |
| `apis/glossary/a/api-provider` | API Provider |
| `apis/glossary/a/api-proxy` | API Proxy |
| `apis/glossary/a/api-versioning` | API Versioning |
| `apis/glossary/a/api` | API |
| `apis/glossary/a/apigee-api-management` | Apigee API Management |
| `apis/glossary/a/application-component` | Application Component |
| `apis/glossary/a/application-problem+json` | application/problem+json |
| `apis/glossary/a/application` | Application |
| `apis/glossary/a/asyncapi` | AsyncAPI |
| `apis/glossary/a/authentication-service` | Authentication Service |
| `apis/glossary/a/authentication` | Authentication |
| `apis/glossary/a/authorization` | Authorization |
| `apis/glossary/a/azure-ad` | Azure AD |
| `apis/glossary/a/azure-devops` | Azure DevOps |
| `apis/glossary/b/backend` | Backend |
| `apis/glossary/b/base-path` | Base Path |
| `apis/glossary/b/basf-integration-hub` | BASF Integration Hub (BIH) |
| `apis/glossary/b/bearer-token` | Bearer Token |
| `apis/glossary/c/client-id` | Client ID |
| `apis/glossary/c/client-secret` | Client Secret |
| `apis/glossary/c/cloud-connector` | Cloud Connector |
| `apis/glossary/c/contract-testing` | Contract Testing |
| `apis/glossary/c/cors` | CORS (Cross-Origin Resource Sharing) |
| `apis/glossary/c/cpi` | CPI (SAP Cloud Platform Integration) |
| `apis/glossary/c/credentials` | Credentials |
| `apis/glossary/c/crud` | CRUD |
| `apis/glossary/c/csrf-token` | CSRF Token |
| `apis/glossary/c/curl` | cURL |
| `apis/glossary/d/data-model` | Data Model |
| `apis/glossary/d/delete` | DELETE |
| `apis/glossary/d/developer-experience` | Developer Experience |
| `apis/glossary/d/developer-portal` | Developer Portal |
| `apis/glossary/d/dil` | DIL |
| `apis/glossary/e/end-user` | End User |
| `apis/glossary/e/endpoint` | Endpoint |
| `apis/glossary/e/entity-relationship-model` | Entity Relationship Model |
| `apis/glossary/f/federation-service` | Federation Service |
| `apis/glossary/f/functional-user` | Functional User |
| `apis/glossary/g/get` | GET |
| `apis/glossary/g/git` | Git |
| `apis/glossary/g/graphql` | GraphQL |
| `apis/glossary/g/grpc` | gRPC |
| `apis/glossary/h/head` | HEAD |
| `apis/glossary/h/http-header` | HTTP Header |
| `apis/glossary/h/http-message-body` | HTTP Message Body |
| `apis/glossary/h/http-method` | HTTP Method |
| `apis/glossary/h/http-request` | HTTP Request |
| `apis/glossary/h/http-response` | HTTP Response |
| `apis/glossary/h/http-status-code` | HTTP Status Code |
| `apis/glossary/h/http` | HTTP |
| `apis/glossary/i/information` | Information |
| `apis/glossary/i/interface` | Interface |
| `apis/glossary/j/json-schema` | JSON Schema |
| `apis/glossary/j/json` | JSON |
| `apis/glossary/j/jwt` | JWT |
| `apis/glossary/k/kvm` | KVM |
| `apis/glossary/m/media-type` | Media Type |
| `apis/glossary/m/microservice` | Microservice |
| `apis/glossary/n/nam` | NAM (NetIQ Access Manager) |
| `apis/glossary/n/named-user` | Named User |
| `apis/glossary/n/newman` | Newman |
| `apis/glossary/o/oauth` | OAuth |
| `apis/glossary/o/odata` | OData |
| `apis/glossary/o/openapi` | OpenAPI |
| `apis/glossary/o/options` | OPTIONS |
| `apis/glossary/o/owasp10` | OWASP 10 |
| `apis/glossary/p/pagination` | Pagination |
| `apis/glossary/p/patch` | PATCH |
| `apis/glossary/p/path-parameter` | Path Parameter |
| `apis/glossary/p/path` | Path |
| `apis/glossary/p/payload` | Payload |
| `apis/glossary/p/persona` | Persona |
| `apis/glossary/p/pipeline` | Pipeline |
| `apis/glossary/p/policy` | Policy (Template) |
| `apis/glossary/p/portman` | Portman |
| `apis/glossary/p/post` | POST |
| `apis/glossary/p/postman` | Postman |
| `apis/glossary/p/principal-propagation` | Principal Propagation |
| `apis/glossary/p/prism` | Prism |
| `apis/glossary/p/product` | Product |
| `apis/glossary/p/put` | PUT |
| `apis/glossary/q/query-parameter` | Query Parameter |
| `apis/glossary/q/quota` | Quota |
| `apis/glossary/r/redirect-url` | Redirect URL |
| `apis/glossary/r/resource` | Resource |
| `apis/glossary/r/rest` | REST |
| `apis/glossary/r/rpc` | RPC |
| `apis/glossary/s/sap-api-management` | SAP API Management |
| `apis/glossary/s/service` | Service |
| `apis/glossary/s/shared-flow` | Shared Flow |
| `apis/glossary/s/soap` | SOAP |
| `apis/glossary/s/spectral` | Spectral |
| `apis/glossary/s/spike-arrest` | Spike Arrest |
| `apis/glossary/s/stoplight-studio` | Stoplight Studio |
| `apis/glossary/s/subroutine` | Subroutine |
| `apis/glossary/s/swagger` | Swagger |
| `apis/glossary/t/threat-protection` | Threat Protection |
| `apis/glossary/u/url` | URL |
| `apis/glossary/v/varation-testing` | Variation Testing |
| `apis/glossary/x/xml` | XML |
| `apis/glossary/y/yaml` | YAML |

### Knowledge Base (27)

| Path | Title |
|------|-------|
| `apis/knowledge-base/api-providers/api-backend/sap-and-odata/csrf-token` | CSRF Token |
| `apis/knowledge-base/api-providers/api-backend/sap-and-odata/pagination` | Server-Side Pagination in SAP SEGW (OData 2.0) |
| `apis/knowledge-base/api-providers/api-backend/sap-and-odata/rest-services` | REST Services |
| `apis/knowledge-base/api-providers/api-definition/api-description` | Consumer-Friendly API Description |
| `apis/knowledge-base/api-providers/api-definition/openapi-url-references` | OpenAPI URL References |
| `apis/knowledge-base/api-providers/api-definition/sort-order` | Sorting Your API Definition |
| `apis/knowledge-base/api-providers/api-operations-pipeline` | API Operations Pipeline |
| `apis/knowledge-base/api-providers/api-operations-pipeline/advanced-settings` | Advanced Settings |
| `apis/knowledge-base/api-providers/api-operations-pipeline/changelog` | API Operations Pipeline |
| `apis/knowledge-base/api-providers/api-operations-pipeline/functionality` | Functionality |
| `apis/knowledge-base/api-providers/api-operations-pipeline/setup` | Initialization & Setup |
| `apis/knowledge-base/api-providers/api-operations-pipeline/troubleshooting` | Troubleshooting |
| `apis/knowledge-base/api-providers/sap-api-management-automation-pipeline` | SAP API Management Automation Pipeline |
| `apis/knowledge-base/api-providers/sap-api-management-automation-pipeline/functionality` | Functionality |
| `apis/knowledge-base/api-providers/sap-api-management-automation-pipeline/setup` | How to Use the Pipeline |
| `apis/knowledge-base/api-providers/sap-api-management-automation-pipeline/troubleshooting` | Troubleshooting |
| `apis/knowledge-base/api-providers/sap-api-management-automation-pipeline/update-api-definition` | How to Update the API Definition |
| `apis/knowledge-base/api-providers/testing` | Testing Your API |
| `apis/knowledge-base/api-providers/testing/different-environments` | Testing Different Environments |
| `apis/knowledge-base/api-providers/testing/file-upload` | Testing Binary Request Bodies |
| `apis/knowledge-base/api-providers/testing/flows` | Testing Flows |
| `apis/knowledge-base/api-providers/testing/nightly-test` | Nightly Test Pipeline |
| `apis/knowledge-base/api-providers/tooling/azure-devops` | Azure DevOps |
| `apis/knowledge-base/api-providers/tooling/stoplight-studio` | Stoplight Studio |
| `apis/knowledge-base/beginners-introduction` | Beginners Introduction |
| `apis/knowledge-base/links` | Link Collection |
| `apis/knowledge-base/start-your-journey` | Start Your Journey as API Provider |

### Api Guidelines (6)

| Path | Title |
|------|-------|
| `apis/api-guidelines` | API Guidelines |
| `apis/api-guidelines/best-practices/pagination` | Pagination |
| `apis/api-guidelines/conventions` | Conventions |
| `apis/api-guidelines/guidelines` | Guidelines for RESTful APIs |
| `apis/api-guidelines/principles` | Principles |
| `apis/api-guidelines/purpose` | Purpose |

### Api Enablement (3)

| Path | Title |
|------|-------|
| `apis/api-enablement/api-enablement-program` | API Enablement Program |
| `apis/api-enablement/api-enablement-team` | API Enablement Team |
| `apis/api-enablement/involved-systems` | Involved Systems |

---

## App Store (`appstore/`, 75 pages)

### Overview (1)

| Path | Title |
|------|-------|
| `appstore` | App Store |

### Templates (46)

| Path | Title |
|------|-------|
| `appstore/templates` | Templates |
| `appstore/templates/create` | Create your own template |
| `appstore/templates/lifecycle` | Lifecycle |
| `appstore/templates/overview/airflow` | Airflow |
| `appstore/templates/overview/angular` | Angular |
| `appstore/templates/overview/arangodb` | ArangoDB |
| `appstore/templates/overview/aspdotnet` | ASP.NET |
| `appstore/templates/overview/celery_flower` | Celery and Flower |
| `appstore/templates/overview/codeserver` | Code server |
| `appstore/templates/overview/couchdb` | CouchDB |
| `appstore/templates/overview/dagster` | Dagster |
| `appstore/templates/overview/django` | Django |
| `appstore/templates/overview/express` | Express.js |
| `appstore/templates/overview/fastapi` | FastAPI |
| `appstore/templates/overview/flask` | Flask |
| `appstore/templates/overview/flaskrestx` | Flask-RESTX |
| `appstore/templates/overview/flutter` | Flutter |
| `appstore/templates/overview/fuseki` | Fuseki |
| `appstore/templates/overview/graph_explorer` | Graph Explorer |
| `appstore/templates/overview/jupyter` | Jupyter |
| `appstore/templates/overview/jupyterlab` | JupyterLab |
| `appstore/templates/overview/kuzu` | Kuzu Explorer |
| `appstore/templates/overview/lit` | Lit |
| `appstore/templates/overview/mariadb` | MariaDB |
| `appstore/templates/overview/mlflow` | MLflow |
| `appstore/templates/overview/mongodb` | MongoDB |
| `appstore/templates/overview/neo4j` | Neo4j |
| `appstore/templates/overview/nginx` | NginX |
| `appstore/templates/overview/nuxt` | Nuxt.js |
| `appstore/templates/overview/pages_blog` | Pages Blog |
| `appstore/templates/overview/pgadmin` | pgAdmin |
| `appstore/templates/overview/plumber` | Plumber |
| `appstore/templates/overview/postgres` | PostgreSQL |
| `appstore/templates/overview/python_library` | Python Library |
| `appstore/templates/overview/react` | React |
| `appstore/templates/overview/redis` | Redis |
| `appstore/templates/overview/rshiny` | Shiny |
| `appstore/templates/overview/rshinypackage` | Shiny Package |
| `appstore/templates/overview/snakemake` | SnakeDev |
| `appstore/templates/overview/springboot` | Spring Boot |
| `appstore/templates/overview/streamlit` | Streamlit |
| `appstore/templates/overview/svelte` | Svelte |
| `appstore/templates/overview/tensorflow` | Tensorflow |
| `appstore/templates/overview/virtuoso` | Virtuoso |
| `appstore/templates/overview/vue` | Vue.js |
| `appstore/templates/overview/web2py` | Web2py |

### Add Or Create (3)

| Path | Title |
|------|-------|
| `appstore/add_or_create` | Add or create a new app |
| `appstore/add_or_create/add_existing_app` | Register existing application |
| `appstore/add_or_create/happy_potter_3` | App creation wizard (Happy Potter 3) |

### Life Cycle Management (2)

| Path | Title |
|------|-------|
| `appstore/life_cycle_management` | Life Cycle Management |
| `appstore/life_cycle_management/citizen_development` | Life Cycle Management |

### Aad Migration (1)

| Path | Title |
|------|-------|
| `appstore/aad_migration` | Microsoft Azure Active Directory in the App Store Portal |

### Analytics (1)

| Path | Title |
|------|-------|
| `appstore/analytics` | Analytics |

### Api (1)

| Path | Title |
|------|-------|
| `appstore/api` | App Store APIs |

### Apigateway (1)

| Path | Title |
|------|-------|
| `appstore/apigateway` | API Gateway |

### Argus (1)

| Path | Title |
|------|-------|
| `appstore/argus` | Argus |

### Atoms Deprecation (1)

| Path | Title |
|------|-------|
| `appstore/atoms_deprecation` | Atoms Deprecation |

### Authentication (1)

| Path | Title |
|------|-------|
| `appstore/authentication` | Authentication |

### Base Images (1)

| Path | Title |
|------|-------|
| `appstore/base_images` | App Store Docker Images |

### Deploy (1)

| Path | Title |
|------|-------|
| `appstore/deploy` | Deploying to the App Store |

### Faq (1)

| Path | Title |
|------|-------|
| `appstore/faq` | FAQ |

### Getting Started (1)

| Path | Title |
|------|-------|
| `appstore/getting-started` | Getting Started |

### Gitlab (1)

| Path | Title |
|------|-------|
| `appstore/gitlab` | GitLab |

### Kpi (1)

| Path | Title |
|------|-------|
| `appstore/kpi` | App Store Key Performance Indicators |

### Logging (1)

| Path | Title |
|------|-------|
| `appstore/logging` | Logging |

### Metadata (1)

| Path | Title |
|------|-------|
| `appstore/metadata` | Application metadata |

### Migrate Apps (1)

| Path | Title |
|------|-------|
| `appstore/migrate_apps` | Migrate Apps |

### Pages (1)

| Path | Title |
|------|-------|
| `appstore/pages` | Pages |

### Policy (1)

| Path | Title |
|------|-------|
| `appstore/policy` | App Store Policy |

### Portal (1)

| Path | Title |
|------|-------|
| `appstore/portal` | App Store Portal |

### Secrets (1)

| Path | Title |
|------|-------|
| `appstore/secrets` | Secrets |

### Security (1)

| Path | Title |
|------|-------|
| `appstore/security` | App Store Security |

### Storage (1)

| Path | Title |
|------|-------|
| `appstore/storage` | App Store Storage |

### Testing (1)

| Path | Title |
|------|-------|
| `appstore/testing` | Testing on the App Store |

---

## Argus (`argus/`, 54 pages)

### Overview (1)

| Path | Title |
|------|-------|
| `argus` | Argus |

### Guides (35)

| Path | Title |
|------|-------|
| `argus/guides/ai-services/ai-multi-service` | Azure AI Multiservice |
| `argus/guides/ai-services/ai-search-service` | Azure AI Search |
| `argus/guides/ai-services/open-ai-service` | Azure OpenAI Service |
| `argus/guides/apps-and-services/backend-applications` | Backend Applications |
| `argus/guides/apps-and-services/deploy-apps-and-services` | Deploy Apps & Services on Argus |
| `argus/guides/apps-and-services/frontend-applications` | Frontend Applications |
| `argus/guides/argus-package-feeds/argus-npm` | How to use the ArgusNPM package feed |
| `argus/guides/argus-package-feeds/argus-pypi` | How to use the ArgusPyPI package feed |
| `argus/guides/compute-infrastructure` | Compute Infrastructure on Argus |
| `argus/guides/data-ml-exploration/jupyterhub` | JupyterHub |
| `argus/guides/data-ml-pipelines/blob-storage-access` | Blob Storage access using Dagster resources |
| `argus/guides/data-ml-pipelines/data-ml-orchestration-with-dagster` | Data & ML orchestration with Dagster |
| `argus/guides/data-ml-pipelines/key-vault-access` | Key Vault access in Dagster Pipelines using dagster resources |
| `argus/guides/data-sources/blob-storage` | Azure Blob Storage |
| `argus/guides/data-sources/business-edl` | Business EDL (SAP) |
| `argus/guides/data-sources/cloudbeaver` | CloudBeaver |
| `argus/guides/data-sources/memgraph` | Using Memgraph |
| `argus/guides/data-sources/mysql` | Using MySQL |
| `argus/guides/data-sources/postgres` | Using PostgreSQL |
| `argus/guides/data-sources/production-edl` | Production EDL (PIMS/LIMS) |
| `argus/guides/data-sources/sharepoint` | Sharepoint |
| `argus/guides/development-workflow/code-quality` | Code Quality |
| `argus/guides/development-workflow/python-dependency-management` | Python Dependency Management |
| `argus/guides/development-workflow/semantic-release` | Semantic Release |
| `argus/guides/manage-secrets-keys` | Manage Environment and Secrets |
| `argus/guides/migrate-apps` | Migrate Apps |
| `argus/guides/ml-model-lifecycle/mlflow` | MLflow |
| `argus/guides/ml-model-lifecycle/model-engineering` | Model Engineering |
| `argus/guides/monitoring/advanced-monitoring` | Advanced monitoring |
| `argus/guides/monitoring/developer-portal` | Developer Portal |
| `argus/guides/routing` | Make services available with built-in authorization |
| `argus/guides/software-catalog` | Software Catalog |
| `argus/guides/ssp-groups` | SSP Group Creation and Management |
| `argus/guides/troubleshooting/access-network` | Troubleshooting Access & Network |
| `argus/guides/troubleshooting/kubernetes` | Troubleshooting Kubernetes workloads |

### Getting Started (4)

| Path | Title |
|------|-------|
| `argus/getting-started/create-your-product` | Create your Product |
| `argus/getting-started/create-your-workspace` | Create your Workspace |
| `argus/getting-started/prerequisites` | Prerequisites |
| `argus/getting-started/setup-storage` | Set up Storage |

### References (4)

| Path | Title |
|------|-------|
| `argus/references/argus-tech-and-processes` | Argus technology and processes |
| `argus/references/data-access-patterns` | Accessing internal and external data sources |
| `argus/references/platform-architecture` | Platform Architecture |
| `argus/references/provisioning` | Provisioning |

### Tutorials (4)

| Path | Title |
|------|-------|
| `argus/tutorials/create-a-data-ml-pipeline` | Create a Data & ML Pipeline |
| `argus/tutorials/create-a-frontend` | Create a Frontend |
| `argus/tutorials/create-a-rag` | Create a Retrieval Augmented Generation (RAG) API |
| `argus/tutorials/create-an-api` | Create an API |

### Introduction (3)

| Path | Title |
|------|-------|
| `argus/introduction/introduction-to-argus` | Introduction to Argus |
| `argus/introduction/problems-argus-solves` | MLOps is hard |
| `argus/introduction/solutions-argus-offers` | Argus makes MLOps easier |

### Explanations (2)

| Path | Title |
|------|-------|
| `argus/explanations/data-access` | Data Access |
| `argus/explanations/identities` | Product Identities |

### Example Projects (1)

| Path | Title |
|------|-------|
| `argus/example-projects` | Example Projects |

---

## Developer Setup (`setup/`, 16 pages)

### Overview (1)

| Path | Title |
|------|-------|
| `setup` | Developer Setup |

### Programming Languages (5)

| Path | Title |
|------|-------|
| `setup/programming-languages/dart` | Dart |
| `setup/programming-languages/java` | Java |
| `setup/programming-languages/javascript` | JavaScript |
| `setup/programming-languages/python` | Python |
| `setup/programming-languages/r` | R |

### Tools (4)

| Path | Title |
|------|-------|
| `setup/tools/docker` | Docker |
| `setup/tools/podman` | Podman |
| `setup/tools/rancherdesktop` | Rancher Desktop |
| `setup/tools/wsl2` | WSL2 |

### Version Control (3)

| Path | Title |
|------|-------|
| `setup/version-control/git` | Git |
| `setup/version-control/gpg` | Configuring GPG Signed Commits on GitHub |
| `setup/version-control/ssh-signing` | Configuring SSH Signed Commits on GitHub |

### Code Editors (2)

| Path | Title |
|------|-------|
| `setup/code-editors/intellij` | IntelliJ |
| `setup/code-editors/vscode` | Visual Studio Code |

### Ca (1)

| Path | Title |
|------|-------|
| `setup/ca` | Certificates |

---

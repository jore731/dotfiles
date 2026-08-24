# Cloud Reference Docs Index

Base URL: `https://docs.cloudreference.basf.com`

The site requires **Azure AD authentication** (BASF SSO, Azure App Service Auth). It is a DocFX static site (server-rendered HTML, not SPA).

**Default access — Azure CLI token broker** (BASF tenant; same `az login` as DevHub but a different resource ID):

```bash
TOKEN=$(az account get-access-token --resource 6b6bc843-3472-4c61-af63-5b99fd17d534 --query accessToken -o tsv)
curl -sk -H "Authorization: Bearer $TOKEN" "https://docs.cloudreference.basf.com/<PATH>"
unset TOKEN   # never print or share the raw token
```

Without a token the site returns `HTTP 401` with a `WWW-Authenticate: Bearer ... resource_id="6b6bc843-3472-4c61-af63-5b99fd17d534"` header. **Fallback:** a valid `AppServiceAuthSession` cookie from the browser (DevTools → Application → Cookies) also works via `curl -sk -b "AppServiceAuthSession=<cookie>"`.

## Site Structure (548 pages, 9 sections)

| Section | Pages | Path Prefix | Description |
|---------|-------|-------------|-------------|
| CRA | 130 | `/CRA/` | Cloud Reference Architecture — IAM, Governance, Networking, Environments, IaaS, Operations |
| CP | 21 | `/CP/` | Container Platform (AKS, Kubernetes) |
| CAP | 5 | `/CAP/` | CAPT |
| CRI | 132 | `/CRI/` | Cloud Reference Implementations — Terraform modules, IaC templates |
| CT | 141 | `/CT/` | Cloud Tutorials & One-Pagers — AdminIT, Connectivity, DevOps, Azure, AWS, K8s, FinOps |
| CFO | 18 | `/CFO/` | Cloud FinOps — cost management, budgets, charging |
| CO | 35 | `/CO/` | Cloud Optimization — cost saving, scheduling, reservations |
| CC | 4 | `/CC/` | China Cloud Team |
| CSC | 62 | `/CSC/` | Cloud Security & Compliance — backup, cryptography, compliance, WAF, NSM |

---

## CRA — Cloud Reference Architecture (130 pages)

### IAM (Identity & Access Management)

| Path | Topic |
|------|-------|
| `CRA/iam/Azure/general.html` | Azure IAM Overview |
| `CRA/iam/Azure/Roles/AdminIT_Roles.html` | AdminIT Roles in Azure |
| `CRA/iam/Azure/Roles/CustomRoles.html` | Custom Roles |
| `CRA/iam/Azure/RBAC/RBAC.html` | Azure RBAC |
| `CRA/iam/Azure/PIM/PIM.html` | Privileged Identity Management |
| `CRA/iam/Azure/AAD_B2C/AAD_B2C.html` | Azure AD B2C |
| `CRA/iam/Azure/AzureAdApplicationPermissions/AzureAdAppPermissions.html` | Azure AD App Permissions |
| `CRA/iam/Azure/EntraIDGroups/EntraIDGroups.html` | Entra ID Groups |
| `CRA/iam/Azure/GroupBasedLicensing/GroupBasedLicensing.html` | Group-Based Licensing |
| `CRA/iam/Azure/ManagedIdentities/ManagedIdentities.html` | Managed Identities |
| `CRA/iam/Azure/ServicePrincipals/ServicePrincipals.html` | Service Principals |
| `CRA/iam/Azure/ExternalIdentities/ExternalIdentities.html` | External Identities |
| `CRA/iam/Azure/Entra_Verified_Id/Entra_Verified_Id.html` | Entra Verified ID |
| `CRA/iam/Azure/FIDO2_Registration/FIDO2.html` | FIDO2 Registration |
| `CRA/iam/Azure/MSALFLUTTER/MSALFLUTTER.html` | MSAL Flutter |
| `CRA/iam/Azure/Workload_Identity_Federation/Workload_Identity_Federation.html` | Workload Identity Federation |
| `CRA/iam/AWS/general.html` | AWS IAM Overview |
| `CRA/iam/AWS/SSO/single-sign-on.html` | AWS SSO |
| `CRA/iam/AWS/functional_users/functional-users.html` | AWS Functional Users |
| `CRA/iam/Aliyun/general.html` | Aliyun IAM |

### Cloud Governance

| Path | Topic |
|------|-------|
| `CRA/cg/Azure/AzureTenants.html` | Azure Tenants |
| `CRA/cg/Azure/ManagementGroups.html` | Management Groups |
| `CRA/cg/Azure/AzureLandingZones/ALZ.html` | Azure Landing Zones |
| `CRA/cg/Azure/ResourceGroups.html` | Resource Groups |
| `CRA/cg/Azure/AzurePolicies.html` | Azure Policies |
| `CRA/cg/Azure/NamingConventions/NamingConventions.html` | BASF Naming Conventions |
| `CRA/cg/Azure/AzureRegions.html` | Azure Regions |
| `CRA/cg/Azure/EntraIDAdminUnits.html` | Entra ID Admin Units |
| `CRA/cg/Azure/Lighthouse/Lighthouse.html` | Azure Lighthouse |
| `CRA/cg/Azure/GovernanceSummary.html` | Governance Summary |
| `CRA/cg/AWS/AWSGeneralGovernance.html` | AWS General Governance |
| `CRA/cg/AWS/AWSOrganizations.html` | AWS Organizations |
| `CRA/cg/AWS/AWSAccountFactory.html` | AWS Account Factory |
| `CRA/cg/AWS/AWSPolicies.html` | AWS Policies |
| `CRA/cg/AWS/AWSNamingConventions.html` | AWS Naming Conventions |
| `CRA/cg/AWS/AWSRegions.html` | AWS Regions |
| `CRA/cg/AWS/AWSSummary.html` | AWS Governance Summary |
| `CRA/cg/Aliyun/AliyunGeneralGovernance.html` | Aliyun Governance |

### Cloud Environments

| Path | Topic |
|------|-------|
| `CRA/ce/Azure/general.html` | Azure Cloud Environment Overview |
| `CRA/ce/Azure/subscription/OrderAzureSubscription.html` | How to Order an Azure Subscription |
| `CRA/ce/Azure/subscription/DeprovisionAzureSubscription.html` | Deprovisioning a Subscription |
| `CRA/ce/Azure/subscription/RecoverAzureSubscription.html` | Recovering a Subscription |
| `CRA/ce/Azure/subscription/AzureSubscriptionDesign.html` | Subscription Design |
| `CRA/ce/Azure/subscription/AccessFromBASFCorpNet.html` | Access from BASF Corp Network |
| `CRA/ce/Azure/tools/AccessViaCLI.html` | Azure CLI Access |
| `CRA/ce/Azure/tools/AccessViaPowerShell.html` | PowerShell Access |
| `CRA/ce/Azure/tools/AccessViaTerraform.html` | Terraform Access |
| `CRA/ce/Azure/tools/AccessViaARMTemplates.html` | ARM Template Access |
| `CRA/ce/Azure/tools/AZCOPY.html` | AzCopy Usage |
| `CRA/ce/Azure/tools/AzureDevOps.html` | Azure DevOps Integration |
| `CRA/ce/AWS/general.html` | AWS Cloud Environment |
| `CRA/ce/AWS/account/OrderAWSAccount.html` | How to Order an AWS Account |
| `CRA/ce/AWS/account/DeprovisionAWSAccount.html` | Deprovisioning an AWS Account |
| `CRA/ce/AWS/account/RecoverAWSAccount.html` | Recovering an AWS Account |
| `CRA/ce/AWS/tools/AccessViaCLI.html` | AWS CLI Access |
| `CRA/ce/Aliyun/general.html` | Aliyun Environment |

### Network Topology & Connectivity (NTAC)

| Path | Topic |
|------|-------|
| `CRA/ntac/ntac_overview.html` | **Network Overview — connectivity options (Public/Intranet/DMZ/AirGap)** |
| `CRA/ntac/Azure/general.html` | Azure Networking General |
| `CRA/ntac/Azure/HubAndSpoke/HubAndSpoke.html` | Hub & Spoke Architecture |
| `CRA/ntac/Azure/Intranet/Intranet.html` | Intranet Connectivity |
| `CRA/ntac/Azure/PublicInternet/PublicInternet.html` | Public Internet Connectivity |
| `CRA/ntac/Azure/DMZ/DMZ.html` | DMZ Connectivity |
| `CRA/ntac/Azure/AirGap/AirGap.html` | AirGap Connectivity |
| `CRA/ntac/Azure/PrivateEndpoints/PrivateEndpoints.html` | **Private Endpoints at BASF** |
| `CRA/ntac/Azure/DNS/DNS.html` | DNS at BASF |
| `CRA/ntac/Azure/DNS/CustomDNS.html` | Custom DNS |
| `CRA/ntac/Azure/Firewall/Firewall.html` | Azure Firewall |
| `CRA/ntac/Azure/Subnets/Subnets.html` | Subnet Design |
| `CRA/ntac/Azure/VirtualWan/VirtualWan.html` | Virtual WAN |
| `CRA/ntac/Azure/CDN/CDN.html` | CDN |
| `CRA/ntac/Azure/ApplicationGateway/ApplicationGateway.html` | Application Gateway |
| `CRA/ntac/Azure/FrontDoor/FrontDoor.html` | Azure Front Door |
| `CRA/ntac/Azure/TrafficManager/TrafficManager.html` | Traffic Manager |
| `CRA/ntac/Azure/WAF/WAF.html` | Web Application Firewall |
| `CRA/ntac/Azure/LoadBalancer/LoadBalancer.html` | Load Balancer |
| `CRA/ntac/Azure/DDOS/DDOS.html` | DDoS Protection |
| `CRA/ntac/Azure/Azure_to_Azure/Azure_to_Azure.html` | Azure-to-Azure |
| `CRA/ntac/Azure/On_premise_to_Azure/On_premise_to_Azure.html` | On-Prem to Azure |
| `CRA/ntac/Azure/Bastion/AzureBastion.html` | Azure Bastion |
| `CRA/ntac/Azure/IPv6.html` | IPv6 |
| `CRA/ntac/AWS/general.html` | AWS Networking |
| `CRA/ntac/AWS/PrivateEndpoints/AWSPrivateLink.html` | AWS PrivateLink |
| `CRA/ntac/AWS/DNS/Route53PrivateHostedZone.html` | Route53 Private Hosted Zone |
| `CRA/ntac/Aliyun/general.html` | Aliyun Networking |

### IaaS

| Path | Topic |
|------|-------|
| `CRA/iaas/Azure/general.html` | Azure IaaS Overview |
| `CRA/iaas/Azure/VM/VMManagement.html` | VM Management |
| `CRA/iaas/Azure/VM/VMBackup.html` | VM Backup |
| `CRA/iaas/Azure/VM/VMUpdate.html` | VM Updates |
| `CRA/iaas/Azure/VM/MachineConfiguration.html` | Machine Configuration |
| `CRA/iaas/Azure/VM/AVDReference.html` | Azure Virtual Desktop |

### Operations

| Path | Topic |
|------|-------|
| `CRA/ops/monitoring/general.html` | Monitoring General |
| `CRA/ops/monitoring/Azure/Azure.html` | Azure Monitoring |
| `CRA/ops/monitoring/AWS/AWS.html` | AWS Monitoring |

---

## CP — Container Platform (21 pages)

| Path | Topic |
|------|-------|
| `CP/index.html` | Container Platform Overview |
| `CP/aks/aks-overview.html` | AKS Overview |
| `CP/aks/aks-provisioning.html` | AKS Provisioning |
| `CP/aks/aks-network.html` | AKS Networking |
| `CP/aks/aks-imagevalidation.html` | AKS Image Validation |
| `CP/aks/aks-firewall-outbound-rules.html` | AKS Firewall Outbound Rules |
| `CP/aks/aks-operations.html` | AKS Operations |
| `CP/aks/aks-upgrades.html` | AKS Upgrades |
| `CP/aks/aks-node-image.html` | AKS Node Images |
| `CP/aks/aks-workload-identity.html` | AKS Workload Identity |
| `CP/aks/aks-monitoring.html` | AKS Monitoring |
| `CP/aks/aks-agw.html` | AKS Application Gateway |
| `CP/aks/aks-front-door-integration.html` | AKS Front Door Integration |
| `CP/aks/aks-ai.html` | AKS AI |
| `CP/aks/aks-addons.html` | AKS Addons |
| `CP/aks/aks-managed-prometheus-grafana.html` | AKS Managed Prometheus/Grafana |
| `CP/aks/aks-automatic.html` | AKS Automatic |
| `CP/aks/aks-service-mesh.html` | AKS Service Mesh |
| `CP/aks/aks-backup.html` | AKS Backup |
| `CP/aks/aks-container-apps.html` | Container Apps |
| `CP/aks/aks-troubleshooting.html` | AKS Troubleshooting |

---

## CRI — Cloud Reference Implementations (132 pages)

Organized by domain: IAM, Governance, Compute, Networking, Storage, Data, Containers, ML, Security.
All under `/CRI/` prefix. Key paths:

| Path | Topic |
|------|-------|
| `CRI/implementations/iam/` | IAM reference implementations |
| `CRI/implementations/governance/` | Governance implementations |
| `CRI/implementations/compute/` | Compute (VM, VMSS, Batch) |
| `CRI/implementations/networking/` | Networking (VNet, NSG, Firewall, DNS, PE) |
| `CRI/implementations/storage/` | Storage implementations |
| `CRI/implementations/data/` | Data (SQL, Cosmos, PostgreSQL, Redis) |
| `CRI/implementations/containers/` | Container implementations (AKS, ACR, ACA) |
| `CRI/implementations/ml/` | Machine Learning |
| `CRI/implementations/security/` | Security implementations (KeyVault, Defender) |

---

## CT — Cloud Tutorials & One-Pagers (141 pages)

### AdminIT & Roles

| Path | Topic |
|------|-------|
| `CT/CloudOnePager/AdminIT/Roles/Technical_Owner.html` | Technical Owner Role |
| `CT/CloudOnePager/AdminIT/Roles/Subscription_Contributor.html` | Subscription Contributor Role |
| `CT/CloudOnePager/AdminIT/Roles/AdminIT_Landingzone_Owner.html` | Landing Zone Owner Role |

### Connectivity

| Path | Topic |
|------|-------|
| `CT/CloudOnePager/Connectivity/Artifactory/howtoartifactory.html` | How to use Artifactory |
| `CT/CloudOnePager/Connectivity/SSH/howtossh.html` | SSH Access |
| `CT/CloudOnePager/Connectivity/MFA/howtomfa.html` | Multi-Factor Authentication |
| `CT/CloudOnePager/Connectivity/PASS/howtopass.html` | PASS Connectivity |

### DevOps

| Path | Topic |
|------|-------|
| `CT/CloudOnePager/DevOps/GitHubActions/howtogithubactions.html` | **GitHub Actions at BASF** |
| `CT/CloudOnePager/DevOps/ServiceConnections/howtosc.html` | **Service Connections** |
| `CT/CloudOnePager/DevOps/BranchPolicies/howtobranchpolicies.html` | Branch Policies |
| `CT/CloudOnePager/DevOps/ForkWorkflow/howtoForkWorkflow.html` | Fork Workflow |
| `CT/CloudOnePager/DevOps/GitHubCopilot/howtogithubcopilot.html` | GitHub Copilot at BASF |
| `CT/CloudOnePager/DevOps/InnerSource/howtoinnerSource.html` | InnerSource |

### Azure Tutorials

| Path | Topic |
|------|-------|
| `CT/AKS/aks_gettingstarted.html` | **AKS Getting Started** |
| `CT/AKS/DeployViaADO.html` | AKS Deploy via Azure DevOps |
| `CT/AKS/AKSGoCheatSheet.html` | AKS Go Cheat Sheet |
| `CT/AzureOpenAI/prereq.html` | Azure OpenAI Prerequisites |
| `CT/AzureOpenAI/setup.html` | Azure OpenAI Setup |
| `CT/Subscription/toc.html` | Azure Subscription Management |
| `CT/Frontdoor-Cloudflare-Migration/index.html` | Front Door/Cloudflare Migration |
| `CT/WAFOrdering/index.html` | WAF Ordering |

### AWS Tutorials

| Path | Topic |
|------|-------|
| `CT/AWS/CostOptimizationHub.html` | AWS Cost Optimization Hub |
| `CT/AWS/VPCEndpoints.html` | VPC Endpoints |
| `CT/AWS/Well-Architected.html` | Well-Architected Tool |

### Kubernetes Tutorials

| Path | Topic |
|------|-------|
| `CT/Kubernetes/ServiceConnection.html` | Kubernetes Service Connections |
| `CT/Kubernetes/DeploymentPipeline.html` | Kubernetes Deployment Pipelines |

### Cloud Charging

| Path | Topic |
|------|-------|
| `CT/CloudOnePager/CloudCharging/CloudChargingOverview.html` | **Cloud Charging Overview** |
| `CT/CloudOnePager/CloudCharging/ChangeTAOInWebInfo.html` | **Change Cost Center (TAO) in WebInfo** |

### Cloud Native Security Baseline

| Path | Topic |
|------|-------|
| `CT/CloudOnePager/CloudNativeBaselineHowTo/CloudNativeSecurityBaseline.html` | Security Baseline Access |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/AppServiceTLS.html` | App Service TLS |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/AppServiceFTPS.html` | App Service FTPS |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/AzureCosmosDBFW.html` | Cosmos DB Firewall |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/CRunrestrictedNetwork.html` | Container Registry Network |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/KeyVaultSoftDelete.html` | Key Vault Soft Delete |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/MgmtPortsVM.html` | VM Management Ports |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/ImplicitFlow.html` | Implicit Flow Vulnerability |
| `CT/CloudOnePager/CloudNativeBaselineHowTo/StrictlyConfidentialAtCloud.html` | Strictly Confidential in Cloud |

### MS Graph API

| Path | Topic |
|------|-------|
| `CT/Graph-API/BASF-Environment.html` | MS Graph API at BASF |
| `CT/Graph-API/Microsoft-Graph-REST-API/Permissions.html` | Graph API Permissions |
| `CT/Graph-API/Development/SendMail-via-GraphAPI.html` | Send Mail via Graph API |

### DevTest Lab / Voca Training

| Path | Topic |
|------|-------|
| `CT/CloudOnePager/DevTestLabVocaTraining/user/en/index.html` | DevTest Lab User Guide (EN) |

---

## CFO — Cloud FinOps (18 pages)

| Path | Topic |
|------|-------|
| `CFO/CloudFinOps/index.html` | Cloud FinOps Introduction |
| `CFO/CloudFinOps/CostManagementBasics/finops-platform-access.html` | **Accessing FinOps Platform** |
| `CFO/CloudFinOps/CostManagementBasics/cost-management-azure.html` | Azure Cost Management |
| `CFO/CloudFinOps/CostManagementBasics/cost-explorer-aws.html` | AWS Cost Explorer |
| `CFO/CloudFinOps/CostManagementBasics/budgets.html` | Cloud Budgets |
| `CFO/CloudFinOps/CostManagementBasics/cost-center-assignments.html` | **Cost Center Assignments** |
| `CFO/CloudFinOps/CloudBudgetsInsights.html` | Cloud Budget Insights |
| `CFO/CloudFinOpsPlatform/index.html` | FinOps Platform Overview |
| `CFO/CloudFinOpsPlatform/FinOpsPlatform-Request-Access-Roles.html` | FinOps Request Access Roles |
| `CFO/CloudFinOpsPlatform/FinOpsPlatform-Login.html` | FinOps Platform Login |
| `CFO/CloudCharging/CloudChargingOverview.html` | **Cloud Charging Overview** |
| `CFO/CloudCharging/ChangeTAOInWebInfo.html` | **Change TAO in WebInfo** |

---

## CO — Cloud Optimization (35 pages)

| Path | Topic |
|------|-------|
| `CO/Budget/AzureBudgets.html` | Azure Budgets |
| `CO/DataEngineering/AdfPipelines.html` | ADF Pipeline Cleanup |
| `CO/Environment-General/AboutTags.html` | About Azure Tags |
| `CO/Environment-Scheduling/OptimizationScheduleDevQA.html` | **Schedule DEV/QA to save costs** |
| `CO/KeyLevers/KeyLevers.html` | BASF Key Cost Levers |
| `CO/Licenses/AzureHybridUseBenefitswithSQLServerDatabases.html` | AHUB — SQL |
| `CO/Licenses/AzureHybridUseBenefitswithWindowsServerVMs.html` | AHUB — Windows VMs |
| `CO/PaaS/AzureFunctions.html` | Optimize Azure Functions |
| `CO/PaaS/AzureAppService.html` | Optimize App Service |
| `CO/PaaS/AzureSQL.html` | Optimize Azure SQL |
| `CO/PaaS/AzureWAF.html` | Optimize Azure WAF |
| `CO/PaaS/PaaSOptimization.html` | General PaaS Optimization |
| `CO/Storage/BlobStorageLifecycle.html` | Blob Storage Lifecycle |
| `CO/Storage/StandardStorageForSnapshots.html` | Standard Storage for Snapshots |
| `CO/VM-General/ReservedInstances.html` | **VM Reservations** |
| `CO/VM-General/AzureSpotInstances.html` | Azure Spot Instances |
| `CO/VM-General/DeleteUnusedIPAdresses.html` | Delete Unused IPs |
| `CO/VM-General/UpdateVmClassVersion.html` | Update VM Class |
| `CO/VM-General/VMClassesOverview.html` | VM Classes Overview |
| `CO/VM-Scheduling/OptimizationScheduleVMsDedicatedSC.html` | Schedule VMs (Dedicated) |
| `CO/VM-Scheduling/OptimizationScheduleVMsSharedRG.html` | Schedule VMs (Shared RG) |
| `CO/VM-Scheduling/OptimizationScheduleVMPipeline.html` | VM Schedule Pipeline |
| `CO/VM-Scheduling/AWSScheduleVMs.html` | AWS Schedule EC2/RDS |

---

## CSC — Cloud Security & Compliance (62 pages)

### Backup & Disaster Recovery

| Path | Topic |
|------|-------|
| `CSC/BackupandDisasterRecovery/CloudAgnostic/CloudAgnosticGuidance.html` | Cloud-Agnostic Backup Guidance |
| `CSC/BackupandDisasterRecovery/Azure/BackupAndDisasterRecovery.html` | Azure Backup & DR |
| `CSC/BackupandDisasterRecovery/AWS/AWSBackupAndDisasterRecovery.html` | AWS Backup & DR |

### Cryptography

| Path | Topic |
|------|-------|
| `CSC/CloudCryptography/CloudCryptpoGuideline_V2_0.html` | Cloud Cryptography Guideline |
| `CSC/CloudCryptography/Corporate_Cloud_Cryptography_Solution_SDD_v1_4.html` | Crypto Solution Design |

### Compliance Management

| Path | Topic |
|------|-------|
| `CSC/ComplianceManagement/General/GeneralComplianceMgmt.html` | General Compliance Process |
| `CSC/ComplianceManagement/General/ComplianceAndPolicyExemptions.html` | Compliance & Policy Exemptions |
| `CSC/ComplianceManagement/Azure/AzureBaselineComplianceMgmt_CIS.html` | Azure CIS Benchmarks v2.0 |
| `CSC/ComplianceManagement/Azure/AzureComplianceRemediation.html` | Azure Compliance Remediation |
| `CSC/ComplianceManagement/AWS/AWSBaselineComplianceMgmt_CIS.html` | AWS CIS Benchmarks v3.0 |
| `CSC/ComplianceManagement/AWS/AWSComplianceRemediation.html` | AWS Compliance Remediation |

### Event Logging & Monitoring

| Path | Topic |
|------|-------|
| `CSC/EventLogging%26Monitoring/Azure/AzureEventLoggingMonitoring.html` | Azure Event Logging |
| `CSC/EventLogging%26Monitoring/AWS/AWSEventLoggingMonitoring.html` | AWS Event Logging |

### WAF Management

| Path | Topic |
|------|-------|
| `CSC/FirewallManagement/Azurewafguide/Azurewafguide.html` | Azure WAF Guideline |
| `CSC/FirewallManagement/Azurewafguide/wafazure.html` | Azure App Gateway WAF Implementation |
| `CSC/FirewallManagement/Azurewafguide/CreateFrontDoor.html` | Azure Front Door WAF |
| `CSC/FirewallManagement/Awswafguide/wafaws.html` | AWS WAF Implementation |
| `CSC/FirewallManagement/WAFConsequenceMgmt/wafconsequencemgmt.html` | WAF Consequence Management |

### Network Security

| Path | Topic |
|------|-------|
| `CSC/NetworkSecurityManagement/Azure/AzureNetworkSecurityManagement.html` | Azure Network Security |
| `CSC/NetworkSecurityManagement/Azure/AzureFirewallManagement.html` | Azure Firewall Management |
| `CSC/NetworkSecurityManagement/AWS/AWSNetworkSecurityManagement.html` | AWS Network Security |
| `CSC/NetworkSecurityManagement/AWS/AWSFirewallManagement.html` | AWS Firewall Management |

### Security Best Practices

| Path | Topic |
|------|-------|
| `CSC/SecurityBestPractices/CloudSecurityAlerts/AzureAlertGuide.html` | Azure Alert Guide |
| `CSC/SecurityBestPractices/CloudSecurityAlerts/AzureSecurityCenter.html` | Microsoft Defender for Cloud |
| `CSC/SecurityBestPractices/CloudSecurityTools/AzureDefender/AzureDefender.html` | Azure Defender |

### Operational Systems Management

| Path | Topic |
|------|-------|
| `CSC/OperationalSystemsManagement/Azure/AzureOperationalSystemsManagement.html` | Azure Ops Management |
| `CSC/OperationalSystemsManagement/AWS/AWSOperationalSystemsManagement.html` | AWS Ops Management |

---

## How to Help Users with Cloud Reference

1. **Search this index** for URLs matching their question
2. **Build the full URL**: `https://docs.cloudreference.basf.com/{path}`
3. **If authenticated access is available** (user provides cookie): fetch content with `curl -sk -b "AppServiceAuthSession=<cookie>" "https://docs.cloudreference.basf.com/{path}"`
4. **If not authenticated**: provide the direct URL for the user to open in their browser
5. **For cost center changes**: documented at both `CFO/CloudCharging/ChangeTAOInWebInfo.html` and Confluence page 321362285
6. **For AKS topics**: check both `/CP/aks/` (reference architecture) and `/CT/AKS/` (tutorials)

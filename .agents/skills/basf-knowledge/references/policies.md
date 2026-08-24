# Key BASF Cloud & Networking Policies

Quick-reference for commonly asked policy questions. Source: Confluence DNSDHCP and BASANTCLOUD spaces.

## DNS Policies

**Source**: [DNS & DHCP Policy/Guidelines](https://confluence.basf.net/display/DNSDHCP/DNS+%26+DHCP+Policy%2FGuidelines) (page 691352050)

### Zone Delegation

> **"Sub zones/domains will not be delegated to third party nameservers."**

This means:
- You **cannot** get NS records pointing to Azure DNS, AWS Route53, or any external DNS provider
- All DNS records under `basf.net`, `basf.com`, and `basf.systems` are centrally managed
- You must use Service4You (S4Y) to request individual DNS records

### Internal DNS Records Available via S4Y

| Record Type | S4Y Article | Purpose |
|-------------|-------------|---------|
| CNAME | GS0000291 | Alias one name to another |
| Round Robin (A records) | GS0000430 | Load distribution across IPs |
| Fixed IP assignment | GS0000256 | Static IP for a device |

### External DNS Records Available via S4Y

| Record Type | S4Y Article | Purpose |
|-------------|-------------|---------|
| A / AAAA | GS0000424 | Map domain to IPv4/IPv6 |
| CNAME | GS0000424 | Alias to another domain |
| MX | GS0000424 | Mail server routing |
| TXT | GSP000278 | SPF, DKIM, verification records |
| Domain registration | GS0000162 | Register a new external domain |

### What Is NOT Available

- **NS records** — zone delegation is not permitted
- **SRV records** — not listed in S4Y catalog
- **Wildcard records** — not documented as available
- **DNSSEC** — not mentioned in current documentation

### Cloud DNS Domains

| Domain Pattern | Cloud Provider |
|----------------|---------------|
| `*.cloud70.basf.systems` | Azure |
| `*.cloud80.basf.systems` | AWS |

These domains are managed by the DNS-DHCP team for cloud resources.

### New Internal Domain Requests

A process exists to request new internal domains, but:
- The domain must end in `basf.net`
- DNS management remains with the DNS-DHCP team (not delegated)
- Requires alignment with the DNS-DHCP team

### Alternatives for Self-Managed DNS

If you need full DNS control (e.g., for dynamic record management, cert-manager, external-dns):

1. **Azure Private DNS Zones** — full self-service within your VNet, any zone name, but only resolves inside the VNet
2. **Use CNAME records** — point a BASF domain via CNAME to an Azure-managed endpoint (e.g., `*.azurewebsites.net`, `*.cloudapp.azure.com`)
3. **External domain** — register your own domain outside BASF and manage DNS there (requires alignment with security)

## Subscription Management

**Source**: BASANTCLOUD Confluence space

### Cost Center Changes

The cost center (TAO) of an Azure subscription is stored in **ServiceNow CMDB** under the Configuration Item's financial reference field.

**Who can change it**: The primary contact of the subscription.

**How to change**:
1. Follow the procedure at `https://docs.cloudreference.basf.com/CT/CloudOnePager/CloudCharging/ChangeTAOInWebInfo.html`
2. Navigate to ServiceNow → CI → Inventory → Accounting/Financial info → Financial reference
3. Update the cost center

**Fallback**: Email `cloud-management@basf.com`

### New Subscription Setup

- Request via Cloud Reference portal or Confluence guide (page 397973264)
- Requires alignment with your cloud contact

### Subscription Access

- Request access via the procedure in page 452177564
- Managed through AccessIT + Azure AD integration

### Subscription Deletion/Modification

- Documented in page 458437685
- Involves ServiceNow CMDB updates

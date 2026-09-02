---
name: m365-cli
description: >
  Use the Microsoft 365 CLI (m365) to automate and manage Microsoft 365 services
  from the command line. Covers authentication (login, browser, app-only, certificate,
  secret), SharePoint Online (spo) commands, Microsoft Teams, Entra ID, Outlook,
  Power Platform, Planner, Viva, Purview, Exchange Online (exo), and SharePoint
  Framework (spfx) projects. Use available web search or page-retrieval tools to
  fetch current command documentation from pnp.github.io/cli-microsoft365. Use
  m365 request for raw Graph API calls.
  Use when asked to: "use m365 cli", "SharePoint automation", "manage SharePoint files",
  "list SharePoint sites", "m365 spo", "m365 teams", "m365 entra", "m365 login",
  "Microsoft 365 automation", "m365 script", "spo file get", "spo listitem",
  "spo site list", "Teams management cli", "Entra ID cli", "m365 request",
  "Graph API cli", "m365 help", "m365 command", "cli-microsoft365", "PnP CLI".
author: Daniel Kaesmayr
metadata:
  category: automation
  version: "1.1.1"
---

# CLI for Microsoft 365 (m365)

Cross-platform CLI for managing Microsoft 365 tenants, SharePoint Online, Teams,
Entra ID, and more. Docs: **https://pnp.github.io/cli-microsoft365/**

## When to Use

- Automate SharePoint Online file/list/site operations
- Manage Microsoft Teams channels, members, apps
- Create or update Entra (AAD) app registrations and users
- Script repetitive M365 admin tasks
- Build CI/CD pipelines that interact with Microsoft 365

---

## Step 1: Look Up Command Documentation

Before running any command, fetch the live docs from the CLI website using any
available web search, crawl, extract, or page-retrieval tool in your environment.
Prefer the exact docs URL when you can derive it directly. The URL pattern is consistent:

```
https://pnp.github.io/cli-microsoft365/cmd/<group>/<subgroup>/<command>/
```

**Examples:**

| What you want             | Doc URL                                                                  |
| ------------------------- | ------------------------------------------------------------------------ |
| `m365 spo file get`       | `https://pnp.github.io/cli-microsoft365/cmd/spo/file/file-get/`          |
| `m365 spo site list`      | `https://pnp.github.io/cli-microsoft365/cmd/spo/site/site-list/`         |
| `m365 spo listitem list`  | `https://pnp.github.io/cli-microsoft365/cmd/spo/listitem/listitem-list/` |
| `m365 teams channel list` | `https://pnp.github.io/cli-microsoft365/cmd/teams/channel/channel-list/` |
| `m365 entra user list`    | `https://pnp.github.io/cli-microsoft365/cmd/entra/user/user-list/`       |
| `m365 login`              | `https://pnp.github.io/cli-microsoft365/cmd/login/`                      |

### Fetch a command's docs

- Open or fetch the exact command page.
- Extract usage, required and optional flags, examples, and notes about permissions or prerequisites.
- If the page is incomplete, also inspect the parent group page and the official GitHub repo.

### Browse all commands in a group

- Fetch the group landing page, such as `https://pnp.github.io/cli-microsoft365/cmd/spo/`.
- Extract subgroup names and command links before choosing the most specific command page.

---

## Step 2: Authentication

### Check login status

```bash
m365 status
# Shows: connectedAs, authType, appId, tenantId, connectionName
```

### Interactive login (browser — most common for interactive use)

```bash
m365 login
# authType: browser — opens system browser for Microsoft sign-in
```

### App-only login (for unattended scripts/CI)

```bash
# Certificate file
m365 login --authType certificate \
  --clientId "<app-id>" \
  --certificateFile "/path/to/cert.pem" \
  --thumbprint "<thumbprint>" \
  --tenant "<tenant-id>"

# Certificate as base64 string
m365 login --authType certificate \
  --clientId "<app-id>" \
  --certificateBase64Encoded "<base64-cert>" \
  --thumbprint "<thumbprint>" \
  --tenant "<tenant-id>"
```

### Secret-based login

```bash
m365 login --authType secret \
  --clientId "<app-id>" \
  --clientSecret "<secret>" \
  --tenant "<tenant-id>"
```

### Logout

```bash
m365 logout
```

> **Note on permissions**: Some commands (e.g. `spo site list`, `teams team list`)
> require elevated scopes or admin consent. If you get a 401 "App is not allowed"
> or a Skype backend error, the operation needs admin-consented app permissions —
> interactive browser auth won't be enough. Use `--debug` to see the exact error.

---

## Step 3: Command Groups Reference

All groups as of v11.6.0 (`m365 --help`):

| Group        | Service                        | Count        |
| ------------ | ------------------------------ | ------------ |
| `spo`        | SharePoint Online              | 376 commands |
| `entra`      | Entra ID (replaces `aad`)      | 117 commands |
| `teams`      | Microsoft Teams                | 72 commands  |
| `outlook`    | Outlook / Exchange             | 22 commands  |
| `planner`    | Microsoft Planner              | 31 commands  |
| `pp`         | Power Platform                 | 28 commands  |
| `viva`       | Viva Engage                    | 30 commands  |
| `purview`    | Microsoft Purview              | 21 commands  |
| `flow`       | Power Automate                 | 19 commands  |
| `pa`         | Power Apps                     | 13 commands  |
| `tenant`     | Tenant admin                   | 24 commands  |
| `onedrive`   | OneDrive                       | 8 commands   |
| `graph`      | Graph extensions/subscriptions | 16 commands  |
| `spe`        | SharePoint Embedded            | 13 commands  |
| `spfx`       | SharePoint Framework           | 9 commands   |
| `todo`       | Microsoft To-Do                | 10 commands  |
| `onenote`    | OneNote                        | 3 commands   |
| `exo`        | Exchange Online                | 1 command    |
| `external`   | External content/connectors    | 8 commands   |
| `file`       | File operations                | 5 commands   |
| `search`     | Microsoft Search               | 5 commands   |
| `app`        | App management                 | 4 commands   |
| `booking`    | Microsoft Bookings             | 2 commands   |
| `connection` | Connection management          | 4 commands   |
| `context`    | CLI context                    | 5 commands   |
| `cli`        | CLI settings                   | 14 commands  |
| `util`       | Utilities                      | 1 command    |

> ⚠️ `aad` is deprecated. Always use `entra` instead.
> ⚠️ `graph` group is **not** for raw API calls — it manages Graph schema extensions,
> open extensions, and subscriptions. Use `m365 request` for raw Graph/REST calls.

---

## Step 4: Common SharePoint Online Operations

### Sites

```bash
# Get a specific site (requires site-level permissions)
m365 spo site get --url https://contoso.sharepoint.com/sites/marketing

# List all sites — requires SharePoint admin or elevated app permissions
# Will fail with 401 if app token lacks admin scope
m365 spo site list

# Filter site list (when admin permissions available)
m365 spo site list --filter "Url -like 'project'"

# List only Team Sites or Communication Sites
m365 spo site list --type TeamSite
m365 spo site list --type CommunicationSite

# Add a site
m365 spo site add --type CommunicationSite \
  --url https://contoso.sharepoint.com/sites/newsite \
  --title "New Site"
```

### Files

```bash
# Get file metadata by server-relative URL
m365 spo file get \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --url "/sites/marketing/Shared Documents/report.pdf"

# Get file metadata by GUID
m365 spo file get \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --id "b2307a39-e878-458b-bc90-03bc578531d6"

# List files in a folder (use --folderUrl, not --folder)
m365 spo file list \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --folderUrl "/sites/marketing/Shared Documents"

# List files recursively
m365 spo file list \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --folderUrl "/sites/marketing/Shared Documents" \
  --recursive

# List specific fields only
m365 spo file list \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --folderUrl "/sites/marketing/Shared Documents" \
  --fields "Name,Length,TimeLastModified"

# Download a file to disk
m365 spo file get \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --url "/sites/marketing/Shared Documents/report.pdf" \
  --asFile --path ./report.pdf

# Get file content as string (e.g. a .txt or .md file)
m365 spo file get \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --url "/sites/marketing/Shared Documents/notes.txt" \
  --asString
```

### List Items

```bash
# List items in a SharePoint list
m365 spo listitem list \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --listTitle "Tasks"

# Get single list item by ID
m365 spo listitem get \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --listTitle "Tasks" \
  --id 42

# Add a list item
m365 spo listitem add \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --listTitle "Tasks" \
  --Title "New task" \
  --Status "Active"

# Update a list item
m365 spo listitem set \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --listTitle "Tasks" \
  --id 42 \
  --Status "Done"
```

### Web / Site Properties

```bash
# Get web properties
m365 spo web get --url https://contoso.sharepoint.com/sites/marketing

# List all document libraries on a site
m365 spo list list \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --baseTemplate DocumentLibrary
```

---

## Step 5: Raw API Calls with `m365 request`

Use `m365 request` to call any Graph API or SharePoint REST endpoint directly.
This is the correct way to make raw API calls — **not** `m365 graph get`.

```bash
# GET current user from Graph API
m365 request --url "https://graph.microsoft.com/v1.0/me"

# GET with specific fields
m365 request \
  --url "https://graph.microsoft.com/v1.0/me?$select=displayName,mail,jobTitle"

# GET users list (requires User.Read.All)
m365 request \
  --url "https://graph.microsoft.com/v1.0/users?$top=10&$select=displayName,mail"

# POST request with body
m365 request \
  --url "https://graph.microsoft.com/v1.0/me/sendMail" \
  --method post \
  --body '{"message":{"subject":"Test","body":{"contentType":"Text","content":"Hello"},"toRecipients":[{"emailAddress":{"address":"user@example.com"}}]}}'

# SharePoint REST API call
m365 request \
  --url "https://contoso.sharepoint.com/sites/marketing/_api/web/lists" \
  --headers '{"Accept":"application/json;odata=nometadata"}'

# Output as JSON (default)
m365 request \
  --url "https://graph.microsoft.com/v1.0/me" \
  --output json
```

> **Tip**: Use `--output json | jq '...'` to filter results from `m365 request`.

---

## Step 6: Entra ID Operations

```bash
# Get current user info
m365 entra user get --userName "user@contoso.com" --output json

# List all users (requires User.Read.All)
m365 entra user list --output json

# Get user by object ID
m365 entra user get --id "c1091dd9-365e-4e02-986f-56b8d96223c2"

# List groups
m365 entra group list --output json

# List app registrations
m365 entra app list --output json

# Create an app registration
m365 entra app add --name "My App"
```

---

## Step 7: Output Formatting

All commands support `--output`:

```bash
# JSON (best for scripting — most detail)
m365 entra user get --userName "user@contoso.com" --output json

# Text table (human readable, fewer fields)
m365 entra user get --userName "user@contoso.com" --output text

# CSV (for spreadsheet import)
m365 spo file list --webUrl https://... --folderUrl "/Shared Documents" --output csv

# Markdown table
m365 entra user list --output md

# JMESPath query to filter/transform JSON
m365 entra user list --output json \
  --query "[?jobTitle=='Manager'].{Name:displayName,Email:mail}"
```

---

## Step 8: Scripting Patterns

### Pipe output to jq for filtering

```bash
# Get all Entra users and extract emails
m365 entra user list --output json | jq -r '.[].mail'

# Filter SPO files larger than 1MB
m365 spo file list \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --folderUrl "/sites/marketing/Shared Documents" \
  --output json | jq '.[] | select(.Length > 1048576) | {Name, Length}'
```

### Loop over results

```bash
# Download all files from a library
files=$(m365 spo file list \
  --webUrl https://contoso.sharepoint.com/sites/marketing \
  --folderUrl "/sites/marketing/Shared Documents" \
  --output json | jq -r '.[].ServerRelativeUrl')

while IFS= read -r fileUrl; do
  filename=$(basename "$fileUrl")
  m365 spo file get \
    --webUrl https://contoso.sharepoint.com/sites/marketing \
    --url "$fileUrl" \
    --asFile --path "./$filename"
done <<< "$files"
```

### Environment variables for auth (CI/CD)

```bash
export CLIMICROSOFT365_AADAPPID="<client-id>"
export CLIMICROSOFT365_TENANT="<tenant-id>"
# Then login with certificate/secret
m365 login --authType certificate --certificateFile cert.pem \
  --thumbprint "<thumbprint>"
```

---

## Step 9: Getting Help

### Built-in help (always accurate for the installed version)

```bash
# List all command groups
m365 --help

# Command group overview
m365 spo --help
m365 spo file --help

# Specific command: full options + examples
m365 spo file get --help
m365 spo file get --help full   # includes response schema

# Show only examples
m365 spo file list --help examples
```

### Fetch live documentation

- Prefer the direct command URL when you know the command shape.
- Otherwise search the official docs site for the intended operation, then open the matching command page.
- Capture usage, all options with descriptions, example invocations, and any warnings about auth, permissions, or preview status.

### Search for commands

- Use a site-scoped web search such as `m365 cli <what you want to do> site:pnp.github.io/cli-microsoft365`.
- If search is noisy, search the group index page first, then open the command page directly.

---

## Troubleshooting

| Error                                                              | Likely Cause                                                                       | Fix                                                                             |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `You are not logged in`                                            | No active session                                                                  | Run `m365 login`                                                                |
| `401 App is not allowed to call SPO with user_impersonation scope` | SPO admin commands need elevated app permissions (e.g. `spo site list`)            | Use app-only auth with `Sites.FullControl.All` or `SharePoint.Read.All`         |
| `Failed to execute Skype backend request`                          | Teams commands need Graph `Team.ReadBasic.All` or admin consent                    | Re-login with app-only auth that has Teams permissions                          |
| `404 FILE NOT FOUND`                                               | Wrong site URL, wrong server-relative path, or file doesn't exist at that location | Check `--webUrl` matches the site, and `--url` is the full server-relative path |
| `Request failed with status code 404`                              | Graph endpoint doesn't exist or resource not found                                 | Check the API URL, verify the resource ID                                       |
| `Access denied`                                                    | Missing SharePoint site permissions                                                | Add user/app to site collection                                                 |
| Stale tokens                                                       | Session expired                                                                    | `m365 logout && m365 login`                                                     |
| `[object Object]` error with no message                            | Use `--debug` flag to see the full HTTP error                                      | `m365 <command> --debug 2>&1 \| tail -40`                                       |

### Debug any failing command

```bash
# See full HTTP request/response and stack trace
m365 spo site list --type TeamSite --debug 2>&1 | tail -50
```

---

## References

- [Official Docs](https://pnp.github.io/cli-microsoft365/)
- [Command Reference](https://pnp.github.io/cli-microsoft365/cmd/login/)
- [Authentication Modes](https://pnp.github.io/cli-microsoft365/concepts/persisting-connection/)
- [Sample Scripts](https://pnp.github.io/cli-microsoft365/sample-scripts/)
- [GitHub Repo](https://github.com/pnp/cli-microsoft365)

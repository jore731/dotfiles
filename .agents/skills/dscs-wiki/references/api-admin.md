# ACL, Auth & System API Reference

Detailed parameters and response schemas for DokuWiki access control, authentication, and system methods.

**Base URL**: `https://wiki.ds.basf.net/lib/exe/jsonrpc.php`

All calls are `POST` with `Content-Type: application/json` and Basic Auth.

---

## core.aclCheck

Check permissions for a page or media file for the current user or a specific user/group.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | string | Yes | Page or media ID |
| `user` | string | No | Username to check. Default: current user |
| `groups` | array | No | Groups to check. Default: `[]` |

**Response:** `integer` — permission level.

**Permission levels:**

| Level | Meaning |
|-------|---------|
| 0 | No access |
| 1 | Read |
| 2 | Edit |
| 4 | Create |
| 8 | Upload |
| 16 | Delete |
| 255 | Admin |

**Example:**

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.aclCheck" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{"page": "dscs:onboarding"}'
```

---

## core.whoAmI

Get info about the currently authenticated user. Useful for verifying connectivity and auth.

**Parameters:** None (empty object `{}`).

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| `login` | string | Login name |
| `name` | string | Full name |
| `mail` | string | Email address |
| `groups` | array | Groups the user belongs to |
| `isadmin` | boolean | Whether the user is a super user |
| `ismanager` | boolean | Whether the user is a manager |

**Example:**

```bash
curl -s -X POST "https://wiki.ds.basf.net/lib/exe/jsonrpc.php/core.whoAmI" \
  -u "$WIKI_USER:$WIKI_PASS" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## core.login

Log in with username and password. Sets cookies for subsequent requests.

> **Note:** Prefer Basic Auth over this method. This is only useful when you need cookie-based session management.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user` | string | Yes | Username |
| `pass` | string | Yes | Password |

**Response:** `integer` — `1` on success.

This method does not require prior authentication (it is the login mechanism).

---

## core.logoff

Log off the current user, deleting session cookies.

**Parameters:** None.

**Response:** `integer`.

---

## core.getWikiVersion

Get the DokuWiki version string (e.g., `"Release 2024-02-06a 'Kaos'"`).

**Parameters:** None (empty object `{}`).

**Response:** `string` — version string.

---

## core.getWikiTitle

Get the wiki's configured title.

**Parameters:** None (empty object `{}`).

**Response:** `string` — wiki title.

This method does not require authentication.

---

## core.getWikiTime

Get the current server time as Unix timestamp. Useful for compensating time differences when working with revision timestamps.

**Parameters:** None (empty object `{}`).

**Response:** `integer` — Unix timestamp.

---

## core.getAPIVersion

Get the API version number. Increases whenever the API definition changes. Check this to verify compatibility.

**Parameters:** None (empty object `{}`).

**Response:** `integer` — API version number (e.g., `14`).

This method does not require authentication.

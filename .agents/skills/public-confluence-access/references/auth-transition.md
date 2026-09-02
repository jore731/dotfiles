## Auth-Ready Transition

Use this guidance when public reads are insufficient.

## Signals That Auth Is Needed

- The endpoint returns `401` or `403`.
- The content endpoint exists, but the page data is missing or restricted.
- The user needs private spaces or private pages.
- User-related endpoints return anonymous or forbidden responses.

## BASF Username Guidance

For BASF Confluence, short usernames are the better first guess for API auth.
Examples observed in API payloads are short account names rather than email-style
identifiers.

If the user needs authenticated access, try the short username first.

## Authentication Options

Basic auth:

```bash
curl -u SHORT_USERNAME:PASSWORD \
  "https://confluence.basf.net/rest/api/content/391850245"
```

Personal access token:

```bash
curl -H "Authorization: Bearer YOUR_PAT" \
  "https://confluence.basf.net/rest/api/content/391850245"
```

Prefer a PAT when available.

## Escalation Rule

Do not start with auth when the task is explicitly about public Confluence.
Only switch to auth-ready patterns after evidence shows the public path is not
enough.

## Safe Verification Steps

1. Test the public content endpoint first.
2. Test the public search endpoint second.
3. If needed, test the same endpoint with auth.
4. Compare the difference in scope or returned fields.
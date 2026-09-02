---
name: basf-rd-experts
description: >
  Extract and structure the list of BASF R&D experts from the BASF Research
  Portal (research.basf.net). The portal requires SSO authentication. Use when
  asked to list BASF researchers, find experts by name or research area, build
  a contact directory, or export the expert registry to CSV/JSON/Markdown.
  Triggers: "list BASF researchers", "BASF R&D experts", "find BASF expert",
  "research.basf.net experts", "BASF expert directory", "who researches X at BASF",
  "extract expert list", "BASF scientist list".
author: Daniel Kaesmayr
metadata:
  category: knowledge-access
  version: "1.0.0"
---

# BASF R&D Experts

Extract the BASF R&D expert registry from the internal research portal at
`https://www.research.basf.net` using an SSO-authenticated browser session.

## Portal URL

```
https://www.research.basf.net/portal/basf/en/dt.jsp?setCursor=1_1888713&letter_1954888=all
```

The query parameter `letter_1954888=all` returns all experts in alphabetical
order across all name initials. To filter by a specific letter, replace `all`
with the desired letter (e.g., `letter_1954888=A`).

The `setCursor` parameter controls pagination. Start with `1_1888713` and
increment the first number by 1 per page if the portal is paginated.

## When to Use This Skill

- The user wants a full or partial list of BASF R&D experts.
- The user wants to find which BASF experts work in a given research field.
- The user wants to export the expert list to a structured format (CSV, JSON, Markdown table).
- The user wants to know contact details, research areas, or group affiliations of BASF researchers.

## Prerequisites

1. You must use an SSO-authenticated browser session — the portal is not
   publicly accessible and redirects anonymous users to the BASF login page.
2. Use the `open_browser_page` tool to open the URL. The user's active SSO
   session in the browser will authenticate automatically.
3. Do NOT attempt to access the portal via `fetch_webpage` without SSO — it
   will return a login redirect, not expert data.

## Default Workflow

### Step 1 — Open the Portal

Open the portal in the user's browser with SSO:

```
open_browser_page("https://www.research.basf.net/portal/basf/en/dt.jsp?setCursor=1_1888713&letter_1954888=all")
```

Wait for the page to load fully. If the page redirects to a login screen,
inform the user that they need to be signed in to their BASF SSO session and
retry once they confirm they are logged in.

### Step 2 — Detect Pagination

After the first page loads:

1. Check the rendered HTML for a total count indicator or "next page" link.
2. If the portal lists experts in batches (e.g., 25 or 50 per page), note
   the total count and calculate the number of pages needed.
3. For letter-filtered views, iterate through `letter_1954888=A` through `Z`
   if individual letter pages have fewer items than the `all` view.

### Step 3 — Extract Expert Data

For each expert entry on the page, extract:

| Field | Description |
|-------|-------------|
| `name` | Full name (first + last) |
| `title` | Job title or academic title (e.g., Dr., Prof.) |
| `research_area` | Research topic, keyword, or group label shown in the portal |
| `group` | Organizational unit or research group, if shown |
| `location` | Site or country, if shown |
| `profile_url` | URL of the expert's individual profile page, if linked |
| `email` | Email address, if shown |

If a field is not present on the listing page, leave it blank — do NOT infer
or guess values.

### Step 4 — Follow Profile Links (Optional, Depth-1)

If the user needs richer data (research interests, publications, full contact):

1. For each expert, open `profile_url` in the browser.
2. Extract additional fields: abstract, keywords, publication count, ORCID,
   phone, full organizational path.
3. Rate-limit requests — wait 1–2 seconds between profiles to avoid triggering
   rate limits on the portal.

### Step 5 — Structure the Output

Return data as a Markdown table by default:

```markdown
| Name | Title | Research Area | Group | Location | Profile |
|------|-------|---------------|-------|----------|---------|
| Jane Doe | Dr. | Catalysis | RCE | Ludwigshafen | [link](url) |
```

On user request, also produce:

- **CSV**: `name,title,research_area,group,location,profile_url,email`
- **JSON**: array of objects with the fields above
- **Filtered view**: filter by research_area keyword or location

Save output to a file when extracting more than 50 experts:

```
notes/research/basf-rd-experts-YYYYMMDD.md   (Markdown)
notes/research/basf-rd-experts-YYYYMMDD.csv  (CSV)
```

## Error Handling

| Symptom | Action |
|---------|--------|
| Page redirects to login | Ask user to sign in via SSO, then retry |
| Page loads but shows no experts | Check if JavaScript rendered content — try scrolling or waiting 3s |
| `open_browser_page` unavailable | Inform the user; fall back to asking them to copy-paste the page HTML |
| Partial load / timeout | Save what was extracted, report the count, offer to retry remaining pages |
| Portal structure changed | Extract as much structure as possible; inform user which fields could not be reliably parsed |

## Data Handling Rules

- **Do NOT publish** or commit expert contact data to public repositories.
- Store output files in private workspace only (e.g., `notes/` folder in the local workspace).
- Do not include email addresses in any files committed to git unless the user explicitly intends to share them.
- If unsure whether output will be committed, strip the `email` column by default.

## Output Quality Checks

Before delivering the final output:

- [ ] At least one expert entry extracted successfully
- [ ] No placeholder or guessed values in any field
- [ ] Pagination completed (all pages or requested subset)
- [ ] Output format matches user request (table / CSV / JSON)
- [ ] File saved if >50 experts extracted
- [ ] Email column stripped unless user explicitly requested it

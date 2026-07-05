# Doc Framework Detection & Navigation Strategies

Per-framework strategies for auto-detecting documentation sites and navigating them efficiently.

## Detection Signals

When fetching a doc page, look for these signals to identify the framework:

| Framework | Detection signals |
|-----------|-------------------|
| **Docusaurus** | `<meta name="generator" content="Docusaurus">`, `/docs/` URL path, `docusaurus.config.js` references, sidebar with collapsible categories |
| **ReadTheDocs** | `.readthedocs.io` domain, `readthedocs` in footer, version selector dropdown, `/_/` API paths |
| **MkDocs** | `<meta name="generator" content="mkdocs">`, `mkdocs-material` theme classes, `/site/` or similar flat URL structure |
| **Sphinx** | `Created using Sphinx` footer, `.rst` source links, `_static/` and `_sources/` directories |
| **OpenAPI/Swagger** | JSON/YAML with `openapi:` or `swagger:` root key, Swagger UI HTML, `/api-docs` or `/swagger` paths |
| **GitHub Wiki** | `github.com/.../wiki` URL, wiki-specific navigation, `_Sidebar.md` |
| **VitePress** | `vitepress` in source, Vue-based hydration, `.vitepress/` config references |
| **Starlight** | `@astrojs/starlight` references, Astro-based structure |
| **Hugo** | `<meta name="generator" content="Hugo">`, Hugo-specific template markers |
| **GitBook** | `gitbook.com` domain or `gitbook` references, chapter-based navigation |
| **Nextra** | Next.js-based docs with `_meta.json` sidebar config |

## Navigation Strategies

### Docusaurus

- **Sidebar**: Look for sidebar JSON in the page source or extract from rendered nav
- **Versioning**: Check for version dropdown — URLs contain `/docs/` (latest) or `/docs/X.Y/`
- **API docs**: Often generated with `docusaurus-plugin-openapi` — look for `/api/` section
- **Best entry point**: `/docs/intro` or `/docs/getting-started`

### ReadTheDocs

- **Sidebar**: Rendered as nested `<ul>` in left sidebar
- **Versioning**: Version selector in the bottom-left — `en/stable/`, `en/latest/`, `en/vX.Y.Z/`
- **Search**: Has built-in search at `/_/search/` — can be useful for targeted queries
- **Best entry point**: `/en/stable/` or `/en/latest/`
- **Raw source**: Often links to `.rst` or `.md` source files — follow "Edit on GitHub" links

### MkDocs / Material for MkDocs

- **Sidebar**: Clean left navigation, often with search
- **Versioning**: If using mike, version selector in header
- **Best entry point**: Root `/` or `/getting-started/`
- **Navigation config**: Defined in `mkdocs.yml` `nav:` section

### Sphinx

- **Sidebar**: `toctree` based navigation, often deep hierarchies
- **Index**: Look for `genindex.html`, `modindex.html` for API references
- **Cross-references**: Heavy use of `:ref:`, `:doc:`, `:func:` — follow these for related content
- **Best entry point**: `index.html` or `contents.html`

### OpenAPI / Swagger

- **Structure**: Paths → Operations → Parameters → Responses
- **Fetch the spec directly**: Look for `/openapi.json`, `/openapi.yaml`, `/swagger.json`, `/v3/api-docs`
- **Navigation**: Group by tags, then by path prefix
- **Code examples**: Check for `x-code-samples` extension or request/response examples
- **Best approach**: Fetch the raw spec file and parse it directly rather than scraping the UI

### GitHub Wiki

- **Sidebar**: `_Sidebar.md` defines navigation (fetch it directly)
- **Pages**: Each page is a separate markdown file
- **URL pattern**: `github.com/owner/repo/wiki/Page-Name`
- **Raw content**: Append `.md` to page URL or use GitHub API
- **Best entry point**: `wiki/Home` page

### Man Pages / CLI Help

- **Access**: `man <command>` or `<command> --help`
- **Structure**: Synopsis → Description → Options → Examples → See Also
- **Subcommands**: `<command> <subcommand> --help` for nested help
- **Best approach**: Start with `--help`, then `man` for full docs

## Framework-Specific Tips

- **Docusaurus + ReadTheDocs + MkDocs**: All support "Edit this page" links — follow them to find the source repo for raw markdown
- **OpenAPI**: If the Swagger UI is slow to parse, find and fetch the raw spec file instead
- **Any framework**: Look for a search endpoint — many doc sites expose search APIs that can shortcut navigation
- **Version pinning**: Always note which version of the docs you're reading. If there's a version mismatch with the user's setup, flag it

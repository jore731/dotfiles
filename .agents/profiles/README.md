# Portable Agent Profiles

This directory is the behavioral source of truth for tiered agents. Profiles intentionally contain no model identifiers, tool names, permissions, or harness-specific frontmatter.

| Profile | Intent | Typical work |
|---|---|---|
| `fast` | Lowest-cost, bounded, read-only work | Search, summaries, extraction, classification |
| `genius` | Strongest tier for complex execution | Multi-file changes, difficult debugging, migrations |

Harness adapters are generated from these profiles. Do not edit generated files directly:

```sh
sh scripts/generate-agent-adapters.sh
sh scripts/check-agent-adapters.sh
```

To change a profile's behavior, edit its file here, regenerate adapters, run the checker, and update `docs/agent-tiers.md` when the tier contract changes.

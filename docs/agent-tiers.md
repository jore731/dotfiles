# Portable Agent Tiers

## Purpose

The tiered-agent setup controls model cost without treating every task as equal. The default parent agent remains the normal coordinator and implementation lead, using Terra or a harness-managed Auto mode. It delegates bounded cheap work to Fast and complex work to Genius.

## Tiers

| Profile | Cost and capability | Use |
|---|---|---|
| Fast | Lowest-cost tier | Search, summaries, extraction, classification, narrow read-only investigation |
| Default parent | Mid-tier or harness Auto | Normal implementation, debugging, validation, and coordination |
| Genius | Strongest tier | Complex execution, difficult debugging, migrations, security, and high-risk infrastructure |
| Dotfiles steward | Genius model with Fast delegation | Safe dotfiles, Stow, profile, adapter, and configuration maintenance |

Do not alternate models by turn. Delegate by task shape, keep parent context coherent, and escalate when a higher-quality first attempt costs less than retries.

## Fast Web Access

Fast is a strictly local, read-only worker in every harness. It has no web-fetch or web-search capability. Delegate external research to another agent so Fast remains cheap, predictable, and constrained to repository evidence.

## Current Model Mapping

| Harness | Fast | Genius |
|---|---|---|
| OpenCode via GitHub Copilot | `github-copilot/gpt-5.6-luna` | `github-copilot/claude-opus-4.8` |
| Claude Code | `haiku` | `opus` |
| VS Code Copilot | `GPT-5.6 Luna (copilot)` | `Claude Opus 4.8 (copilot)` |

When OpenCode exposes `github-copilot/gpt-5.6-sol`, replace the Genius OpenCode mapping in `scripts/generate-agent-adapters.sh`, regenerate the adapters, and update this table. Do not change the canonical Genius behavior unless its role changes.

## Ownership

| Location | Owns |
|---|---|
| `.agents/profiles/` | Harness-neutral behavior and tier boundaries |
| `scripts/generate-agent-adapters.sh` | Model, tools, permissions, step limits, and harness frontmatter |
| `.config/opencode/agents/` | Generated OpenCode adapters |
| `.claude/agents/` | Generated Claude Code adapters |
| `.copilot/agents/` | Generated VS Code Copilot user-level adapters |

The `dotfiles` steward is a repository-specific Genius-model specialist. It may delegate focused read-only lookups to Fast but does not create a new cost tier.

Never edit generated adapters directly. The consistency checker fails if their body diverges from the canonical profile or if a safety-critical frontmatter field changes.

## Operations

After modifying a profile or mapping:

```sh
sh scripts/generate-agent-adapters.sh
sh scripts/check-agent-adapters.sh
stow --no-folding --target="$HOME" . --ignore='^\.copilot/settings\.json$'
```

Restart OpenCode after any config or agent change. Restart Claude Code if `.claude/agents/` did not exist when the session began. Reload VS Code after changing custom agents.

Repository documentation and scripts are intentionally excluded from Stow by `.stow-local-ignore`; `AGENTS.md` remains globally stowed as shared agent instructions.

## Invocation Examples

```text
@fast Locate all pgAdmin ingress definitions. Do not edit.
@fast Summarize this diff and recommend the narrowest validation command.
@genius Implement the approved multi-file migration, validate it, and report evidence.
@genius Diagnose this persistent failure. Do not edit until you have a supported root-cause hypothesis.
```

## Non-Goals

- Transparent per-turn model switching is not implemented. OpenCode and Copilot agents use fixed model selections.
- Automatic cost routing is not implemented. The parent or user chooses delegation based on the documented task boundaries.
- Genius does not bypass harness approval gates.

## Adding a Harness

1. Confirm the harness's documented agent file format, discovery path, model syntax, tools, and permissions.
2. Add two templates to `scripts/generate-agent-adapters.sh` that append the existing canonical profiles unchanged.
3. Add body and mapping assertions to `scripts/check-agent-adapters.sh`.
4. Add the mapping and reload instructions here.
5. Verify discovery, Fast read-only behavior, and Genius approval behavior before relying on the new adapter.

## VS Code Copilot Verification

The adapters use the documented user-level `~/.copilot/agents/` location and the VS Code custom-agent frontmatter fields `tools`, `model`, `user-invocable`, `disable-model-invocation`, and `agents`. Source: [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents).

After changing Copilot adapters:

1. Reload VS Code and confirm `Fast` and `Genius` appear in custom-agent discovery.
2. Invoke Fast for a local read-only task and confirm it exposes no terminal, edit, or web tools.
3. Invoke Genius for an edit and confirm the normal approval flow remains active.
4. Confirm Genius can delegate to Fast and both configured model labels resolve.

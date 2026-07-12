# ADR-001: Use Canonical Portable Agent Profiles

## Status

Accepted

## Date

2026-07-11

## Context

The development environment uses OpenCode, Claude Code, and VS Code Copilot. Each harness has different agent discovery paths, frontmatter fields, model identifiers, tool names, and permission semantics. We need a low-cost Fast tier and a strongest-tier Genius agent without maintaining unrelated copies of their behavioral instructions.

## Decision

Store harness-neutral behavior in `.agents/profiles/`. Generate thin adapters for OpenCode, Claude Code, and VS Code Copilot with `scripts/generate-agent-adapters.sh`. The VS Code Copilot adapters use its documented user-level `~/.copilot/agents/` discovery path. Verify adapters with `scripts/check-agent-adapters.sh`.

Fast is a bounded local read-only Luna-equivalent worker with no web access. Genius is an implementation-capable strongest-tier worker for complex execution. The normal parent agent remains Terra or harness Auto and owns ordinary coordination.

## Alternatives Considered

### One shared agent file

Rejected. OpenCode, Claude Code, and VS Code Copilot use incompatible frontmatter, tool, model, and permission schemas.

### Independent agent copies per harness

Rejected. Behavioral instructions would drift and model changes would be error-prone.

### Automatic model routing

Deferred. OpenCode plugins cannot replace a selected model per turn, and Copilot traffic cannot be directed through a custom model router.

### Strongest tier only for reviews

Rejected. Complex implementation and debugging benefit from a stronger first attempt before failures occur.

## Consequences

- Behavioral changes occur once in the canonical profile, then adapters are regenerated.
- Model, tool, and permission changes remain localized to adapter templates.
- Generated adapters must not be edited by hand.
- A future Sol model only changes the relevant harness mapping, not Genius behavior.
- Fast has no web-fetch or web-search tools in any supported harness; external research uses another agent.
- VS Code Copilot adapter fields and user-level discovery follow [the VS Code custom-agent documentation](https://code.visualstudio.com/docs/agent-customization/custom-agents).

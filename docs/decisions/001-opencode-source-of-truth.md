# ADR-001: Use OpenCode As Configuration Source

## Status

Accepted

## Context

The environment uses OpenCode, Claude Code, Copilot CLI, and the Copilot app. Each harness has different discovery paths, frontmatter fields, model identifiers, tool names, and permission semantics. Parallel authored profiles and adapter scripts duplicate behavior and create drift.

## Decision

Use OpenCode-native files under `.config/opencode/` as the only authored source of truth. Define agents, commands, skills, plugins, and MCP configuration with OpenCode's native schema. The `/sync-harness-config` command translates supported definitions into native Claude Code, Copilot CLI, and Copilot app files when explicitly requested.

The command must show proposed mappings before editing target files, preserve unrelated target configuration and the unmanaged live Copilot settings file, and report features that cannot be represented in a target harness.

## Consequences

- OpenCode changes are authored once and translated on demand.
- Translation is explicit and reviewable rather than automatic.
- Target files may diverge where a harness cannot represent an OpenCode feature.
- OpenCode configuration changes require restarting OpenCode.

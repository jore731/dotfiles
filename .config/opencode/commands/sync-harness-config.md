---
description: Sync OpenCode agents, commands, skills, and related config to other harnesses.
agent: dotfiles
---

Synchronize the OpenCode configuration in this repository to the supported non-OpenCode targets: Claude Code, Copilot CLI, and the Copilot app.

OpenCode is the only source of truth. Inspect `.config/opencode/` and translate its agents, commands, skills, plugins, and relevant configuration into each target's native format and documented discovery path. Do not copy OpenCode frontmatter blindly: preserve each target's model, tool, permission, invocation, and file-format semantics. Remove or update stale generated target files that this sync owns, but preserve unrelated user files and the live `~/.copilot/settings.json`.

Before editing, show the files and mappings you intend to change. Do not add credentials. Do not modify symlink destinations directly; edit this repository. After editing, validate generated files with each target's available parser or the narrowest safe check, then report mappings, changed files, commands, results, and any target features that cannot be represented.

Arguments: $ARGUMENTS

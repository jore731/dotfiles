# Dotfiles Agent Instructions

## Scope

This repository is the source of truth for stowed user configuration. Edit files here, not their symlinked destinations under `$HOME`.

## Stow

Root dot-directories are linked into `$HOME` with:

```sh
stow --no-folding --target="$HOME" . --ignore='^\.copilot/settings\.json$'
```

The live `~/.copilot/settings.json` is not currently stowed, so preserve it until its source-of-truth migration is complete. After changing stowed configuration, run the command above. Do not replace symlinks or edit generated runtime files directly.

## OpenCode

OpenCode is the source of truth for agents, commands, skills, plugins, and MCP configuration under `.config/opencode/`.

- Use native OpenCode files and schemas; do not maintain parallel authored harness profiles.
- Run `/sync-harness-config` from OpenCode to translate supported configuration for Claude Code, Copilot CLI, and the Copilot app.
- Review the proposed mappings before allowing the command to edit generated target files.
- Restart OpenCode after changing config, agents, commands, skills, plugins, or MCP settings.

## Safety

- Preserve existing permission and approval gates.
- Do not add credentials to this repository.
- Do not edit `Brewfile` manually; regenerate it with `brew bundle dump --file=Brewfile --force`.
- Do not add global packages to `devbox-global`; use Homebrew for global packages.

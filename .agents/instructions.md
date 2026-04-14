# Global Agent Instructions

## About Me

Platform engineer working with Kubernetes, Azure, and DevOps tooling. I work across personal projects and BASF corporate environments.

## Stack

- **Cloud**: Azure (AKS, Container Apps, Key Vault, PostgreSQL, Storage)
- **Infrastructure**: Pulumi (Python), Terraform/OpenTofu, Bicep
- **Containers**: Kubernetes, Helm, Istio, ArgoCD, Docker/Podman, Colima
- **Languages**: Python (primary), shell scripting, Go
- **Python tooling**: uv for project management, Ruff for linting
- **Package management**: Devbox (Nix-based) for CLI tools, Homebrew for GUI apps
- **Editor**: VS Code with Copilot, GitLens, Docker/Kubernetes extensions
- **Terminal**: Alacritty, Zsh with Oh My Zsh, Starship prompt
- **Git**: Multiple identities via conditional includes, 1Password SSH agent
- **Monitoring**: k9s, Grafana, Application Insights

## Conventions

- **Agent configuration goes in `.agents/`** — use `.agents/` for instructions, skills, and agent config in any repo. Do not use `.copilot/`, `.claude/`, or other tool-specific directories. The `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` env var points Copilot CLI to `~/.agents/`.
- **Always use `devbox run`** to execute commands in projects that have a `devbox.json`. Use the pattern `devbox run "cd target_directory && command"` because devbox opens in the project root.
- **Python projects**: Initialize with `devbox init`, `devbox add uv`, then `uv init` — prompt me for project name, type (app/lib), and options step by step.
- **Keep setup minimal**: Don't add VS Code extension recommendations, extra configs, or boilerplate unless I ask for it. Start with the bare minimum.
- **Shell scripts**: Use `#!/bin/sh` and stay POSIX-compatible where possible.
- **Brewfile is auto-generated**: Never edit it by hand. Use `brew bundle dump --file=Brewfile --force`.

## Second Brain (Obsidian)

- I maintain a personal knowledge base in an Obsidian vault at `~/secondbrain` (git-synced to `jore731/secondbrain`).
- When documenting learnings, meeting notes, research, troubleshooting runbooks, or architecture decisions, write them as notes in the vault using the `obsidian` skill.
- **Obsidian is not the only documentation target** — keep project READMEs in their repos, code-level docs as inline comments/docstrings, and API docs in their standard formats. Use the vault for personal/cross-project knowledge.

## Preferences

- I prefer concise output — don't over-explain routine operations.
- Ask me before making design decisions that significantly affect implementation approach.
- When debugging infrastructure issues, isolate and validate base resources first before tackling dependent resources.
- When using the Figma MCP server, if nothing is selected, abort immediately and ask me to select something in Figma.

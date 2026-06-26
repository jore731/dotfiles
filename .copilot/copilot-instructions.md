# Global Agent Instructions

## About Me

Platform engineer working with Kubernetes, Azure, and DevOps tooling. I work across personal projects and BASF corporate environments.

## Stack

- **Cloud**: Azure (AKS, Container Apps, Key Vault, PostgreSQL, Storage)
- **Infrastructure**: Terraform/OpenTofu, Bicep
- **Containers**: Kubernetes, Helm, Istio, ArgoCD, Docker/Podman, Colima
- **Languages**: Python (primary), shell scripting, Go
- **Python tooling**: uv for project management, Ruff for linting
- **Package management**: Homebrew is the default for all global packages (CLI tools + GUI apps); Devbox (Nix-based) is reserved for project-scoped overrides — pinning a specific version or installing a tool I deliberately don't want globally. npm/uv handle language-specific global packages.

## Global Package Management

Dotfiles are managed at `~/dotfiles` (`jore731/dotfiles`). Global language-specific packages are stowed from there.

**Strategy:** Homebrew is the global baseline for everything I want available system-wide (CLI tools *and* GUI apps). Devbox is **only** for project-scoped overrides — pinning a different version than the global one, or installing a tool I deliberately don't want globally. The existing `devbox-global` set is legacy/frozen: don't add new globals there.

- **Homebrew (all globals — CLI tools, GUI apps, fonts)**: `brew install <formula>` (CLI) or `brew install --cask <app>` (GUI), then `brew bundle dump --file=~/dotfiles/Brewfile --force` and commit. This is the default for anything that should be globally available.
- **Devbox (project-scoped overrides only)**: Add a project-local `devbox.json` to pin a specific version or install a tool I don't want globally. Do **not** add new packages to `~/dotfiles/devbox-global/devbox.json` — that global set is frozen and kept only for tools not yet migrated to Homebrew.
- **Node packages**: Run `cd ~/.node-global && pnpm add <package>`. Commit updated `package.json` and `pnpm-lock.yaml` in `~/dotfiles/node-global/`.
- **Python packages**: Run `cd ~/.python-global && uv add <package>`. Commit updated `pyproject.toml` and `uv.lock` in `~/dotfiles/python-global/`.
- **Oh My Zsh**: not a package-manager install — set up via the official curl script (`tools/install.sh --unattended`) into `~/.oh-my-zsh`, plus the custom plugins (`zsh-syntax-highlighting`, `zsh-autosuggestions`, `zsh-completions`) git-cloned into `$ZSH_CUSTOM/plugins`. See the dotfiles README Quick Start.
- **Editor**: VS Code with Copilot, GitLens, Docker/Kubernetes extensions
- **Terminal**: Ghostty, Zsh with Oh My Zsh, Starship prompt
- **Git**: Multiple identities via conditional includes, 1Password SSH agent
- **Monitoring**: k9s, Grafana, Application Insights

## Conventions

- **Agent configuration goes in `.github/`** — use `.github/copilot-instructions.md` for repo-level custom instructions, `.github/skills/` for skills, and `.copilot/` only for MCP servers. Do not scatter agent config across `.claude/`, `.codex/`, or other tool-specific directories.
- **Always use `devbox run`** to execute commands in projects that have a `devbox.json`. Use the pattern `devbox run "cd target_directory && command"` because devbox opens in the project root.
- **Python projects**: Initialize with `devbox init`, `devbox add uv`, then `uv init` — prompt me for project name, type (app/lib), and options step by step.
- **Keep setup minimal**: Don't add VS Code extension recommendations, extra configs, or boilerplate unless I ask for it. Start with the bare minimum.
- **Shell scripts**: Use `#!/bin/sh` and stay POSIX-compatible where possible.
- **Brewfile is auto-generated**: Never edit it by hand. Use `brew bundle dump --file=Brewfile --force`.

## Second Brain (Obsidian)

- I maintain a personal knowledge base in an Obsidian vault at `~/secondbrain` (git-synced to `jore731/secondbrain`).
- **Wiki layer** lives at `~/secondbrain/wiki/` — LLM-maintained compiled knowledge. Always read `wiki/index.md` first. Use the `wiki` skill for ingest/query/lint operations.
- **Raw sources** in `_raw/` are immutable — read but never modify after creation.
- **Tag taxonomy:** `concept/X`, `entity/tool/X`, `entity/org/X`, `entity/person/X`, `project/X`, `source/TYPE`, `daily`. No flat tags.
- **Profile** at `_profile.md` has managed sections (identity, tooling, goals, vetoes) — only edit inside `<!-- managed:TYPE:start/end -->` delimiters.
- When documenting learnings, meeting notes, research, troubleshooting runbooks, or architecture decisions, write them as notes in the vault using the `wiki` or `obsidian` skill.
- **Obsidian is not the only documentation target** — keep project READMEs in their repos, code-level docs as inline comments/docstrings, and API docs in their standard formats. Use the vault for personal/cross-project knowledge.
- **Research reports** — after completing a deep research task, move the final report from the session state directory to `~/secondbrain/research/` so it is persisted in the vault. Use a descriptive kebab-case filename (e.g., `llm-wiki-pattern-karpathy.md`).

## GitHub Identity

- For any GitHub interaction with `jore731/*` or `1010izer/skinalyse*` repos, always use the `jore731` account (`gh auth switch --user jore731`).
- For any GitHub interaction with `basf-global/*` or `PulidoJ_basf/*` repos, always use the `PulidoJ_basf` account (`gh auth switch --user PulidoJ_basf`).
- When in doubt, check repo ownership to pick the right account.

## Preferences

- I prefer concise output — don't over-explain routine operations.
- Ask me before making design decisions that significantly affect implementation approach.
- When debugging infrastructure issues, isolate and validate base resources first before tackling dependent resources.
- When using the Figma MCP server, if nothing is selected, abort immediately and ask me to select something in Figma.

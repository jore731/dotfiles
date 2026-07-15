# Dotfiles

Reproducible development machine provisioning — designed to be run by an AI agent on a fresh macOS or Linux box.

[![Master Your New Laptop Setup: Tools, Configs, and Secrets!](https://img.youtube.com/vi/FH083GOJoIM/0.jpg)](https://youtu.be/FH083GOJoIM)

## How It Works

| Tool | Role |
|------|------|
| [Homebrew](https://brew.sh) | Default global package manager — installs CLI tools, GUI apps, fonts, and VS Code extensions |
| [Devbox](https://www.jetify.com/devbox) (Nix) | Project-scoped version overrides + a frozen legacy set of global CLI tools; also provides `stow` for setup tasks |
| [GNU Stow](https://www.gnu.org/software/stow/) | Symlinks config files from this repo into their OS-specific target paths |

Setup is driven by [`AGENTS.md`](AGENTS.md) — an AI agent reads those instructions and executes each phase interactively, asking before proceeding.

## What's Managed

**Shell & Terminal** — Zsh (Oh My Zsh), Starship prompt, Ghostty, fastfetch

**Dev Tools** — Git (multi-identity via conditional includes), SSH (1Password agent), Docker, Neovim

**Kubernetes** — kubectl, Helm, k9s, ArgoCD CLI, kubelogin, kubecolor

**Cloud** — Azure CLI, Azure Storage Explorer, Colima

**AI Assistants** — GitHub Copilot, Claude Code, MCP servers (Figma, Azure, K8s, draw.io)

**Apps** — VS Code (56 extensions), Obsidian, Raycast, Figma, Slack, Teams, Chrome, and more

**Second Brain** — Obsidian vault auto-synced via Git, with Copilot skills for agent integration

## Repository Structure

```
dotfiles/
├── .agents/               # Canonical external skills and agent tooling
├── .claude/               # Claude Code configuration and generated agents
├── .config/              # Ghostty, fastfetch, starship, 1Password SSH, OpenCode agents
├── .copilot/              # Copilot instructions, MCP servers, skills, generated agents
├── .docker/              # Docker context and ACR registries
├── .gitconfig            # Git config with conditional includes
├── .gitconfig.d/         # Per-identity git configs (personal / BASF)
├── .kube/                # kubecolor theming
├── .local/hooks/         # Azure login hook, git reset
├── .profile              # POSIX shell profile
├── .ssh/                 # SSH config and public keys (1Password agent)
├── .vscode/              # Workspace-level VS Code settings
├── Brewfile              # Auto-generated — default global packages: CLI tools, GUI apps, fonts, extensions
├── devbox-global/        # Frozen legacy global CLI tools (→ ~/.local/share/devbox/global); new globals go to Homebrew
├── devbox.json           # Project-local: stow only
├── docs/                  # Architecture decisions and operational documentation
├── k9s-config/           # k9s views (→ ~/Library/Application Support/k9s)
├── vscode-user-config/   # VS Code settings & keybindings (→ Code/User)
└── zsh/                  # .zshrc (→ $HOME)
```

Items at the root are symlinked into `$HOME` with GNU Stow. Named packages (e.g. `zsh/`, `k9s-config/`) are stowed to specific target directories.

## Quick Start

> Full step-by-step instructions are in [`AGENTS.md`](AGENTS.md).

```sh
# 1. Clone
git clone git@github.com:jore731/dotfiles.git ~/dotfiles
cd ~/dotfiles

# 2. Install Homebrew, then all global packages (primary package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew bundle

# 3. Install Devbox (used for the frozen global shell scripts and project-scoped overrides)
curl -fsSL https://get.jetify.com/devbox | bash

# 4. Stow the devbox-global config (shell scripts only — package set is now empty)
mkdir -p "$HOME/.local/share/devbox/global/default"
devbox run "stow --target=$HOME/.local/share/devbox/global/default devbox-global"
devbox global install

# 5. Install Oh My Zsh (curl, unattended) + the custom plugins referenced in .zshrc
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
ZSH_CUSTOM="$HOME/.oh-my-zsh/custom"
git clone https://github.com/zsh-users/zsh-syntax-highlighting "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
git clone https://github.com/zsh-users/zsh-autosuggestions   "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-completions        "$ZSH_CUSTOM/plugins/zsh-completions"

# 6. Install GNU Stow and link all dotfiles
brew install stow
stow --no-folding --target="$HOME" . --ignore='^\.copilot/settings\.json$'
```

## Maintenance

```sh
# Re-sync configs after editing files in this repo.
# Preserve the currently unmanaged live Copilot settings file.
stow --no-folding --target="$HOME" . --ignore='^\.copilot/settings\.json$'

# Sync OpenCode configuration to Claude Code, Copilot CLI, and Copilot app
# Run `/sync-harness-config` in OpenCode and review its proposed mappings.

# Add a new global package (default path — Homebrew)
brew install <formula>          # CLI tool
brew install --cask <app>       # GUI app
brew bundle dump --file=Brewfile --force   # snapshot (never edit Brewfile by hand)

# Override a version per-project (Devbox)
# Add a project-local devbox.json pinning the version you need.
# Do NOT add new globals to devbox-global/ — that set is frozen.

# Add a new app config
# Create a directory, mirror the target structure inside it,
# add the directory name to .stow-local-ignore, then stow
```

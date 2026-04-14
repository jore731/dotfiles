# Dotfiles

Reproducible development machine provisioning — designed to be run by an AI agent on a fresh macOS or Linux box.

[![Master Your New Laptop Setup: Tools, Configs, and Secrets!](https://img.youtube.com/vi/FH083GOJoIM/0.jpg)](https://youtu.be/FH083GOJoIM)

## How It Works

| Tool | Role |
|------|------|
| [Devbox](https://www.jetify.com/devbox) (Nix) | Installs ~30 CLI tools globally and provides `stow` for setup tasks |
| [GNU Stow](https://www.gnu.org/software/stow/) | Symlinks config files from this repo into their OS-specific target paths |
| [Homebrew](https://brew.sh) | Installs GUI apps, fonts, and VS Code extensions (macOS) |

Setup is driven by [`AGENTS.md`](AGENTS.md) — an AI agent reads those instructions and executes each phase interactively, asking before proceeding.

## What's Managed

**Shell & Terminal** — Zsh (Oh My Zsh), Starship prompt, Alacritty, fastfetch

**Dev Tools** — Git (multi-identity via conditional includes), SSH (1Password agent), Docker, Neovim

**Kubernetes** — kubectl, Helm, k9s, ArgoCD CLI, kubelogin, kubecolor

**Cloud** — Azure CLI, Azure Storage Explorer, Colima

**AI Assistants** — GitHub Copilot, Claude Code, Codex (Azure OpenAI), MCP servers (Figma, Azure, K8s, draw.io)

**Apps** — VS Code (56 extensions), Obsidian, Raycast, Figma, Slack, Teams, Chrome, and more

**Second Brain** — Obsidian vault auto-synced via Git, with Copilot skills for agent integration

## Repository Structure

```
dotfiles/
├── .config/              # Alacritty, fastfetch, starship, 1Password SSH
├── .copilot/             # Copilot instructions, MCP servers, skills
├── .docker/              # Docker context and ACR registries
├── .gitconfig            # Git config with conditional includes
├── .gitconfig.d/         # Per-identity git configs (personal / BASF)
├── .kube/                # kubecolor theming
├── .local/hooks/         # Azure login hook, git reset
├── .profile              # POSIX shell profile
├── .ssh/                 # SSH config and public keys (1Password agent)
├── .vscode/              # Workspace-level VS Code settings
├── Brewfile              # Auto-generated — GUI apps, fonts, extensions
├── codex-config/         # Codex AI config (→ ~/.codex)
├── devbox-global/        # ~30 global CLI tools (→ ~/.local/share/devbox/global)
├── devbox.json           # Project-local: stow only
├── k9s-config/           # k9s views (→ ~/Library/Application Support/k9s)
├── vscode-user-config/   # VS Code settings & keybindings (→ Code/User)
└── zsh/                  # .zshrc (→ $HOME)
```

Items at the root are symlinked into `$HOME` via `stow .`. Named packages (e.g. `zsh/`, `codex-config/`) are stowed to specific target directories.

## Quick Start

> Full step-by-step instructions are in [`AGENTS.md`](AGENTS.md).

```sh
# 1. Clone
git clone git@github.com:jore731/dotfiles.git ~/dotfiles
cd ~/dotfiles

# 2. Install Devbox
curl -fsSL https://get.jetify.com/devbox | bash

# 3. Install global CLI tools
mkdir -p "$HOME/.local/share/devbox/global/default"
devbox run "stow --target=$HOME/.local/share/devbox/global/default devbox-global"
devbox global install

# 4. Install Homebrew + apps (macOS)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew bundle

# 5. Set up Zsh + Oh My Zsh, then link configs
# (see AGENTS.md Phases 6–8 for full details)

# 6. Link all dotfiles
devbox run "stow ."
```

## Maintenance

```sh
# Re-sync configs after editing files in this repo
devbox run "stow ."

# Add a new CLI tool
# Edit devbox-global/devbox.json, then:
devbox global install

# Snapshot current Homebrew state (never edit Brewfile by hand)
brew bundle dump --file=Brewfile --force

# Add a new app config
# Create a directory, mirror the target structure inside it,
# add the directory name to .stow-local-ignore, then stow
```
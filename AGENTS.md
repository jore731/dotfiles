# Agent Instructions — Dotfiles Setup

This repository contains dotfiles and configuration for provisioning a development machine. It uses two core tools:

- **Devbox** (Nix-based): Manages CLI tool installations. The project-local `devbox.json` provides `stow` for setup tasks. The global set at `devbox-global/devbox.json` provides ~30 CLI tools used across all projects (starship, fzf, kubectl, claude-code, neovim, etc.).
- **GNU Stow**: Symlinks configuration directories from this repo to their OS-specific target paths. Each top-level directory is a stow "package" that mirrors the target directory structure internally. Stow is available via `devbox run "stow ..."`.

## Stow Target Mappings

| Package | macOS target | Linux target |
|---|---|---|
| `zsh/` | `$HOME` | `$HOME` |
| `vscode-user-config/` | `~/Library/Application Support/Code/User` | `~/.config/Code/User` |
| `k9s-config/` | `~/Library/Application Support/k9s` | `~/.config/k9s` |
| `devbox-global/` | `~/.local/share/devbox/global/default` | `~/.local/share/devbox/global/default` |
| `npm-global/` | `~/.npm-global` | `~/.npm-global` |
| Root (`stow .`) | `$HOME` | `$HOME` |

Within `.copilot/skills/`, the Obsidian skills from `kepano/obsidian-skills` are stowed from the submodule at `.copilot/thirdparty/obsidian-skills`.

Root stow links the following into `$HOME` (individual files are symlinked, not directories):
- `.copilot/` — copilot-instructions.md, mcp-config.json, skills/
- `.config/` — alacritty, fastfetch, starship, 1Password SSH agent
- `.docker/config.json` — Docker context and ACR registries
- `.gitconfig`, `.gitconfig.d/` — Git configuration with conditional includes
- `.kube/color.yaml` — kubecolor theming
- `.local/hooks/` — azure-login-hook, git-reset
- `.profile` — POSIX shell profile
- `.ssh/` — SSH config and public keys
- `.vscode/` — project-specific VS Code settings (terminal profile)

The `.stow-local-ignore` file controls which top-level items are excluded from root stow.

## Full Machine Setup

Execute these phases in order. Ask the user before each phase whether to proceed. Skip platform-irrelevant steps.

### Phase 1 — Platform Detection

Detect the operating system:

```sh
uname  # "Darwin" = macOS, "Linux" = Linux
# For WSL detection:
test -f /proc/sys/fs/binfmt_misc/WSLInterop  # exists = WSL
```

Windows (Cygwin/MSYS) is not supported for Devbox. Abort setup if detected.

### Phase 2 — Devbox Bootstrap

Install Devbox if `devbox` is not on PATH:

```sh
curl -fsSL https://get.jetify.com/devbox | bash
```

### Phase 3 — Devbox Global Setup

This installs all global CLI tools (~30 packages including starship, eza, fzf, zoxide, kubectl, helm, claude-code, neovim, etc.). The project-local `devbox.json` only contains `stow` — everything else comes from global.

```sh
# Create the global config directory if it doesn't exist
mkdir -p "$HOME/.local/share/devbox/global/default"

# Link the global devbox config from this repo
devbox run "stow --target=$HOME/.local/share/devbox/global/default devbox-global"

# Install all global packages
devbox global install
```

After this phase, all tools defined in `devbox-global/devbox.json` are available in the shell (once `eval "$(devbox global shellenv)"` is sourced, which `.zshrc` handles).

### Phase 3b — npm Global Packages

Some CLI tools (like `defuddle`) are distributed via npm and not available in Nix. These are managed via a stowed `package.json` at `~/.npm-global/`.

```sh
mkdir -p "$HOME/.npm-global"
devbox run "stow --target=$HOME/.npm-global npm-global"
cd "$HOME/.npm-global" && npm install
```

After this, binaries are available at `~/.npm-global/node_modules/.bin/` (added to PATH by `.zshrc`).

### Phase 4 — macOS-Specific Setup

Skip this phase entirely on Linux/WSL.

**Enable Rosetta 2** (Apple Silicon only):

```sh
softwareupdate --install-rosetta --agree-to-license
```

**Enable Touch ID for sudo**:

```sh
# Only if /etc/pam.d/sudo_local doesn't already exist
echo "auth       sufficient     pam_tid.so" | sudo tee /etc/pam.d/sudo_local
```

### Phase 5 — Homebrew Setup

Install Homebrew if `brew` is not on PATH:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Install all packages from the Brewfile:

```sh
brew bundle
```

This installs CLI tools available only via Homebrew (kubecolor, bat, git-lfs), GUI apps (Alacritty, VS Code, Obsidian, Podman Desktop, Raycast, etc.), and VS Code extensions.

### Phase 6 — Zsh Setup

**Add Homebrew zsh to valid shells** (if not already present):

```sh
# Check
grep -q "$(brew --prefix)/bin/zsh" /etc/shells

# Add if missing
echo "$(brew --prefix)/bin/zsh" | sudo tee -a /etc/shells
```

**Set zsh as default shell**:

```sh
chsh -s "$(brew --prefix)/bin/zsh"
```

**Install Oh My Zsh** (if `~/.oh-my-zsh` doesn't exist):

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
```

**Install Oh My Zsh plugins**:

```sh
git clone https://github.com/zsh-users/zsh-completions "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-completions"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"
git clone https://github.com/zsh-users/zsh-autosuggestions "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions"
```

**Link zsh config**:

```sh
rm -f ~/.zshrc
devbox run "stow --target=$HOME zsh"
```

### Phase 7 — App Config Linking

For each app, create the target directory if it doesn't exist, then stow. All stow commands use `devbox run`.

**VS Code** (skip on WSL — configure from the Windows side instead):

```sh
# macOS
devbox run "stow --target='$HOME/Library/Application Support/Code/User' vscode-user-config"

# Linux
devbox run "stow --target=$HOME/.config/Code/User vscode-user-config"
```

**k9s**:

```sh
# macOS
devbox run "stow --target='$HOME/Library/Application Support/k9s' k9s-config"

# Linux
devbox run "stow --target=$HOME/.config/k9s k9s-config"
```

### Phase 7b — Obsidian Second Brain Setup

**Clone the vault** (if `~/secondbrain` doesn't exist):

```sh
git clone git@github.com:jore731/secondbrain.git ~/secondbrain
```

**Stow the Obsidian skills** from the submodule into `.copilot/skills/`:

```sh
git submodule update --init
devbox run "stow --dir=.copilot/thirdparty/obsidian-skills --target=.copilot/skills skills"
```

The Obsidian Git plugin config is committed in the vault at `.obsidian/plugins/obsidian-git/data.json` (auto-save/push/pull every 5 minutes, rebase sync). On first launch, open the vault in Obsidian and install the "Obsidian Git" community plugin — the settings will be picked up automatically.

### Phase 8 — Root Stow

Link all remaining dotfiles (`.config/`, `.gitconfig`, `.ssh/`, `.docker/`, `.copilot/`, etc.) into `$HOME`:

```sh
devbox run "stow ."
```

### Phase 9 — Post-Setup

Remind the user to start a new shell or run:

```sh
source ~/.zshrc
```

## Maintenance Tasks

**Re-sync configs after editing files in this repo**:

```sh
devbox run "stow ."
```

For app-specific configs, re-run the stow command with the appropriate `--target`.

**Dump current Homebrew state to Brewfile**:

```sh
brew bundle dump --file=Brewfile --force
```

Then commit the updated Brewfile. Never edit `Brewfile` by hand — it's auto-generated.

**Add a new CLI tool**: Add the package to `devbox-global/devbox.json`, then run `devbox global install`.

**Add a new npm global tool**: Add the package to `npm-global/package.json`, then run `cd ~/.npm-global && npm install`. Commit the updated `package.json` and `package-lock.json`.

**Add a new app config**: Create a new top-level directory in this repo, place config files inside mirroring the target directory structure, add the directory name to `.stow-local-ignore`, then stow with the appropriate `--target`.

**Update Obsidian skills**: Pull the latest from the submodule, then re-stow:

```sh
cd .copilot/thirdparty/obsidian-skills && git pull origin main && cd ../../..
devbox run "stow --dir=.copilot/thirdparty/obsidian-skills --target=.copilot/skills skills"
```

## Important Notes

- **Agent config convention**: All agent configuration (instructions, skills, MCP servers) lives in `.copilot/` as required by Copilot CLI. Root stow links `.copilot/` contents into `~/.copilot/` alongside Copilot's runtime files.
- **Git config** uses conditional includes: `.gitconfig.d/personal.gitconfig` is the default; `.gitconfig.d/basf.gitconfig` activates for remotes matching `github.com:basf-global` or `gitlab.roqs.basf.net`. Credentials use `gh auth git-credential`.
- **SSH** uses the 1Password SSH agent (`~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock`). Keys are referenced by public key files in `.ssh/`.
- **Alacritty themes** are a git submodule at `.config/alacritty/themes`. Run `git submodule update --init` if themes are missing.
- **Starship prompt** config is at `.config/starship.toml` — it's stowed via root stow, not a separate package.
- **Shell**: `.zshrc` (in `zsh/` stow package) uses Oh My Zsh with plugins: git, history-substring-search, macos, zsh-syntax-highlighting, zsh-autosuggestions, zsh-completions.
- **MCP servers** are configured in `.copilot/mcp-config.json` (stowed to `~/.copilot/mcp-config.json`). Includes figma, azure, kubernetes, drawio, and proxmox servers.
- **Docker** config at `.docker/config.json` stores ACR registry names and context settings. Credentials are in macOS Keychain via `credsStore: osxkeychain` — no secrets in the file.
- **Obsidian second brain**: The vault at `~/secondbrain` is a private git repo (`jore731/secondbrain`). The Obsidian Git plugin handles auto-sync. Obsidian skills from `kepano/obsidian-skills` are stowed as a submodule at `.copilot/thirdparty/obsidian-skills`. A custom `obsidian` skill at `.copilot/skills/obsidian/SKILL.md` guides agents on vault structure and when to use it.
- **Devbox project vs global**: The project `devbox.json` only contains `stow` (for setup tasks). All other CLI tools come from `devbox-global/devbox.json` which is stowed to the global devbox path.

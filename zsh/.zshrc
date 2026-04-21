# Oh My Zsh setup
export ZSH="$HOME/.oh-my-zsh"
skip_global_compinit=1
plugins=(git history-substring-search macos zsh-syntax-highlighting zsh-autosuggestions zsh-completions)

# Completions — fpath must be set before compinit
fpath=("$HOME/.zsh/completions" "$HOME/.local/share/devbox/global/default/.devbox/nix/profile/default/share/zsh/site-functions" $fpath)

# Cache compinit — only regenerate dump once per day
autoload -Uz compinit
if [[ -n "$HOME/.zcompdump(#qN.mh+24)" ]]; then
  compinit
else
  compinit -C
fi

# Cache devbox completions to file instead of subshell every startup
_devbox_comp_cache="$HOME/.zsh/completions/_devbox_cached"
if [[ ! -f "$_devbox_comp_cache" || "$_devbox_comp_cache" -ot "$(command -v devbox)" ]]; then
  devbox completion zsh > "$_devbox_comp_cache" 2>/dev/null
fi
source "$_devbox_comp_cache"

setopt HIST_IGNORE_ALL_DUPS

# 1Password SSH Agent
export SSH_AUTH_SOCK="$HOME/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"

# SSL Setup
export SSL_CERT_DIR="/etc/ssl/certs"
export SSL_CERT_FILE="$SSL_CERT_DIR/BASF_internal_and_public_ca_bundle.crt"
export NIX_SSL_CERT_FILE=$SSL_CERT_FILE

# Devbox
DEVBOX_NO_PROMPT=true
eval "$(devbox global shellenv --init-hook)"

LANG=en_US.UTF-8

# Shell integrations
eval "$(starship init zsh)"
eval "$(zoxide init --cmd cd zsh)"

# The Fuck — lazy-load to avoid slow init on every shell
fuck() {
  unset -f fuck
  eval $(thefuck --alias)
  fuck "$@"
}

# Source Oh My Zsh (after compinit and integrations)
source $ZSH/oh-my-zsh.sh

# kubecolor
compdef kubecolor=kubectl

# Aliases (after Oh My Zsh to override its defaults)
alias ls='eza --long --all --no-permissions --no-filesize --no-user --no-time --git'
alias lst='eza --long --all --no-permissions --no-filesize --no-user --git --sort modified'
alias fzfp='fzf --preview "bat --number --color always {}"'
alias cat='bat --paging never --theme DarkNeon --style plain'
alias kubectl='kubecolor'
alias k='kubectl'
alias kls="k config get-contexts"
alias kns="k config set-context --current --namespace $1"
alias kuse="k config use-context $1"
alias de="devbox"
alias amd64="env /usr/bin/arch -x86_64 /bin/zsh --login"
alias tm='task-master'
alias taskmaster='task-master'

# PATH
export PATH="$HOME/.npm-global/node_modules/.bin:$PATH"
export PATH="$HOME/go/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.local/hooks:$PATH"
export PATH="$HOME/.python-global/.venv/bin:$PATH"

export EDITOR="nano"

# Docker wrapper — injects BASF CA certs on build
docker-ca() {
    if [[ $1 == "build" ]]; then
        command docker "$@" --secret id=ca-certificates,src=$SSL_CERT_FILE
    else
        command docker "$@"
    fi
}

# Defer GITHUB_TOKEN — evaluated on first use
github_token() {
  if [[ -z "$GITHUB_TOKEN" ]]; then
    export GITHUB_TOKEN=$(gh auth token --user PulidoJ_basf)
  fi
  echo "$GITHUB_TOKEN"
}

restart_gp() {
    launchctl unload /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*
    sleep 5
    launchctl load /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*
}

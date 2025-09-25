# Completions
fpath=("$PWD/.devbox/virtenv/zsh" "$HOME/.local/share/devbox/global/default/.devbox/nix/profile/default/share/zsh/site-functions" $fpath)

autoload -Uz compinit
compinit

source <(devbox completion zsh)

# Ignore duplicates in history
setopt HIST_IGNORE_ALL_DUPS

# Setup 1password SSH Agent
export SSH_AUTH_SOCK="$HOME/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"

# SSL Setup
export SSL_CERT_DIR="/etc/ssl/certs"
export SSL_CERT_FILE="$SSL_CERT_DIR/BASF_internal_and_public_ca_bundle.crt"
export NIX_SSL_CERT_FILE=$SSL_CERT_FILE

# Devbox
DEVBOX_NO_PROMPT=true
eval "$(devbox global shellenv --init-hook)"

# Git
LANG=en_US.UTF-8

# Starship
eval "$(starship init zsh)"

# The Fuck
eval $(thefuck --alias)

# Zoxide
eval "$(zoxide init --cmd cd zsh)"

# kubecolor
compdef kubecolor=kubectl


# Aliases
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

export PATH="$HOME/go/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.local/hooks:$PATH"
export PATH="$VENV_DIR/bin:$PATH"

export EDITOR="nano"

# Docker wrapper
docker() {
    if [[ $1 == "build" ]]; then
        command docker "$@" --secret id=ca-certificates,src=$SSL_CERT_FILE
    else
        command docker "$@"
    fi
}


export GITHUB_TOKEN=$(gh auth token)

restart_gp() {
    launchctl unload /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*
    sleep 5
    launchctl load /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*
}
autoload -Uz compinit
compinit

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

# Completions
source <(devbox completion zsh)
source <(docker completion zsh)
source <(kubectl completion zsh)
source <(op completion zsh)

# Starship
eval "$(starship init zsh)"

# The Fuck
eval $(thefuck --alias)

# Zoxide
eval "$(zoxide init --cmd cd zsh)"

# kubecolor
compdef kubecolor=kubectl

### Added by Zinit's installer
if [[ ! -f $HOME/.local/share/zinit/zinit.git/zinit.zsh ]]; then
    print -P "%F{33} %F{220}Installing %F{33}ZDHARMA-CONTINUUM%F{220} Initiative Plugin Manager (%F{33}zdharma-continuum/zinit%F{220})…%f"
    command mkdir -p "$HOME/.local/share/zinit" && command chmod g-rwX "$HOME/.local/share/zinit"
    command git clone https://github.com/zdharma-continuum/zinit "$HOME/.local/share/zinit/zinit.git" && \
        print -P "%F{33} %F{34}Installation successful.%f%b" || \
        print -P "%F{160} The clone has failed.%f%b"
fi

source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# Load a few important annexes, without Turbo
# (this is currently required for annexes)
zinit light-mode for \
    zdharma-continuum/zinit-annex-as-monitor \
    zdharma-continuum/zinit-annex-bin-gem-node \
    zdharma-continuum/zinit-annex-patch-dl \
    zdharma-continuum/zinit-annex-rust

### End of Zinit's installer chunk

# Zsh plugins
zinit light zsh-users/zsh-autosuggestions
zinit light zsh-users/zsh-history-substring-search
zinit light zsh-users/zsh-syntax-highlighting
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
zstyle ':completion:*' menu yes select

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
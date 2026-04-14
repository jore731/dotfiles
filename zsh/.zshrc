# Completions
fpath=("$HOME/.zsh/completions" "$HOME/.local/share/devbox/global/default/.devbox/nix/profile/default/share/zsh/site-functions" $fpath)

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

# Agent config (Copilot CLI reads instructions from this dir)
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="$HOME/.agents"

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
docker-ca() {
    if [[ $1 == "build" ]]; then
        command docker "$@" --secret id=ca-certificates,src=$SSL_CERT_FILE
    else
        command docker "$@"
    fi
}


export GITHUB_TOKEN=$(gh auth token --user PulidoJ_basf)

restart_gp() {
    launchctl unload /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*
    sleep 5
    launchctl load /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*
}

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

plugins=(git history-substring-search macos zsh-syntax-highlighting zsh-autosuggestions zsh-completions)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='nvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# Set personal aliases, overriding those provided by Oh My Zsh libs,
# plugins, and themes. Aliases can be placed here, though Oh My Zsh
# users are encouraged to define aliases within a top-level file in
# the $ZSH_CUSTOM folder, with .zsh extension. Examples:
# - $ZSH_CUSTOM/aliases.zsh
# - $ZSH_CUSTOM/macos.zsh
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# fastfetch
# Task Master aliases added on 4/9/2026
alias tm='task-master'
alias taskmaster='task-master'

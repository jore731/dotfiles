#! /bin/sh
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh

title "Homebrew Setup"

# Homebrew installation
if ! command -v brew &> /dev/null; then
    confirm "Homebrew is not installed. Would you like to install it?" && {
        info "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        eval "$(/opt/homebrew/bin/brew shellenv)"
        log "Homebrew installed successfully."
    } || {
        info "Homebrew installation skipped."
    }
else
    info "Homebrew is already installed."
fi

# Homebrew packages installation
if subtask "Installing Homebrew packages..." "brew bundle"; then
    log "Homebrew packages installed successfully."
else
    log "Homebrew packages installation failed."
    exit 1
fi

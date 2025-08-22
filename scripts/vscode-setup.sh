#! /bin/bash
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh
source $(dirname $0)/../functions/utils.sh # Relative path to utils.sh

if is_macos; then
    vscode_path="$HOME/Library/Application Support/Code/User"
elif is_windows; then
    vscode_path="$HOME/AppData/Roaming/Code/User"
elif is_linux; then
    vscode_path="$HOME/.config/Code/User"
fi

title "VSCode Setup"
# Ensure vscode is installed
if ! command -v code &> /dev/null; then
    error "VSCode is not installed."
    exit 1
fi

# Install vscode extensions
confirm "Would you like to install VSCode extensions from vscode-extensions file?" && {
    info "Installing VSCode extensions from vscode-extensions file..."
    if subtask "Installing VSCode extensions..." "$(dirname $0)/../scripts/vscode_install_extensions.sh"; then
        log "VSCode extensions installed successfully."
    else
        log "VSCode extensions installation failed."
        exit 1
    fi
} || {
    info "VSCode extensions installation skipped."
}

if is_wsl; then
    banner "VSCode WSL Configuration is not recommended. Please delegate VSCode configuration to the windows native VSCode application. Run this script again from the Windows environment."
    exit 0
elif is_windows; then
    banner "Windows VSCode Setup is not yet ready."
else
    # Ensure vscode user config directory exists
    if [ ! -d "$vscode_path" ]; then
        confirm "VSCode user config directory does not exist. Would you like to create it?" && {
            info "Creating VSCode user config directory..."
            mkdir -p "$vscode_path"
            log "VSCode user config directory created successfully."
        } || {
            info "VSCode user config directory creation skipped."
        }
    else
        info "VSCode user config directory already exists."
    fi

    confirm "Would you like to link VSCode settings?" && {
        info "Linking VSCode settings..."
        stow --target="$vscode_path" vscode-user-config
    }
fi
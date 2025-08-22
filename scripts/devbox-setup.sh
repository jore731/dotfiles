#! /bin/bash
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh
source $(dirname $0)/../functions/utils.sh # Relative path to utils.sh

title "Devbox Setup"

global_devbox_path="$HOME/.local/share/devbox/global/default"

if is_windows; then
    banner "Windows does not support devbox. Skipping..."
else
    # Ensure devbox global directory exists
    if [ ! -d "$global_devbox_path" ]; then
        confirm "Devbox global directory does not exist. Would you like to create it?" && {
            info "Creating Devbox global directory..."
            mkdir -p "$global_devbox_path"
            log "Devbox global directory created successfully."
        } || {
            info "Devbox global directory creation skipped."
        }
    else
        info "Devbox global directory already exists."
    fi

    confirm "Would you like to link Devbox global settings?" && {
        info "Linking Devbox global settings..."
        stow --target="$global_devbox_path" devbox-global
    }
fi


# Devbox global environment installation
if subtask "Installing Devbox global environment..." "devbox global install"; then
    log "Devbox global environment installed successfully."
else
    log "Devbox global environment installation failed."
    exit 1
fi

#! /bin/sh
source $(dirname $0)/../functions/utils.sh # Relative path to utils.sh

echo "Devbox Setup"

global_devbox_path="$HOME/.local/share/devbox/global/default"
# Devbox installation
if ! command -v devbox &> /dev/null; then
    confirm "Devbox is not installed. Would you like to install it?" && {
        echo "Installing Devbox..."
        /bin/bash -c "$(curl -fsSL https://get.jetify.com/devbox)"
        echo "Devbox installed successfully."
    } || {
        echo "Devbox installation skipped."
    }
else
    echo "Devbox is already installed."
fi

if is_windows; then
    echo "Windows does not support devbox. Skipping..."
else
    # Ensure devbox global directory exists
    if [ ! -d "$global_devbox_path" ]; then
        confirm "Devbox global directory does not exist. Would you like to create it?" && {
            echo "Creating Devbox global directory..."
            mkdir -p "$global_devbox_path"
            echo "Devbox global directory created successfully."
        } || {
            echo "Devbox global directory creation skipped."
        }
    else
        echo "Devbox global directory already exists."
    fi

    confirm "Would you like to link Devbox global settings?" && {
        echo "Linking Devbox global settings..."
        stow --target="$global_devbox_path" devbox-global
    }
fi


# Devbox global environment installation
if subtask "Installing Devbox global environment..." "devbox global install"; then
    echo "Devbox global environment installed successfully."
else
    echo "Devbox global environment installation failed."
    exit 1
fi

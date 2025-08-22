#! /bin/sh
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh
source $(dirname $0)/../functions/utils.sh # Relative path to utils.sh

if is_windows; then
    banner "Windows does not support devbox. Skipping..."
else
    # Devbox installation
    if ! command -v devbox &> /dev/null; then
        echo "Installing Devbox..."
        /bin/bash -c "$(curl -fsSL https://get.jetify.com/devbox)"
    else
        echo "Devbox is already installed."
    fi
fi
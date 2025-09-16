#! /bin/bash
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh

title "MacOS Setup"

# Use Touch ID for sudo
confirm "Would you like to enable Touch ID for sudo?" && {
    if [ ! -f /etc/pam.d/sudo_local ]; then
        echo "auth       sufficient     pam_tid.so" | sudo tee /etc/pam.d/sudo_local && {
            log "Touch ID for sudo enabled."
        }
    else
        log "Touch ID for sudo is already enabled."
    fi
} || {
    log "Touch ID for sudo not enabled."
}

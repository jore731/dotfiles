#! /bin/sh
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh
source $(dirname $0)/../functions/utils.sh # Relative path to utils.sh

title "K9S Setup"
if is_macos; then
    k9s_path="$HOME/Library/Application Support/k9s"
elif is_windows; then
    k9s_path="$HOME/AppData/Roaming/k9s"
elif is_linux; then
    k9s_path="$HOME/.config/k9s"
fi

# Ensure k9s directory exists
if [ ! -d "$k9s_path" ]; then
    confirm "K9s configuration directory does not exist. Would you like to create it?" && {
        info "Creating K9s configuration directory..."
        mkdir -p "$k9s_path"
        log "K9s configuration directory created successfully."
    } || {
        info "K9s configuration directory creation skipped."
    }
else
    info "K9s configuration directory already exists."
fi


confirm "Would you like to link K9s settings?" && {
    info "Linking K9s settings..."
    stow --target="$k9s_path" k9s-config
    log "K9s settings linked successfully."
} || {
    info "K9s settings linking skipped."
}
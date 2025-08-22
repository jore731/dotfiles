#! /bin/bash
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh

title "Homebrew Config Dump"
confirm "Would you like to dump your Homebrew configuration? This will overwrite any existing Brewfile." && {
    info "Dumping Homebrew configuration..."
    # Dump the Brewfile
    brew bundle dump --file=Brewfile --force
    log "Homebrew configuration dumped successfully to Brewfile."
    confirm "Would you like to commit this change?" && {
        git add Brewfile
        git commit -m "Update Homebrew configuration"
        log "Homebrew configuration committed successfully."
    } || {
        info "Homebrew configuration commit skipped."
    }
} || {
    info "Homebrew configuration dump skipped."
}
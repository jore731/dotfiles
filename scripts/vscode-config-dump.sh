#! /bin/sh
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh

title "VSCode Configuration Dump"
confirm "Would you like to dump your VSCode installed extensions? This will overwrite the existing vscode-extensions file." && {
    info "Dumping VSCode extension list..."
    # Dump the extensions
    code --list-extensions > vscode-extensions
    log "VSCode extension list dumped successfully to vscode-extensions."
    confirm "Would you like to commit this change?" && {
        git add vscode-extensions
        git commit -m "Update VSCode extension list"
        log "VSCode extension list committed successfully."
    } || {
        info "VSCode extension list commit skipped."
    }
} || {
    info "VSCode extension list dump skipped."
}
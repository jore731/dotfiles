#! /bin/sh
source $(dirname $0)/../functions/gum.sh # Relative path to gum.sh

title "Zsh Setup"

# Ensure zsh is a valid shell option
if ! cat /etc/shells | grep $HOMEBREW_PREFIX/bin/zsh > /dev/null; then
  confirm "Zsh is not a valid shell option. Would you like to add it?" && {
      sudo sh -c "echo $HOMEBREW_PREFIX/bin/zsh >> /etc/shells"
      log "Zsh added to /etc/shells"
  } || {
      info "Zsh addition to /etc/shells skipped."
  }
else
  info "Zsh already in /etc/shells"
fi
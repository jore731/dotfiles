#!/bin/sh
SERVICE="dotfiles"
KEYCHAIN="login.keychain"

store() {
  security delete-generic-password -s "$SERVICE" -a "$1" "$KEYCHAIN" 2>/dev/null
  security add-generic-password -s "$SERVICE" -a "$1" -w "$2" "$KEYCHAIN"
  echo "  ✓ $1"
}

echo "Syncing secrets from 1Password to Keychain..."
store ROQS_GITLAB_TOKEN "$(op read 'op://CLI/GitLab ROQS/credential')"
store RGQDS_AZURE_DEVOPS_PAT "$(op read 'op://CLI/Azure DevOps RGQDS/credential')"
store RGQDS_AZURE_DEVOPS_PAT_B64 "$(printf '%s:%s' "$(op read 'op://CLI/Azure DevOps RGQDS/email')" "$(op read 'op://CLI/Azure DevOps RGQDS/credential')" | base64)"

echo "Done. Secrets synced to Keychain."

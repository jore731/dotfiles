#!/bin/sh
# macOS-specific defaults configuration
# Run once after setup or whenever you want to reapply defaults.

if [ "$(uname)" != "Darwin" ]; then
  echo "Skipping: not macOS"
  exit 0
fi

echo "Applying macOS defaults..."

# Prevent .DS_Store files on network and USB volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true

echo "Done. Some changes may require a logout/restart to take effect."

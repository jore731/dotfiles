# Enable Rosetta 2 for Apple Silicon
softwareupdate --install-rosetta --agree-to-license

# Enable touch id for terminal sudo commands
sed "s/^#auth/auth/" /etc/pam.d/sudo_local.template | sudo tee /etc/pam.d/sudo_local

# https://github.com/ryanoasis/nerd-fonts?tab=readme-ov-file
brew install font-fira-code-nerd-font font-hack-nerd-font

# https://github.com/zdharma-continuum/zinit?tab=readme-ov-file#install
bash -c "$(curl --fail --show-error --silent --location https://raw.githubusercontent.com/zdharma-continuum/zinit/HEAD/scripts/install.sh)"


# https://www.kcl-lang.io/docs/user_docs/getting-started/install#homebrew-macos-1
brew install kcl-lang/tap/kcl-lsp

# https://www.jetify.com/docs/devbox/installing_devbox/?install-method=macos
curl -fsSL https://get.jetify.com/devbox | bash
# https://github.com/hidetatz/kubecolor
brew install kubecolor

# https://github.com/sharkdp/bat
brew install bat

brew install visual-studio-code

brew install podman-desktop

brew install docker-credential-helper

brew install azure-cli
az extension add --name azure-devops

brew install microsoft-azure-storage-explorer

brew install alacritty

devbox run -- ./sync.sh

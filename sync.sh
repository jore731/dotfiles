rm ~/.zshrc

stow .

gum format

echo '## Execute `source ~/.zshrc`.' | gum format

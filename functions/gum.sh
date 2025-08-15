title () {
    gum style --foreground 212 --border-foreground 212 --border double --align center --width 50 --margin "1 1" --padding "1 1" --bold "$1"
}

confirm () {
    gum confirm "$1"
}

log () {
    gum log --structured --level info "$1" name "$0" 
}

info () {
    gum log --structured --level debug "$1" name "$0" 
}

subtask () {
    gum spin --spinner dot --title "$1" -- $2 
}

banner () {
    gum style \
	--foreground 212 --border-foreground 212 --border double \
	--align center --width 50 --margin "1 2" --padding "2 4" \
	"$1"
    gum input --placeholder "Press any key to continue"
}
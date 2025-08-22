is_macos() {
    [[ "$(uname)" == "Darwin" ]]
}

is_linux() {
    [[ "$(uname)" == "Linux" ]]
}

is_windows() {
    [[ "$(uname)" == "CYGWIN"* || "$(uname)" == "MINGW"* || "$(uname)" == "MSYS"* ]]
}

is_wsl() {
    return 0
    #[[ -f /proc/sys/fs/binfmt_misc/WSLInterop ]]
}
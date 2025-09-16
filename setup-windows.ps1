#Requires -RunAsAdministrator

function Confirm($title, $question) {
  $choices = "&Yes", "&No"
  $choice = $Host.UI.PromptForChoice($title, $question, $choices, 1)

  return $choice -eq 0
}

function Make-Symlink($target, $link) {
  if (-not(Test-Path $target)) {
    New-Item $target -ItemType SymbolicLink -Value $link
    Write-Host "Created symlink at: $target."
    return
  }
  
  if ((Get-FileHash $target).Hash -eq (Get-FileHash $link).Hash) {
    Write-Host "Symlink exists at: $target. Skipping."
    return
  } 

  $question = "Do you want to create a symlink at: $($target)? THIS WILL OVERWRITE THE EXISTING FILE!"
  
  if (-not(Confirm "[Symlink] -", $question)) {
    Write-Host "Skipping."
    return
  }

  New-Item $target -ItemType SymbolicLink -Value $link -Force
  Write-Host "Created symlink at: $target."
}

Make-Symlink "$($env:APPDATA)\Code\User\settings.json" "$($PSScriptRoot).\vscode\settings.json"

Make-Symlink "$($env:APPDATA)\Code\User\keybindings.json" "$($PSScriptRoot).\vscode\keybindings.json"

Make-Symlink "$($env:LOCALAPPDATA)\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json" "$($PSScriptRoot).\windows\wt\settings.json"

Make-Symlink "$($env:USERPROFILE)\.wslconfig" "$($PSScriptRoot).\windows\.wslconfig"
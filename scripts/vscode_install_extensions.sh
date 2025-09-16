#! /bin/bash

xargs -I {} -n 1 code --install-extension {} --force < vscode-extensions
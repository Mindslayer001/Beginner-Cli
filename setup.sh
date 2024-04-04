#!/bin/bash

current_dir=$(pwd)
echo "Installing Dependencies"
pip install -r "$current_dir/requirements.txt" --break-system-packages > /dev/null 2>&1

# Check if .zshrc exists
echo "Trying to add alias for easier access"
if [ -f "$HOME/.zshrc" ]; then
    # If .zshrc exists, add the alias to .zshrc
    echo "alias begcli='python \"$current_dir/beg_cli/argsparser.py\"'" >> "$HOME/.zshrc"
    $(source $HOME/.zshrc)
    echo "Alias added to .zshrc"
else
    # If .zshrc doesn't exist, add the alias to .bashrc
    echo "alias begcli='python \"$current_dir/beg_cli/argsparser.py\"'" >> "$HOME/.bashrc"
    $(source $HOME/.bashrc)
    echo "Alias added to .bashrc"
fi

# Set executable permission for argsparser.py
chmod +x "$current_dir/beg_cli/argsparser.py"

echo "try typing 'begcli -i ls' for starters"

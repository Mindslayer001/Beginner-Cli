#!/bin/bash

# Function to check if the alias is already defined in the shell configuration file
check_alias() {
    local alias_name="$1"
    local file="$2"

    if [ -f "$file" ]; then
        if grep -q "alias $alias_name='" "$file"; then
            return 0  # Alias exists
        fi
    fi
    return 1  # Alias does not exist
}

current_dir=$(pwd)
echo "Installing Dependencies"
pip install -r "$current_dir/requirements.txt" --break-system-packages > /dev/null 2>&1

# Check if .zshrc exists
echo "Trying to add alias for easier access"
if [ -f "$HOME/.zshrc" ]; then
    # If .zshrc exists and alias is not defined, add the alias to .zshrc
    if ! check_alias "begcli" "$HOME/.zshrc"; then
        echo "alias begcli='python \"$current_dir/beg_cli/argsparser.py\"'" >> "$HOME/.zshrc"
        source "$HOME/.zshrc"  # Source .zshrc to apply changes immediately
        echo "Alias added to .zshrc"
    else
        echo "Alias 'begcli' is already defined in .zshrc"
    fi
else
    # If .zshrc doesn't exist and alias is not defined, add the alias to .bashrc
    if ! check_alias "begcli" "$HOME/.bashrc"; then
        echo "alias begcli='python \"$current_dir/beg_cli/argsparser.py\"'" >> "$HOME/.bashrc"
        source "$HOME/.bashrc"  # Source .bashrc to apply changes immediately
        echo "Alias added to .bashrc"
    else
        echo "Alias 'begcli' is already defined in .bashrc"
    fi
fi

# Set executable permission for argsparser.py
chmod +x "$current_dir/beg_cli/argsparser.py"

echo "Try typing 'begcli -i ls' for starters"

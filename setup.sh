#!/bin/bash
# Install dependencies using Poetry
current_dir=$(pwd)
echo "Installing Dependencies"
poetry install

# Check if .zshrc exists
echo "trying to add alias for easier access"
if [ -f "$HOME/.zshrc" ]; then
    # If .zshrc exists, add the alias to .zshrc
    echo "alias beg-cli='poetry run python $current_dir/beg_cli/argsparser.py'" >> "$HOME/.zshrc"
    echo "Alias added to .zshrc"
else
    # If .zshrc doesn't exist, add the alias to .bashrc
    echo "alias beg-cli='poetry run python /path/to/beg_cli/argsparser.py'" >> "$HOME/.bashrc"
    echo "Alias added to .bashrc"
fi

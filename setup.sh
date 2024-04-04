#!/bin/bash
# Install dependencies using Poetry
poetry install

# Check if .zshrc exists
if [ -f "$HOME/.zshrc" ]; then
    # If .zshrc exists, add the alias to .zshrc
    echo "alias mycli='poetry run python /path/to/beg_cli/argsparser.py'" >> "$HOME/.zshrc"
    echo "Alias added to .zshrc"
else
    # If .zshrc doesn't exist, add the alias to .bashrc
    echo "alias mycli='poetry run python /path/to/beg_cli/argsparser.py'" >> "$HOME/.bashrc"
    echo "Alias added to .bashrc"
fi

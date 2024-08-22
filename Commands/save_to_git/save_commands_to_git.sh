#!/bin/bash

# Define directories
COMMANDS_DIR="$HOME/.mcmd_commands"

# Prompt user for the Git repository directory
read -p "Enter the path to the Git repository folder: " REPO_DIR

# Check if the commands directory exists
if [ ! -d "$COMMANDS_DIR" ]; then
    echo "Commands directory ($COMMANDS_DIR) does not exist."
    exit 1
fi

# Check if the Git repository directory exists
if [ ! -d "$REPO_DIR" ]; then
    echo "Git repository directory ($REPO_DIR) does not exist."
    echo "Would you like to initialize a new Git repository here? (y/n): "
    read -r initialize_repo
    if [ "$initialize_repo" = "y" ]; then
        mkdir -p "$REPO_DIR"
        cd "$REPO_DIR" || exit
        git init
        echo "Git repository initialized in $REPO_DIR."
    else
        exit 1
    fi
fi

# Copy commands to the Git repository directory
cp -r "$COMMANDS_DIR"/* "$REPO_DIR/"

# Change to the repository directory
cd "$REPO_DIR" || exit

# Check if there is a remote repository
if git remote -v | grep -q "origin"; then
    # Prompt for commit message
    read -p "Enter a commit message: " COMMIT_MESSAGE
    
    # Add all changes to Git
    git add .

    # Commit changes
    git commit -m "$COMMIT_MESSAGE"

    # Push changes to the remote repository
    git push
else
    echo "No remote repository found. Please add a remote repository and push manually."
fi

echo "Custom commands saved to Git repository."

#!/bin/bash

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Paths
MCMD_PATH="${PWD}/mcmd"
MCMD_DIR="${PWD}"
MCMD_COMMANDS_DIR="$HOME/.mcmd_commands"
BASH_PROFILE="$HOME/.bash_profile"
COMMANDS_SRC_DIR="${PWD}/Commands"
COMMANDS_DST_DIR="$MCMD_COMMANDS_DIR"

# Function to add export command to the shell configuration file
add_to_bash_profile() {
    local path_to_add="$1"
    local export_command="$2"

    if ! grep -q "export $export_command" "$BASH_PROFILE"; then
        echo -e "${RED}Adding '$export_command' to $BASH_PROFILE...${NC}"
        echo "" >> "$BASH_PROFILE"
        echo "export $export_command" >> "$BASH_PROFILE"
        echo -e "${GREEN}'$export_command' added to $BASH_PROFILE.${NC}"
        # Apply the changes
        source "$BASH_PROFILE"
        echo -e "${GREEN}Applied changes to $BASH_PROFILE.${NC}"
    else
        echo -e "${GREEN}'$export_command' is already in $BASH_PROFILE.${NC}"
    fi
}

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo -e "${RED}Homebrew not found. Installing Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo -e "${GREEN}Homebrew is already installed.${NC}"
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 could not be found. Installing using Homebrew...${NC}"
    brew install python
else
    echo -e "${GREEN}Python3 is already installed.${NC}"
fi

# Check if Bash is installed
if ! command -v bash &> /dev/null; then
    echo -e "${RED}Bash could not be found. Installing using Homebrew...${NC}"
    brew install bash
else
    echo -e "${GREEN}Bash is already installed.${NC}"
fi

# Make the mcmd script executable and move it to a globally accessible directory
chmod +x "$MCMD_PATH"
echo -e "${GREEN}Made mcmd script executable.${NC}"

# Ensure the global directory is in PATH
GLOBAL_BIN_DIR="/usr/local/bin"
if ! command -v mcmd &> /dev/null; then
    echo -e "${RED}Moving mcmd script to /usr/local/bin...${NC}"
    sudo cp "$MCMD_PATH" "$GLOBAL_BIN_DIR/mcmd"
    echo -e "${GREEN}mcmd script moved to /usr/local/bin.${NC}"
else
    echo -e "${GREEN}mcmd is already in PATH.${NC}"
fi

# Add the mcmd and commands directory to PATH and MCMD_COMMANDS_DIR in ~/.bash_profile
add_to_bash_profile "$MCMD_DIR" "\"PATH=\$PATH:$MCMD_DIR\""
add_to_bash_profile "$MCMD_COMMANDS_DIR" "MCMD_COMMANDS_DIR=$MCMD_COMMANDS_DIR"

# Move all command directories and scripts to the commands directory
if [ -d "$COMMANDS_SRC_DIR" ]; then
    echo -e "${RED}Moving command directories and scripts to $COMMANDS_DST_DIR...${NC}"
    
    # Ensure the destination directory exists
    mkdir -p "$COMMANDS_DST_DIR"
    
    # Move the source directory and its contents to the destination directory
    cp -rf "$COMMANDS_SRC_DIR"/* "$COMMANDS_DST_DIR"
    
    # Set executable permissions for all .sh files
    find "$COMMANDS_DST_DIR" -type f -name "*.sh" -exec chmod +x {} \;
    
    echo -e "${GREEN}All command directories and scripts moved, and permissions set.${NC}"
else
    echo -e "${RED}Commands source directory does not exist: $COMMANDS_SRC_DIR${NC}"
fi

echo -e "${GREEN}All prerequisites installed and mcmd configured.${NC}"

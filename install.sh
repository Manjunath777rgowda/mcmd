#!/bin/bash
set -e
# -------------------------------------------------------------------------------------------
# This script help to run in the editable mode where you can develop and test at the run time
# -------------------------------------------------------------------------------------------

YELLOW_BG='\033[43;30m' # Yellow background with black text
GREEN='\033[42;30m'  # Green background with black text
RED='\033[41;30m'    # Red background with black text
RESET='\033[0m'  # Reset color

print_log() {
    echo -e "${GREEN}$1${RESET}"
}

print_error() {
    echo -e "${RED}$1${RESET}"
}

print_warn() {
    echo -e "${YELLOW_BG}$1${RESET}"
}

promt() {
    local message="$1"
    echo -e "${YELLOW_BG}${message}${RESET}\c"
}

print_centered() {
    local message=$1
    local symbol=$2
    if [ -z "$symbol" ]; then
        symbol='*'
    fi
    local term_width=$(tput cols)  # Get the width of the terminal
    local message_length=${#message}  # Get the length of the message
    local total_padding=$((term_width - message_length))  # Total padding needed
    local left_padding=$((total_padding / 2))  # Padding on the left side
    local right_padding=$((total_padding - left_padding))  # Padding on the right side

    # Generate the centered message with # padding
    printf "\033[33m%${left_padding}s" | tr ' ' "${symbol}"  # Print left # padding
    printf "%s" "$message"  # Print the message
    printf "%${right_padding}s" | tr ' ' "${symbol}"  # Print right # padding
    printf "\n\033[0m"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Homebrew and install if not exists
if ! command_exists brew; then
    print_warn "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    print_log "Homebrew is already installed."
fi

# Check for Python 3 and install if it doesn't exist
if ! command_exists python3; then
    print_warn "Python 3 is not installed. Installing..."
    brew install python
else
    print_warn "Python 3 is already installed."
fi

# Check for pip3 and install if it doesn't exist
if ! command_exists pip3; then
    print_warn "pip3 is not installed. Installing..."
    python3 -m ensurepip --upgrade
else
    print_warn "pip3 is already installed."
fi

# Uninstall the mcmd package
print_log "Uninstalling mcmd..."
pip3 uninstall mcmd -y

# Remove build artifacts
print_log "Removing build artifacts..."
rm -rf build dist *egg* __pycache__

# Install requirements
print_log "Installing requirements."
pip3 install setuptools typer

print_log "Installing the package..."
pip3 install git+https://github.com/Manjunath777rgowda/mcmd.git

print_centered "Setup completed successfully." "-"

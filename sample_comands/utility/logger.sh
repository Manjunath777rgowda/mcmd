#!/bin/bash

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
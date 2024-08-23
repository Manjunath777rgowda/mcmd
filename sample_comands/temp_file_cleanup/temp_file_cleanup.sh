#!/bin/bash

# Define directories
TEMP_DIR="$HOME/Library/Caches"
LOG_DIR="$HOME/Library/Logs"

# ANSI escape codes for red text
RED='\033[0;31m'
NC='\033[0m' # No Color

# Notify the user about OS compatibility
echo -e "${RED}Note: This script is only supported on macOS.${NC}"

# Remove temporary files
find "$TEMP_DIR" -type f -name "*.tmp" -delete

# Remove old logs
find "$LOG_DIR" -type f -name "*.log" -mtime +30 -delete

# Notify the user
echo "Temporary files and old logs removed."

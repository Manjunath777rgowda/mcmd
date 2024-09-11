#!/bin/bash

source  ~/.mcmd_commands/utility/logger.sh

# Define directories
TEMP_DIR="$HOME/Library/Caches"
LOG_DIR="$HOME/Library/Logs"

# Notify the user about OS compatibility
print_error "Note: This script is only supported on macOS."

# Remove temporary files
find "$TEMP_DIR" -type f -name "*.tmp" -delete

# Remove old logs
find "$LOG_DIR" -type f -name "*.log" -mtime +30 -delete

# Notify the user
print_log "Temporary files and old logs removed."

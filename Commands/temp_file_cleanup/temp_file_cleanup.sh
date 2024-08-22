#!/bin/bash

# Define directories
TEMP_DIR="$HOME/Library/Caches"
LOG_DIR="$HOME/Library/Logs"

# Remove temporary files
find "$TEMP_DIR" -type f -name "*.tmp" -delete

# Remove old logs
find "$LOG_DIR" -type f -name "*.log" -mtime +30 -delete

# Notify the user
echo "Temporary files and old logs removed."

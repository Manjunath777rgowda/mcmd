# mcmd Project

## Overview

`mcmd` is a tool designed to help manage custom commands. It allows users to create, remove, update, list, and execute commands stored in a specific directory. The commands are stored as shell scripts with associated description files.

## Features

- **Create Commands**: Add new commands with custom logic.
- **Remove Commands**: Delete existing commands.
- **Update Commands**: Modify existing commands and their descriptions.
- **List Commands**: View all available commands.
- **Execute Commands**: Run custom commands directly from the terminal.
- **Help**: Display help information for using `mcmd`.

## Setup

To set up the `mcmd` tool, follow these steps:

1. **Download the Setup Script**

   Download the `setup.sh` script using `curl`:

   ```bash
   curl -o setup.sh https://raw.githubusercontent.com/Manjunath777rgowda/mcmd/main/setup.sh
   ```

   Or use `wget`:

   ```bash
   wget -O setup.sh https://raw.githubusercontent.com/Manjunath777rgowda/mcmd/main/setup.sh
   ```

2. **Make the Script Executable**

   Change the permissions of the `setup.sh` script to make it executable:

   ```bash
   chmod +x setup.sh
   ```

3. **Run the Setup Script**

   Execute the `setup.sh` script to configure `mcmd`:

   ```bash
   ./setup.sh
   ```

   This script will install prerequisites, set up environment variables, and configure `mcmd`.

## Commands

- **Create Command**: `mcmd create` - Prompts for command name and logic, creates a new command.
- **Remove Command**: `mcmd remove` - Lists existing commands and removes the selected one.
- **Update Command**: `mcmd update` - Updates the logic and description of an existing command.
- **List Commands**: `mcmd` - Lists all available commands.
- **Execute Command**: `mcmd <command>` - Executes a specified command.
- **Help**: `mcmd help` - Displays help information.

## Directory Structure

- **Commands Directory**: Stores command scripts and their descriptions.
- **HELP**: Contains help documentation.
- **README.md**: This file.
- **mcmd**: The main executable script.
- **setup.sh**: The setup script for installing and configuring `mcmd`.

## Contributing

If you have any improvements or bug fixes, feel free to submit a pull request or open an issue on the GitHub repository.
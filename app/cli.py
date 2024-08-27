#!/usr/bin/env python3

import os
import subprocess
import typer
import shutil
from rich.console import Console
from rich.table import Table
from typing import List, Optional
from app.log_util import Log
import tkinter as tk
from tkinter import filedialog

app = typer.Typer()
console = Console()
log = Log()
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Define the commands directory relative to the current script's location
MCMD_COMMANDS_DIR = os.path.expanduser("~/.mcmd_commands")

def is_valid_command_name(command_name):
    # Simple validation: only allows alphanumeric characters and underscores
    return command_name.isidentifier()

def get_input(message):
    """
    Display a message in blue and read the user's input.

    Args:
        message (str): The prompt message to display.

    Returns:
        str: The user's input.
    """
    blue_color = '\033[94m'
    reset_color = '\033[0m'
    
    # Print the message in blue color and read the input
    user_input = input(f"{blue_color}{message}{reset_color}")
    return user_input

def add_shebang_if_missing(file_path):
    # Check if the file has a .sh extension and add a shebang if missing
    if file_path.endswith('.sh'):
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            if not lines or not lines[0].startswith('#!'):
                file.seek(0, 0)
                file.write('#!/bin/bash\n' + ''.join(lines))
                file.flush()
                log.info(f"Added shebang to '{file_path}'.")

def create_or_update_command():
    command_name = get_input("Enter the command name: mcmd exec ")

    # Validate the command name
    if not is_valid_command_name(command_name):
        log.error("Invalid command name. Command names should only contain alphanumeric characters and underscores.")
        return

    command_description = get_input(f"Enter a description for 'mcmd exec {command_name}': ")

    # Define paths for command logic and description files
    command_dir = os.path.join(MCMD_COMMANDS_DIR, command_name)
    command_file = os.path.join(command_dir, f"{command_name}.sh")
    description_file = os.path.join(command_dir, f"{command_name}.desc")
    
    os.makedirs(command_dir, exist_ok=True)
    
    # Check if the command exists
    if os.path.exists(command_file):
        log.warn(f"Command 'mcmd {command_name}' already exists.")
        while True:
            response = get_input("Do you want to update it? (y/n): ").lower()
            if response == 'y':
                log.info(f"Updating command 'mcmd {command_name}'.")
                accept_command_details("update", command_file, command_name)
                break
            elif response == 'n':
                log.info("Command update canceled.")
                return
            else:
                log.error("Invalid input. Please enter 'y' or 'n'.")
                continue
    else:
        log.error(f"Command 'mcmd {command_name}' does not exist.")
        log.info(f"Creating new command 'mcmd {command_name}'.")
        accept_command_details("create", command_file, command_name)

    try:
        # Save the command description
        with open(description_file, 'w') as file:
            file.write(command_description + "\n")
        
        os.chmod(command_file, 0o755)
    except Exception as e:
        log.error(f"Error creating/updating command: {e}")

def accept_command_details(operation, command_file, command_name):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    while True:
        response = get_input("Do you already have the path for the command logic file? (y/n): ").lower()
        if response == 'y':
            log.info("Please select a .sh file from...")
            existing_file_path = filedialog.askopenfilename(
                title="Select a .sh file",
                filetypes=[("Shell Script Files", "*.sh")]
            )
            if existing_file_path:
                if os.path.exists(existing_file_path):
                    subprocess.run(['cp', existing_file_path, command_file])
                    add_shebang_if_missing(command_file)
                    log.info(f"Command 'mcmd {command_name}' {operation}d with the contents of {existing_file_path}.")
                else:
                    log.error(f"File '{existing_file_path}' does not exist. Command {operation} canceled.")
            else:
                log.error("No file selected. Command {operation} canceled.")
            break
        elif response == 'n':
            log.info(f"Opening vi editor for 'mcmd {command_name}' command logic...")
            try:
                subprocess.run(['vi', command_file])
                add_shebang_if_missing(command_file)
                log.info(f"Command 'mcmd {command_name}' {operation}d successfully.")
            except Exception as e:
                log.error(f"Error opening vi editor: {e}")
            break
        else:
            log.error("Invalid input. Please enter 'y' or 'n'.")

def remove_command():
    if not os.path.exists(MCMD_COMMANDS_DIR):
        log.error("No commands found.")
        return

    # Collect commands from subfolders
    command_items = []
    for root, dirs, files in os.walk(MCMD_COMMANDS_DIR):
        for file in files:
            if file.endswith('.sh'):
                command_name = file[:-3]
                command_path = os.path.join(root, file)
                # Get the relative path to use for listing commands
                relative_path = os.path.relpath(command_path, MCMD_COMMANDS_DIR)
                command_items.append((command_name, relative_path))

    if not command_items:
        log.error("No commands found.")
        return

    # Display commands with their relative paths
    log.info("Existing commands:")
    for idx, (cmd_name, rel_path) in enumerate(command_items, start=1):
        print(f"  {idx}. mcmd {cmd_name}")

    try:
        choice = int(get_input("Enter the number of the command to remove: "))
        if 1 <= choice <= len(command_items):
            command_name, command_path = command_items[choice - 1]
            command_dir = os.path.dirname(os.path.join(MCMD_COMMANDS_DIR, command_path))
            
            # Remove .sh and .desc files
            os.remove(os.path.join(MCMD_COMMANDS_DIR, command_path))
            desc_path = os.path.join(command_dir, f"{command_name}.desc")
            if os.path.exists(desc_path):
                os.remove(desc_path)
            
            # Remove empty directories
            while command_dir != MCMD_COMMANDS_DIR:
                if not os.listdir(command_dir):
                    os.rmdir(command_dir)
                    command_dir = os.path.dirname(command_dir)
                else:
                    break

            log.info(f"Command 'mcmd {command_name}' removed successfully.")
        else:
            log.error("Invalid choice. No command removed.")
    except ValueError:
        log.error("Invalid input. Please enter a number.")
    except Exception as e:
        log.error(f"Error removing command: {e}")
        
def list_commands():
    if os.path.exists(MCMD_COMMANDS_DIR):
        subfolders = [f for f in os.listdir(MCMD_COMMANDS_DIR) if os.path.isdir(os.path.join(MCMD_COMMANDS_DIR, f))]
        if subfolders:
            log.warn("CUSTOM COMMANDS:")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Command", style="dim")
            table.add_column("Description")
            for cmd in subfolders:
                command_dir = os.path.join(MCMD_COMMANDS_DIR, cmd)
                desc_file = os.path.join(command_dir, f"{cmd}.desc")
                description = ""
                if os.path.exists(desc_file):
                    with open(desc_file, 'r') as file:
                        description = file.read().strip()
                
                if len(description) > 200:
                    description = description[:200] + "..."
                
                table.add_row(f"mcmd exec {cmd}", description)
                table.add_row("")  
            console.print(table)
        else:
            log.error("No commands found.")
    else:
        log.error("Commands directory does not exist.")

def execute_command(command_name: str, args):
    if args is None:
        args = []

    command_file = os.path.join(MCMD_COMMANDS_DIR, command_name, f"{command_name}.sh")
    
    try:
        if os.path.exists(command_file):
            subprocess.run([command_file] + args, check=True)
        else:
            log.error(f"Command 'mcmd {command_name}' not found.")
    except subprocess.CalledProcessError as e:
        log.error(f"Error executing command '{command_name}': {e}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")

def export_command():
    root = tk.Tk()
    root.withdraw()

    log.info("Please select the destination folder...")
    destination_path = filedialog.askdirectory(title="Choose a destination folder")
    
    if not destination_path:
        log.error("No destination folder selected. Export canceled.")
        return
    
    destination_path = os.path.join(destination_path, "mcmd")
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    if not os.path.exists(MCMD_COMMANDS_DIR):
        log.error(f"Source directory '{MCMD_COMMANDS_DIR}' does not exist.")
        return
    
    try:
        subfolders = [f for f in os.listdir(MCMD_COMMANDS_DIR) if os.path.isdir(os.path.join(MCMD_COMMANDS_DIR, f))]
        
        if subfolders:
            for cmd in subfolders:
                src_dir = os.path.join(MCMD_COMMANDS_DIR, cmd)
                shutil.copytree(src_dir, os.path.join(destination_path, cmd), dirs_exist_ok=True)
            
            log.info(f"All custom commands have been exported successfully to '{destination_path}'.")
        else:
            log.warn("No commands found to move.")
    except Exception as e:
        log.error(f"Error during export: {e}")

def display_help(command_name: str):
    """
    Display the help message for the command, including usage, description, and arguments.
    """
    description_file = os.path.join(MCMD_COMMANDS_DIR, command_name, f"{command_name}.desc")
    if os.path.exists(description_file):
        with open(description_file, 'r') as file:
            description = file.read()
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Command", style="dim")
        table.add_column("Description")
        table.add_row(f"mcmd exec {command_name}", description)
        console.print(table)
    else:
        log.error(f"Description file for 'mcmd {command_name}' does not exist.")

@app.command()
def create():
    """Create or update a custom command."""
    create_or_update_command()

@app.command()
def list():
    """List all custom command."""
    list_commands()

@app.command()
def remove():
    """Remove custom command."""
    remove_command()

@app.command()
def exec(
    command_name: str,
    args: Optional[List[str]] = typer.Argument(None, help="Arguments for the command")
):
    """
    Entry point to execute custom commands if no other command is specified.
    """
    if command_name:
        if is_valid_command_name(command_name):
            if args and args[-1] == 'help':
                display_help(command_name)
            else:
                # If args is None, set it to an empty list
                execute_command(command_name, args)
        else:
            log.error("Invalid command name. Command names should only contain alphanumeric characters and underscores.")
    else:
        log.error("No command provided. Use help for options.")

@app.command()
def export():
    """
    Export all custom commands to the selected destination folder.
    """
    export_command()

if __name__ == "__main__":
    app()
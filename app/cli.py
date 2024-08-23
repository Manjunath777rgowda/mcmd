#!/usr/bin/env python3

import os
import sys
import subprocess
import typer
from rich.console import Console
from rich.table import Table
from typing import List, Optional

app = typer.Typer()
console = Console()

# Define the commands directory relative to the current script's location
MCMD_COMMANDS_DIR = os.path.expanduser("~/.mcmd_commands")

def is_valid_command_name(command_name):
    # Simple validation: only allows alphanumeric characters and underscores
    return command_name.isidentifier()

def create_or_update_command():
    command_name = input("Enter the command name: mcmd ")

    # Validate the command name
    if not is_valid_command_name(command_name):
        print("Invalid command name. Command names should only contain alphanumeric characters and underscores.")
        return

    command_description = input(f"Enter a description for 'mcmd {command_name}': ")

    # Define paths for command logic and description files
    command_dir = os.path.join(MCMD_COMMANDS_DIR, command_name)
    command_file = os.path.join(command_dir, f"{command_name}.sh")
    description_file = os.path.join(command_dir, f"{command_name}.desc")
    
    os.makedirs(command_dir, exist_ok=True)
    
    # Check if the command exists
    if os.path.exists(command_file):
        print(f"Command 'mcmd {command_name}' already exists.")
        while True:
            response = input("Do you want to update it? (y/n): ").lower()
            if response == 'y':
                print(f"Updating command 'mcmd {command_name}'.")
                break
            elif response == 'n':
                print("Command update canceled.")
                return
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                continue
    else:
        print(f"Creating new command 'mcmd {command_name}'.")

    try:
        # Open vi editor for editing the command logic
        print(f"Opening vi editor for 'mcmd {command_name}' command logic...")
        subprocess.run(['vi', command_file])
        
        # Save the command description
        with open(description_file, 'w') as file:
            file.write(command_description + "\n")
        
        os.chmod(command_file, 0o755)
        print(f"Command 'mcmd {command_name}' updated successfully.")
    except Exception as e:
        print(f"Error creating/updating command: {e}")

def remove_command():
    if not os.path.exists(MCMD_COMMANDS_DIR):
        print("No commands found.")
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
        print("No commands found.")
        return

    # Display commands with their relative paths
    print("Existing commands:")
    for idx, (cmd_name, rel_path) in enumerate(command_items, start=1):
        print(f"  {idx}. mcmd {cmd_name}")

    try:
        choice = int(input("Enter the number of the command to remove: "))
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

            print(f"Command 'mcmd {command_name}' removed successfully.")
        else:
            print("Invalid choice. No command removed.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"Error removing command: {e}")
        
def list_commands():
    if os.path.exists(MCMD_COMMANDS_DIR):
        subfolders = [f for f in os.listdir(MCMD_COMMANDS_DIR) if os.path.isdir(os.path.join(MCMD_COMMANDS_DIR, f))]
        if subfolders:
            console.print("[bold yellow]CUSTOM COMMANDS:[/bold yellow]")
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
                table.add_row(f"mcmd exec {cmd}", description)
            console.print(table)
        else:
            console.print("No commands found.")
    else:
        console.print("Commands directory does not exist.")

def execute_command(command_name: str, args):
    if args is None:
        args = []

    command_file = os.path.join(MCMD_COMMANDS_DIR, command_name, f"{command_name}.sh")
    
    try:
        if os.path.exists(command_file):
            subprocess.run([command_file] + args, check=True)
        else:
            console.print(f"[bold red]Command 'mcmd {command_name}' not found.[/bold red]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error executing command '{command_name}': {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        console.print(f"[bold yello]Ensure the sebang is added. if not add it at the beggining of the file (#!/bin/bash)[/bold yello]")

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
            # If args is None, set it to an empty list
            execute_command(command_name, args)
        else:
            print("Invalid command name. Command names should only contain alphanumeric characters and underscores.")
    else:
        print("No command provided. Use --help for options.")


if __name__ == "__main__":
    app()
import os
import typer
from rich.console import Console
from app.log_util import Log
from app.operations import *
import subprocess
import shutil
import pkg_resources
from rich.table import Table
import tkinter as tk
from tkinter import filedialog
from app.settings import get_settings

MCMD_COMMANDS_DIR = os.path.expanduser(get_settings("MCMD_COMMANDS_DIR"))

log = Log()
console = Console()

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
                command_description = get_input(f"Update a description for 'mcmd exec {command_name}'. (Presss enter to ignore..)").strip()
                # Only write description if it's not empty
                if command_description.strip():
                    with open(description_file, 'w') as file:
                        file.write(command_description + "\n")
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
        while True:
            command_description = get_input(f"Enter a description for 'mcmd exec {command_name}': ").strip()
            if command_description:
                try:
                    with open(description_file, 'w') as file:
                        file.write(command_description + "\n")
                    break
                except Exception as e:
                    log.error(f"Error saving command description: {e}")
            else:
                log.error("Description cannot be empty. Please enter a valid description.")
        
        accept_command_details("create", command_file, command_name)

    try:
        # Make the command file executable
        os.chmod(command_file, 0o755)
    except Exception as e:
        log.error(f"Error while changing the permission: {e}")
    auto_export()

def auto_export():
    try:
        if get_settings("ENABLE_AUTO_EXPORT"):
            export_dir = get_settings("MCMD_EXPORT_DIR")
            if export_dir:
                export(export_dir)
    except Exception as e:
        log.error(f"Error while performing auto export : {e}")

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

    list_commands()

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
    if not os.path.exists(MCMD_COMMANDS_DIR):
        log.error("Commands directory does not exist.")
        return

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
    
    log.warn("CUSTOM COMMANDS:")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("No.", style="dim")
    table.add_column("Command", style="dim")
    table.add_column("Description")

    for index, (cmd_name, rel_path) in enumerate(command_items, start=1):
        command_dir = os.path.dirname(os.path.join(MCMD_COMMANDS_DIR, rel_path))
        desc_file = os.path.join(command_dir, f"{cmd_name}.desc")
        description = ""
        
        if os.path.exists(desc_file):
            with open(desc_file, 'r') as file:
                description = file.read().strip()
            
            if len(description) > 200:
                description = description[:200] + "..."
        else: continue
        
        table.add_row(str(index), f"mcmd exec {cmd_name}", description)
        table.add_row("")  
    console.print(table)

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

def export_commands():
    export_dir = get_settings("MCMD_EXPORT_DIR")
    if export_dir:
        while True:
            response = get_input("Do you want to export to default location (y/n): ").lower()
            if response == 'y':
                export(export_dir)
                break
            elif response == 'n':
                root = tk.Tk()
                root.withdraw()

                log.info("Please select the destination folder...")
                destination_path = filedialog.askdirectory(title="Choose a destination folder")
                
                if not destination_path:
                    log.error("No destination folder selected. Export canceled.")
                    return
                
                export(destination_path)
                break
            else:
                log.error("Invalid input. Please enter 'y' or 'n'.")
                continue   

def export(destination_path):
    
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
            
        else:
            log.warn("No commands found to move.")
    except Exception as e:
        log.error(f"Error during export: {e}")

def import_commands():
    import_dir = get_settings("MCMD_EXPORT_DIR")
    if import_dir:
        while True:
            response = get_input("Do you want to import from default location (y/n): ").lower()
            if response == 'y':
                imports(import_dir)
                break
            elif response == 'n':
                root = tk.Tk()
                root.withdraw()

                log.info("Please select the folder...")
                destination_path = filedialog.askdirectory(title="Choose a folder")
                
                if not destination_path:
                    log.error("No folder selected. Export canceled.")
                    return
                
                imports(destination_path)
                break
            else:
                log.error("Invalid input. Please enter 'y' or 'n'.")
                continue   

def imports(import_dir):
    try:
        import_path = os.path.join(import_dir, "mcmd")
        if not os.path.exists(import_path):
            log.error(f"Invalid Directory '{import_path}' does not exist.")
            return
    
        if is_git_repo(import_dir):
            log.info(f"{import_dir} is a git repository.")
            changes = get_git_status(import_dir)
            
            if changes:
                log.error("Uncommitted changes detected:")
                log.error(changes)
                log.info("Please commit the changes before import...")
                return
            else:
                result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if result.returncode == 0:
                    log.info(f"Successfully pulled latest changes in {import_dir}")
                else:
                    log.warn(f"Error pulling changes in {import_dir}: {result.stderr}")
                
        else:
            log.warn(f"'{import_path}' is not a Git repository.")
        
        shutil.copytree(import_path, MCMD_COMMANDS_DIR, dirs_exist_ok=True)
        log.info(f"Imported Successfully from '{import_path}'")
    except Exception as e:
        log.error(f"Error during export: {e}")

def is_git_repo(path):
    return os.path.isdir(os.path.join(path, '.git'))

def get_git_status(path):
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'], 
            cwd=path, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        # If there's any output, there are changes
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    
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

def get_banner_file_path():
    return pkg_resources.resource_filename(__name__, 'banner.txt')

def read_banner_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Banner file not found."
    except Exception as e:
        return f"Error reading banner file: {e}"

def print_banner():
    banner_file_path = get_banner_file_path()
    banner_content = read_banner_file(banner_file_path)
    log.warn(banner_content)

def custom_help(ctx: typer.Context, param: typer.Option, value: bool):
    if value:
        print_banner()
        with console.capture() as capture:
            typer.echo(ctx.get_help())
        help_output = capture.get()

        # Print the help output
        console.print(help_output)
        if get_settings("ENABLE_AUTO_EXPORT"):
            log.info("Auto export enabled")
            export_dir = get_settings("MCMD_EXPORT_DIR")
            if export_dir:
                log.info(f"Export Dir : {export_dir}")
            else:
                log.error("Set export dir using 'mcmd setting edit MCMD_EXPORT_DIR <path>'")
        else:
            log.warn("Enable auto export using 'mcmd setting edit ENABLE_AUTO_EXPORT true'")
        ctx.exit()

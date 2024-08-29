import os
import json
from app.log_util import Log
import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer()
log = Log()
console = Console()

MCMD_COMMANDS_DIR = os.path.expanduser("~/.mcmd_commands")

def get_settings(setting, path=MCMD_COMMANDS_DIR):
    settings = get_all_settings(path)
    keys = setting.split('.')
    value = settings
    
    for key in keys:
        value = value.get(key)
        if value is None:
            raise KeyError(f"Setting '{setting}' not found.")
    
    # Extract and return only the 'value' field from the settings dictionary
    if isinstance(value, dict) and 'value' in value:
        return value['value']
    else:
        raise ValueError(f"Setting '{setting}' does not have a 'value' field.")

def get_all_settings(path=MCMD_COMMANDS_DIR):
    setting_file = os.path.expanduser(path + '/settings.json')
    try:
        with open(setting_file, 'r') as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        log.error(f"{setting_file} not found.")
        raise Exception("settings.json not found.")
    except json.JSONDecodeError:
        log.error("Error decoding JSON in settings file.")
        raise Exception("Error decoding JSON in settings file.")

def save_settings(settings):
    setting_file =  MCMD_COMMANDS_DIR+'/settings.json'
    with open(setting_file, 'w') as file:
        json.dump(settings, file, indent=4)

@app.command()
def list():
    """List all settings"""
    settings = get_all_settings()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Key")
    table.add_column("Value")
    table.add_column("Description")
    
    for key, value in settings.items():
        value_str = str(value.get('value', ''))
        description = value.get('description', '')
        table.add_row(key, value_str, description)
        table.add_row("")
    
    console.print(table)

@app.command()
def edit(key: str, value: str):
    """Edit an existing setting"""
    settings = get_all_settings()
    keys = key.split('.')
    
    # Navigate to the right place in the dictionary
    d = settings
    for k in keys[:-1]:
        if k not in d:
            log.info(f"Setting '{key}' does not exist.")
            return
        d = d[k]
    
    # Update only the 'value' field if the setting exists and is a dictionary
    if keys[-1] in d:
        if isinstance(d[keys[-1]], dict):
            d[keys[-1]]['value'] = value
            save_settings(settings)
            log.info(f"Setting '{key}' updated to '{value}'")
        else:
            log.info(f"Setting '{key}' is not a dictionary and cannot be updated.")
    else:
        log.info(f"Setting '{key}' does not exist.")

def compare_and_update_settings(old_path: str, new_path: str):
    """
    Compare two settings files and update the old one with any new settings.
    
    Parameters:
    - old_path: Path to the old settings file
    - new_path: Path to the new settings file
    """
    # Expand user paths
    old_path = os.path.expanduser(old_path) + "/settings.json"
    new_path = os.path.expanduser(new_path) + "/settings.json"


    # Load old settings
    old_settings = {}
    try:
        with open(old_path, 'r') as file:
            old_settings = json.load(file)
    except FileNotFoundError:
        log.error(f"Old settings file '{old_path}' not found.")
    except json.JSONDecodeError:
        log.error(f"Error decoding JSON in old settings file '{old_path}'.")
        raise Exception(f"Error decoding JSON in old settings file '{old_path}'.")

    # Load new settings
    try:
        with open(new_path, 'r') as file:
            new_settings = json.load(file)
    except FileNotFoundError:
        log.error(f"New settings file '{new_path}' not found.")
        raise Exception(f"New settings file '{new_path}' not found.")
    except json.JSONDecodeError:
        log.error(f"Error decoding JSON in new settings file '{new_path}'.")
        raise Exception(f"Error decoding JSON in new settings file '{new_path}'.")


    # Find new settings to add
    settings_to_add = {k: v for k, v in new_settings.items() if k not in old_settings}
    
    if not settings_to_add:
        return
    
    # Update old settings with new settings
    old_settings.update(settings_to_add)
    
    # Save the updated old settings
    try:
        with open(old_path, 'w') as file:
            json.dump(old_settings, file, indent=4)
        log.info(f"Old settings file '{old_path}' updated with new settings.")
    except IOError:
        log.error(f"Error writing to old settings file '{old_path}'.")
        raise Exception(f"Error writing to old settings file '{old_path}'.")
    
     # Print all old and new values
    log.info("Changes Added:")
    for key, value in settings_to_add.items():
        log.info(f"{key}: {value}")
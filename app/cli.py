#!/usr/bin/env python3

import os
import typer
from rich.console import Console
from typing import List, Optional
from app.log_util import Log
from app.operations import *
from app.settings import app as settings

os.environ['TK_SILENCE_DEPRECATION'] = '1'

app = typer.Typer()
app.add_typer(settings, name="setting",help="List and edit the settings")

console = Console()
log = Log()

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
    Export custom commands to the default folder else selected destination folder from the command repo.
    """
    export_commands()

@app.command()
def imports():
    """
    Import custom commands from the default folder else selected destination folder to the command repo.
    """
    import_commands()

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    help: bool = typer.Option(
        None, "--help", "-h", is_eager=True, callback=custom_help, help="Show this message and exit."
    ),
):
    if ctx.invoked_subcommand is None:
        console.print("[bold red]No command provided. Use --help to see available commands.[/bold red]")
        ctx.exit()

if __name__ == "__main__":
    app()
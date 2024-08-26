# mcmd

## Problem Statement

In the fast-paced world of software development and system administration, repetitive tasks and commands can quickly become a burden. Many professionals find themselves frequently typing the same commands, managing multiple scripts, and navigating to various directories, which can be both time-consuming and error-prone. Below are some common issues faced:

### Repetition of Commands

**Problem**: Are you stuck in the routine of typing the same command multiple times every day? Repetitive tasks can lead to inefficiency and frustration.

**Example**: You need to run a specific command regularly, such as building a project or running tests, but entering it manually each time takes up valuable time.

### Managing Custom Scripts

**Problem**: Are you creating scripts to automate your work but struggling to remember what each script does? This lack of clarity can lead to mistakes and wasted time.

**Example**: You have several scripts for different tasks, but remembering the exact purpose and usage of each script becomes cumbersome.

### Navigating to Script Directories

**Problem**: Do you find yourself constantly traversing to different directories to execute scripts? This frequent navigation can interrupt your workflow and reduce productivity.

**Example**: You need to execute a script located in a specific folder, but switching to that directory every time you want to run it is inefficient.

## Introducing `mcmd (Manjunath Command Assist)`

`mcmd` is an innovative solution designed to address these common challenges:

- **Simplify Command Execution**: Store and execute frequently used commands with ease. No more repetitive typing—just call your custom commands with a simple alias.

- **Organize and Document Scripts**: Create, update, and manage custom commands with associated descriptions. Keep track of what each command does and streamline your workflow.

- **Easy Navigation**: Access your custom commands from anywhere without needing to navigate to specific directories. Execute commands directly from your command line, improving efficiency.

- **Export Commands**: Move or copy all your custom commands to a different directory, making it easy to back up or transfer your setup.

By using `mcmd`, you can enhance your productivity, reduce repetitive tasks, and maintain a more organized approach to managing your scripts and commands.

## Features

- **Create and Update Commands**: Define new commands or modify existing ones with custom logic and descriptions.
- **List Commands**: View all available custom commands and their descriptions in a neatly formatted table.
- **Remove Commands**: Delete commands that are no longer needed.
- **Execute Commands**: Run custom commands with optional arguments from anywhere in your system.
- **Export Commands**: Copy all custom commands to a specified destination folder for backup or transfer.

`mcmd` is designed to make your command-line experience smoother and more efficient, helping you focus on what matters most—getting your work done.

## Uninstalling mcmd

If you have an existing installation of `mcmd`, you can uninstall it with the following command:

```bash
pip uninstall mcmd
```

## Installing mcmd

To install the latest version of `mcmd` directly from the GitHub repository, use the following command:

```bash
pip install git+https://github.com/Manjunath777rgowda/mcmd.git
```

## Usage

Once installed, you can use the `mcmd` command. Below is the help message for `mcmd`:

```bash
mcmd --help
```

```plaintext
Usage: mcmd [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                     │
│ --show-completion             Show completion for the current shell, to copy it or          │
│                               customize the installation.                                   │
│ --help                        Show this message and exit.                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────╮
│ create   Create or update a custom command.                                                 │
│ exec     Entry point to execute custom commands if no other command is specified.           |
│ export   Export all custom commands to the specified destination folder.                    |
│ list     List all custom commands.                                                          │
│ remove   Remove a custom command.                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Command Descriptions

- **create**: Create or update a custom command.

  ```bash
  mcmd create <command_name>
  ```

- **exec**: Execute a custom command if no other command is specified.

  ```bash
  mcmd exec <command_name> [args...]
  ```

- **export**: Export all custom commands to the specified destination folder.

  ```bash
  mcmd export <destination_folder>
  ```

- **list**: List all custom commands.

  ```bash
  mcmd list
  ```

- **remove**: Remove a custom command.

  ```bash
  mcmd remove
  ```

## Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request. Issues and feature requests are also encouraged.

```

This `README.md` provides clear instructions based on the `mcmd --help` command, making it easy for users to understand how to work with `mcmd`.
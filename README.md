# mcmd

`mcmd` is a Python application designed to help you create, manage, and execute custom shell commands easily.

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
│ exec     Entry point to execute custom commands if no other command is specified.           │
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

- **list**: List all custom commands.

  ```bash
  mcmd list
  ```

- **remove**: Remove a custom command.

  ```bash
  mcmd remove
  ```

## Troubleshooting

If you encounter issues with `mcmd`, try the following:

1. Ensure that the installation directory is in your `PATH`.
2. If using a virtual environment, make sure it's activated.
3. Reinstall the package if necessary.

## Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request. Issues and feature requests are also encouraged.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

This `README.md` provides clear instructions based on the `mcmd --help` command, making it easy for users to understand how to work with `mcmd`.
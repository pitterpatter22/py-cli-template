# MyCLIApp

A Python-based interactive CLI framework using `prompt_toolkit`, `argparse`, and modular command registration. This template includes command parsing, styled output, command auto-completion, logging, and configuration loading via JSON.

---

## Project Structure

```
mycliapp/
├── __init__.py
├── main.py               # Entry point to start the CLI
├── cli.py                # PromptSession-based CLI loop and UI logic
├── commands/
│   ├── __init__.py
│   ├── base.py           # Command registration + Command class
│   └── account.py        # Example commands: addmoney, listaccounts, transfer
├── config/
│   ├── __init__.py
│   ├── config_parser.py  # Config file parsing logic
│   └── settings.py       # Global Settings model (Pydantic)
├── utils/
│   ├── __init__.py
│   ├── errors.py         # Custom exceptions like CommandError
│   ├── formatter.py      # Rich-based output formatting helpers
│   └── logger.py         # Logging setup
```

---

## Configuration

You can optionally provide a config JSON file via `--config` when launching the app:

```bash
python -m mycliapp.main --config config.json
```

Example `config.json`:

```json
{
  "debug": true,
  "app_name": "DemoBank",
  "log_level": "DEBUG",
  "env": {
    "API_KEY": "abc123",
    "DEFAULT_REGION": "us-east-1"
  },
  "run_on_start": [
    "addmoney -account 123 -amount 10",
    "listaccounts"
  ]
}
```

Fields:
- `debug`: Enables verbose logging if true.
- `app_name`: Changes CLI banner.
- `log_level`: INFO, DEBUG, etc.
- `env`: Injects environment variables.
- `run_on_start`: List of commands to run after startup (requires user approval).

---

## Features

- Interactive prompt with tab completion
- Automatic command help (`help <command>` or `<command> -h`)
- Configurable via JSON
- Pretty CLI output with `rich`
- Easy command definition with `Command` class
- Optional logging and debug mode

---

## How Commands Work

### Command Definition (in `mycliapp/commands/account.py`)

Each command is registered using the `Command` class:

```python
from mycliapp.commands.base import Command
from argparse import ArgumentParser

def get_addmoney_parser():
    parser = ArgumentParser(prog="addmoney", description="Add money to an account.")
    parser.add_argument("-account", required=True, help="Account ID")
    parser.add_argument("-amount", type=float, required=True, help="Amount to add")
    return parser

def handle_addmoney(settings, parsed_args):
    print(f"Added ${parsed_args.amount} to account {parsed_args.account}")

Command(
    name="addmoney",
    description="Add money to an account.",
    parser_func=get_addmoney_parser,
    handler_func=handle_addmoney,
    completion_options=["-account", "-amount"]
)
```

This registers `addmoney` automatically in `command_registry`.

---

## ➕ How to Add a New Command

1. Create a new parser function that returns an `ArgumentParser`.
2. Create a handler function that receives `settings` and the parsed args.
3. Instantiate a `Command(...)` with:
   - `name`: command name (e.g. `"sync"`)
   - `description`: used in help
   - `parser_func`: function that returns the parser
   - `handler_func`: the function that runs the logic
   - `completion_options`: tab-completion options

**Example**: New command `sync` in `commands/account.py`

```python
def get_sync_parser():
    parser = ArgumentParser(prog="sync", description="Sync all accounts.")
    parser.add_argument("--dry-run", action="store_true", help="Do not commit changes")
    return parser

def handle_sync(settings, args):
    print("Syncing accounts...")
    if args.dry_run:
        print("Dry run mode")

Command(
    name="sync",
    description="Sync account data.",
    parser_func=get_sync_parser,
    handler_func=handle_sync,
    completion_options=["--dry-run"]
)
```

---

## 🧪 Running the App

```bash
python -m mycliapp.main
```

With config:
```bash
python -m mycliapp.main --config config.json
```

---

## Command List (predefined)

| Command        | Description                     |
|----------------|---------------------------------|
| `addmoney`     | Add money to an account         |
| `transfer`     | Transfer money between accounts |
| `listaccounts` | Show all accounts               |
| `help`         | Show help                       |
| `exit`         | Exit the CLI                    |

---

## Optional Enhancements

- Add command aliases
- Support chained command execution
- Add history search with up/down arrows
- Save session history to disk

---

## Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- `prompt_toolkit`
- `pyfiglet`
- `rich`
- `pydantic`
import json
import os
from mycliapp.utils.formatter import error, success, info
from mycliapp.config.settings import Settings
from mycliapp.utils.errors import CommandError
from mycliapp.commands.base import command_registry
import shlex

def load_config_file(path: str, settings: Settings) -> None:
    if not os.path.exists(path):
        error(f"Config file not found: {path}")
        raise CommandError("Missing config file")

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        error(f"Invalid JSON in config: {e}")
        raise CommandError("Malformed JSON config")

    apply_config(data, settings)
    success(f"Loaded config from {path}")

def apply_config(config: dict, settings: Settings) -> None:
    from mycliapp.utils.formatter import warn, sub_message, print_line

    if "debug" in config:
        settings.debug = bool(config["debug"])
        info(f"Set debug = {settings.debug}")

    if "app_name" in config:
        settings.app_name = str(config["app_name"])
        info(f"Set app_name = {settings.app_name}")

    if "env" in config:
        set_env_vars(config["env"])

    run_on_start = config.get("run_on_start")
    if not run_on_start:
        return

    # Support string or list
    if isinstance(run_on_start, str):
        run_on_start = [run_on_start]

    # Show startup command list
    warn("The following startup commands are about to run:")
    print_line(newline=False)
    for cmd in run_on_start:
        sub_message(f"  {cmd}")
    print_line()

    if not config.get("startup_auto_confirm", False):
        proceed = input("Proceed? [y/N]: ").strip().lower()
        if proceed not in ("y", "yes"):
            warn("Startup commands skipped.")
            return

    # Run each command
    for line in run_on_start:
        try:
            args = shlex.split(line)
        except ValueError as e:
            error(f"Invalid startup command: {line} — {e}")
            continue

        if not args:
            continue

        cmd_name, *cmd_args = args
        cmd = command_registry.get(cmd_name)
        if not cmd:
            error(f"Unknown startup command: {cmd_name}")
            continue

        info(f"Running startup command: {line}")
        try:
            cmd.run(settings, cmd_args)
        except CommandError as e:
            error(f"Startup command failed: {e}")

def set_env_vars(env_dict: dict, override: bool = False):
    for key, value in env_dict.items():
        if key in os.environ and not override:
            info(f"ENV already set: {key} (keeping existing value)")
            continue
        os.environ[key] = str(value)
        info(f"ENV set: {key} = {value}")
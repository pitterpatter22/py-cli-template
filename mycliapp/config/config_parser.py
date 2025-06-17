import json
import os
from mycliapp.utils.formatter import error, success, info
from mycliapp.config.settings import Settings
from mycliapp.utils.errors import CommandError

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
    if "debug" in config:
        settings.debug = bool(config["debug"])
        info(f"Set debug = {settings.debug}")

    if "app_name" in config:
        settings.app_name = str(config["app_name"])
        info(f"Set app_name = {settings.app_name}")

    if "env" in config:
        set_env_vars(config["env"])

    if config.get("run_on_start") == "listaccounts":
        from mycliapp.commands.account import list_accounts
        list_accounts(settings, "")

def set_env_vars(env_dict: dict, override: bool = False):
    for key, value in env_dict.items():
        if key in os.environ and not override:
            info(f"ENV already set: {key} (keeping existing value)")
            continue
        os.environ[key] = str(value)
        info(f"ENV set: {key} = {value}")
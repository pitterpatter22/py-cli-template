"""
Entrypoint for launching the interactive CLI app.
Handles command-line arguments like --config.
"""

import argparse
from mycliapp.cli import InteractiveShell
from mycliapp.config.settings import Settings
from mycliapp.utils.logger import setup_logger
from mycliapp.config.config_parser import load_config_file

def main():
    # Set up logger temporarily at INFO level before config
    setup_logger()

    parser = argparse.ArgumentParser(description="Start MyCLIApp")
    parser.add_argument('--config', help='Optional JSON config file path')
    args = parser.parse_args()

    # Create settings and shell early
    settings = Settings()
    shell = InteractiveShell(settings)
    shell.print_entry()  # Print the welcome banner FIRST

    # Now load config (may print logs after banner)
    if args.config:
        load_config_file(args.config, settings)

    # Re-configure logger after config
    log_level = getattr(settings, "log_level", None)
    if not log_level and getattr(settings, "debug", False):
        log_level = "DEBUG"
    setup_logger(log_level or "INFO")

    shell.run()

if __name__ == "__main__":
    main()
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
    setup_logger()

    parser = argparse.ArgumentParser(description="Start MyCLIApp")
    parser.add_argument('--config', help='Optional JSON config file path')
    args = parser.parse_args()

    settings = Settings()
    if args.config:
        load_config_file(args.config, settings)

    shell = InteractiveShell(settings)
    shell.cmdloop()

if __name__ == "__main__":
    main()
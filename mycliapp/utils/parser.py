"""
Provides a custom ArgumentParser that raises errors instead of exiting.
"""

from argparse import ArgumentParser
from mycliapp.utils.errors import CommandError

class SilentParser(ArgumentParser):
    def error(self, message):
        raise CommandError(f"Invalid arguments: {message}")
# mycliapp/commands/base.py
from typing import Callable, Optional
from argparse import ArgumentParser

command_registry = {}

class Command:
    def __init__(
        self,
        name: str,
        description: str,
        parser_func: Callable[[], ArgumentParser],
        handler_func: Callable,
        completion_options: Optional[list[str]] = None
    ):
        self.name = name
        self.description = description
        self.parser_func = parser_func
        self.handler_func = handler_func
        self.completion_options = completion_options or []
        command_registry[name] = self

    def run(self, settings, args: list[str]):
        parser = self.parser_func()
        try:
            parsed = parser.parse_args(args)
            self.handler_func(settings, parsed)
        except SystemExit as e:
            if e.code == 0:
                return  # Help was requested
            if any(arg in ("-h", "--help") for arg in args):
                raise
            from mycliapp.utils.errors import CommandError
            raise CommandError(f"Invalid arguments: use '{self.name} -h' for details")

    def print_help(self):
        self.parser_func().print_help()
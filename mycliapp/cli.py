# mycliapp/cli.py
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import shlex
from mycliapp.commands import account  # triggers registration
from mycliapp.commands.base import command_registry
from mycliapp.utils.errors import CommandError
from mycliapp.utils.formatter import error, sub_message, print_line, console, success
from mycliapp.config.settings import Settings
import pyfiglet
import logging

logger = logging.getLogger(__name__)



class CLICompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        try:
            args = shlex.split(text)
        except ValueError:
            return  # Ignore bad quotes during tab-completion
        if not args:
            for name in command_registry:
                yield Completion(name, start_position=0)
            return

        if len(args) == 1 and not text.endswith(" "):
            for name in command_registry:
                if name.startswith(args[0]):
                    yield Completion(name, start_position=-len(args[0]))
            return

        command_name = args[0]
        if command_name in command_registry:
            current_arg = document.get_word_before_cursor()
            cmd = command_registry[command_name]
            for opt in cmd.completion_options:
                if opt.startswith(current_arg):
                    yield Completion(opt, start_position=-len(current_arg))


class InteractiveShell:
    def __init__(self, settings=None):
        self.settings = settings or Settings()
        self.session = PromptSession(completer=CLICompleter())
        logger.info("CLI app started")
        self.style = Style.from_dict({
            'prompt': 'bold cyan',
            'command': 'bold yellow',
            'arg': 'ansiblue',
        })

    def run(self):
        while True:
            try:
                line = self.session.prompt(
                    HTML('<prompt>mycliapp&gt;</prompt> '),
                    style=self.style
                )
                if not line.strip():
                    continue
                if line.strip() == "exit":
                    logger.info("CLI app exited")
                    success("Exiting...")
                    break
                self._run_command(line)
            except (KeyboardInterrupt, EOFError):
                logger.info("CLI app exited via keyboard interrupt")
                success("Exiting...")
                break
            except Exception as e:
                error(str(e))
            
    def _run_command(self, line):
        try:
            args = shlex.split(line)
        except ValueError as e:
            error("Syntax error: Unmatched quotes. Use \"...\" or escape spaces properly.")
            return
        if not args:
            return
        command = args[0]
        if command == "help":
            self._print_help()
            return
        cmd_obj = command_registry.get(command)
        if not cmd_obj:
            error(f"Unknown command: {command}")
            return

        try:
            cmd_obj.run(self.settings, args[1:])
        except CommandError as e:
            error(str(e))
            cmd_obj.print_help()
        finally:
            console.print()

    def _print_help(self):
        print("\nAvailable commands:")
        for name, cmd in sorted(command_registry.items()):
            print(f"  {name:<12} {cmd.description}")
        print("  exit        Exit the CLI\n")
        
    def print_entry(self):
        result = pyfiglet.figlet_format(self.settings.app_name)
        print(result)
        sub_message(f"Version {self.settings.version}")
        print_line(color='blue')

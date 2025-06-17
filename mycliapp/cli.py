"""
Implements the interactive shell using cmd.Cmd.
Handles command execution, tab-completion, and help display.
"""

import cmd
import shlex
from mycliapp.config.settings import Settings
from mycliapp.commands import account
from mycliapp.utils.errors import CommandError
from mycliapp.utils.formatter import success, error, info

class InteractiveShell(cmd.Cmd):
    prompt = 'mycliapp> '

    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings or Settings()
        self.commands = {
            'listaccounts': self.do_listaccounts,
            'addmoney': self.do_addmoney,
            'transfer': self.do_transfer,
        }

    def default(self, line):
        error(f"Unknown command: {line}")

    def do_exit(self, arg):
        """Exit the CLI."""
        return True

    def do_listaccounts(self, arg):
        """List all accounts."""
        try:
            account.list_accounts(self.settings, arg)
        except CommandError as e:
            error(f"{e}")

    def do_addmoney(self, arg):
        from mycliapp.commands.account import add_money
        try:
            add_money(self.settings, shlex.split(arg))
        except CommandError as e:
            error(f"{e}")

    def help_addmoney(self):
        """Show help for addmoney (same as addmoney -h)."""
        from mycliapp.commands.account import get_add_parser
        get_add_parser().print_help()

    def do_transfer(self, arg):
        """Transfer money between accounts. Usage: transfer -from ID -to ID -amount N [--note MSG]"""
        from mycliapp.commands.account import transfer_funds
        try:
            transfer_funds(self.settings, shlex.split(arg))
        except CommandError as e:
            error(f"{e}")
                        

    def complete_addmoney(self, text, line, begidx, endidx):
        options = ['-account', '-amount']
        args = shlex.split(line[:begidx])
        if text.startswith('-'):
            return [opt for opt in options if opt.startswith(text)]
        return []

    def complete_listaccounts(self, text, line, begidx, endidx):
        return []

    def completenames(self, text, *ignored):
        completions = [cmd for cmd in self.commands if cmd.startswith(text)]
        if not completions and not text:
            print("\nAvailable commands:")
            for cmd_name in sorted(self.commands):
                print(f"  {cmd_name}")
        return completions
            
    def complete_transfer(self, text, line, begidx, endidx):
        options = ['-from', '-to', '-amount', '--note']
        return [opt for opt in options if opt.startswith(text)]
"""
Command handlers for account-related actions.
"""

from mycliapp.utils.formatter import table, success, info
from mycliapp.utils.errors import CommandError
from mycliapp.utils.parser import SilentParser

def list_accounts(settings, args):
    """Display a list of accounts in a table."""
    accounts = [
        ["123", "Checking", "$500.00"],
        ["456", "Savings", "$1200.00"]
    ]
    table("Accounts", ["ID", "Type", "Balance"], accounts)

def get_add_parser():
    """Return a configured argument parser for addmoney."""
    parser = SilentParser(prog="addmoney", description="Add money to an account.")
    parser.add_argument("-account", required=True, help="Account ID to credit")
    parser.add_argument("-amount", type=float, required=True, help="Amount to add")
    return parser

def add_money(settings, args):
    """Add money to a specified account using parsed arguments."""
    parser = get_add_parser()
    try:
        parsed = parser.parse_args(args)
        success(f"Added ${parsed.amount:.2f} to account {parsed.account}")
    except SystemExit as e:
        if any(arg in ("-h", "--help") for arg in args):
            raise  # Let argparse print help and exit cleanly
        raise CommandError("Invalid arguments: use 'help addmoney' for details")
    
    
def get_transfer_parser():
    """Return a configured parser for transferring funds."""
    parser = SilentParser(prog="transfer", description="Transfer funds between accounts.")
    parser.add_argument("-from", dest="source", required=True, help="Source account ID")
    parser.add_argument("-to", dest="destination", required=True, help="Destination account ID")
    parser.add_argument("-amount", type=float, required=True, help="Amount to transfer")
    parser.add_argument("--note", help="Optional transfer note")
    return parser

def transfer_funds(settings, args):
    """Transfer money from one account to another."""
    parser = get_transfer_parser()
    try:
        parsed = parser.parse_args(args)
        # Business logic goes here
        success(f"Transferred ${parsed.amount:.2f} from {parsed.source} to {parsed.destination}")
        if parsed.note:
            info(f"Note: {parsed.note}")
    except SystemExit as e:
        if any(arg in ("-h", "--help") for arg in args):
            raise  # Let argparse print help and exit cleanly
        raise CommandError("Invalid arguments: use 'help addmoney' for details")
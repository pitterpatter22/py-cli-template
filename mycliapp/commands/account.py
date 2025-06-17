# mycliapp/commands/account.py
from mycliapp.commands.base import Command
from mycliapp.utils.formatter import success, info, table
from mycliapp.utils.parser import SilentParser

def listaccounts_parser():
    parser = SilentParser(prog="listaccounts", description="List all accounts.")
    return parser  # even if no args, still needed for `-h` support

def listaccounts_handler(settings, parsed):
    accounts = [
        ["123", "Checking", "$500.00"],
        ["456", "Savings", "$1200.00"]
    ]
    table("Accounts", ["ID", "Type", "Balance"], accounts)

Command(
    name="listaccounts",
    description="List all available accounts.",
    parser_func=listaccounts_parser,
    handler_func=listaccounts_handler,
    completion_options=[]
)


def addmoney_parser():
    parser = SilentParser(prog="addmoney", description="Add money to an account.")
    parser.add_argument("-account", required=True, help="Account ID to credit")
    parser.add_argument("-amount", type=float, required=True, help="Amount to add")
    return parser

def addmoney_handler(settings, parsed):
    success(f"Added ${parsed.amount:.2f} to account {parsed.account}")

Command(
    name="addmoney",
    description="Add money to an account.",
    parser_func=addmoney_parser,
    handler_func=addmoney_handler,
    completion_options=["-account", "-amount"]
)

def transfer_parser():
    parser = SilentParser(prog="transfer", description="Transfer between accounts.")
    parser.add_argument("-from", dest="source", required=True, help="Source account ID")
    parser.add_argument("-to", dest="destination", required=True, help="Destination account ID")
    parser.add_argument("-amount", type=float, required=True, help="Amount to transfer")
    parser.add_argument("--note", help="Optional note")
    return parser

def transfer_handler(settings, parsed):
    success(f"Transferred ${parsed.amount:.2f} from {parsed.source} to {parsed.destination}")
    if parsed.note:
        info(f"Note: {parsed.note}")

Command(
    name="transfer",
    description="Transfer funds between accounts.",
    parser_func=transfer_parser,
    handler_func=transfer_handler,
    completion_options=["-from", "-to", "-amount", "--note"]
)
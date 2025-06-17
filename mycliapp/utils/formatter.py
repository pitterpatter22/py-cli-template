from rich.console import Console
from rich.text import Text
from rich.table import Table
import logging

console = Console()

def success(message: str):
    _log_and_print("SUCCESS", message, style="green")

def error(message: str):
    _log_and_print("ERROR", message, style="bold red")

def info(message: str):
    _log_and_print("INFO", message, style="cyan")

def warn(message: str):
    _log_and_print("WARN", message, style="yellow")

def table(title: str, columns: list[str], rows: list[list[str]]):
    t = Table(title=title)
    for col in columns:
        t.add_column(col, style="bold")
    for row in rows:
        t.add_row(*[str(cell) for cell in row])
    console.print(t)

def _log_and_print(level: str, message: str, style: str):
    console.print(f"[{style}]{level}: {message}[/]")
    getattr(logging, level.lower() if level != "SUCCESS" else "info")(message)
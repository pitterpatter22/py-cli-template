from dataclasses import dataclass

@dataclass
class Settings:
    app_name: str = "MyCLIApp"
    version: str = "0.1"
    debug: bool = False
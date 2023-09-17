from dataclasses import dataclass


@dataclass
class Contribution:
    filename: str
    username: str
    date: str

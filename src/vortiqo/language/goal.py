from dataclasses import dataclass


@dataclass
class Goal:
    action: str
    target: str
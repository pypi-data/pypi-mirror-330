from dataclasses import dataclass


@dataclass
class Target:
    host: str
    port: str = 502

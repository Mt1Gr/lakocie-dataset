from dataclasses import dataclass
from enum import Enum


@dataclass
class BaseStore:
    name: str
    base_url: str
    scrap_start_url: str


class StoreChoice(Enum):
    KF = BaseStore(
        name="Kocie Figle",
        base_url="https://kociefigle.pl/",
        scrap_start_url="https://kociefigle.pl/Karmy-Mokre",
    )

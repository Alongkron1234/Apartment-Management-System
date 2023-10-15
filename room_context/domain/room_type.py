from dataclasses import dataclass


@dataclass
class RoomType:
    name: str
    description: str
    price: float
    deposit: float

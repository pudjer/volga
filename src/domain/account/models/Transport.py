
from dataclasses import dataclass
from enum import Enum

class TransportType(str, Enum):
    Car: 'Car'
    Bike: 'Bike'
    Scooter: 'Scooter'


@dataclass
class Transport:
    id: int
    canBeRented: bool
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minutePrice: float | None
    dayPrice: float | None
    type: TransportType
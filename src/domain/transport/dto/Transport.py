from typing import Annotated
from fastapi import Query
from pydantic import BaseModel
from dataclasses import dataclass
from enum import Enum

class TransportType(str, Enum):
    Car = 'Car'
    Bike = 'Bike'
    Scooter = 'Scooter'
class TransportTypeWithAll(str, Enum):
    Car = 'Car'
    Bike = 'Bike'
    Scooter = 'Scooter'
    All = 'All'

class TransportDTO(BaseModel):
    id: int
    canBeRented: bool
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: Annotated[float, Query(ge=-90, le=90)]
    longitude: Annotated[float, Query(ge=-180, le=180)]
    minutePrice: float | None
    dayPrice: float | None
    transportType: TransportType
    ownerId: int

class TransportDTOWithoutId(BaseModel):
    canBeRented: bool
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minutePrice: float | None
    dayPrice: float | None
    transportType: TransportType
    ownerId: int

class TransportCreateDTO(BaseModel):
    canBeRented: bool
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minutePrice: float | None
    dayPrice: float | None
    transportType: TransportType
from datetime import datetime
from enum import Enum
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel

from ...transport.dto.Transport import TransportTypeWithAll

class PriceTypeEnum(str, Enum):
    Minutes = "Minutes"
    Days = "Days"

class Rent(BaseModel):
    transportId: int
    userId: int
    timeStart: datetime
    timeEnd: None | datetime
    priceOfUnit: float
    priceType: PriceTypeEnum
    finalPrice: float | None 

class RentWithId(BaseModel):
    id: int
    transportId: int
    userId: int
    timeStart: datetime
    timeEnd: None | datetime
    priceOfUnit: float
    priceType: PriceTypeEnum
    finalPrice: float | None

class GetAvailableTransportDTO(BaseModel):
    lat: Annotated[float, Query(ge=-90, le=90)]
    long: Annotated[float, Query(ge=-180, le=180)]
    radius: float
    type: TransportTypeWithAll
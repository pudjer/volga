from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class TransportType(Enum):
    Car = 'Car'
    Bike = 'Bike'
    Scooter = 'Scooter'


class Transport(Base):
    __tablename__ = 'transport'

    id = Column(Integer, primary_key=True)
    canBeRented = Column(Boolean, nullable=False)
    model = Column(String, nullable=False)
    color = Column(String, nullable=False)
    identifier = Column(String, nullable=False)
    description = Column(Text)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    minutePrice = Column(Float)
    dayPrice = Column(Float)
    transportType = Column(Enum(TransportType), nullable=False)

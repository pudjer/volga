import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from .database import Base
from sqlalchemy.orm import relationship, Mapped


class AccountScheme(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashedPassword = Column(String)
    isAdmin = Column(Boolean, default=False)
    balance = Column(Float, default=0)
    validSince = Column(Integer)
    transports: Mapped[list['TransportScheme']] = relationship("TransportScheme", back_populates="owner", uselist=True)
    rents: Mapped[list['RentScheme']] = relationship("RentScheme", back_populates="user", uselist=True)



class TransportScheme(Base):
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
    transportType = Column(String, nullable=False)
    ownerId: Mapped[int] = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    owner: Mapped["AccountScheme"] = relationship("AccountScheme", back_populates="transports")
    rents: Mapped[list['RentScheme']] = relationship("RentScheme", back_populates="transport", uselist=True)

class RentScheme(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transportId: Mapped[int] = Column(Integer, ForeignKey('transport.id'), nullable=False)
    userId: Mapped[int] = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    timeStart = Column(DateTime, nullable=False)
    timeEnd = Column(DateTime, nullable=True)
    priceOfUnit = Column(Float, nullable=False)
    priceType = Column(String, nullable=False)
    finalPrice = Column(Float, nullable=True)
    transport: Mapped["TransportScheme"] = relationship("TransportScheme", back_populates="rents")
    user: Mapped["AccountScheme"] = relationship("AccountScheme", back_populates="rents")
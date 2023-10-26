import enum
from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String, Text
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
    transport: Mapped[list['TransportScheme']] = relationship("TransportScheme", back_populates="owner", uselist=True)




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
    owner: Mapped["AccountScheme"] = relationship("AccountScheme", back_populates="transport")
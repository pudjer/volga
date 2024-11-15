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




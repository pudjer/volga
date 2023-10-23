from sqlalchemy import Boolean, Column, Float, Integer, String
from ..database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashedPassword = Column(String)
    isAdmin = Column(Boolean, default=False)
    balance = Column(Float, default=0)
    validSince = Column(Integer)

from pydantic import BaseModel

class Account(BaseModel):
    id: int
    username: str
    isAdmin: bool 
    balance: float
    hashedPassword: str
    validSince: int | None
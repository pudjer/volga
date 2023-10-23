
from dataclasses import dataclass


@dataclass
class Account:
    id: int
    username: str
    hashedPassword: str
    isAdmin: bool 
    balance: float
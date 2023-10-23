

from typing import Optional
from pydantic import BaseModel

from ....domain.account.models.Account import Account

class AccountPublicDto(BaseModel):
    id: int
    username: str
    isAdmin: bool 
    balance: float
    
class AccountDto(BaseModel):
    id: int
    username: str
    isAdmin: bool 
    balance: float
    hashedPassword: str
    validSince: str | None

class AccountUpdateDto(BaseModel):
    username: Optional[str]
    password: Optional[str]

class Credentials(BaseModel):
    username: str
    password: str
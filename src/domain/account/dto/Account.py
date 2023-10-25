from pydantic import BaseModel

class AccountDTO(BaseModel):
    id: int
    username: str
    isAdmin: bool 
    balance: float
    hashedPassword: str
    validSince: int | None

class AccountPublicDto(BaseModel):
    id: int
    username: str
    isAdmin: bool 
    balance: float

class AccountUpdateDto(BaseModel):
    username: str
    password: str

class Credentials(BaseModel):
    username: str
    password: str

class AdminCreateAccountDTO(BaseModel):
    username: str
    password: str
    isAdmin: bool
    balance: float
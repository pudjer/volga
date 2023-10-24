from pydantic import BaseModel


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
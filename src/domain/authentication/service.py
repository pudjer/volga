import datetime
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import jwt

from ...domain.account.dto.Account import AccountDto, AccountPublicDto
from ...domain.account.repositories.AccountRepository import GetById
from ...infrastructure.persistence.database import get_db
from .models.Token import Token
from .oauth2 import oauth2_scheme
import os
SECRET_KEY = os.environ.get('SECRET_KEY')

def create_jwt_token(data: dict):
    return jwt.encode(AccountPublicDto(**data.__dict__).__dict__, SECRET_KEY, algorithm="HS256")


async def decode_jwt_token(token = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(token)
    decodedToken = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    acc = await GetById(db, decodedToken['id'])
    if acc.validSince and acc.validSince > datetime.now(datetime.timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="Token has expired")
    try:
        return acc
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")

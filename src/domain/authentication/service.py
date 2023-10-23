
import time
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
EXPIRATION_TIME = int(os.environ.get('EXPIRATION_TIME'))

def create_jwt_token(data: dict):
    now = int(time.time())
    expIn = now+EXPIRATION_TIME
    return jwt.encode(
        {**AccountPublicDto(**data.__dict__).__dict__,
        'expIn': expIn,
        'iat': now},
        SECRET_KEY,
        algorithm="HS256")


async def decode_jwt_token(token = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try: 
        decodedToken = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        acc = await GetById(db, decodedToken['id'])
        now = int(time.time())
        isBaned = (acc.validSince and acc.validSince > decodedToken['iat'])
        isExpired = (decodedToken['expIn'] < now)
        if isBaned or isExpired:
            raise HTTPException(status_code=401, detail="Token has expired")
        return acc
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")

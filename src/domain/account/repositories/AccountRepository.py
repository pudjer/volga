import datetime
import time
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....domain.account.dto.Account import AccountDto, AccountUpdateDto, Credentials
from ....infrastructure.persistence.models.Account import Account
import bcrypt

async def Create(db: Session, credentials: Credentials) -> AccountDto:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(credentials.password.encode(), salt)
    acc = Account(username=credentials.username, hashedPassword=hashed_password.decode())
    db.add(acc)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exist")
    db.refresh(acc)
    res = AccountDto(**acc.__dict__)
    return res

async def GetById(db: Session, id: int):
    acc = db.query(Account).filter(Account.id == id).first()
    if acc is None:
        raise HTTPException(status_code=401, detail="User not found")
    res = AccountDto(**acc.__dict__)
    return res
    
async def GetByUsername(db: Session, username: str):
    acc = db.query(Account).filter(Account.username == username).first()
    if acc is None:
        raise HTTPException(status_code=401, detail="User not found")
    res = AccountDto(**acc.__dict__)
    return res

async def Validate(db: Session, credentials: Credentials):
    acc = db.query(Account).filter(Account.username == credentials.username).first()
    if acc is None:
        raise HTTPException(status_code=401, detail="User not found")
    print(acc.hashedPassword)
    if not bcrypt.checkpw(credentials.password.encode(), acc.hashedPassword.encode()):
        raise HTTPException(status_code=401, detail="Bad password")
    res = AccountDto(**acc.__dict__)
    return res

async def ChangeAttrsById(db: Session, id: int, attrs: AccountUpdateDto):
    acc = db.query(Account).filter(Account.id == id).first()
    for key, value in attrs.__dict__.items():
        setattr(acc, key, value)
    db.commit()
    db.refresh(acc)
    res = AccountDto(**acc.__dict__)
    return res

async def InvalidateById(db: Session, id: int):
    acc = db.query(Account).filter(Account.id == id).first()
    setattr(acc, 'validSince', int(time.time()))
    db.commit()
    db.refresh(acc)
    res = AccountDto(**acc.__dict__)
    return res
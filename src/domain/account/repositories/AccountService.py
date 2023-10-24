import time
from sqlalchemy.orm import Session
from ....domain.account.models.Account import Account
from ....domain.account.dto.Account import  AccountUpdateDto, Credentials
from ....infrastructure.persistence.models.Account import AccountScheme
import bcrypt
from .AccountErrors import *


async def Create(db: Session, credentials: Credentials) -> Account:
    another = db.query(AccountScheme).filter(AccountScheme.username == credentials.username).first()
    if another:
        raise UserNameUniqueError
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(credentials.password.encode(), salt)
    acc = AccountScheme(username=credentials.username, hashedPassword=hashed_password.decode())
    db.add(acc)
    db.commit()
    db.refresh(acc)
    res = Account(**acc.__dict__)
    return res

async def GetById(db: Session, id: int) -> Account :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    if acc is None:
        raise UserNotFoundError
    res = Account(**acc.__dict__)
    return res
    
async def GetByUsername(db: Session, username: str) -> Account :
    acc = db.query(AccountScheme).filter(AccountScheme.username == username).first()
    if acc is None:
        raise UserNotFoundError
    res = Account(**acc.__dict__)
    return res

async def Validate(db: Session, credentials: Credentials) -> Account :
    acc = db.query(AccountScheme).filter(AccountScheme.username == credentials.username).first()
    if acc is None:
        raise UserNotFoundError
    if not bcrypt.checkpw(credentials.password.encode(), acc.hashedPassword.encode()):
        raise IncorectPasswordError
    res = Account(**acc.__dict__)
    return res

async def ChangeAttrsById(db: Session, id: int, attrs: AccountUpdateDto) -> Account :
    another = db.query(AccountScheme).filter(AccountScheme.username == attrs.username).first()
    if another:
        raise UserNameUniqueError
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(attrs.password.encode(), salt)
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    acc.username = attrs.username
    acc.hashedPassword = hashed_password.decode()
    db.refresh(acc)
    res = Account(**acc.__dict__)
    return res

async def InvalidateById(db: Session, id: int) -> Account :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    acc.validSince = int(time.time())
    db.commit()
    db.refresh(acc)
    res = Account(**acc.__dict__)
    return res

async def HesoyamById(db: Session, id: int) -> Account :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    if acc is None:
        raise UserNotFoundError
    acc.balance += 250000
    db.commit()
    db.refresh(acc)
    res = Account(**acc.__dict__)
    return res
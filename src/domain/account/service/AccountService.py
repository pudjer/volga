import time
from sqlalchemy.orm import Session
from ....domain.account.dto.Account import *
from ....infrastructure.persistence.models import AccountScheme
import bcrypt
from .AccountErrors import *
from typing import List


async def Create(db: Session, credentials: AdminCreateAccountDTO | Credentials) -> AccountDTO:
    another = db.query(AccountScheme).filter(AccountScheme.username == credentials.username).first()
    if another:
        raise UserNameUniqueError
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(credentials.password.encode(), salt).decode()
    toCreate = {'username': credentials.username, 'hashedPassword': hashed_password}
    if hasattr(credentials, 'balance'):
        toCreate['balance'] = credentials.balance
    if hasattr(credentials, 'isAdmin'):
        toCreate['isAdmin'] =credentials.isAdmin
    acc = AccountScheme(**toCreate)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc

async def GetById(db: Session, id: int) -> AccountDTO :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    if acc is None:
        raise UserNotFoundError
    return acc
    
async def GetByUsername(db: Session, username: str) -> AccountDTO :
    acc = db.query(AccountScheme).filter(AccountScheme.username == username).first()
    if acc is None:
        raise UserNotFoundError
    return acc

async def Validate(db: Session, credentials: Credentials) -> AccountDTO :
    acc = db.query(AccountScheme).filter(AccountScheme.username == credentials.username).first()
    if acc is None:
        raise UserNotFoundError
    if not bcrypt.checkpw(credentials.password.encode(), acc.hashedPassword.encode()):
        raise IncorectPasswordError
    return acc

async def ChangeAttrsById(db: Session, id: int, attrs: AccountUpdateDto | AdminCreateAccountDTO) -> AccountDTO :
    another = db.query(AccountScheme).filter(AccountScheme.username == attrs.username, AccountScheme.id != id).first()
    if another:
        raise UserNameUniqueError
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    for field, value in attrs.model_dump().items():
            setattr(acc, field, value)
    if hasattr(attrs, 'password'):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(attrs.password.encode(), salt)
        acc.hashedPassword = hashed_password.decode()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(acc)
    return acc

async def InvalidateById(db: Session, id: int) -> AccountDTO :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    acc.validSince = int(time.time())
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(acc)
    return acc

async def HesoyamById(db: Session, id: int) -> AccountDTO :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    if acc is None:
        raise UserNotFoundError
    acc.balance = acc.balance + 250000
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(acc)
    return acc


async def GetSlice(db: Session, start: int = 0, count: int | None = None) -> List[AccountDTO]:
    if start < 0:
        raise Exception('start has to be greater than 0')
    query = db.query(AccountScheme)
    if count is not None:
        query = query.slice(start, start + count)
    else:
        query = query.slice(start, None)
    accounts = query.all()
    return accounts

async def DeleteById(db: Session, id: int) -> AccountDTO :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    if acc is None:
        raise UserNotFoundError
    db.delete(acc)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return acc

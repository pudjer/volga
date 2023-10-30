from datetime import datetime
import time
from sqlalchemy.orm import Session, joinedload

from ....domain.common.Errors import CantBeDeletedError
from ....domain.account.dto.Account import *
from ....infrastructure.persistence.models import AccountScheme, RentScheme, TransportScheme
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

async def GetById(db: Session, id: int) -> AccountScheme :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    if acc is None:
        raise UserNotFoundError
    return acc
    
async def GetByUsername(db: Session, username: str) -> AccountScheme :
    acc = db.query(AccountScheme).filter(AccountScheme.username == username).first()
    if acc is None:
        raise UserNotFoundError
    return acc

async def Validate(db: Session, credentials: Credentials) -> AccountScheme :
    acc = db.query(AccountScheme).filter(AccountScheme.username == credentials.username).first()
    if acc is None:
        raise UserNotFoundError
    if not bcrypt.checkpw(credentials.password.encode(), acc.hashedPassword.encode()):
        raise IncorectPasswordError
    return acc

async def ChangeAttrsById(db: Session, id: int, attrs: AccountUpdateDto | AdminCreateAccountDTO) -> AccountScheme :
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

async def InvalidateById(db: Session, id: int) -> AccountScheme :
    acc = db.query(AccountScheme).filter(AccountScheme.id == id).first()
    acc.validSince = int(time.time())
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(acc)
    return acc

async def HesoyamById(db: Session, id: int) -> AccountScheme :
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


async def GetSlice(db: Session, start: int = 0, count: int | None = None) -> List[AccountScheme]:
    if start < 0:
        raise Exception('start has to be greater than 0')
    query = db.query(AccountScheme)
    if count is not None:
        query = query.slice(start, start + count)
    else:
        query = query.slice(start, None)
    accounts = query.all()
    return accounts

async def DeleteById(db: Session, id: int) -> AccountScheme :
    acc = db.query(AccountScheme).options(joinedload(AccountScheme.rents).joinedload(RentScheme.transport), joinedload(AccountScheme.transports).joinedload(TransportScheme.rents)).filter(AccountScheme.id == id).first()

    if acc is None:
        raise UserNotFoundError

    current_time = datetime.now()
    
    # Check if the account has any current rents
    if any(rent.timeEnd is None or rent.timeEnd > current_time for rent in acc.rents):
        raise CantBeDeletedError('Account has current rents')

    # Check if the account owns any transports with current rents
    if any(rent.timeEnd is None or rent.timeEnd > current_time for transport in acc.transports for rent in transport.rents):
        raise CantBeDeletedError('Some transport of account is in use')

    db.delete(acc)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return acc

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from ...dto.Error import ErrorResponse
from ...dto.Token import Token
from ....domain.account.service.AccountService import ChangeAttrsById, Create, GetById, InvalidateById, Validate
from ....domain.authentication.service import create_jwt_token, decode_jwt_token
from ....infrastructure.persistence.database import get_db
from ....domain.account.dto.Account import *
from sqlalchemy.orm import Session
from ....domain.account.service.AccountErrors import *

account_router = APIRouter()



@account_router.get('/Me/', response_model=AccountPublicDto, responses={401: {"model": ErrorResponse}})
async def GetMe(
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ):
    res = AccountPublicDto(**(await GetById(db, account.id)).__dict__)
    return res

@account_router.post('/SignIn/', response_model=Token, responses={401: {"model": ErrorResponse}})
async def SignIn(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
    ):
    try: 
        res = AccountPublicDto(**(await Validate(db, Credentials(**form_data.__dict__))).__dict__)
    except IncorectPasswordError:
        raise HTTPException(status_code=401, detail='Incorrect password')
    except UserNotFoundError:
        raise HTTPException(status_code=401, detail='Username not found')
    return Token(access_token=create_jwt_token(res), token_type='bearer')

@account_router.post('/SignUp/', response_model=AccountPublicDto, responses={400: {"model": ErrorResponse}})
async def SignUp(
    credentials: Credentials,
    db: Session = Depends(get_db)
    ):
    try: 
        return AccountPublicDto(**(await Create(db, credentials)).__dict__)
    except UserNameUniqueError:
        raise HTTPException(status_code=400, detail='Username already exists')

@account_router.put('/Update/', response_model=AccountPublicDto, responses={400: {"model": ErrorResponse}})
async def Update(
    credentials: AccountUpdateDto,
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ):
    try: 
        res = AccountPublicDto(**(await ChangeAttrsById(db, account.id, credentials)).__dict__)
    except UserNameUniqueError:
        raise HTTPException(status_code=400, detail='Username already exists')
    return res

@account_router.post('/SignOut/', response_model=AccountPublicDto, responses={401: {"model": ErrorResponse}})
async def SignOut(
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ):
    return AccountPublicDto(**(await InvalidateById(db, account.id)).__dict__)

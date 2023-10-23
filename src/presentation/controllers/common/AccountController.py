from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ....domain.authentication.models.Token import Token
from ....domain.account.repositories.AccountRepository import ChangeAttrsById, Create, GetById, InvalidateById, Validate
from ....domain.authentication.service import create_jwt_token, decode_jwt_token
from ....infrastructure.persistence.database import get_db
from ....domain.account.dto.Account import AccountDto, AccountPublicDto, AccountUpdateDto, Credentials
from sqlalchemy.orm import Session

account_router = APIRouter()

@account_router.get('/Me/')
async def GetMe(account: AccountDto = Depends(decode_jwt_token), db: Session = Depends(get_db)):
    res = AccountPublicDto(**(await GetById(db, account.id)).__dict__)
    return account

@account_router.post('/SignIn/')
async def SignIn(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    res = AccountPublicDto(**(await Validate(db, Credentials(**form_data.__dict__))).__dict__)
    return Token(access_token=create_jwt_token(res), token_type='bearer')

@account_router.post('/SignUp/')
async def SignUp(credentials: Credentials, db: Session = Depends(get_db)):
    return AccountPublicDto(**(await Create(db, credentials)).__dict__)

@account_router.put('/Update/')
async def Update(credentials: AccountUpdateDto, account: AccountDto = Depends(decode_jwt_token), db: Session = Depends(get_db)):
    res = AccountPublicDto(**(await ChangeAttrsById(db, account.id, credentials)).__dict__)
    return 'me'

@account_router.post('/SignOut/')
async def SignOut(account: AccountDto = Depends(decode_jwt_token), db: Session = Depends(get_db)):
    return AccountPublicDto(**(await InvalidateById(db, account.id)).__dict__)


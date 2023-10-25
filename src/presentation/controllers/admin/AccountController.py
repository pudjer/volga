from fastapi import APIRouter, Depends, HTTPException

from ....domain.authentication.service import decode_admin_jwt_token
from ....domain.account.dto.Account import AccountPublicDto, AdminCreateAccountDTO, AccountDTO
from ....domain.account.service.AccountErrors import UserNameUniqueError, UserNotFoundError
from ....domain.account.service.AccountService import *
from ....infrastructure.persistence.database import get_db
from sqlalchemy.orm import Session


admin_account_router = APIRouter()

class ErrorResponse(BaseModel):
    detail: str



@admin_account_router.get('/', response_model=AccountPublicDto, responses={401: {"model": ErrorResponse}})
async def GetManyAccounts(
    start: int = 0,
    count: int | None = None,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
):
    return AccountPublicDto(**(await GetSlice(db, start, count)).__dict__)


@admin_account_router.get('/{id}/', response_model=AccountPublicDto, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}})
async def GetAccountById(
    id: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
):
    try:
        return AccountPublicDto(**(await GetById(db, id)).__dict__)
    except UserNotFoundError:
        raise HTTPException(status_code=400, detail='Id not found')

@admin_account_router.post('/', response_model=AccountPublicDto, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}})
async def CreateAccount(
    acc: AdminCreateAccountDTO,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
):
    try: 
        return AccountPublicDto(**(await Create(db, acc)).__dict__)
    except UserNameUniqueError:
        raise HTTPException(status_code=400, detail='Username already exists')


@admin_account_router.put('/{id}/', response_model=AccountPublicDto, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}})
async def UpdateAccount(
    id: int,
    toUpdate: AdminCreateAccountDTO,
    account: AccountDTO = Depends(decode_admin_jwt_token),
    db: Session = Depends(get_db)
):
    try: 
        res = AccountPublicDto(**(await ChangeAttrsById(db, id, toUpdate)).__dict__)
    except UserNameUniqueError:
        raise HTTPException(status_code=400, detail='Username already exists')
    return res


@admin_account_router.delete('/{id}/', response_model=AccountPublicDto, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}})
async def DeleteAccount(
    id: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
):
    try:
        return AccountPublicDto(**(await DeleteById(db, id)).__dict__)
    except UserNotFoundError:
        raise HTTPException(status_code=400, detail='Id not found')

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....presentation.dto.Error import ErrorResponse
from ....domain.account.dto.Account import AccountPublicDto, AccountDTO
from ....domain.account.service.AccountErrors import UserNotFoundError
from ....domain.account.service.AccountService import HesoyamById
from ....domain.authentication.service import decode_jwt_token
from ....infrastructure.persistence.database import get_db

payment_router = APIRouter()

@payment_router.post('/Hesoyam/{accountId}/',
    summary="Perform Hesoyam Operation",
    description="Perform the Hesoyam operation on the specified account.",
    response_model=AccountPublicDto,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    }
)
async def Hesoyam(
    accountId: int,
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ):
    if (not account.isAdmin) and account.id != accountId:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try: 
        acc = await HesoyamById(db, accountId)
        res = AccountPublicDto(**acc.__dict__)
    except UserNotFoundError:
        raise HTTPException(status_code=400, detail='User not found')
    return res
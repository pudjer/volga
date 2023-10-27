from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....domain.account.dto.Account import AccountPublicDto, AccountDTO
from ....domain.account.service.AccountErrors import UserNotFoundError
from ....domain.account.service.AccountService import HesoyamById
from ....domain.authentication.service import decode_jwt_token
from ....infrastructure.persistence.database import get_db

payment_router = APIRouter()

@payment_router.post('/Hesoyam/{accountId}/')
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
        raise HTTPException(status_code=400, detail='Id not found')
    return res
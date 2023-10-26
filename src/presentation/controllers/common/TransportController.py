from fastapi import APIRouter, Depends, HTTPException
from domain.account.dto.Account import AccountDTO
from sqlalchemy.orm import Session
from domain.authentication.service import decode_jwt_token
from domain.transport.dto.Transport import TransportCreateDTO, TransportDTO
from domain.transport.service.TransportErrors import TransportNotFoundError
from domain.transport.service.TransportService import GetTransportById
from infrastructure.persistence.database import get_db


transport_router = APIRouter()

@transport_router.get('/{id}/')
async def Get(id: int, db: Session = Depends(get_db)):
    try:
        return TransportDTO(**(await GetTransportById(db, id)).__dict__)
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')


@transport_router.post('/')
async def Add(transport: TransportCreateDTO, db: Session = Depends(get_db)):
    return 'me'

@transport_router.put('/{id}/')
async def Update():
    return 'me'

@transport_router.delete('/{id}/')
async def Delete():
    return 'me'



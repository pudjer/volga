from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ....domain.account.dto.Account import AccountDTO
from sqlalchemy.orm import Session
from ....domain.authentication.service import decode_jwt_token
from ....domain.transport.dto.Transport import TransportCreateDTO, TransportDTO, TransportDTOWithoutId
from ....domain.transport.service.TransportErrors import TransportNotFoundError
from ....domain.transport.service.TransportService import CreateTransport, DeleteTransport, GetTransportById, UpdateTransport
from ....infrastructure.persistence.database import get_db

class ErrorResponse(BaseModel):
    detail: str

transport_router = APIRouter()

@transport_router.get('/{id}/', response_model=TransportDTO, responses={400: {"model": ErrorResponse}})
async def Get(id: int, db: Session = Depends(get_db)):
    try:
        return await GetTransportById(db, id)
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')

@transport_router.post('/', response_model=TransportDTO, responses={400: {"model": ErrorResponse}})
async def Add(
    transport: TransportCreateDTO,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_jwt_token)
    ):
    toCreate = TransportDTOWithoutId(**transport.__dict__, ownerId=account.id)
    return await CreateTransport(db, toCreate)

@transport_router.put('/{id}/', response_model=TransportDTO, responses={400: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def Update(
    id: int,
    transport: TransportCreateDTO,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_jwt_token)
    ):
    try:
        owner =  (await GetTransportById(db, id)).ownerId
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')
    if owner != account.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    try:
        return await UpdateTransport(db, transport, id)
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')

@transport_router.delete('/{id}/', response_model=TransportDTO, responses={400: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def Delete(
    id: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_jwt_token)
    ):
    try:
        owner =  (await GetTransportById(db, id)).ownerId
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')
    if owner != account.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    try:
        return await DeleteTransport(db, id)
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')



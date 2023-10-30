from fastapi import APIRouter, Depends, HTTPException

from ....domain.common.Errors import CantBeDeletedError
from ...dto.Error import ErrorResponse
from ....domain.account.dto.Account import AccountDTO
from sqlalchemy.orm import Session
from ....domain.authentication.service import decode_jwt_token
from ....domain.transport.dto.Transport import TransportCreateDTO, TransportDTO, TransportDTOWithoutId
from ....domain.transport.service.TransportErrors import TransportNotFoundError
from ....domain.transport.service.TransportService import CreateTransport, DeleteTransport, GetTransportById, UpdateTransport
from ....infrastructure.persistence.database import get_db


transport_router = APIRouter()

@transport_router.get(
    '/{id}/',
    response_model=TransportDTO,
    responses={
        404: {"model": ErrorResponse, "description": "Transport not found"}
    },
    summary="Get a transport by ID",
    description="Get a transport by its ID."
)
async def Get(id: int, db: Session = Depends(get_db)):
    try:
        return TransportDTO(**(await GetTransportById(db, id)).__dict__)
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')

@transport_router.post(
    '/',
    response_model=TransportDTO,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"}, 401: {"model": ErrorResponse}
    },
    summary="Create a new transport",
    description="Create a new transport with the provided data."
)
async def Add(
    transport: TransportCreateDTO,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_jwt_token)
    ):
    toCreate = TransportDTOWithoutId(**transport.__dict__, ownerId=account.id)
    return TransportDTO(**(await CreateTransport(db, toCreate)).__dict__)

@transport_router.put(
    '/{id}/',
    response_model=TransportDTO,
    responses={
        404: {"model": ErrorResponse, "description": "Transport not found"},
        403: {"model": ErrorResponse, "description": "Forbidden"}, 401: {"model": ErrorResponse}
    },
    summary="Update a transport by ID",
    description="Update a transport by its ID."
)
async def Update(
    id: int,
    transport: TransportCreateDTO,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_jwt_token)
    ):
    try:
        owner =  (await GetTransportById(db, id)).ownerId
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')
    if owner != account.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    try:
        return TransportDTO(**(await UpdateTransport(db, transport, id)).__dict__)
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')

@transport_router.delete(
    '/{id}/',
    response_model=TransportDTO,
    responses={
        404: {"model": ErrorResponse, "description": "Transport not found"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        401: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    },
    summary="Delete a transport by ID",
    description="Delete a transport by its ID."
)
async def Delete(
    id: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_jwt_token)
    ):
    try:
        owner =  (await GetTransportById(db, id)).ownerId
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')
    if owner != account.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    try:
        return TransportDTO(**(await DeleteTransport(db, id)).__dict__)
    except CantBeDeletedError as e:
        raise HTTPException(status_code=400, detail=e.message)
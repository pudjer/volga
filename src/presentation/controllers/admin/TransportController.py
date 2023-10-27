from enum import Enum
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...dto.Error import ErrorResponse
from ....domain.transport.service.TransportErrors import OwnerNotFoundError, TransportNotFoundError
from ....domain.transport.dto.Transport import TransportDTO, TransportDTOWithoutId
from ....domain.transport.service.TransportService import CreateTransport, DeleteTransport, GetManyTransports, GetTransportById, UpdateTransport
from ....domain.account.dto.Account import AccountDTO
from ....domain.authentication.service import decode_admin_jwt_token
from ....infrastructure.persistence.database import get_db


admin_transport_router = APIRouter()


class TransportType(str, Enum):
    Car = 'Car'
    Bike = 'Bike'
    Scooter = 'Scooter'
    All = 'All'


@admin_transport_router.get(
    '/',
    response_model=list[TransportDTO],
    response_model_exclude_unset=True,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"}
    },
    summary="Get a list of transports",
    description="Get a list of transports with optional filtering parameters.",
)
async def GetMany(
    start: Annotated[int | None, Query(ge=1)] = 1,
    count: Annotated[int | None, Query(ge=0)] = None,
    transportType: Annotated[TransportType, Query()] = TransportType.All,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
):
    start -= 1
    transportType = transportType.value
    if transportType == 'All':
        transportType = None
    transports = await GetManyTransports(db, start, count, transportType)
    return [TransportDTO(**i.__dict__) for i in transports]

@admin_transport_router.get(
    '/{id}/',
    response_model=TransportDTO,
    response_model_exclude_unset=True,
    responses={
        404: {"model": ErrorResponse, "description": "Transport not found"}
    },
    summary="Get a single transport by ID",
    description="Get a single transport by its ID.",
)
async def GetOne(
    id: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try:
        return TransportDTO(**(await GetTransportById(db, id)).__dict__)
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')

@admin_transport_router.post(
    '/',
    response_model=TransportDTO,
    response_model_exclude_unset=True,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"}
    },
    summary="Add a new transport",
    description="Create a new transport with the provided data."
)
async def Add(
    transport: TransportDTOWithoutId,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try:
        return TransportDTO(**(await CreateTransport(db, transport)).__dict__)
    except OwnerNotFoundError:
        raise HTTPException(status_code=400, detail='Owner of transport not found')

@admin_transport_router.put(
    '/{id}/',
    response_model=TransportDTO,
    response_model_exclude_unset=True,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Transport not found"}
    },
    summary="Update an existing transport by ID",
    description="Update an existing transport with the provided data."
)
async def Update(
    id: int,
    transport: TransportDTOWithoutId,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try:
        return TransportDTO(**(await UpdateTransport(db, transport, id)).__dict__)
    except OwnerNotFoundError:
        raise HTTPException(status_code=400, detail='Owner of transport not found')
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')

@admin_transport_router.delete(
    '/{id}/',
    response_model=TransportDTO,
    response_model_exclude_unset=True,
    responses={
        404: {"model": ErrorResponse, "description": "Transport not found"}
    },
    summary="Delete a transport by ID",
    description="Delete a transport by its ID."
)
async def Delete(
    id: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try:
        return TransportDTO(**(await DeleteTransport(db, id)).__dict__)
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')
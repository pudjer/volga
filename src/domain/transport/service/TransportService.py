from datetime import datetime
from typing import List
from sqlalchemy.orm import Session, joinedload

from ....domain.common.Errors import CantBeDeletedError

from ...account.service.AccountErrors import UserNotFoundError

from ...account.service.AccountService import GetById
from .TransportErrors import OwnerNotFoundError, TransportNotFoundError
from ....infrastructure.persistence.models import TransportScheme
from ...transport.dto.Transport import TransportCreateDTO, TransportDTO, TransportDTOWithoutId


async def CreateTransport(db: Session, transport_create: TransportDTOWithoutId) -> TransportScheme:
    try: 
        await GetById(db, transport_create.ownerId)
    except UserNotFoundError:
        raise OwnerNotFoundError()
    try:
        transport = TransportScheme(**transport_create.model_dump())
        db.add(transport)
        db.commit()
        db.refresh(transport)
    except Exception as e:
        db.rollback()
        raise e
    return transport

async def UpdateTransport(db: Session, transport: TransportDTOWithoutId, id: int) -> TransportScheme:
    if hasattr(transport, 'ownerId'):
        try: 
            await GetById(db, id)
        except UserNotFoundError:
            raise OwnerNotFoundError()
    transportModel = db.query(TransportScheme).filter(TransportScheme.id == id).first()
    if not transportModel:
        raise TransportNotFoundError()
    try:
        transportProps = transport.model_dump()
        for (field, value) in transportProps.items():
            setattr(transportModel, field, value)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(transportModel)
    return transportModel

async def DeleteTransport(db: Session, transport_id: int) -> TransportScheme:
    transport = db.query(TransportScheme).options(joinedload(TransportScheme.rents)).filter(TransportScheme.id == transport_id).first()
    
    if not transport:
        db.rollback()
        raise TransportNotFoundError()

    current_time = datetime.now()
    
    # Check if the transport has any current rents
    if any(rent.timeEnd is None or rent.timeEnd > current_time for rent in transport.rents):
        db.rollback()
        raise CantBeDeletedError("Transport has current rentals and cannot be deleted")

    db.delete(transport)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return transport


async def GetTransportById(db: Session, transport_id) -> TransportScheme:
    res =  db.query(TransportScheme).filter(TransportScheme.id == transport_id).first()
    if not res:
        raise TransportNotFoundError()
    return res


async def GetManyTransports(db: Session, start: int, count: int, type: str) -> List[TransportScheme]:
    query = db.query(TransportScheme)
    if type is not None:
        query = query.filter(TransportScheme.transportType==type)
    if count is not None:
        query = query.slice(start, start + count)
    else:
        query = query.slice(start, None)
    transports = query.all()
    return transports


from sqlalchemy.orm import Session
from .TransportErrors import TransportNotFoundError
from ....infrastructure.persistence.models import TransportScheme
from ...transport.dto.Transport import TransportCreateDTO, TransportDTO, TransportDTOWithoutId


async def CreateTransport(db: Session, transport_create: TransportDTOWithoutId) -> TransportScheme:
    try:
        transport = TransportScheme(**transport_create.model_dump())
        db.add(transport)
        db.commit()
        db.refresh(transport)
    except Exception as e:
        db.rollback()
        raise e
    return transport

async def UpdateTransport(db: Session, transport: TransportCreateDTO, id: int) -> TransportScheme:
    transportModel = db.query(TransportScheme).filter(TransportScheme.id == id).first()
    if not transportModel:
        raise TransportNotFoundError()
    try:
        print(transport.model_dump())
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
    transport = db.query(TransportScheme).filter(TransportScheme.id == transport_id).first()
    if transport:
        db.delete(transport)
        db.commit()
    else:
        raise TransportNotFoundError()
    return transport


async def GetTransportById(db: Session, transport_id) -> TransportScheme:
    res =  db.query(TransportScheme).filter(TransportScheme.id == transport_id).first()
    if not res:
        raise TransportNotFoundError()
    return res


from sqlalchemy.orm import Session
from ....infrastructure.persistence.models.Transport import Transport
from ...transport.dto.Transport import TransportCreateDTO

def CreateTransport(db: Session, transport_create: TransportCreateDTO) -> Transport:
    try:
        transport = Transport(**transport_create.model_dump())
        db.add(transport)
        db.commit()
        db.refresh(transport)
    except Exception as e:
        db.rollback()
        raise e
    return transport

def UpdateTransport(db: Session, transport: TransportCreateDTO, id: int) -> Transport:
    transportModel = db.query(Transport).filter(Transport.id == id).first()
    try:
        for field, value in transport.model_dump():
            setattr(transportModel, field, value)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(transportModel)
    return transportModel

def DeleteTransport(db: Session, transport_id: int) -> Transport:
    transport = db.query(Transport).filter(Transport.id == transport_id).first()
    if transport:
        db.delete(transport)
        db.commit()
    else:
        db.rollback()
        raise
    return transport


def GetTransportById(db: Session, transport_id) -> Transport:
    try:
        return db.query(Transport).filter(Transport.id == transport_id).first()
    except Exception as e:
        raise e

def GetAllTransports(db: Session):
    try:
        return db.query(Transport).all()
    except Exception as e:
        raise e

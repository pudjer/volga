from datetime import datetime
import math
from sqlalchemy import func
from sqlalchemy.orm import Session

from ....domain.account.service.AccountService import GetById

from ....domain.transport.service.TransportService import GetTransportById

from ....domain.rent.service.RentErrors import AlreadyEndedError, CanNotBeRentedError, InsufficientBalanceError, RentNotFoundError
from ....domain.rent.dto.Rent import GetAvailableTransportDTO, Rent
from ....infrastructure.persistence.models import RentScheme, TransportScheme


async def GetAvailableTransport(db: Session, req: GetAvailableTransportDTO):
    req.type = req.type.value
    query = db.query(TransportScheme)
    if req.type != 'All':
        query = query.filter(TransportScheme.transportType == req.type)

    earth_radius = 6371

    available_transport = query.filter(
        TransportScheme.canBeRented == True,
        func.acos(
            func.sin(math.radians(req.lat)) * func.sin(func.radians(TransportScheme.latitude)) +
            func.cos(math.radians(req.lat)) * func.cos(func.radians(TransportScheme.latitude)) * func.cos(func.radians(TransportScheme.longitude - req.long))
        ) * earth_radius <= req.radius
    ).all()

    return available_transport

async def GetRentById(db: Session, id: int):
    res = db.query(RentScheme).filter(RentScheme.id == id).first()
    if not res:
        raise RentNotFoundError()
    return res


async def DeleteRentById(db: Session, id: int):
    res = await GetRentById(db, id)
    db.delete(res)
    db.refresh(res)
    return res

async def CreateRentAdmin(db: Session, rental: Rent):
    await GetById(db, rental.userId)
    transport = await GetTransportById(db, rental.transportId)
    transport.canBeRented = False
    timeStart = rental.timeStart
    priceType = rental.priceType
    priceOfUnit = rental.priceOfUnit
    newRental = RentScheme(transportId=rental.transportId, userId=rental.userId,
                           priceType=priceType, priceOfUnit=priceOfUnit,
                           timeStart=timeStart)
    db.add(newRental)
    db.commit()
    db.refresh(newRental)
    return newRental

async def UpdateRentById(db: Session, rental: Rent, id: int):
    await GetById(db, id)
    transport = await GetTransportById(db, rental.transportId)
    transport.canBeRented = False
    res = await GetRentById(db, id)
    for prop, value in rental.model_dump().items():
        setattr(res, prop, value)
    db.commit()
    db.refresh(res)
    return res


async def CreateRent(db: Session, transportId: int, userId: int, priceType: str):
    transport = await GetTransportById(db, transportId)
    if not transport.canBeRented:
        raise CanNotBeRentedError()
    if userId == transport.ownerId:
        raise CanNotBeRentedError('This is your transport')
    transport.canBeRented = False
    timeStart = datetime.now()
    if priceType == 'Days':
        dayPrice = transport.dayPrice
        if not dayPrice:
            raise CanNotBeRentedError('Transport hasn\'t day-price')
        priceOfUnit = dayPrice
    else:
        minutePrice = transport.minutePrice
        if not minutePrice:
            raise CanNotBeRentedError('Transport hasn\'t minute-price')
        priceOfUnit = minutePrice
    newRental = RentScheme(transportId=transportId, userId=userId,
                           priceType=priceType, priceOfUnit=priceOfUnit,
                           timeStart=timeStart)
    db.add(newRental)
    db.commit()
    db.refresh(newRental)
    return newRental
    
    
async def EndRentById(db: Session, rentId: int, lat:float, long:float):
    currentTime = datetime.now()
    rental = await GetRentById(db, rentId)
    if rental.timeEnd:
        raise AlreadyEndedError()
    transport = await GetTransportById(db, rental.transportId)
    provider = transport.owner
    user = rental.user
    rentType = rental.priceType
    timeInRent =  currentTime - rental.timeStart
    
    try:
        if rentType == 'Days':
            days = timeInRent.days
            price = rental.priceOfUnit * days
        else:
            minutes = math.ceil(timeInRent.seconds / 60)
            price = rental.priceOfUnit * minutes

        transport.canBeRented = True
        rental.finalPrice = price
        rental.timeEnd = currentTime
        user.balance -= price
        provider.balance += price
        transport.latitude = lat
        transport.longitude = long
        
        db.commit()
        db.refresh(rental)
        return rental
    except Exception as e:
        db.rollback()
        raise e
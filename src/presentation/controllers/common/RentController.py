from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....presentation.dto.Error import ErrorResponse
from ....domain.account.dto.Account import AccountDTO
from ....domain.account.service.AccountService import GetById
from ....domain.authentication.service import decode_jwt_token
from ....domain.rent.service.RentErrors import AlreadyEndedError, CanNotBeRentedError, InsufficientBalanceError, RentNotFoundError
from ....domain.transport.service.TransportErrors import TransportNotFoundError
from ....domain.transport.service.TransportService import GetTransportById
from ....domain.transport.dto.Transport import TransportDTO, TransportTypeWithAll
from ....domain.rent.dto.Rent import GetAvailableTransportDTO, PriceTypeEnum, Rent, RentWithId
from ....domain.rent.service.RentService import CreateRent, EndRentById, GetAvailableTransport, GetRentById
from ....infrastructure.persistence.database import get_db


rent_router = APIRouter()

@rent_router.get('/Transport/',
    summary="Get All Available Transport",
    description="Get a list of available transport based on location and type.",
    response_model=List[TransportDTO]

)
async def GetAllAwailableTransport(
    lat: Annotated[float, Query(ge=-90, le=90)],
    long: Annotated[float, Query(ge=-180, le=180)],
    radius: Annotated[float, Query(ge=0, le=20004, description="Radius in km.")],
    type: TransportTypeWithAll = TransportTypeWithAll.All,
    db: Session = Depends(get_db)
    ):
    query = GetAvailableTransportDTO(lat=lat, long=long, radius=radius, type=type)
    transports = await GetAvailableTransport(db, query)
    res = []
    for i in transports:
        res.append(TransportDTO(**i.__dict__))
    return res




@rent_router.get('/MyHistory/',
    summary="Get My Rental History",
    description="Get the rental history for the logged-in user.",
    response_model=List[RentWithId],
    responses={401: {"model": ErrorResponse}}
)
async def GetMyHistory(
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ) -> List[Rent]:
    acc = await GetById(db, account.id)
    rents = acc.rents
    res = []
    for i in rents:
        res.append(RentWithId(**i.__dict__))
    res = sorted(res, key=lambda x: x.timeStart)
    return res

@rent_router.get('/TransportHistory/{transportId}/',
    summary="Get Transport Rental History",
    description="Get the rental history for a specific transport.",
    response_model=List[RentWithId],
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def GetTransportHistory(
    transportId: int,
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ):
    try: 
        transport = await GetTransportById(db, transportId)
    except TransportNotFoundError:
        raise HTTPException(status_code=404, detail='Transport not found')
    if account.id != transport.ownerId:
        raise HTTPException(status_code=403, detail='Forbidden')
    rents = transport.rents
    res = []
    for i in rents:
        res.append(RentWithId(**i.__dict__))
    res = sorted(res, key=lambda x: x.timeStart)
    return res 

@rent_router.post('/New/{transportId}/',
    summary="Rent a Transport",
    description="Rent a transport with the specified parameters.",
    response_model=RentWithId,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def RentTransport(
    rentType: PriceTypeEnum, 
    transportId: int,
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ):
    rentType = rentType.value
    try:
        res = RentWithId(**(await CreateRent(db, transportId, account.id, rentType)).__dict__)
    except CanNotBeRentedError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')
    return res
    
@rent_router.post('/End/{rentId}/',
    summary="End a Rental",
    description="End a rental with the specified parameters.",
    response_model=RentWithId,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def EndRent(
    lat: Annotated[float, Query(ge=-90, le=90)],
    long: Annotated[float, Query(ge=-180, le=180)],
    rentId: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_jwt_token),
    ):
    try:
        if account.id != await GetRentById(db, rentId):
            raise HTTPException(status_code=403, detail='Forbidden')
    except RentNotFoundError:
            raise HTTPException(status_code=404, detail='Rental not found')
    try:
        res = RentWithId(**(await EndRentById(db, rentId, lat, long)).__dict__)
    except AlreadyEndedError:
        raise HTTPException(status_code=400, detail='Already ended')
    return res


    


@rent_router.get('/{rentId}/',
    summary="Get Rental by ID",
    description="Get a rental by its ID.",
    response_model=RentWithId,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def GetRent(
    rentId: int,
    account: AccountDTO = Depends(decode_jwt_token),
    db: Session = Depends(get_db)
    ):
    try:
        rent = await GetRentById(db, rentId)
    except RentNotFoundError:
        raise HTTPException(status_code=404, detail='Rental not found')
    userId = rent.userId
    transport = rent.transport
    providerId = transport.ownerId
    if account.id != userId and account.id != providerId:
        raise HTTPException(status_code=403, detail='Forbidden')
    else:
        return RentWithId(**(rent).__dict__)
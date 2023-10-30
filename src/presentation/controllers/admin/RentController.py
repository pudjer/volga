from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from ....domain.account.service.AccountErrors import UserNotFoundError
from ....domain.account.service.AccountService import GetById
from ....domain.rent.dto.Rent import Rent, RentWithId
from ....domain.rent.service.RentErrors import AlreadyEndedError, RentNotFoundError
from ....domain.transport.service.TransportErrors import TransportNotFoundError
from ....domain.transport.service.TransportService import GetTransportById
from ....presentation.dto.Error import ErrorResponse
from ....domain.rent.service.RentService import CreateRentAdmin, DeleteRentById, EndRentById, GetRentById, UpdateRentById
from ....domain.account.dto.Account import AccountDTO
from ....domain.authentication.service import decode_admin_jwt_token
from ....infrastructure.persistence.database import get_db
from sqlalchemy.orm import Session


admin_rent_router = APIRouter()

@admin_rent_router.get('/{rentId}/',
                      response_model=RentWithId,
                      summary="Get Rent by ID",
                      description="Retrieve a rent record by rent ID.",
                      responses={401: {'model': ErrorResponse}, 404: {'model': ErrorResponse}})
async def GetRent(
    rentId: int, 
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
):
    try:
        rent = await GetRentById(db, rentId)
    except RentNotFoundError:
        raise HTTPException(status_code=404, detail='Rental not found')
    return RentWithId(**rent.__dict__)

@admin_rent_router.get('/UserHistory/{userId}/',
                      summary="Get User Rent History",
                      description="Retrieve the rent history for a user by user ID.",
                      responses={404: {'model': ErrorResponse}, 401: {'model': ErrorResponse}})
async def GetUserHistory(
    userId: int, 
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try:
        acc = await GetById(db, userId)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail='User not found')
    rents = acc.rents
    res = []
    for i in rents:
        res.append(RentWithId(**i.__dict__))
    res = sorted(res, key=lambda x: x.timeStart)
    return res

@admin_rent_router.get('/TransportHistory/{transportId}/',
                      summary="Get Transport Rent History",
                      description="Retrieve the rent history for a transport by transport ID.",
                      responses={404: {'model': ErrorResponse}, 401: {'model': ErrorResponse}})
async def GetTransportHistory(
    transportId: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try: 
        transport = await GetTransportById(db, transportId)
    except TransportNotFoundError:

        raise HTTPException(status_code=404, detail='Transport not found')
    rents = transport.rents
    res = []
    for i in rents:
        res.append(RentWithId(**i.__dict__))
    res = sorted(res, key=lambda x: x.timeStart)
    return res 

@admin_rent_router.post('/',
                       response_model=RentWithId,
                       summary="Add a New Rent",
                       description="Create a new rent record.",
                       responses={400: {'model': ErrorResponse}, 401: {'model': ErrorResponse}})
async def AddRent(
    rental: Rent,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try: 
        res = await CreateRentAdmin(db, rental)
    except TransportNotFoundError:
        raise HTTPException(status_code=400, detail='Transport not found')
    except UserNotFoundError:
        raise HTTPException(status_code=400, detail='User not found')
    return RentWithId(**(res).__dict__)
    


@admin_rent_router.post('/End/{rentId}/',
                       response_model=RentWithId,
                       summary="End Rent",
                       description="End a rent by rent ID and provide end location coordinates.",
                       responses={404: {'model': ErrorResponse}, 401: {'model': ErrorResponse}, 400: {'model': ErrorResponse}})
async def EndRent(
    lat: Annotated[float, Query(ge=-90, le=90)],
    long: Annotated[float, Query(ge=-180, le=180)],
    rentId: int,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try:
        res = RentWithId(**(await EndRentById(db, rentId, lat, long)).__dict__)
    except AlreadyEndedError:
        raise HTTPException(status_code=400, detail='Already ended')
    except RentNotFoundError:
        raise HTTPException(status_code=404, detail='Rent not found')
    return res

@admin_rent_router.put('/{id}/',
                      response_model=RentWithId,
                      summary="Update Rent",
                      description="Update a rent record by rent ID.",
                      responses={400: {'model': ErrorResponse}, 401: {'model': ErrorResponse}, 404: {'model': ErrorResponse}})
async def UpdateRent(
    id: int,
    rental: Rent,
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
    ):
    try:
        res = await UpdateRentById(db, rental, id)
    except UserNotFoundError:
        raise HTTPException(status_code=401, detail='Rent not found')
    except TransportNotFoundError:
        raise HTTPException(status_code=401, detail='Transport not found')
    except RentNotFoundError:
        raise HTTPException(status_code=404, detail='Rental not found')
    return RentWithId(**res.__dict__)

@admin_rent_router.delete('/{id}/',
                         response_model=RentWithId,
                         summary="Delete Rent",
                         description="Delete a rent record by rent ID.",
                         responses={401: {'model': ErrorResponse}, 404: {'model': ErrorResponse}})
async def DeleteRent(rentId: int, 
    db: Session = Depends(get_db),
    account: AccountDTO = Depends(decode_admin_jwt_token)
):
    try:
        rent = await DeleteRentById(db, rentId)
    except RentNotFoundError:
        raise HTTPException(status_code=404, detail='Rental not found')
    return RentWithId(**rent.__dict__)




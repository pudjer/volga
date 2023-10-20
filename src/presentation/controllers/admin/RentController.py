from fastapi import APIRouter
from app import app


rent_router = APIRouter()


@rent_router.get('{rentId}')
async def GetRent():
    return {'username': 'str', 'password': 'str'}

@rent_router.get('/UserHistory/{userId}')
async def GetUserHistory():
    return {'username': 'str', 'password': 'str'}

@rent_router.get('TransportHistory/{transportId}')
async def GetTransportHistory():
    return {'username': 'str', 'password': 'str'}

@rent_router.post()
async def AddRent():
    return 'me'


@rent_router.post('/End/{rentId}')
async def EndRent():
    return 'me'

@rent_router.put('/{id}')
async def UpdateRent():
    return 'me'

@rent_router.delete('/{id}')
async def DeleteRent():
    return 'me'



app.include_router(rent_router, prefix="/Admin/Rent")
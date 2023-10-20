from fastapi import APIRouter
from app import app


rent_router = APIRouter()

@rent_router.get('/Transport')
async def GetAllAwailableTransport():
    return {'username': 'str', 'password': 'str'}

@rent_router.get('{rentId}')
async def GetRent():
    return {'username': 'str', 'password': 'str'}

@rent_router.get('/MyHistory')
async def GetMyHistory():
    return {'username': 'str', 'password': 'str'}

@rent_router.get('TransportHistory/{transportId}')
async def GetTransportHistory():
    return {'username': 'str', 'password': 'str'}

@rent_router.post('/New/{transportId}')
async def RentTransport():
    return 'me'

@rent_router.post('/End/{rentId}')
async def EndRent():
    return 'me'




app.include_router(rent_router, prefix="/Rent")
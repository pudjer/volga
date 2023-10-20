from fastapi import APIRouter
from app import app


transport_router = APIRouter()

@transport_router.get('/{id}')
async def Get():
    return {'username': 'str', 'password': 'str'}

@transport_router.post()
async def Add():
    return 'me'

@transport_router.put('/{id}')
async def Update():
    return 'me'

@transport_router.delete('/{id}')
async def Delete():
    return 'me'



app.include_router(transport_router, prefix="/Transport")
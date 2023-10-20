from fastapi import APIRouter
from app import app


account_router = APIRouter()

@account_router.get()
async def GetMany():
    return {'username': 'str', 'password': 'str'}

@account_router.get('/{id}')
async def GetById():
    return {'username': 'str', 'password': 'str'}

@account_router.post()
async def Create():
    return 'me'

@account_router.put('/{id}')
async def Update():
    return 'me'

@account_router.delete('/{id}')
async def Delete():
    return 'me'



app.include_router(account_router, prefix="/Admin/Account")
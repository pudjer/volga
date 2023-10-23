from fastapi import APIRouter


admin_account_router = APIRouter()

@admin_account_router.get('/')
async def GetMany():
    return {'username': 'str', 'password': 'str'}

@admin_account_router.get('/{id}/')
async def GetById():
    return {'username': 'str', 'password': 'str'}

@admin_account_router.post('/')
async def Create():
    return 'me'

@admin_account_router.put('/{id}/')
async def Update():
    return 'me'

@admin_account_router.delete('/{id}/')
async def Delete():
    return 'me'



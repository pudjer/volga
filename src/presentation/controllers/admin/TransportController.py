from fastapi import APIRouter


admin_transport_router = APIRouter()

@admin_transport_router.get('/')
async def GetMany():
    return {'username': 'str', 'password': 'str'}

@admin_transport_router.get('/{id}/')
async def GetOne():
    return {'username': 'str', 'password': 'str'}

@admin_transport_router.post('/')
async def Add():
    return 'me'

@admin_transport_router.put('/{id}/')
async def Update():
    return 'me'

@admin_transport_router.delete('/{id}/')
async def Delete():
    return 'me'



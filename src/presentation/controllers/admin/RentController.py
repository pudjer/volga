from fastapi import APIRouter


admin_rent_router = APIRouter()


@admin_rent_router.get('/UserHistory/{userId}/')
async def GetUserHistory():
    return {'username': 'str', 'password': 'str'}

@admin_rent_router.get('TransportHistory/{transportId}/')
async def GetTransportHistory():
    return {'username': 'str', 'password': 'str'}

@admin_rent_router.post('/')
async def AddRent():
    return 'me'


@admin_rent_router.post('/End/{rentId}/')
async def EndRent():
    return 'me'

@admin_rent_router.put('/{id}/')
async def UpdateRent():
    return 'me'

@admin_rent_router.delete('/{id}/')
async def DeleteRent():
    return 'me'

@admin_rent_router.get('/{rentId}/')
async def GetRent():
    return {'username': 'str', 'password': 'str'}



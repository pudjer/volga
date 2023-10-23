from fastapi import APIRouter

payment_router = APIRouter()

@payment_router.post('/Hesoyam/{accountId}/')
async def Hesoyam():
    return 'me'

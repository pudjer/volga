from fastapi import APIRouter
from app import app


account_router = APIRouter()

@account_router.get('/Me')
async def GetMe():
    return {'username': 'str', 'password': 'str'}

@account_router.post('/SignIn')
async def SignIn():
    return 'me'

@account_router.post('/SignUp')
async def SignUp():
    return 'me'

@account_router.post('/Update')
async def Update():
    return 'me'



app.include_router(account_router, prefix="/Account")
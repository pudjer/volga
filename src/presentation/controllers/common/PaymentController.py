from fastapi import APIRouter
from app import app


@app.post('/Payment/Hesoyam/{accountId}')
async def Hesoyam():
    return 'me'
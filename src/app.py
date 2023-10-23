from fastapi import APIRouter, FastAPI
from .infrastructure.persistence.database import engine, Base
from .infrastructure.persistence.models import *
from .presentation.controllers.common import *
from .presentation.controllers.admin import *
app = FastAPI()

@app.get('/')
def hello():
    return 'sdfads'

Base.metadata.create_all(bind=engine)

router = APIRouter()
router.include_router(account_router, prefix="/Account")
router.include_router(payment_router, prefix='/Payment')
router.include_router(rent_router, prefix="/Rent")
router.include_router(transport_router, prefix="/Transport")
router.include_router(admin_account_router, prefix="/Admin/Account")
router.include_router(admin_rent_router, prefix="/Admin/Rent")
router.include_router(admin_transport_router, prefix="/Admin/Transport")
app.include_router(router, prefix='/api')

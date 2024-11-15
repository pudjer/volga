from fastapi import APIRouter, FastAPI
from .domain.account.service.AccountService import Create
from .domain.account.dto.Account import AdminCreateAccountDTO
from .infrastructure.persistence.database import engine, Base, get_db
from .infrastructure.persistence.models import *
from .presentation.controllers.common import *
from .presentation.controllers.admin import *


app = FastAPI()


Base.metadata.create_all(bind=engine)

router = APIRouter()
router.include_router(account_router, prefix="/Account")
router.include_router(admin_account_router, prefix="/Admin/Account")
app.include_router(router, prefix='/api')

#create admin account
admin = AdminCreateAccountDTO(username="admin", password='admin', isAdmin=True, balance=0)
try:
    db = get_db().send(None)
    Create(db, admin).send(None)
except: pass

from fastapi import APIRouter,  status , Path, Depends 
from auth.utils import get_current_user
from sqlalchemy.orm import Session
from config.database import get_db
from auth.models import User
from .crud import create_order


router = APIRouter(prefix="/checkout", tags = ["Payment Checkout"])


@router.get("/", status_code = 201)
async def create_checkout( 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user
                                 )):
    return create_order(db,current_user)
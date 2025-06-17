from fastapi import APIRouter, Depends, Path
from auth.utils import get_current_user
from sqlalchemy.orm import Session
from config.database import get_db
from auth.models import User
from .crud import get_orders, get_order_detail


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", status_code=200)
async def get_order_history(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await get_orders(db, current_user)


@router.get("/{order_id}", status_code=200)
async def get_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_order_detail(order_id, db, current_user)

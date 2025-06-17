from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from auth.utils import get_current_user
from auth.models import User
from typing import List
from .schemas import CartCreate, CartResponse, CartUpdate, CartComplete
from .crud import add_to_cart, get_user_cart, update_cart_item, remove_from_cart

router = APIRouter(prefix="/cart", tags=["Cart Management"])


# Add a cart
@router.post("/", status_code=201)
async def add_product_to_cart(
    cart_data: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await add_to_cart(cart_data, db, current_user)


# View Cart
@router.get("/", status_code=200)
async def view_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await get_user_cart(db, current_user)


# Update a cart
@router.put("/", status_code=200)
async def update_cart_quantity(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_cart_item(product_id, quantity, db, current_user)


# Remove a cart
@router.delete("/{product_id}", status_code = 200)
async def remove_product_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await remove_from_cart(product_id, db, current_user)

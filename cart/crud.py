from .schemas import CartCreate, CartUpdate, CartResponse
from fastapi import HTTPException, status
from .models import Cart
from sqlalchemy.orm import Session
from auth.models import User


def add_to_cart(cart_data: CartCreate, db: Session, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="user not authorized")

    # Check if product already in cart
    existing_item = (
        db.query(Cart)
        .filter(
            Cart.user_id == current_user.id, Cart.product_id == cart_data.product_id
        )
        .first()
    )

    if existing_item:
        # Update quantity if exists
        existing_item.quantity += cart_data.quantity
    else:
        # Create new cart item
        new_cart = Cart(
            user_id=current_user.id,
            product_id=cart_data.product_id,
            quantity=cart_data.quantity,
        )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return {"message": "Product added to cart", "data": new_cart}


def get_user_cart(db: Session, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="user not authorized")

    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

    return {"data": cart_items}


def update_cart_item(product_id: int, quantity: int, db: Session, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="user not authorized")

    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id, Cart.product_id == product_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart"
        )

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)

    return {"message": "Cart updated successfully", "data": cart_item}


def remove_from_cart(product_id: int, db: Session, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="user not authorized")

    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id, Cart.product_id == product_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart"
        )

    db.delete(cart_item)
    db.commit()

    return {"Item removed from cart"}

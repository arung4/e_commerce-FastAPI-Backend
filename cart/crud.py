from .schemas import CartCreate, CartUpdate, CartResponse
from fastapi import HTTPException, status
from .models import Cart
from sqlalchemy.orm import Session
from auth.models import User
from config.logging import logger 
from exceptions.custom_exception import UserNotFoundException, AdminNotAllowedException, ProductNotFoundCartException

def add_to_cart(cart_data: CartCreate, db: Session, current_user: User):

    if not current_user:
        logger.error("***** USER NOT FOUND ******")
        raise UserNotFoundException()

    if current_user.role != "user":
        logger.error("***** ADMIN ROLE NOT ALLOWED TO ADD PRODUCT *****")
        raise AdminNotAllowedException()

    # Check if product already in cart
    existing_item = (
        db.query(Cart)
        .filter(
            Cart.user_id == current_user.id, Cart.product_id == cart_data.product_id
        )
        .first()
    )

    if existing_item:
        logger.info("***** PRODUCT ALREADY THEIR IN CART , UPDATING QUANTITY *****")
        # Update quantity if exists
        existing_item.quantity += cart_data.quantity
    else:
        logger.info("***** ADDING PRODUCT TO CART *****")
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
        logger.error("***** USER NOT FOUND *****")
        raise UserNotFoundException()

    if current_user.role != "user":
        logger.error("***** ADMIN NOT ALLOWED *****")
        raise AdminNotAllowedException()
    
    logger.info(" **** FETCHING USER CART ITEMS *****")
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

    return {"data": cart_items}


def update_cart_item(product_id: int, quantity: int, db: Session, current_user: User):

    if not current_user:
        logger.error("***** USER NOT FOUND *****")
        raise UserNotFoundException()

    if current_user.role != "user":
        logger.error("***** ADMIN NOT ALLOWED *****")
        raise AdminNotAllowedException()

    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id, Cart.product_id == product_id)
        .first()
    )

    if not cart_item:
        logger.error("***** ITEM NOT FOUND IN CART *****")
        raise ProductNotFoundCartException()

    logger.info("***** UPDATING PRODUCT QUANTITY IN CART *****")
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)

    logger.info("***** PRODUCT UPDATED IN CART *****")
    return {"message": "Cart updated successfully", "data": cart_item}


def remove_from_cart(product_id: int, db: Session, current_user: User):

    if not current_user:
        logger.error("***** USER NOT FOUND *****")
        raise UserNotFoundException()

    if current_user.role != "user":
        logger.error("***** ADMIN NOT ALLOWED *****")
        raise AdminNotAllowedException()

    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id, Cart.product_id == product_id)
        .first()
    )

    if not cart_item:
        logger.error("***** ITEM NOT FOUND IN CART *****")
        raise ProductNotFoundCartException()

    db.delete(cart_item)
    db.commit()
    logger.info("***** PRODUCT REMOVED FROM CART *****")
    return {"Item removed from cart"}

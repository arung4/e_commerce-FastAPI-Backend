from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from .models import Order, OrderItem
from auth.models import User
from config.logging import logger 
from exceptions.custom_exception import UserNotFoundException, AdminNotAllowedException, OrderNotFoundException

async def get_orders(db: Session, current_user: User):

    if not current_user:
        logger.error(" ***** USER NOT FOUND *****")
        raise UserNotFoundException()

    if current_user.role != "user":
        logger.error("***** ADMIN NOT ALLOWED *****")
        raise AdminNotAllowedException()

    orders = db.query(Order).filter(Order.user_id == current_user.id).all()

    logger.info("***** ORDERES FETCHED *****")
    return [
        {
            "order_id": order.id,
            "date": order.created_at,
            "total": order.total_amount,
            "status": order.status.value,
        }
        for order in orders
    ]


async def get_order_detail(order_id: int, db: Session, current_user: User):

    if not current_user:
        logger.error(" ***** USER NOT FOUND *****")
        raise UserNotFoundException()

    if current_user.role != "user":
        logger.error("***** ADMIN NOT ALLOWED *****")
        raise AdminNotAllowedException()

    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == current_user.id)
        .first()
    )

    if not order:
        logger.error("***** ORDER NOT FOUND *****")
        raise OrderNotFoundException()

    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    logger.info("***** ORDER DETAILS FETCHED *****")
    return {
        "order_id": order.id,
        "date": order.created_at,
        "total": order.total_amount,
        "status": order.status.value,
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "category": item.product.category,
                "price_at_purchase": item.price_at_purchase,
                "subtotal": item.quantity * item.price_at_purchase,
            }
            for item in items
        ],
    }

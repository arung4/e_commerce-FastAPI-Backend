from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from .models import Order, OrderItem
from auth.models import User


def get_orders(db: Session, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Only users can view orders")

    orders = db.query(Order).filter(Order.user_id == current_user.id).all()

    return [
        {
            "order_id": order.id,
            "date": order.created_at,
            "total": order.total_amount,
            "status": order.status.value,
        }
        for order in orders
    ]


def get_order_detail(order_id: int, db: Session, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Only users can view orders")

    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == current_user.id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

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

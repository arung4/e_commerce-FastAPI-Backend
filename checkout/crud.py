
from fastapi import HTTPException
from sqlalchemy.orm import Session 
from auth.models import User
from cart.models import Cart
from products.models import Product
from orders.models import Order, OrderItem , OrderStatus
from datetime import datetime


def create_order(db: Session , current_user: User): 

    if not current_user: 
        raise HTTPException(status_code = 401 , detail = "User not Authenticated")
    
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Only users can checkout")
    
    # Fetch users cart items 
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

    if not cart_items: 
        raise HTTPException(status_code=400, detail = "Cart is empty")
    
    total_amount = 0.0 
    order_items_response = []
    for item in cart_items: 
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product: 
            raise HTTPException(status_code = 404, detail = f"Product ID {item.product_id} Not found in the products list")
        
        total_amount += item.quantity * product.price 

        order_items_response.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": item.quantity,
            "category":product.category,
            "price_at_purchase": product.price,
        })


     # Create order
    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status=OrderStatus.PAID,
        created_at=datetime.now()
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Create order items 
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        db.add(order_item)


    # Clear cart 
    for item in cart_items: 
                db.delete(item)        

    db.commit()

    return {
                "message": "Checkout successfull",
                "order_id": new_order.id,
                "total_amount": new_order.total_amount,
                "status": new_order.status,
                "created_at": new_order.created_at,
                "items": order_items_response
            }           
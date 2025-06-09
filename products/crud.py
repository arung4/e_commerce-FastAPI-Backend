from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreate, ProductUpdate, ProductResponse
from fastapi import HTTPException
from auth.models import User




def create_product(db: Session, product_details: ProductCreate, current_user: User):

    if current_user.role != "admin": 
        raise HTTPException(status_code=403, detail="User not authorized")
    
    existing_product = db.query(Product).filter(Product.name == product_details.name).first()

    if existing_product: 
        raise HTTPException(status_code=400, detail="Product exist with this name")
    
    new_product = Product(
         name = product_details.name,
         description = product_details.description,
         price = product_details.price,
         stock = product_details.stock,
         category=product_details.category,
         image_url =product_details.image_url,
         admin_id = current_user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product added successfully",
        "user": new_product
    }

def get_all_products(db:Session , current_user: User, skip : int, limit:int):
       
       if current_user.role != "admin": 
        raise HTTPException(status_code=403, detail="User not authorized")
       
       prodcuts = db.query(Product).offset(skip).limit(limit).all()

       if not prodcuts: 
           raise HTTPException(status_code =500 , details = "Something went wrong while fetching records")
       
       return {
           "message": "Products fetched successfully", 
           "data": prodcuts
       }


       
       


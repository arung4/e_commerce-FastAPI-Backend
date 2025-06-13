from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreate, ProductUpdate, ProductResponse
from fastapi import HTTPException
from auth.models import User


def create_product(db: Session, product_details: ProductCreate, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="User not authorized")

    existing_product = (
        db.query(Product).filter(Product.name == product_details.name).first()
    )

    if existing_product:
        raise HTTPException(status_code=400, detail="Product exist with this name")

    new_product = Product(
        name=product_details.name,
        description=product_details.description,
        price=product_details.price,
        stock=product_details.stock,
        category=product_details.category,
        image_url=product_details.image_url,
        admin_id=current_user.id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully", "user": new_product}


def get_all_products(db: Session, current_user: User, skip: int, limit: int):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="User not authorized")

    products = (
        db.query(Product)
        .filter(Product.admin_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {"message": "Products fetched successfully", "data": products}


def get_product_by_id(db: Session, product_id: int, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="User not authorized")

    products = db.query(Product).filter(Product.admin_id == current_user.id).all()

    product = None
    for pro in products:
        if pro.id == product_id:
            product = pro
            break

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product fetched successfully", "user": product}


def update_product(
    db: Session, product_id: int, updated_data: ProductUpdate, current_user: User
):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="User not authorized")

    products = db.query(Product).filter(Product.admin_id == current_user.id).all()

    product = None
    for pro in products:
        if pro.id == product_id:
            product = pro
            break

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update fields
    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.stock = updated_data.stock
    product.category = updated_data.category
    product.image_url = updated_data.image_url

    db.commit()
    db.refresh(product)

    return {"message": "Product updated successfully", "user": product}


def delete_product(db: Session, product_id: int, current_user: User):

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="User not authorized")

    products = db.query(Product).filter(Product.admin_id == current_user.id).all()

    product = None
    for pro in products:
        if pro.id == product_id:
            product = pro
            break

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


# Public API functions


def list_public_products(
    db: Session,
    category: str | None,
    min_price: float | None,
    max_price: float | None,
    sort_by: str,
    page: int,
    page_size: int,
):

    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort_by == "price":
        query = query.order_by(Product.price)
    elif sort_by == "name":
        query = query.order_by(Product.name)
    elif sort_by == "category":
        query = query.order_by(Product.category)

    offset = (page - 1) * page_size

    products = query.offset(offset).limit(page_size).all()

    return {"message": "Products fetched successfully", "data": products}


def search_products_by_keyword(db: Session, keyword: str):

    products = (
        db.query(Product)
        .filter(
            Product.name.ilike(f"%{keyword}%")
            | Product.description.ilike(f"%{keyword}%")
            | Product.category.ilike(f"%{keyword}%")
        )
        .all()
    )
    if not products: 
        raise HTTPException(status_code =404, detail = "Products not exists")
    
    return {"message": "Products fetched successfully", "data": products}


def get_product_by_id_public(db: Session, product_id: int):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product fetched successfully", "user": product}

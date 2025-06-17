from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreate, ProductUpdate, ProductResponse
from fastapi import HTTPException
from auth.models import User
from config.logging import logger 
from exceptions.custom_exception import UserNotFoundException, UserNotAllowedException, ProductAlreadyExistsException , ProductNotFoundException


async def create_product(db: Session, product_details: ProductCreate, current_user: User):

    if not current_user:
        logger.error(" USER NOT FOUND ****")
        raise UserNotFoundException()

    if current_user.role != "admin":
        logger.error(" ****** USER NOT ALLOWED *****")
        raise UserNotAllowedException()

    existing_product = (
        db.query(Product).filter(Product.name == product_details.name).first()
    )

    if existing_product:
        logger.error("**** PRODUCT ALREADY THEIR *****")
        raise ProductAlreadyExistsException()

    logger.info("***** CREATING PRODUCT ENTRY *****")
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

    logger.info("***** PRODUCT SAVED IN DB *****")
    return {"message": "Product added successfully", "data": new_product}


async def get_all_products(db: Session, current_user: User, skip: int, limit: int):

    if not current_user:
        logger.error(" USER NOT FOUND ****")
        raise UserNotFoundException()

    if current_user.role != "admin":
        logger.error(" ****** NOT ALLOWED *****")
        raise UserNotAllowedException()

    products = (
        db.query(Product)
        .filter(Product.admin_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    logger.info("**** PRODUCTS FETCHED SUCCESS *****")
    return {"message": "Products fetched successfully", "data": products}


async def get_product_by_id(db: Session, product_id: int, current_user: User):

    if not current_user:
        logger.error(" USER NOT FOUND ****")
        raise UserNotFoundException()

    if current_user.role != "admin":
        logger.error(" ******USER NOT ALLOWED *****")
        raise UserNotAllowedException()

    products = db.query(Product).filter(Product.admin_id == current_user.id).all()

    product = None
    for pro in products:
        if pro.id == product_id:
            product = pro
            break

    if not product:
        logger.error(" ***** PRODUCT NOT FOUND WITH THIS ID *****")
        raise ProductNotFoundException()

    return {"message": "Product fetched successfully", "data": product}


async def update_product(
    db: Session, product_id: int, updated_data: ProductUpdate, current_user: User
):

    if not current_user:
        logger.error(" USER NOT FOUND ****")
        raise UserNotFoundException()

    if current_user.role != "admin":
        logger.error(" ******USER NOT ALLOWED *****")
        raise UserNotAllowedException()

    products = db.query(Product).filter(Product.admin_id == current_user.id).all()

    product = None
    for pro in products:
        if pro.id == product_id:
            product = pro
            break

    if not product:
        logger.error("***** PRODUCT NOT FOUND WITH THIS ID *****")
        raise ProductNotFoundException()

    # Update fields
    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.stock = updated_data.stock
    product.category = updated_data.category
    product.image_url = updated_data.image_url

    db.commit()
    db.refresh(product)

    logger.info("***** PRODUCT UPDATED *****")
    return {"message": "Product updated successfully", "data": product}


async def delete_product(db: Session, product_id: int, current_user: User):

    if not current_user:
        logger.error(" USER NOT FOUND ****")
        raise UserNotFoundException()

    if current_user.role != "admin":
        logger.error(" ******USER NOT ALLOWED *****")
        raise UserNotAllowedException()

    products = db.query(Product).filter(Product.admin_id == current_user.id).all()

    product = None
    for pro in products:
        if pro.id == product_id:
            product = pro
            break

    if not product:
        logger.error("***** PRODUCT NOT FOUND WITH THIS ID *****")
        raise ProductNotFoundException()

    db.delete(product)
    db.commit()

    logger.info(" ***** PRODUCT DELETED *****")
    return {"message": "Product deleted successfully"}


# Public API functions


async def list_public_products(
    db: Session,
    category: str | None,
    min_price: float | None,
    max_price: float | None,
    sort_by: str,
    page: int,
    page_size: int,
):

    query = db.query(Product)

    logger.info("***** FILTERING PRODUCTS *****")
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

    logger.info("**** PRODUCT FETCHED *****")

    return {"message": "Products fetched successfully", "data": products}


async def search_products_by_keyword(db: Session, keyword: str):

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
        logger.error("***** PRODUCT NOT FOUND WITH THIS KEYWORD *****")
        raise HTTPException(status_code =404, detail = "Products not exists")
    
    return {"message": "Products fetched successfully", "data": products}


async def get_product_by_id_public(db: Session, product_id: int):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        logger.error("***** PRODUCT NOT FOUND WITH THIS ID *****")
        raise ProductNotFoundException()

    return {"message": "Product fetched successfully", "data": product}

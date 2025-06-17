from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from auth.utils import get_current_user
from config.database import get_db
from .schemas import ProductResponse, AllProducts
from auth.models import User
from .crud import (
    get_product_by_id_public,
    list_public_products,
    search_products_by_keyword,
)


router = APIRouter(prefix="/public/products", tags=["View Products-Public"])

# Public API Endpoints


@router.get("/", response_model=AllProducts)
async def list_products(
    db: Session = Depends(get_db),
    category: str | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    sort_by: str = Query("price"),  # or category,name,price_range,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):

    return await list_public_products(
        db, category, min_price, max_price, sort_by, page, page_size
    )


@router.get("/search", response_model=AllProducts)
async def search_products(
    keyword: str = Query(..., min_length=2), db: Session = Depends(get_db)
):
    return await search_products_by_keyword(db, keyword)


# Get Product by ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(
    product_id: int = Path(..., gt=0),  # required path parameters , greater than > 0
    db: Session = Depends(get_db),
):
    return await get_product_by_id_public(db, product_id)

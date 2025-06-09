from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.utils import get_current_user
from config.database import get_db
from .schemas import ProductCreate,ProductResponse,ProductUpdate
from .models import Product
from auth.models import User
from .crud import create_product


router = APIRouter(prefix="/admin/products", tags=["Product Management"])


@router.post("/", response_model=ProductResponse)
async def product_create_endpoint(product_data: ProductCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)): 
    return create_product(db,product_data,current_user)



from fastapi import APIRouter, Depends , Path
from sqlalchemy.orm import Session
from auth.utils import get_current_user
from config.database import get_db
from .schemas import ProductCreate,ProductResponse,ProductUpdate , AllProducts
from .models import Product
from auth.models import User
from .crud import create_product , get_all_products , get_product_by_id , update_product , delete_product


router = APIRouter(prefix="/admin/products", tags=["Product Management"])

# Add a new product
@router.post("/", response_model=ProductResponse)
async def product_create_endpoint(product_data: ProductCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)): 
    return create_product(db,product_data,current_user)

# Get all products
@router.get("/",response_model=AllProducts)
async def products_fetch_endpoint(db: Session = Depends(get_db), current_user: User=Depends(get_current_user),skip: int = 0, limit: int = 100): 
    return get_all_products(db,current_user, skip = skip, limit=limit)


# Get Product by ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(
    product_id: int = Path(..., gt=0), # required path parameters , greater than > 0
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_product_by_id(db, product_id, current_user)

# Update Product
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_product(db, product_id, product_data, current_user)

# Delete Product
@router.delete("/{product_id}")
async def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_product(db, product_id, current_user)


       
       


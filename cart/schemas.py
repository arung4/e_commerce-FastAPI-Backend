from pydantic import BaseModel
from typing import Optional


class CartBase(BaseModel):
    product_id: int
    quantity: int = 1

    class Config:
        orm_mode = True


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    quantity: int


class CartComplete(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    product_price: float
    product_image: Optional[str]

    class Config:
        from_attributes = True


class CartResponse(CartComplete):
    message: str
    data: CartComplete

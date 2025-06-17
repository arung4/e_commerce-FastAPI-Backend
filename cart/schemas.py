from pydantic import BaseModel , field_validator
from typing import Optional


class CartBase(BaseModel):
    product_id: int
    quantity: int = 1

    @field_validator("product_id")
    def validate_productId(cls,v):
        if v < 0: 
            raise ValueError("Product must be positive")
        return v
    
    @field_validator("quantity")
    def validate_quantity(cls,v):
        if v < 0: 
            raise ValueError("Quantity must be positive")
        return v

    
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

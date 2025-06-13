from pydantic import BaseModel, field_validator
import re


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str | None = None

    # Validate name: not empty, allows alphanumeric + -@% only
    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        if len(v) < 3:
            raise ValueError("Name length must be greater than 3 characters.")
        if len(v) > 35:
            raise ValueError("Name length must be less-than 25 characters")
        if not re.match(r"^[A-Za-z0-9\s\-@%]+$", v):
            raise ValueError(
                "Name can only contain letters, numbers , spaces and basic punctuations."
            )

        return v

    # Validate description: not empty, alphanumeric + space + basic punctuation
    @field_validator("description")
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError("Description cannot be empty")
        if not re.match(r'^[A-Za-z0-9\s.,;:!?\'"-]+$', v):
            raise ValueError(
                "Description can contain only letters, numbers, spaces, and basic punctuation"
            )
        if len(v) > 200:
            raise ValueError("Description must be less than or equal to 200 characters")
        return v

    # Validate price: must be float, between 1 and 10,00,000 (customize if needed)
    @field_validator("price")
    def validate_price(cls, v):
        if v < 1.0:
            raise ValueError("Price must be at least 1.0")
        if v > 100000000.0:
            raise ValueError("Price cannot exceed 10,00,00000.0")
        return v

    # Validate stock: must be positive int
    @field_validator("stock")
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock cannot be negative")
        if v > 100000:
            raise ValueError("Stock cannot exceed 1,00,000 units")
        return v

    # Validate category: only alphabets, max 20 chars
    @field_validator("category")
    def validate_category(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        if not re.match(r"^[A-Za-z\s]+$", v):
            raise ValueError("Category must contain only letters and spaces")
        if len(v) > 20:
            raise ValueError("Category must be less than or equal to 20 characters")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductComplete(ProductBase):
    id: int
    admin_id: int

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    message: str
    user: ProductComplete

    class Config:
        orm_mode = True


class AllProducts(BaseModel):
    message: str
    data: list[ProductComplete]

    class Config:
        orm_mode = True

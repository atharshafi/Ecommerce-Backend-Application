from pydantic import BaseModel
from typing import Optional

# Base model for product with common fields
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    local_image_path: Optional[str] = None
    category: Optional[str] = None

# Model for creating a new product
class ProductCreate(ProductBase):
    pass

# Model for product with ID and ORM compatibility
class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True  # Enable ORM compatibility for DB models

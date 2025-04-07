from pydantic import BaseModel
from typing import List
from app.schemas.product import Product

# Base model for cart item with product ID and quantity
class CartItemBase(BaseModel):
    product_id: int
    quantity: int

# Model for creating a cart item
class CartItemCreate(CartItemBase):
    pass

# Model for updating a cart item (quantity only)
class CartItemUpdate(BaseModel):
    quantity: int

# Model for cart item with detailed product info
class CartItem(CartItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True  # Enable ORM compatibility

# Model for the shopping cart containing multiple items
class Cart(BaseModel):
    id: int
    items: List[CartItem]

    class Config:
        orm_mode = True  # Enable ORM compatibility

from pydantic import BaseModel
from typing import List
from app.schemas.product import Product

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItem(CartItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True

class Cart(BaseModel):
    id: int
    items: List[CartItem]

    class Config:
        orm_mode = True
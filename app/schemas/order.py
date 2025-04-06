from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemas.product import Product

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

class OrderItem(OrderItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    total_amount: float

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class Order(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True
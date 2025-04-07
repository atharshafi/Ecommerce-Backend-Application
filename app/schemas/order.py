from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemas.product import Product

# Base model for order item with product ID, quantity, and price at the time of purchase
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

# Model for order item including product details
class OrderItem(OrderItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True  # Enable ORM compatibility

# Base model for order with total amount
class OrderBase(BaseModel):
    total_amount: float

# Model for creating an order, includes list of order items
class OrderCreate(OrderBase):
    items: List[OrderItemBase]

# Model for order with detailed information, including items and creation timestamp
class Order(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True  # Enable ORM compatibility

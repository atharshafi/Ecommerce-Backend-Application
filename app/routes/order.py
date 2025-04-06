from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import Order, OrderCreate, OrderItem
from app.services.order import (
    create_order,
    get_user_orders,
    get_order_details,
    cancel_order
)
from app.services.auth import get_current_user
from app.schemas.user import User
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def create_new_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order from cart"""
    order = create_order(db, current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create order with empty cart"
        )
    return order

@router.get("/", response_model=List[Order])
def list_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all orders for current user"""
    return get_user_orders(db, current_user.id)

@router.get("/{order_id}", response_model=Order)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get order details"""
    order = get_order_details(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.post("/{order_id}/cancel", response_model=Order)
def cancel_user_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel an order"""
    order = cancel_order(db, order_id, current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be cancelled"
        )
    return order

@router.get("/{order_id}/items", response_model=List[OrderItem])
def get_order_items(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get items for specific order"""
    order = get_order_details(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order.items
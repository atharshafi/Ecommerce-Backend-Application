from sqlalchemy.orm import Session
from datetime import datetime
from app.models.order import (Order, OrderItem)
from app.models.cart import (Cart,CartItem)
from typing import Optional


def create_order(db: Session, user_id: int) -> Optional[Order]:
    """
    Creates an order from the user's cart
    Returns None if cart is empty
    """
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        return None

    # Calculate total amount
    total_amount = sum(
        item.product.price * item.quantity
        for item in cart.items
        if item.product  # Ensure product exists
    )

    # Create the order
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        created_at=datetime.utcnow(),
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Create order items
    for cart_item in cart.items:
        if not cart_item.product:
            continue  # Skip items with missing products

        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price_at_purchase=cart_item.product.price
        )
        db.add(order_item)

    # Clear the cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return order


def get_user_orders(db: Session, user_id: int) -> list[Order]:
    """Returns all orders for a user"""
    return db.query(Order).filter(Order.user_id == user_id) \
        .order_by(Order.created_at.desc()) \
        .all()


def get_order_details(db: Session, order_id: int) -> Optional[Order]:
    """Returns detailed order information"""
    return db.query(Order).filter(Order.id == order_id) \
        .first()


def cancel_order(db: Session, order_id: int, user_id: int) -> Optional[Order]:
    """
    Cancels an order if it's still pending
    Returns the cancelled order or None if cancellation failed
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id,
        Order.status == "pending"
    ).first()

    if not order:
        return None

    order.status = "cancelled"
    order.cancelled_at = datetime.utcnow()
    db.commit()
    db.refresh(order)

    return order


def get_order_items(db: Session, order_id: int) -> list[OrderItem]:
    """Returns all items for a specific order"""
    return db.query(OrderItem).filter(OrderItem.order_id == order_id) \
        .all()


def update_order_status(
        db: Session,
        order_id: int,
        new_status: str
) -> Optional[Order]:
    """
    Updates order status (admin function)
    Valid statuses: pending, processing, shipped, delivered, cancelled
    """
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        return None

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    order.status = new_status

    if new_status == "shipped":
        order.shipped_at = datetime.utcnow()
    elif new_status == "delivered":
        order.delivered_at = datetime.utcnow()

    db.commit()
    db.refresh(order)
    return order
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem


def get_user_cart(db: Session, user_id: int) -> Cart:
    """Get or create a cart for the user"""
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1) -> Cart:
    """Add an item to the cart"""
    cart = get_user_cart(db, user_id)

    # Check if item already exists in cart
    existing_item = next(
        (item for item in cart.items if item.product_id == product_id),
        None
    )

    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(new_item)

    db.commit()
    db.refresh(cart)
    return cart


def remove_from_cart(db: Session, user_id: int, product_id: int) -> Cart:
    """Remove an item from the cart"""
    cart = get_user_cart(db, user_id)
    item_to_remove = next(
        (item for item in cart.items if item.product_id == product_id),
        None
    )

    if item_to_remove:
        db.delete(item_to_remove)
        db.commit()
        db.refresh(cart)

    return cart


def clear_cart(db: Session, user_id: int) -> None:
    """Clear all items from the cart"""
    cart = get_user_cart(db, user_id)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()


def update_cart_item_quantity(
        db: Session,
        user_id: int,
        product_id: int,
        new_quantity: int
) -> Cart:
    """Update the quantity of an item in the cart"""
    if new_quantity <= 0:
        raise ValueError("Quantity must be positive")

    cart = get_user_cart(db, user_id)
    item = next(
        (item for item in cart.items if item.product_id == product_id),
        None
    )

    if not item:
        raise ValueError("Item not found in cart")

    item.quantity = new_quantity
    db.commit()
    db.refresh(cart)
    return cart
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem


def get_user_cart(db: Session, user_id: int) -> Cart:
    """Retrieve or create a cart for the user."""
    # Try to fetch the user's cart from the database
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        # Create a new cart if it doesn't exist for the user
        cart = Cart(user_id=user_id)
        db.add(cart)  # Add new cart to the session
        db.commit()  # Commit the transaction to save the cart
        db.refresh(cart)  # Refresh the cart instance with the latest data
    return cart


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1) -> Cart:
    """Add a product to the user's cart."""
    cart = get_user_cart(db, user_id)  # Retrieve or create user's cart

    # Check if the product is already in the cart
    existing_item = next(
        (item for item in cart.items if item.product_id == product_id),
        None
    )

    if existing_item:
        # If the item is already in the cart, increase the quantity
        existing_item.quantity += quantity
    else:
        # If it's a new product, create a new CartItem and add it to the cart
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(new_item)  # Add the new item to the session

    db.commit()  # Commit the changes to the database
    db.refresh(cart)  # Refresh the cart instance to include the updated items
    return cart


def remove_from_cart(db: Session, user_id: int, product_id: int) -> Cart:
    """Remove a product from the user's cart."""
    cart = get_user_cart(db, user_id)  # Retrieve the user's cart
    item_to_remove = next(
        (item for item in cart.items if item.product_id == product_id),
        None
    )

    if item_to_remove:
        # If the product exists in the cart, delete the item
        db.delete(item_to_remove)
        db.commit()  # Commit the changes to the database
        db.refresh(cart)  # Refresh the cart instance to reflect the update

    return cart


def clear_cart(db: Session, user_id: int) -> None:
    """Clear all items from the user's cart."""
    cart = get_user_cart(db, user_id)  # Retrieve the user's cart
    # Delete all items in the cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()  # Commit the transaction to clear the cart


def update_cart_item_quantity(
        db: Session,
        user_id: int,
        product_id: int,
        new_quantity: int
) -> Cart:
    """Update the quantity of an item in the user's cart."""
    if new_quantity <= 0:
        raise ValueError("Quantity must be positive")  # Validate positive quantity

    cart = get_user_cart(db, user_id)  # Retrieve the user's cart
    item = next(
        (item for item in cart.items if item.product_id == product_id),
        None
    )

    if not item:
        raise ValueError("Item not found in cart")  # Raise an error if the item is not in the cart

    # Update the quantity of the cart item
    item.quantity = new_quantity
    db.commit()  # Commit the changes to the database
    db.refresh(cart)  # Refresh the cart instance to reflect the updated quantity
    return cart

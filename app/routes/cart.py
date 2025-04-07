from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cart import Cart, CartItemCreate
from app.services.cart import (
    get_user_cart,
    add_to_cart,
    remove_from_cart,
    clear_cart
)
from app.services.auth import get_current_user
from app.schemas.user import User

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=Cart)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Retrieve current user's cart
    return get_user_cart(db, current_user.id)


@router.post("/items/", response_model=Cart)
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Add a product to the cart
    return add_to_cart(db, current_user.id, item.product_id, item.quantity)


@router.delete("/items/{product_id}", response_model=Cart)
def remove_item_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Remove a product from the cart
    cart = remove_from_cart(db, current_user.id, product_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )
    return cart


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_user_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Clear all items in the user's cart
    clear_cart(db, current_user.id)
    return None


@router.put("/items/{product_id}", response_model=Cart)
def update_cart_item(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Update the quantity of a specific cart item
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be positive"
        )

    cart = get_user_cart(db, current_user.id)
    item = next((i for i in cart.items if i.product_id == product_id), None)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )

    item.quantity = quantity
    db.commit()
    db.refresh(cart)
    return cart

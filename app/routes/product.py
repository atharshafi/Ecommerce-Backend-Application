from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import Product, ProductCreate
from app.services.product import get_products, create_product, get_product
from app.dependencies import get_admin_user  # Import your admin user dependency
from app.models.user import User  # Add this import if not already there
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=Product)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    # Removed 'admin' parameter as it's no longer needed.
    admin: User = Depends(get_admin_user)  # The check for admin is handled here
):
    return create_product(db=db, product=product)

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
from app.database import get_db
from app.schemas.product import Product, ProductCreate
from app.services.product import create_product, get_product, get_products
from app.dependencies import get_admin_user
from app.models.user import User
from app.utils.file_upload import save_upload_file
from fastapi import status

router = APIRouter(prefix="/products", tags=["products"])

# Endpoint to create a new product
@router.post("/", response_model=Product)
async def create_new_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    image_file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)  # Ensure the user is an admin
):
    # Ensure at least one image source is provided
    if not image_file and not image_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either image_file or image_url must be provided"
        )

    try:
        # Prepare product data for creation
        product_data = {
            "name": name,
            "description": description,
            "price": price,
            "category": category,
            "image_url": image_url
        }

        # Create the product in the database
        db_product = create_product(db, ProductCreate(**product_data))

        # Process image file if provided
        if image_file:
            # Save the image and update the product with the file path
            local_path = save_upload_file(image_file, db_product.id)
            db_product.local_image_path = local_path
            db.commit()
            db.refresh(db_product)

        return db_product

    except Exception as e:
        db.rollback()  # Rollback transaction if an error occurs
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )

# Endpoint to retrieve all products
@router.get("/", response_model=list[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

# Endpoint to retrieve a specific product by ID
@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

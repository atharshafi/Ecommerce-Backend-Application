from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of products, with pagination support.
    Skips the first 'skip' products and limits the result to 'limit' products.
    """
    return db.query(Product).offset(skip).limit(limit).all()  # Fetch products with pagination

def create_product(db: Session, product: ProductCreate):
    """
    Create a new product in the database.
    """
    db_product = Product(**product.dict())  # Instantiate a new Product object from the provided schema
    db.add(db_product)  # Add the new product to the session
    db.commit()  # Commit the transaction to save the product to the database
    db.refresh(db_product)  # Refresh the object to get the updated product with an ID
    return db_product  # Return the created product

def get_product(db: Session, product_id: int):
    """
    Retrieve a specific product by its ID.
    """
    return db.query(Product).filter(Product.id == product_id).first()  # Fetch the product by its ID

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, product, cart, order
from app.config import settings
from fastapi.staticfiles import StaticFiles

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files from the "uploads" directory under the "/uploads" path
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers for authentication, products, cart, and orders
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)


@app.get("/")
def read_root():
    """
    Root endpoint, serves as a simple health check for the API.
    """
    return {"message": "E-Commerce API"}


@app.on_event("startup")
def startup_event():
    """
    Event triggered at startup. Creates the first superuser if it doesn't already exist.
    This ensures an admin user is always available for the system.
    """
    from app.database import SessionLocal
    from app.models.user import User
    from app.utils.security import get_password_hash

    db = SessionLocal()
    try:
        # Check if the superuser already exists
        user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
        if not user:
            # Create and add the superuser to the database if it doesn't exist
            db_user = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_active=True,
                role="admin"
            )
            db.add(db_user)
            db.commit()
    finally:
        db.close()

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, product, cart, order
from app.config import settings

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)


@app.get("/")
def read_root():
    return {"message": "E-Commerce API"}


@app.on_event("startup")
def startup_event():
    # Create first superuser if doesn't exist
    from app.database import SessionLocal
    from app.models.user import User
    from app.utils.security import get_password_hash

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
        if not user:
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
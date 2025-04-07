from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    """
    Verify if the provided plain password matches the hashed password.
    Uses bcrypt for password comparison.
    """
    return pwd_context.verify(plain_password, hashed_password)  # Compare the plain and hashed passwords

def get_password_hash(password: str):
    """
    Generate a hashed password using bcrypt.
    """
    return pwd_context.hash(password)  # Hash the provided password

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT token with the provided data and expiration time.
    If no expiration is specified, defaults to 15 minutes.
    """
    to_encode = data.copy()  # Create a copy of the data dictionary
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Use provided expiration time if available
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiration time (15 minutes)
    to_encode.update({"exp": expire})  # Add expiration time to the payload
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.algorithm)  # Encode the JWT
    return encoded_jwt  # Return the generated JWT

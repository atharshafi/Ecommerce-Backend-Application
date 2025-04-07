from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

# Enum to define user roles
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

# Base model for user with email and full name
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

# Model for creating a new user with password and default role
class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.CUSTOMER

# Model for user with ID, active status, and role
class User(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        orm_mode = True  # Enable ORM compatibility for DB models

# Model for authentication token with access and type
class Token(BaseModel):
    access_token: str
    token_type: str

# Model for token data with optional email field
class TokenData(BaseModel):
    email: Optional[str] = None

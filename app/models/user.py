from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
from enum import Enum as PyEnum


class UserRole(PyEnum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)

    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.services.auth import get_current_user
from app.utils.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db_session():
    """Dependency that provides a DB session"""
    return Depends(get_db)


def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    """Dependency to get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_admin_user(
        current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency to verify admin privileges"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def get_customer_user(
        current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency to verify customer privileges"""
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action is restricted to customers"
        )
    return current_user


def verify_current_user(
        user_id: int,
        current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency to verify user owns the resource"""
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own resources"
        )
    return current_user


def get_verified_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency that verifies user exists and current user has access"""
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own resources"
        )

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


def get_password_verifier(
        plain_password: str,
        current_user: User = Depends(get_current_active_user)
) -> bool:
    """Dependency to verify user's password"""
    if not verify_password(plain_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    return True
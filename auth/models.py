from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from config.database import Base
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mobile = Column(String)
    role = Column(
        SQLEnum(UserRole), default=UserRole.user, nullable=False
    )  # e.g., "user", "admin"

    # reverse relationship with products

    products = relationship("Product", back_populates="admin")

    carts = relationship("Cart", back_populates="user")

    orders = relationship("Order", back_populates="user")

    resetToken = relationship("PasswordResetToken", back_populates="user")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True, nullable=False)
    expiration_time = Column(DateTime)
    used = Column(Boolean, default=False)

    user = relationship("User")

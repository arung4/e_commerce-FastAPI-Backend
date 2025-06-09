from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from config.database import Base
from enum import Enum as PyEnum

class UserRole(str,PyEnum): 
    user = 'user'
    admin = 'admin'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,autoincrement=True, index=True)
    email = Column(String,unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mobile = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.user, nullable = False)  # e.g., "user", "admin"

    # reverse relationship with products 

    products = relationship("Product", back_populates="admin")



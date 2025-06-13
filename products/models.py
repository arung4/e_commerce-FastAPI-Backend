from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    # FK TO admin(user) - to tell the db how both tables are related
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # relationship with admin(user) - for the Pytho orm code , that objects(products and users) are related
    admin = relationship("User", back_populates="products")

    carts = relationship("Cart", back_populates="product")

    order_items = relationship("OrderItem", back_populates="product")

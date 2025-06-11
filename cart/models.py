from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base



class Cart(Base): 
    __tablename__ = "carts"

    id = Column(Integer, primary_key = True,index=True, autoincrement = True)
    user_id =Column(Integer, ForeignKey("users.id"), index=True,nullable = False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable = False)
    quantity = Column(Integer, default = 1,nullable = False)

    # relationships with user, and products - for the python orm code, that objecs are related to each other

    user = relationship("User", back_populates="carts")
    product = relationship("Product", back_populates="carts")

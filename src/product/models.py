from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from src.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    total_price = Column(Float, nullable=False)
    status = Column(Enum('pending', 'completed', name='order_status'), nullable=False, default='pending')
    
    items = relationship("OrderItem", backref="order")



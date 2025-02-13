from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItem(OrderItemCreate):
    product: Product
    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    id: int
    items: List[OrderItem]
    total_price: float
    status: str
    model_config = ConfigDict(from_attributes=True)

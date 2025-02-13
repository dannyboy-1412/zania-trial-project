from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.product import models, schemas

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self):
        return self.db.query(models.Product).all()

    def create_product(self, product: schemas.ProductCreate):
        if product.price <= 0:
            raise ValueError("Price must be greater than 0")
        db_product = models.Product(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: schemas.OrderCreate):
        # Calculate total price and validate stock
        total_price = 0
        order_items = []
        
        for item in order.items:
            product = self.db.get(models.Product, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product {product.name}. Available: {product.stock}"
                )
            
            # Update stock
            product.stock -= item.quantity
            total_price += product.price * item.quantity
            
            # Create order item
            order_items.append(models.OrderItem(
                product_id=item.product_id,
                quantity=item.quantity
            ))
        
        # Create order
        db_order = models.Order(
            total_price=total_price,
            items=order_items
        )
        
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

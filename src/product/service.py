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
            
        if product.stock < 0:
            raise ValueError("Stock cannot be negative")
            
        try:
            db_product = models.Product(**product.model_dump())
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            return db_product
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: schemas.OrderCreate):
        if not order or not order.items:
            raise ValueError("Order must contain at least one item")

        total_price = 0
        order_items = []
        
        try:
            for item in order.items:
                if item.quantity <= 0:
                    raise ValueError(f"Quantity must be greater than 0 for product {item.product_id}")
                
                product = self.db.get(models.Product, item.product_id)
                if not product:
                    raise ValueError(f"Product {item.product_id} not found")
                
                if product.stock < item.quantity:
                    raise ValueError(
                        f"Insufficient stock for product {product.name}. Available: {product.stock}"
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
            
        except ValueError:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

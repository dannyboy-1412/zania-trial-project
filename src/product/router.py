from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.product import schemas
from src.product.service import ProductService, OrderService
from src.database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["Products"])

@router.get("/products", response_model=List[schemas.Product])
async def get_products(db: Session = Depends(get_db)):
    try:
        product_service = ProductService(db)
        return product_service.get_all_products()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching products"
        )

@router.post("/products", response_model=schemas.Product, status_code=201)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        product_service = ProductService(db)
        return product_service.create_product(product)
    except IntegrityError:

        raise HTTPException(
            status_code=400,
            detail="Product with this name already exists"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while creating product"
        )

@router.post("/orders", response_model=schemas.Order, status_code=201)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        order_service = OrderService(db)
        return order_service.create_order(order)
    except HTTPException as he:
        # Re-raise HTTP exceptions from the service
        raise he
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()  # Ensure any failed transaction is rolled back
        raise HTTPException(
            status_code=500,
            detail="Internal server error while creating order"
        )

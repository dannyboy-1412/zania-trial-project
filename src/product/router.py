from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.product import schemas
from src.product.service import ProductService, OrderService
from src.database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["Products"])

@router.get("/products", response_model=schemas.ResponseModel[List[schemas.Product]])
async def get_products(db: Session = Depends(get_db)):
    try:
        product_service = ProductService(db)
        return {
            "data": product_service.get_all_products(),
            "error": False,
            "message": "Products retrieved successfully"
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail={
                "data": None,
                "error": True,
                "message": "Internal server error while fetching products"
            }
        )

@router.post("/products", response_model=schemas.ResponseModel[schemas.Product], status_code=201)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        product_service = ProductService(db)
        return {
            "data": product_service.create_product(product),
            "error": False,
            "message": "Product created successfully"
        }
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail={
                "data": None,
                "error": True,
                "message": "Product with this name already exists"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "data": None,
                "error": True,
                "message": str(e)
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail={
                "data": None,
                "error": True,
                "message": "Internal server error while creating product"
            }
        )

@router.post("/orders", response_model=schemas.ResponseModel[schemas.Order], status_code=201)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        order_service = OrderService(db)
        return {
            "data": order_service.create_order(order),
            "error": False,
            "message": "Order created successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "data": None,
                "error": True,
                "message": str(e)
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "data": None,
                "error": True,
                "message": "Internal server error while creating order"
            }
        )

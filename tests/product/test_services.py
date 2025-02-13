import pytest
from sqlalchemy.orm import Session
from src.product.service import ProductService, OrderService
from src.product.schemas import ProductCreate, OrderCreate, OrderItemCreate
from src.product.models import Product, Order
from pydantic import ValidationError

def test_create_product(db_session: Session):
    product_service = ProductService(db_session)
    product_data = ProductCreate(
        name="Test Product",
        description="Test Description",
        price=10.0,
        stock=5
    )
    
    product = product_service.create_product(product_data)
    
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.stock == 5

def test_create_product_invalid_price(db_session: Session):
    with pytest.raises(ValidationError) as exc:
        product_data = ProductCreate(
            name="Test Product",
            description="Test Description",
            price=-10.0,
            stock=5
        )
    
    assert "Input should be greater than 0" in str(exc.value)

def test_create_order_insufficient_stock(db_session: Session):
    # Create a product with low stock
    product_service = ProductService(db_session)
    product_data = ProductCreate(
        name="Test Product",
        description="Test Description",
        price=10.0,
        stock=1
    )
    product = product_service.create_product(product_data)
    
    # Try to order more than available
    order_service = OrderService(db_session)
    order_data = OrderCreate(
        items=[
            OrderItemCreate(product_id=product.id, quantity=2)
        ]
    )
    
    with pytest.raises(Exception) as exc:
        order_service.create_order(order_data)
    assert "Insufficient stock" in str(exc.value)

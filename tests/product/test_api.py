from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.main import app
from src.database import get_db
import pytest

@pytest.fixture(name="client")
def client_fixture(db_session: Session):
    def override_get_db():
        return db_session
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_get_products(client: TestClient):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_create_product(client: TestClient):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "stock": 5
    }
    
    response = client.post("/api/v1/products", json=product_data)
    assert response.status_code == 201
    assert response.json()["data"]["name"] == product_data["name"]
    assert response.json()["data"]["price"] == product_data["price"]

def test_create_product_invalid_data(client: TestClient):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": -10.0,  # Invalid price
        "stock": 5
    }
    
    response = client.post("/api/v1/products", json=product_data)
    assert response.status_code == 422

def test_create_order(client: TestClient):
    # First create a product
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "stock": 5
    }
    product_response = client.post("/api/v1/products", json=product_data)
    product_id = product_response.json()["data"]["id"]
    
    # Create an order
    order_data = {
        "items": [
            {"product_id": product_id, "quantity": 2}
        ]
    }
    
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    assert len(response.json()["data"]["items"]) == 1
    assert response.json()["data"]["total_price"] == 20.0

def test_create_order_insufficient_stock(client: TestClient):
    # First create a product with low stock
    product_data = {
        "name": "Low Stock Product",
        "description": "Test Description",
        "price": 10.0,
        "stock": 1
    }
    product_response = client.post("/api/v1/products", json=product_data)
    product_id = product_response.json()["data"]["id"]
    
    # Try to order more than available
    order_data = {
        "items": [
            {"product_id": product_id, "quantity": 2}
        ]
    }
    
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]["message"]

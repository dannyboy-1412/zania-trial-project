# FastAPI Product API

A FastAPI application for managing products with SQLite database and Alembic migrations.

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized setup)

## Setup and Installation

### Local Setup

1. Clone the repository

```bash
git clone <repository-url>
cd fastapi-product-api
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```


4. Create a `.env` file based on `.env.example`

```bash
cp .env.example .env
```


5. Initialize the database and run migrations

```bash
alembic init alembic
alembic migrate
```

6. Run the application

```bash
uvicorn src.main:app --reload
```

7. Run the Tests

```bash
pytest tests/ -v  
```




### Docker Setup

1. Create a `.env` file based on `.env.example`

```bash
cp .env.example .env
```

2. Build the Docker image

```bash
docker build -t fastapi-product-api .
```

3. Run the Docker container

```bash
docker run -d -p 8000:8000 fastapi-product-api
```

4. Access the application

```bash
http://localhost:8000/
```

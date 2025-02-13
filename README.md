# FastAPI Product API

A FastAPI application for managing products with SQLite database and Alembic migrations.

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized setup)

## Setup and Installation


### Setup

1. Clone the repository

```bash
cd zania-trial-project
```

2. Create and activate a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create data directory for SQLite database

```bash
mkdir data
```

5. Create a `.env` file based on `.env.example` and update the configurations

```bash
cp .env.example .env
# Edit .env file with your configurations
```

6. Initialize the database and run migrations

```bash
alembic upgrade head
```



7. Run the application locally

```bash
uvicorn src.main:app --reload
```

8. Run the Tests

```bash
pytest tests/ -v  
```

### Docker Setup

1. Build the Docker image

```bash
docker build -t fastapi-product-api .
```

2. Run the Docker container

```bash
docker run -d -p 8000:8000 fastapi-product-api
```

### Access the application's API documentation

```bash
http://localhost:8000/docs
```

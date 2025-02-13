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


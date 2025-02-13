# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY src/ src/
COPY alembic/ alembic/
COPY tests/ tests/
COPY alembic.ini .
COPY .env .

# Create SQLite database directory
RUN mkdir -p /app/data

# Setup database and run migrations
RUN alembic upgrade head

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
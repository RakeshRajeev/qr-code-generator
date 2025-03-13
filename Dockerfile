# Build stage
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for QR codes
RUN mkdir -p /app/qr_codes

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m myuser && \
    chown -R myuser:myuser /app
USER myuser

ENV PYTHONPATH=/app

# Use python -m to ensure proper module execution
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

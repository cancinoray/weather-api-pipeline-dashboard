# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cache utilization
COPY requirements.txt .

# Install Python packages with specific versions
RUN pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY weather_pipeline.py .
COPY database_setup.sql .

# Create directories for volumes
RUN mkdir -p /app/logs /app/plots

# Run the application
CMD ["python", "weather_pipeline.py"]
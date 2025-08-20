# BrokerFlow AI - Dockerfile

# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        tesseract-ocr \
        libtesseract-dev \
        poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories
RUN mkdir -p inbox output templates logs

# Expose ports for API and Streamlit frontend
EXPOSE 8000
EXPOSE 8501

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Default command - can be overridden
CMD ["python", "main.py"]
# Use lightweight official Python slim image for optimization
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose application port
EXPOSE 5000

# Run with production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Use official Python image (slim for smaller size)
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev build-essential python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Create virtual environment
RUN python3.12 -m venv /opt/venv

# Activate virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run with uvicorn from virtualenv
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

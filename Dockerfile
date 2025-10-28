FROM python:3.12-slim

# Set working directory to /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Copenhagen

# Install system dependencies for psycopg2, Pillow, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into /app
COPY . .

# Ensure /app is in Python's path
ENV PYTHONPATH=/app

EXPOSE 2500

# Run manage.py inside the trustpilot-praktikplads-backend folder
CMD python trustpilot-praktikplads-backend/manage.py migrate --database=default && python trustpilot-praktikplads-backend/manage.py runserver 0.0.0.0:2500
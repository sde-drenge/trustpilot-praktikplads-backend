FROM python:3.12-slim

# Set working directory to /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Copenhagen

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files into /app
COPY . .

# Ensure /app is in Python's path
ENV PYTHONPATH=/app

EXPOSE 2500

# Run manage.py inside the trustpilot-praktikplads-backend folder
CMD ["sh", "-c", "\
  python backend/manage.py migrate --database=default && \
  python backend/manage.py runserver 0.0.0.0:2500 \
"]
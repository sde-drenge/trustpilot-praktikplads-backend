FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Copenhagen

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/*

# Work in /app
WORKDIR /app

# Install Python deps (copy reqs explicitly so Docker layer caching works)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copy ONLY the backend folder (where manage.py lives)
COPY backend/ /app/backend/

# Run from backend/
WORKDIR /app/backend

EXPOSE 2500

CMD sh -lc "python manage.py migrate --database=default && python manage.py runserver 0.0.0.0:2500"
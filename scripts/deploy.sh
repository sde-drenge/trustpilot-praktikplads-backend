#!/usr/bin/env bash
set -e

echo "Pulling latest changes..."
git pull

echo "Building new image..."
podman build -t localhost/trustpilotpraktikpladsbackend:latest .

echo "Stopping old container (if running)..."
podman stop trustpilotpraktikplads-backend 2>/dev/null || true
podman rm trustpilotpraktikplads-backend 2>/dev/null || true

echo "Starting new container..."
podman run -d \
  --name trustpilotpraktikplads-backend \
  -p 8080:2500 \
  --env-file .env \
  --restart unless-stopped \
  localhost/trustpilotpraktikpladsbackend:latest

echo "Deployment complete."
echo "Visit: http://<server-ip>:8080/admin"
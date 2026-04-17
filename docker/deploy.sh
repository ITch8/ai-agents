#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.prod.yml"

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: docker is not installed."
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "Error: docker compose or docker-compose is required."
  exit 1
fi

if [ ! -f "${PROJECT_ROOT}/.env" ]; then
  if [ -f "${PROJECT_ROOT}/.env.example" ]; then
    cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"
    echo "Created ${PROJECT_ROOT}/.env from .env.example"
    echo "Please edit .env with valid keys before production use."
  else
    echo "Error: missing .env and .env.example in ${PROJECT_ROOT}"
    exit 1
  fi
fi

cd "${SCRIPT_DIR}"

echo "Deploying with ${COMPOSE_FILE}"
echo "Step 1/3: Pull base images"
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" pull

echo "Step 2/3: Build application image"
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" build --pull

echo "Step 3/3: Start services"
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" up -d

echo "Deployment complete."
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" ps

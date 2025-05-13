#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until pg_isready -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}"; do
  echo "Still waiting for ${POSTGRES_HOST}:${POSTGRES_PORT}..."
  sleep 1
done
echo "Postgres is ready"

echo "Applying migrations"
alembic upgrade head

echo "Starting application: $@"
exec "$@"


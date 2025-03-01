#!/usr/bin/env bash

# This script cleans up LocalStack and restarts it using docker compose

# Stop and remove the LocalStack services using docker compose
docker compose down

# Remove all LocalStack volumes
docker volume rm $(docker volume ls -qf "name=localstack-main") || true

# Start LocalStack using docker compose
docker compose up -d

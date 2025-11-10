#!/usr/bin/env bash
set -euo pipefail

echo "Setting up environment..."
# Create a logs directory
mkdir -p logs

if [ -z "${DB_PASSWORD:-}" ]; then
  export DB_PASSWORD='example_secure_password'
  echo "DB_PASSWORD was not set - using temporary example value."
fi

echo "Environment ready"

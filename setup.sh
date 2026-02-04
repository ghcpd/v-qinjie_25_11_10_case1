#!/bin/bash

# Security Audit Setup Script for Linux/macOS
# This script sets up the environment to test the vulnerable and fixed code

set -e

echo "=== Security Audit Environment Setup ==="
echo "Platform: Linux/macOS"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Create logs directory
mkdir -p logs

# Set environment variable for testing
export DB_PASSWORD="test_password_123"

echo "=== Setup Complete ==="
echo "To run tests:"
echo "  source venv/bin/activate"
echo "  bash run_test.sh"

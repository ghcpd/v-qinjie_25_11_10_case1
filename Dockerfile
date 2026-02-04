FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY input.py input_fixed.py user_script.py test_*.py ./

# Set environment variable
ENV DB_PASSWORD="test_password_123"

# Create logs directory
RUN mkdir -p logs

# Run tests
CMD ["python", "test_original.py"]

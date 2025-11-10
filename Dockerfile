FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x run_test.sh || true
CMD ["python", "run_tests_auto.py"]

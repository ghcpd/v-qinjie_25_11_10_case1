FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["/bin/bash", "-lc", "python run_all_tests.py"]

# Generic Dockerfile for FastAPI microservices using SQLite
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY back_end/ ./back_end/
COPY app.py ./app.py

# Set PYTHONPATH to ensure all modules are discoverable
ENV PYTHONPATH=/app

# Expose port (override in docker-compose)
EXPOSE 8000

CMD ["uvicorn", "back_end.app:app", "--host", "0.0.0.0", "--port", "8000"]

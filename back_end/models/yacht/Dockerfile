FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8050"]

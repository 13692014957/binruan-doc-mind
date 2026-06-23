FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/.hf_models

EXPOSE 8000

ENV HF_ENDPOINT=https://hf-mirror.com
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/.hf_models
ENV DB_DIR=/app/data

VOLUME ["/app/.hf_models"]
VOLUME ["/app/data"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

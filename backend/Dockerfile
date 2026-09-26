FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/saidjadli/enterprise-ai-assistant"


WORKDIR /app


COPY backend/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000


CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000
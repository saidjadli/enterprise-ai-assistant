FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/saidjadli/enterprise-ai-assistant"

WORKDIR /app


COPY frontend/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY frontend .


EXPOSE 8501


CMD streamlit run app.py --server.address=0.0.0.0 --server.port=8501
# 🤖 Enterprise Knowledge Assistant

A production-oriented Generative AI application based on Retrieval
Augmented Generation (RAG).

## Features

-   JWT Authentication
-   PDF Document Management
-   RAG Pipeline
-   ChromaDB Vector Search
-   Persistent Conversations
-   Redis Memory
-   Source Citations
-   Docker Deployment

## Architecture

User → Streamlit Frontend → FastAPI Backend → RAG Pipeline → ChromaDB →
LLM

## Technology Stack

-   FastAPI
-   Streamlit
-   LangChain
-   ChromaDB
-   Redis
-   SQLite
-   Docker

## Run

``` bash
docker compose build
docker compose up
```

Frontend: http://localhost:8501

Backend: http://localhost:8000

Swagger: http://localhost:8000/docs

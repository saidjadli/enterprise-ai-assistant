# System Architecture

## Overview

The application follows a modular architecture composed of:

-   Frontend layer
-   API layer
-   Authentication layer
-   Conversation management
-   RAG processing layer
-   Storage layer

## Architecture Flow

    User
     |
    Streamlit Frontend
     |
    FastAPI Backend
     |
    +----------------+
    | Authentication |
    +----------------+

     |
    RAG Pipeline

    PDF → Extraction → Cleaning → Chunking → Embeddings → ChromaDB → LLM

     |
    Answer + Sources

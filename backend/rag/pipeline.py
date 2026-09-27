from backend.rag.loader import load_pdf
from backend.rag.splitter import split_documents
from backend.rag.vectorstore import create_vectorstore
from backend.rag.embeddings import get_embedding_model


def ingest_document(pdf_path):

    documents = load_pdf(pdf_path)

    chunks = split_documents(
        documents
    )

    embeddings = get_embedding_model()

    vectorstore = create_vectorstore(
        chunks,
        embeddings
    )

    return vectorstore
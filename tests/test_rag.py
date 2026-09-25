from backend.rag.pipeline import ingest_document


def test_rag_ingestion():

    vectorstore = ingest_document(
        "data/documents/security_policy.pdf"
    )

    assert vectorstore is not None

    print("RAG ingestion completed successfully")
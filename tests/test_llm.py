from backend.rag.pipeline import ingest_document
from backend.rag.retriever import get_retriever
from backend.rag.chain import create_rag_chain



PDF_PATH = "data/documents/security_policy.pdf"



def test_rag_generation():


    vectorstore = ingest_document(
        PDF_PATH
    )


    retriever = get_retriever(
        vectorstore
    )


    rag_chain = create_rag_chain(
        retriever
    )


    response = rag_chain.invoke(
        "What is the password recovery procedure?"
    )


    print(response)


    assert response is not None

    assert len(response) > 0
from backend.rag.pipeline import ingest_document
from backend.rag.retriever import get_retriever
from backend.rag.chain import create_rag_chain
from backend.rag.service import ask_question



PDF_PATH = (
"data/documents/security_policy.pdf"
)



def test_rag_with_sources():


    vectorstore = ingest_document(
        PDF_PATH
    )


    retriever = get_retriever(
        vectorstore
    )


    chain = create_rag_chain(
        retriever
    )


    response = ask_question(
        "What is the password recovery procedure?",
        retriever,
        chain
    )


    print("\nANSWER:")
    print(
        response["answer"]
    )


    print("\nSOURCES:")
    print(
        response["sources"]
    )


    assert "answer" in response

    assert "sources" in response

    assert len(
        response["sources"]
    ) > 0
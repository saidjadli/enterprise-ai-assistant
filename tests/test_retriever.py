from backend.rag.pipeline import ingest_document
from backend.rag.retriever import get_retriever



PDF_PATH = "data/documents/security_policy.pdf"



def test_retriever_search():

    # 1. Création du vectorstore
    vectorstore = ingest_document(
        PDF_PATH
    )


    # 2. Création du retriever
    retriever = get_retriever(
        vectorstore
    )


    # 3. Question utilisateur
    query = (
        "What is the password recovery procedure?"
    )


    # 4. Recherche sémantique
    documents = retriever.invoke(
        query
    )


    # 5. Vérifications
    assert documents is not None

    assert len(documents) > 0



    # Affichage pour inspection humaine
    print("\nRetrieved documents:")

    for doc in documents:

        print("----------------")

        print(
            doc.page_content[:300]
        )


def test_retrieved_content():

    vectorstore = ingest_document(
        PDF_PATH
    )


    retriever = get_retriever(
        vectorstore
    )


    docs = retriever.invoke(
        "How can I reset my password?"
    )


    contents = " ".join(
        doc.page_content.lower()
        for doc in docs
    )


    assert "password" in contents
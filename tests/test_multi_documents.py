from backend.rag.vectorstore import load_vectorstore


def test_multiple_documents():

    vectorstore = load_vectorstore()


    results = vectorstore.similarity_search(
        "network security policy",
        k=5
    )


    for doc in results:

        print(
            doc.metadata
        )


    assert len(results) > 0
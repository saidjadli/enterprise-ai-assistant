from backend.rag.llm import get_llm



def test_llm_connection():

    llm = get_llm()


    response = llm.invoke(
        "Explain what a RAG system is in one sentence."
    )


    print("\nLLM response:")
    print(response.content)


    assert response.content is not None

    assert len(response.content) > 0
from backend.rag.sources import extract_sources



def ask_question(
    question,
    retriever,
    rag_chain
):


    documents = retriever.invoke(
        question
    )


    answer = rag_chain.invoke(
        question
    )


    sources = extract_sources(
        documents
    )


    return {

        "answer": answer,

        "sources": sources

    }
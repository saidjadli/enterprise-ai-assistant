from langchain_chroma import Chroma



def create_vectorstore(
        chunks,
        embeddings
):


    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=
        "vectorstore/chroma_db"
    )


    return vectorstore
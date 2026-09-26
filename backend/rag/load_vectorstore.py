from langchain_chroma import Chroma

from backend.rag.embeddings import get_embedding_model


VECTORSTORE_PATH = "vectorstore/chroma_db"



def load_vectorstore():

    embeddings = get_embedding_model()


    vectorstore = Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings
    )


    return vectorstore
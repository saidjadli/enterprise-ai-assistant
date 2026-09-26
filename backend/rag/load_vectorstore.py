from langchain_chroma import Chroma

from backend.rag.embeddings import get_embedding_model
from backend.config.settings import settings





def load_vectorstore():

    embeddings = get_embedding_model()


    vectorstore = Chroma(
        persist_directory=settings.VECTORSTORE_PATH,
        embedding_function=embeddings
    )


    return vectorstore
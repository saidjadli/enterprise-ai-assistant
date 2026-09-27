from langchain_chroma import Chroma

from backend.rag.embeddings import get_embedding_model
from backend.config.settings import settings

from backend.utils.logger import get_logger


logger = get_logger(__name__)



def load_vectorstore():

    logger.info(
        "Loading vector database..."
    )


    embeddings = get_embedding_model()


    vectorstore = Chroma(
        persist_directory=settings.VECTORSTORE_PATH,
        embedding_function=embeddings
    )


    logger.info(
        "Vector database loaded successfully"
    )


    return vectorstore



def add_documents(chunks):

    logger.info(
        "Adding documents to vector database..."
    )


    vectorstore = load_vectorstore()


    vectorstore.add_documents(
        chunks
    )


    logger.info(
        "Documents added successfully"
    )


    return vectorstore
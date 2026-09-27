from langchain_chroma import Chroma

from backend.config.settings import settings
from backend.rag.embeddings import get_embedding_model
from backend.utils.logger import get_logger


logger = get_logger(__name__)


def create_vectorstore(
    chunks,
    embeddings
):

    logger.info(
        "Creating new vector database..."
    )


    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.VECTORSTORE_PATH
    )


    logger.info(
        "Vector database created"
    )


    return vectorstore



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



def add_documents(
    chunks
):

    logger.info(
        "Adding documents to existing vector database..."
    )


    vectorstore = load_vectorstore()


    vectorstore.add_documents(
        chunks
    )


    logger.info(
        "Documents added successfully"
    )


    return vectorstore

def delete_document_vectors(
    filename: str
):

    logger.info(
        f"Deleting vectors for document: {filename}"
    )


    vectorstore = load_vectorstore()


    collection = vectorstore._collection


    results = collection.get(
        where={
            "document_name": filename
        }
    )


    ids = results.get(
        "ids",
        []
    )


    if ids:

        collection.delete(
            ids=ids
        )


        logger.info(
            f"Deleted {len(ids)} vectors"
        )

    else:

        logger.warning(
            "No vectors found for document"
        )
from pathlib import Path
import shutil

from fastapi import UploadFile

from backend.config.settings import settings
from backend.rag.pipeline import ingest_document
from backend.utils.logger import get_logger
from backend.rag.vectorstore import delete_document_vectors

logger = get_logger(__name__)


DOCUMENT_PATH = Path(
    settings.DOCUMENT_PATH
)


DOCUMENT_PATH.mkdir(
    parents=True,
    exist_ok=True
)



def save_document(
    file: UploadFile
):

    file_path = DOCUMENT_PATH / file.filename


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    logger.info(
        f"Document saved: {file_path}"
    )


    return file_path



def index_document(
    file_path: Path
):

    logger.info(
        f"Indexing document: {file_path}"
    )


    ingest_document(
        str(file_path)
    )


    logger.info(
        "Document indexed successfully"
    )



def list_documents():

    documents = []


    for file in DOCUMENT_PATH.glob(
        "*.pdf"
    ):

        documents.append(
            {
                "filename": file.name,
                "size": file.stat().st_size
            }
        )


    return documents



def delete_document(
    filename: str
):

    file_path = DOCUMENT_PATH / filename


    if not file_path.exists():

        return False


    # supprimer le PDF

    file_path.unlink()


    # supprimer les embeddings Chroma

    delete_document_vectors(
        filename
    )


    logger.info(
        f"Document completely deleted: {filename}"
    )


    return True
from pathlib import Path
import shutil

from fastapi import UploadFile

from backend.config.settings import settings
from backend.rag.pipeline import ingest_document
from backend.rag.vectorstore import delete_document_vectors
from backend.utils.logger import get_logger

from backend.services.status_service import (
    update_document_status
)


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


    update_document_status(
        file.filename,
        "uploaded"
    )


    return file_path





def index_document(
    file_path: Path
):

    try:

        update_document_status(
            file_path.name,
            "processing"
        )


        logger.info(
            f"Starting indexing: {file_path.name}"
        )


        ingest_document(
            str(file_path)
        )


        update_document_status(
            file_path.name,
            "indexed"
        )


        logger.info(
            f"Indexing completed successfully: {file_path.name}"
        )


    except Exception as e:


        update_document_status(
            file_path.name,
            "failed",
            error=str(e)
        )


        logger.error(
            f"Indexing failed for {file_path.name}: {e}"
        )


        raise





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


    update_document_status(
        filename,
        "deleted"
    )


    logger.info(
        f"Document completely deleted: {filename}"
    )


    return True
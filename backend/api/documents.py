from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.document_service import (
    save_document,
    index_document,
    list_documents,
    delete_document
)

from backend.utils.logger import get_logger


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


logger = get_logger(__name__)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    logger.info(
        f"Uploading document: {file.filename}"
    )


    if not file.filename.endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )


    file_path = save_document(
        file
    )


    index_document(
        file_path
    )


    return {
        "message":
        "Document uploaded and indexed successfully",

        "filename":
        file.filename
    }



@router.get("/")
def get_documents():

    return list_documents()



@router.delete("/{filename}")
def remove_document(
    filename: str
):

    deleted = delete_document(
        filename
    )


    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    return {
        "message":
        "Document deleted successfully"
    }
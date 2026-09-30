from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    BackgroundTasks
)


from backend.services.document_service import (
    save_document,
    index_document,
    list_documents,
    delete_document
)


from backend.services.status_service import (
    get_document_status
)


from backend.utils.logger import get_logger



router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)



logger = get_logger(__name__)





@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):


    logger.info(
        f"Uploading document: {file.filename}"
    )



    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )



    file_path = save_document(
        file
    )



    background_tasks.add_task(
        index_document,
        file_path
    )



    return {

        "message":
        "Document uploaded successfully",

        "status":
        "processing",

        "filename":
        file.filename
    }





@router.get("/")
def get_documents():

    return list_documents()





@router.get("/status/{filename}")
def document_status(
    filename: str
):


    status = get_document_status(
        filename
    )


    if not status:

        raise HTTPException(
            status_code=404,
            detail="Document status not found"
        )


    return status





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
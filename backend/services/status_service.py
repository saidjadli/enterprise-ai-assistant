import json
from pathlib import Path
from datetime import datetime

from backend.utils.logger import get_logger


logger = get_logger(__name__)


STATUS_FILE = Path(
    "backend/storage/document_status.json"
)


STATUS_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


if not STATUS_FILE.exists():

    STATUS_FILE.write_text(
        "{}"
    )



def load_status():

    with open(
        STATUS_FILE,
        "r"
    ) as f:

        return json.load(f)



def save_status(data):

    with open(
        STATUS_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



def update_document_status(
    filename,
    status,
    chunks=None,
    error=None
):

    data = load_status()


    data[filename] = {

        "filename": filename,

        "status": status,

        "chunks": chunks,

        "error": error,

        "updated_at":
        datetime.utcnow().isoformat()

    }


    save_status(data)


    logger.info(
        f"Document status updated: {filename} -> {status}"
    )



def get_document_status(
    filename
):

    data = load_status()


    return data.get(
        filename
    )
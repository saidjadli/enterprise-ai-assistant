from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path


def load_pdf(file_path):

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    filename = Path(file_path).name


    for doc in documents:

        doc.metadata = {
            "document_name": filename,
            "source": filename,
            "page": doc.metadata.get("page", 0)
        }


    return documents
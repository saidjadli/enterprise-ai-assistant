import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(ROOT_DIR)
)


from backend.rag.pipeline import ingest_document



PDF_PATH = (
    "data/documents/security_policy.pdf"
)



def main():

    print(
        "Starting document ingestion..."
    )


    vectorstore = ingest_document(
        PDF_PATH
    )


    print(
        "Vectorstore created successfully"
    )



if __name__ == "__main__":

    main()
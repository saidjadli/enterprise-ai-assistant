import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(ROOT_DIR)
)


from backend.rag.pipeline import ingest_document



DOCUMENT_DIR = Path(
    "data/documents"
)



def main():

    print(
        "Starting documents ingestion..."
    )


    pdf_files = DOCUMENT_DIR.glob(
        "*.pdf"
    )


    count = 0


    for pdf in pdf_files:

        print(
            f"Ingesting: {pdf.name}"
        )


        ingest_document(
            str(pdf)
        )


        count += 1


    print(
        f"{count} documents indexed successfully"
    )



if __name__ == "__main__":

    main()
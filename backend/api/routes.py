from fastapi import APIRouter


from backend.api.schemas import (
    QuestionRequest,
    AnswerResponse
)


from backend.rag.pipeline import ingest_document

from backend.rag.retriever import get_retriever

from backend.rag.chain import create_rag_chain

from backend.rag.service import ask_question



router = APIRouter()



PDF_PATH = (
    "data/documents/security_policy.pdf"
)



# Initialisation RAG

vectorstore = ingest_document(
    PDF_PATH
)


retriever = get_retriever(
    vectorstore
)


rag_chain = create_rag_chain(
    retriever
)



@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(
    request: QuestionRequest
):


    response = ask_question(
        request.question,
        retriever,
        rag_chain
    )


    return response
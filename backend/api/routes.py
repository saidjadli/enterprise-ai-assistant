from uuid import uuid4

from fastapi import APIRouter
from fastapi import HTTPException


from backend.api.schemas import (
    QuestionRequest,
    AnswerResponse
)


from backend.rag.load_vectorstore import load_vectorstore
from backend.rag.retriever import get_retriever
from backend.rag.chain import create_rag_chain
from backend.rag.service import ask_question

from backend.memory.redis_memory import ConversationMemory


from backend.utils.logger import get_logger


logger = get_logger(__name__)


router = APIRouter()


# Initialisation RAG
vectorstore = load_vectorstore()


retriever = get_retriever(
    vectorstore
)


rag_chain = create_rag_chain(
    retriever
)


# Conversation memory
memory = ConversationMemory()


@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(
    request: QuestionRequest
):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )


    conversation_id = (
        request.conversation_id
        or str(uuid4())
    )


    logger.info(
        f"User question: {request.question} "
        f"| conversation_id={conversation_id}"
    )


    try:

        response = ask_question(
            request.question,
            conversation_id,
            retriever,
            rag_chain,
            memory
        )

        return response


    except Exception as e:

        logger.exception(
            "Error while processing question"
        )

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the question"
        ) from e


@router.delete(
    "/conversations/{conversation_id}"
)
def clear_conversation(
    conversation_id: str
):

    try:

        memory.clear(
            conversation_id
        )

        return {
            "message":
            "Conversation cleared successfully"
        }


    except Exception as e:

        logger.exception(
            "Error while clearing conversation"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to clear conversation"
        ) from e

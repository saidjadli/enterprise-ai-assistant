from backend.rag.sources import extract_sources
from backend.rag.query_rewriter import rewrite_query
from backend.utils.logger import get_logger


logger = get_logger(__name__)


def format_chat_history(history):

    if not history:

        return "No previous conversation."


    lines = []


    for message in history:

        role = message.get(
            "role",
            "user"
        ).upper()

        content = message.get(
            "content",
            ""
        )


        lines.append(
            f"{role}: {content}"
        )


    return "\n".join(
        lines
    )


def ask_question(
    question,
    conversation_id,
    retriever,
    rag_chain,
    memory
):


    history = memory.get_history(
        conversation_id
    )


    history_text = format_chat_history(
        history
    )



    standalone_query = rewrite_query(
        question,
        history_text
    )


    logger.info(
        f"Original question: {question}"
    )


    logger.info(
        f"Rewritten query: {standalone_query}"
    )


    documents = retriever.invoke(
        standalone_query
    )


    question_with_history = (
        "Conversation history:\n"
        f"{history_text}\n\n"
        "Current question:\n"
        f"{question}"
    )



    answer = rag_chain.invoke(
        {
            "context": documents,

            "question_with_history":
                question_with_history
        }
    )



    sources = extract_sources(
        documents
    )


    memory.add_message(
        conversation_id,
        "user",
        question
    )


    memory.add_message(
        conversation_id,
        "assistant",
        answer
    )



    return {

        "answer": answer,

        "sources": sources,

        "conversation_id":
            conversation_id

    }
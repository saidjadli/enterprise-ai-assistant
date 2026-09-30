from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from backend.rag.llm import get_llm


QUERY_REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a query rewriting assistant for an enterprise
document retrieval system.

Your task is to rewrite the user's current question into
a standalone question that can be understood without
the previous conversation.

Rules:
- Use the conversation history to resolve references such as:
  "it", "that", "this", "they", "the previous step", etc.
- Preserve the original meaning.
- Do not answer the question.
- Do not add information that is not present in the conversation.
- If the question is already standalone, keep its meaning unchanged.
- Return ONLY the rewritten standalone question.
- Do not add explanations.
"""
        ),
        (
            "human",
            """
Conversation history:
{history}

Current question:
{question}
"""
        )
    ]
)


def rewrite_query(
    question,
    history_text
):

    # No history means there is nothing to rewrite.
    if not history_text or history_text == "No previous conversation.":

        return question.strip()


    llm = get_llm()


    rewrite_chain = (
        QUERY_REWRITE_PROMPT
        |
        llm
        |
        StrOutputParser()
    )


    rewritten_query = rewrite_chain.invoke(
        {
            "history": history_text,
            "question": question
        }
    )


    return rewritten_query.strip()
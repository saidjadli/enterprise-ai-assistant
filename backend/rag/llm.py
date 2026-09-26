from langchain_groq import ChatGroq

from backend.config.settings import settings


def get_llm():

    llm = ChatGroq(
        model=settings.MODEL_NAME,
        temperature=0.1,
        api_key=settings.GROQ_API_KEY
    )

    return llm
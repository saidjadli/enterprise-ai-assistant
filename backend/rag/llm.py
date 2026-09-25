from langchain_groq import ChatGroq

from backend.config.settings import settings


def get_llm():

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.1,
        api_key=settings.groq_api_key
    )

    return llm
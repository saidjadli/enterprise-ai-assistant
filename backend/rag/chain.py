from langchain_core.output_parsers import StrOutputParser


from backend.rag.llm import get_llm
from backend.rag.prompts import RAG_PROMPT
from backend.rag.utils import format_documents


def create_rag_chain(
    retriever=None
):


    llm = get_llm()


    def build_context(inputs):

        documents = inputs.get(
            "context",
            []
        )


        return format_documents(
            documents
        )


    rag_chain = (

        {
            "context":
                build_context,

            "question":
                lambda inputs:
                inputs["question_with_history"]
        }

        |

        RAG_PROMPT

        |

        llm

        |

        StrOutputParser()

    )


    return rag_chain
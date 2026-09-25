from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


from backend.rag.llm import get_llm
from backend.rag.prompts import RAG_PROMPT
from backend.rag.utils import format_documents



def create_rag_chain(retriever):


    llm = get_llm()


    rag_chain = (

        {
            "context":
                retriever 
                | format_documents,

            "question":
                RunnablePassthrough()
        }

        |

        RAG_PROMPT

        |

        llm

        |

        StrOutputParser()

    )


    return rag_chain
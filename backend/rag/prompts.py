from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_template(
"""
You are an enterprise knowledge assistant.

Answer the question ONLY using the context below.

If the answer is not in the context,
say:
"I don't have enough information."


Context:

{context}


Question:

{question}


Answer:
"""
)
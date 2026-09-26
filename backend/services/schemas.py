from pydantic import BaseModel



class Source(BaseModel):

    document: str

    page: int | str



class RAGResponse(BaseModel):

    answer: str

    sources: list[Source]
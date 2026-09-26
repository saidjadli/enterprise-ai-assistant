from pydantic import BaseModel



class QuestionRequest(BaseModel):

    question: str



class SourceResponse(BaseModel):

    document: str

    page: int | str



class AnswerResponse(BaseModel):

    answer: str

    sources: list[SourceResponse]
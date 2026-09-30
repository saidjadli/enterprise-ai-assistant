from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
    conversation_id: str | None = None


class SourceResponse(BaseModel):
    document: str
    page: int | str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    conversation_id: str

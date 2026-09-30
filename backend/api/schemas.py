from pydantic import BaseModel, Field


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


class RegisterRequest(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: str

    password: str = Field(
        min_length=8,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: str

    password: str


class UserResponse(BaseModel):

    id: int

    username: str

    email: str

    role: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str

    user: UserResponse
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: str
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class MessageCreate(BaseModel):
    conversation_id: str
    role: str
    content: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: str
    role: str
    content: str
    created_at: datetime
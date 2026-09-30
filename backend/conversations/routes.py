from fastapi import APIRouter, Depends, HTTPException

from backend.auth.dependencies import get_current_user

from backend.conversations.service import (
    get_user_conversations,
    get_conversation_messages
)


router = APIRouter()



@router.get(
    "/conversations"
)
def list_conversations(
    current_user: dict = Depends(get_current_user)
):

    return get_user_conversations(
        current_user["id"]
    )



@router.get(
    "/conversations/{conversation_id}"
)
def conversation_history(
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):

    messages = get_conversation_messages(
        conversation_id
    )


    if not messages:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    return {
        "conversation_id": conversation_id,
        "messages": messages
    }
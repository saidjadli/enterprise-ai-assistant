from backend.conversations.service import (
    get_conversation_messages
)



def load_conversation_history(
    conversation_id
):

    messages = get_conversation_messages(
        conversation_id
    )


    history = []


    for message in messages:

        history.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )


    return history
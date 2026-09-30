import os
from uuid import uuid4

import requests
import streamlit as st


API_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000/api/ask"
)


st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖"
)


st.title(
    "🤖 Enterprise Knowledge Assistant"
)


st.write(
    "Ask questions about company documents."
)


# Persistent conversation identifier
if "conversation_id" not in st.session_state:

    st.session_state.conversation_id = str(
        uuid4()
    )


# UI history
if "messages" not in st.session_state:

    st.session_state.messages = []


# Start a new conversation
if st.button(
    "🆕 New conversation"
):

    clear_url = (
        API_URL.rsplit(
            "/api/ask",
            1
        )[0]
        + "/api/conversations/"
        + st.session_state.conversation_id
    )


    try:

        requests.delete(
            clear_url,
            timeout=10
        )

    except requests.RequestException:

        pass


    st.session_state.conversation_id = str(
        uuid4()
    )


    st.session_state.messages = []


    st.rerun()


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# User input
question = st.chat_input(
    "Ask your question..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    try:

        response = requests.post(

            API_URL,

            json={
                "question": question,
                "conversation_id":
                    st.session_state.conversation_id
            },

            timeout=180
        )


        response.raise_for_status()


        data = response.json()


        answer = data["answer"]

        sources = data["sources"]


        # Use the ID returned by the backend
        st.session_state.conversation_id = data[
            "conversation_id"
        ]


        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                answer
            )


            st.subheader(
                "📚 Sources"
            )


            for source in sources:

                st.write(
                    f"- {source['document']} "
                    f"(page {source['page']})"
                )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    except requests.RequestException as e:

        st.error(
            f"API Error: {e}"
        )


    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )

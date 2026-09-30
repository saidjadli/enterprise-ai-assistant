import streamlit as st
import requests
from datetime import datetime


API_URL = "http://backend:8000/api"


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================
# CSS
# =========================

st.markdown(
    """
<style>

.main-title {
    font-size:40px;
    font-weight:700;
}

.subtitle {
    color:#888;
    font-size:18px;
}


.source-card {
    background:#1f2937;
    padding:12px;
    border-radius:10px;
    margin-top:8px;
}


.sidebar-user {
    background:#111827;
    padding:15px;
    border-radius:12px;
}

</style>
""",
    unsafe_allow_html=True
)



# =========================
# Session state
# =========================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []



# =========================
# Headers
# =========================

def auth_headers():

    return {
        "Authorization": 
        f"Bearer {st.session_state.token}"
    }



# =========================
# Login
# =========================

def login():

    st.title("🔐 Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email":email,
                "password":password
            }
        )


        if response.status_code == 200:

            data=response.json()

            st.session_state.token = data["access_token"]
            st.session_state.user = data["user"]

            st.success("Login successful")

            st.rerun()

        else:

            st.error(
                response.json()
            )



# =========================
# Conversations
# =========================


def get_conversations():

    r=requests.get(
        f"{API_URL}/conversations",
        headers=auth_headers()
    )

    if r.status_code==200:
        return r.json()

    return []



def get_messages(cid):

    r=requests.get(
        f"{API_URL}/conversations/{cid}",
        headers=auth_headers()
    )

    if r.status_code==200:

        return r.json()["messages"]

    return []



def delete_conversation(cid):

    requests.delete(
        f"{API_URL}/conversations/{cid}",
        headers=auth_headers()
    )



# =========================
# Sidebar
# =========================

def sidebar():


    with st.sidebar:


        st.markdown(
            "## 🤖 Enterprise AI"
        )


        user=st.session_state.user


        st.markdown(
            f"""
<div class="sidebar-user">

👤 {user['email']}  

Role : {user['role']}

</div>
""",
            unsafe_allow_html=True
        )


        st.divider()



        if st.button(
            "🆕 New conversation",
            use_container_width=True
        ):

            st.session_state.conversation_id=None
            st.session_state.messages=[]
            st.rerun()



        st.divider()


        st.subheader(
            "💬 History"
        )


        conversations=get_conversations()


        for conv in conversations:


            col1,col2=st.columns(
                [5,1]
            )


            with col1:

                if st.button(
                    conv["title"][:30],
                    key=conv["id"],
                    use_container_width=True
                ):

                    st.session_state.conversation_id=conv["id"]

                    st.session_state.messages = get_messages(
                        conv["id"]
                    )

                    st.rerun()



            with col2:

                if st.button(
                    "🗑",
                    key="del"+conv["id"]
                ):

                    delete_conversation(
                        conv["id"]
                    )

                    st.rerun()



# =========================
# Chat
# =========================


def ask_question(question):


    payload={
        "question":question
    }


    if st.session_state.conversation_id:

        payload["conversation_id"] = (
            st.session_state.conversation_id
        )


    r=requests.post(
        f"{API_URL}/ask",
        json=payload,
        headers=auth_headers()
    )


    if r.status_code==200:

        return r.json()

    else:

        st.error(r.text)

        return None



def display_chat():


    st.markdown(
        """
<div class="main-title">
🤖 Enterprise Knowledge Assistant
</div>

<div class="subtitle">
Ask questions about company documents
</div>

<br>
""",
        unsafe_allow_html=True
    )



    for msg in st.session_state.messages:


        with st.chat_message(
            msg["role"]
        ):

            st.write(
                msg["content"]
            )



    question=st.chat_input(
        "Ask your question..."
    )


    if question:


        st.session_state.messages.append(
            {
                "role":"user",
                "content":question
            }
        )


        with st.chat_message("user"):

            st.write(question)



        response=ask_question(
            question
        )


        if response:


            st.session_state.conversation_id = (
                response["conversation_id"]
            )


            answer=response["answer"]


            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )


            with st.chat_message(
                "assistant"
            ):

                st.write(answer)


                if response.get("sources"):


                    st.markdown(
                        "### 📚 Sources"
                    )


                    for src in response["sources"]:

                        st.markdown(
                            f"""
<div class="source-card">

📄 {src['document']}  

Page : {src['page']}

</div>
""",
                            unsafe_allow_html=True
                        )



# =========================
# Application
# =========================


if st.session_state.token is None:


    login()


else:

    sidebar()

    display_chat()
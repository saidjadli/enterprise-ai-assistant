import streamlit as st
import requests
import json


API_URL = "http://backend:8000/api"


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


st.markdown(
    """
<style>

.stApp {
    background:#0f1117;
}


.main-title {
    font-size:42px;
    font-weight:800;
}


.subtitle {
    color:#9ca3af;
    font-size:18px;
}


.profile-card {

    background:#161b27;
    padding:20px;
    border-radius:15px;
    margin-bottom:20px;

}


.source-card {

    background:#161b27;
    border:1px solid #30363d;
    padding:15px;
    border-radius:12px;
    margin-top:10px;

}


</style>
""",
    unsafe_allow_html=True
)



if "token" not in st.session_state:

    st.session_state.token = st.query_params.get("token")


if "user" not in st.session_state:

    user_data = st.query_params.get("user")

    if user_data:
        st.session_state.user = json.loads(user_data)

    else:
        st.session_state.user = None



if "conversation_id" not in st.session_state:

    st.session_state.conversation_id = None



if "messages" not in st.session_state:

    st.session_state.messages = []




def headers():

    return {

        "Authorization":
        f"Bearer {st.session_state.token}"

    }




def save_session():

    st.query_params["token"] = st.session_state.token

    st.query_params["user"] = json.dumps(
        st.session_state.user
    )




def clear_session():

    st.query_params.clear()

    st.session_state.clear()




def login_page():


    st.markdown(
        """
<div class="main-title">
🔐 Login
</div>

<p class="subtitle">
Enterprise Knowledge Assistant
</p>
""",
        unsafe_allow_html=True
    )


    email = st.text_input(
        "Email"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button(
        "Login",
        use_container_width=True
    ):


        r = requests.post(

            f"{API_URL}/auth/login",

            json={

                "email":email,

                "password":password

            }

        )


        if r.status_code == 200:


            data = r.json()


            st.session_state.token = data["access_token"]

            st.session_state.user = data["user"]


            save_session()


            st.success(
                "Login successful"
            )


            st.rerun()


        else:

            st.error(
                "Invalid credentials"
            )




def get_conversations():


    r = requests.get(

        f"{API_URL}/conversations",

        headers=headers()

    )


    if r.status_code == 200:

        return r.json()


    return []




def get_conversation(cid):


    r = requests.get(

        f"{API_URL}/conversations/{cid}",

        headers=headers()

    )


    if r.status_code == 200:

        return r.json()["messages"]


    return []




def remove_conversation(cid):


    r = requests.delete(

        f"{API_URL}/conversations/{cid}",

        headers=headers()

    )


    return r.status_code == 200




def ask(question):


    payload = {

        "question": question

    }


    if st.session_state.conversation_id:

        payload["conversation_id"] = (
            st.session_state.conversation_id
        )


    r = requests.post(

        f"{API_URL}/ask",

        json=payload,

        headers=headers()

    )


    if r.status_code == 200:

        return r.json()


    st.error(r.text)

    return None


def get_documents():

    r = requests.get(
        f"{API_URL}/documents/",
        headers=headers()
    )

    if r.status_code == 200:
        return r.json()

    return []



def upload_document(file):

    files = {
        "file": (
            file.name,
            file,
            "application/pdf"
        )
    }

    r = requests.post(
        f"{API_URL}/documents/upload",
        files=files,
        headers=headers()
    )

    if r.status_code == 200:
        return r.json()

    return None



def delete_document(filename):

    r = requests.delete(
        f"{API_URL}/documents/{filename}",
        headers=headers()
    )

    return r.status_code == 200



def document_manager():

    st.divider()

    st.markdown("## 📚 Documents")

    documents = get_documents()

    for doc in documents:

        col1, col2 = st.columns([5,1])

        with col1:
            size = round(doc["size"] / 1024, 2)
            st.write(f"📄 {doc['filename']} ({size} KB)")

        with col2:
            if st.button("🗑", key="doc_delete_" + doc["filename"]):
                if delete_document(doc["filename"]):
                    st.success("Document deleted")
                    st.rerun()

    if not documents:
        st.info("No documents available")

    st.markdown("### ➕ Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button(
            "Upload document",
            use_container_width=True
        ):

            result = upload_document(uploaded_file)

            if result:
                st.success(
                    f"{result['filename']} uploaded"
                )
                st.info("Indexing started...")
                st.rerun()
            else:
                st.error("Upload failed")


def sidebar():


    with st.sidebar:


        st.markdown(
            "## 🤖 Enterprise AI"
        )


        user = st.session_state.user


        st.markdown(

            f"""

<div class="profile-card">

👤 <b>{user['email']}</b>

<br><br>

Role : {user['role']}

</div>

""",

            unsafe_allow_html=True

        )



        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):


            clear_session()

            st.rerun()



        st.divider()



        if st.button(
            "🆕 New conversation",
            use_container_width=True
        ):


            st.session_state.conversation_id = None

            st.session_state.messages = []

            st.rerun()



        st.divider()



        st.markdown(
            "## 💬 History"
        )



        conversations = get_conversations()



        for conv in conversations:


            col1,col2 = st.columns(
                [5,1]
            )



            with col1:


                if st.button(

                    conv["title"][:25],

                    key="open_"+conv["id"],

                    use_container_width=True

                ):


                    st.session_state.conversation_id = conv["id"]

                    st.session_state.messages = get_conversation(
                        conv["id"]
                    )

                    st.rerun()



            with col2:


                if st.button(

                    "🗑",

                    key="delete_"+conv["id"]

                ):


                    if remove_conversation(
                        conv["id"]
                    ):


                        if st.session_state.conversation_id == conv["id"]:

                            st.session_state.conversation_id = None

                            st.session_state.messages = []


                        st.success(
                            "Conversation deleted"
                        )


                        st.rerun()




        document_manager()


def welcome():


    st.markdown(

        """

<div class="main-title">

🤖 Enterprise Knowledge Assistant

</div>


<p class="subtitle">

Your AI assistant for company knowledge

</p>

""",

        unsafe_allow_html=True

    )



    st.write(
        "Suggested questions:"
    )



    suggestions = [

        "What are the recruitment steps?",

        "What are the network security rules?",

        "Explain cloud security policy"

    ]



    cols = st.columns(3)



    for col,text in zip(cols,suggestions):


        with col:


            if st.button(

                text,

                use_container_width=True,

                key=text

            ):


                response = ask(text)


                if response:


                    st.session_state.conversation_id = response["conversation_id"]


                    st.session_state.messages = [

                        {

                            "role":"user",

                            "content":text

                        },

                        {

                            "role":"assistant",

                            "content":response["answer"]

                        }

                    ]


                    st.rerun()




def chat():


    if not st.session_state.messages:


        welcome()



    for msg in st.session_state.messages:


        with st.chat_message(
            msg["role"]
        ):


            st.write(
                msg["content"]
            )



    question = st.chat_input(
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



        with st.chat_message("assistant"):


            with st.spinner(
                "Searching documents..."
            ):


                response = ask(
                    question
                )



            if response:


                st.session_state.conversation_id = response["conversation_id"]


                answer = response["answer"]


                st.write(answer)



                st.session_state.messages.append(

                    {

                        "role":"assistant",

                        "content":answer

                    }

                )



                if response.get("sources"):


                    st.markdown(
                        "### 📚 Sources"
                    )



                    for src in response["sources"]:


                        st.markdown(

                            f"""

<div class="source-card">

📄 {src['document']}

<br>

Page : {src['page']}

</div>

""",

                            unsafe_allow_html=True

                        )





if st.session_state.token is None:


    login_page()



else:


    sidebar()

    chat()
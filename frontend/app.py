import streamlit as st
import requests



API_URL = "http://127.0.0.1:8000/api/ask"



st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖"
)



st.title("🤖 Enterprise Knowledge Assistant")

st.write(
    "Ask questions about company documents."
)



# Historique conversation

if "messages" not in st.session_state:

    st.session_state.messages = []



# Affichage historique

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



# Input utilisateur

question = st.chat_input(
    "Ask your question..."
)



if question:


    # Ajouter question

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)



    # Appel API FastAPI

    try:

        response = requests.post(

            API_URL,

            json={
                "question": question
            }

        )


        data = response.json()



        answer = data["answer"]

        sources = data["sources"]



        # Afficher réponse

        with st.chat_message(
            "assistant"
        ):

            st.markdown(answer)



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
                "role":"assistant",
                "content":answer
            }

        )


    except Exception as e:

        st.error(
            f"API Error: {e}"
        )
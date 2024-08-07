import streamlit as st
from llm_model import MockModel
from chat_session import ChatSession
from sql_connection import get_database_session  # Import your SQLiteConnection class
import os  # Import os module for file operations

conn = get_database_session()

# Create the ChatSession object (only once)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession(connection=conn)

chat_session = st.session_state.chat_session

# --- Get URL Parameters ---
google_token = st.query_params.get("google_token")
persona_name = st.query_params.get("persona_name", "empty")
model_familly = st.query_params.get("model_familly", "Mock")
model_name = st.query_params.get("model_name", "mock:9b")
model_temperature = st.query_params.get("model_temperature", 1.0)


# --- Function to Update Chat Settings ---
def update_chat_settings(
    persona_name, model_familly, model_name, model_temperature
):
    """Updates the chat settings based on user input."""
    gemini_api_key = None

    if not (
        persona_name
        and (model_familly != "Gemini" or gemini_api_key and model_familly == "Gemini")
        and model_name
        and model_temperature
    ):
        return False

    chat_session.persona_path = (
        "personas/" + persona_name + "/" + persona_name + ".json"
    )
    chat_session.load_persona()  # Reload the persona

    if model_familly == "Mock":
        chat_session.update_model(
            MockModel(model_name=model_name, temperature=float(model_temperature))
        )
        return True
    else:
        st.warning("Please provide a valid model familly - " + model_familly)


is_model_initialized = update_chat_settings(
    persona_name, model_familly, model_name, model_temperature
)

st.info(
    f"Dani Stella, sua professora digital de redações da Unicamp, está ansiosa para lhe ajudar. Não seja tímida(o)! Tome a iniciativa e comece a conversa."
)

# --- Display Chat History ---
chat_history = chat_session.get_history()
for role, message in chat_history:
    if role == "assistant":
        avatar = "🧑‍💻"
    else:
        avatar = "🧑‍🎓"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message)

# --- User Input ---
prompt_input = st.chat_input("Me pergunte qualquer coisa!")

if not chat_session.is_model_initialized():
    st.warning("Por favor, selecione um modelo e atualize as configurações do chat.")
    st.stop()

# --- Send Prompt to Model ---
if prompt_input:
    # Display user message
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt_input)

    # Send prompt to chosen model and stream response
    with st.chat_message("assistant", avatar="🧑‍💻"):
        try:
            response_stream = chat_session.send_stream_message(prompt_input)
            response = st.write_stream(response_stream)
        except Exception as e:
            st.error("Error: " + str(e))

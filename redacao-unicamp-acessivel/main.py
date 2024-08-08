import streamlit as st
from chat_session import ChatSession
from llm_model import MockModel, GeminiModel
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
model_familly = st.query_params.get("model_familly", "Gemini")
model_name = st.query_params.get("model_name", "gemini-1.5-flash")
model_temperature = st.query_params.get("model_temperature", 1.0)


# --- Update Chat Settings ---
chat_session.persona_path = (
    "personas/" + persona_name + "/" + persona_name + ".json"
)
chat_session.load_persona()  # Reload the persona

is_model_initialized = False

if model_familly == "Mock":
    chat_session.update_model(
        MockModel(model_name=model_name, temperature=float(model_temperature))
    )

    is_model_initialized = True
elif model_familly == "Gemini":
    gemini_api_key = st.text_input(
        "Entre com sua chave de API Gemini",
        type="password",
        value=google_token,
    )

    if not gemini_api_key:
        st.warning("Por favor, forneça acima uma chave de API válida. Para criar uma chave, entre em: https://aistudio.google.com/app/apikey")
    else:
        chat_session.update_model(
            GeminiModel(
                model_name=model_name,
                api_key=gemini_api_key,
                temperature=float(model_temperature),
            )
        )

        is_model_initialized = True
else:
    raise "Familia de LLM invalida"

if is_model_initialized:
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

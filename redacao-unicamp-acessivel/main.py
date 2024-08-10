import streamlit as st
from chat_session import ChatSession
from llm_model import MockModel, GeminiModel
from sql_connection import get_database_session  # Import your SQLiteConnection class
import os  # Import os module for file operations

nome_da_plataforma = "Redação Unicamp Acessível: o caminho para a escrita leve e autoral na vida"

st.set_page_config(
    page_title=nome_da_plataforma,
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

conn = get_database_session()

# Create the ChatSession object (only once)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession(connection=conn)

chat_session = st.session_state.chat_session


@st.cache_resource
def create_gemini_model(model_name, gemini_api_key, model_temperature):
    return GeminiModel(
        model_name=model_name,
        api_key=gemini_api_key,
        temperature=float(model_temperature),
    )

# --- Get URL Parameters ---
google_token = st.query_params.get("google_token", "")
persona_name = st.query_params.get("persona_name", "dani_stella")
model_familly = st.query_params.get("model_familly", "Gemini")
model_name = st.query_params.get("model_name", "gemini-1.5-flash")
model_temperature = st.query_params.get("model_temperature", 1.0)


# --- Update Chat Settings ---
chat_session.load_persona(
    "personas/" + persona_name + "/" + persona_name + ".json"
)

is_model_initialized = False

_, profile_image, _ = st.columns([0.35, 0.3, 0.35])

with profile_image:
    st.markdown('<h2 style="text-align: center;">' + nome_da_plataforma + '</h2>', unsafe_allow_html=True)
    st.markdown("TODO: descricao do que e a plataforma e como utiliza-la")
    st.image("personas/dani_stella/dani_stella_the_digital_teacher_profile_picture.png", caption=chat_session.persona["nome_da_persona"], use_column_width="always")

st.divider()

colunas_personalidade = st.columns(len(chat_session.persona["personalidade_da_persona"]))

for personalidade, coluna in zip(chat_session.persona["personalidade_da_persona"], colunas_personalidade):
    with coluna:
        with st.popover(personalidade):
            st.empty()
        # st.caption(personalidade)

with st.expander("Sobre Dani Stella"):
    st.markdown(chat_session.persona["descricao_da_persona"])

model_settings_expanded = False
with st.expander("Configuracoes do modelo de Inteligência Artificial", expanded=model_settings_expanded):
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

        if gemini_api_key:
            gemini_model = create_gemini_model(
                model_name,
                gemini_api_key,
                model_temperature
            )
            chat_session.update_model(gemini_model)
            is_model_initialized = True
    else:
        raise "Familia de LLM invalida"

if is_model_initialized:
    st.info(
        f"Dani Stella, sua professora digital de redações da Unicamp, está ansiosa para lhe ajudar. Não seja tímida(o)! Tome a iniciativa e comece a conversa."
    )
else:
    st.warning("Por favor, forneça acima uma chave de API válida. Para criar uma chave, entre em: https://aistudio.google.com/app/apikey")

student_emoji = "🧑🏾‍🎓"
teacher_emoji = "👩🏾‍🏫"

# --- Display Chat History ---
chat_history = chat_session.get_history()
for role, message in chat_history:
    if role == "assistant":
        avatar = teacher_emoji
    else:
        avatar = student_emoji
    with st.chat_message(role, avatar=avatar):
        st.markdown(message)

# --- User Input ---
prompt_input = st.chat_input("Me pergunte qualquer coisa!")

if not chat_session.is_model_initialized():
    st.stop()

# --- Send Prompt to Model ---
if prompt_input:
    # Display user message
    with st.chat_message("user", avatar=student_emoji):
        st.markdown(prompt_input)

    # Send prompt to chosen model and stream response
    with st.chat_message("assistant", avatar=teacher_emoji):
        try:
            response_stream = chat_session.send_stream_message(prompt_input)
            response = st.write_stream(response_stream)
        except Exception as e:
            st.error("Error: " + str(e))

import json
import pandas
import streamlit as st
from chat_session import ChatSession
from llm_model import MockModel, GeminiModel
from sql_connection import get_database_session  # Import your SQLiteConnection class
import os  # Import os module for file operations

nome_da_plataforma = "Redação Unicamp Acessível: o caminho para a escrita leve e autoral"

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

column1, column2 = st.columns(2)

with column1:
    with st.expander("✍️ Redação Unicamp Acessível: a chave para a escrita leve e autoral"):
        with open("documentacao/secao_1_breve_descricao_plataforma.md") as f:
            st.markdown(f.read())

    with st.expander("🌎 A Unicamp: um portal para o futuro"):
        with open("documentacao/secao_2_a_unicamp.md") as f:
            st.markdown(f.read())

    with st.expander("🗝️ Redação Unicamp: desvendando os segredos da escrita"):
        with open("documentacao/secao_3_a_prova_de_redacao_unicamp.md") as f:
            st.markdown(f.read())

with column2:
    with st.expander("👩🏾‍🏫 Dani Stella: a professora digital que te guia na jornada da escrita"):
        with open("documentacao/secao_4_dani_stella_a_professora_digital.md") as f:
            _, dani_stella_imagem_col, _ = st.columns([0.3, 0.4, 0.3])

            with dani_stella_imagem_col:
                st.image("personas/dani_stella/dani_stella_the_digital_teacher_profile_picture.png", caption="")

                bin_prompt_persona = json.dumps(chat_session.persona).encode('utf-8')

                st.download_button(
                    label="Download do prompt de Dani Stella: a professora digital de redações",
                    data=bin_prompt_persona,
                    file_name="prompt_dani_stella.json",
                    mime="application/json",
                )

            st.markdown(f.read())

    # Seção com provas passadas
    with st.expander("📚 Provas de Redação Passadas: desvendando os segredos da Unicamp"):
        with open("documentacao/secao_5_prova_de_redacao_passadas.md") as f:
            st.markdown(f.read())

        propostas_redacoes = pandas.read_csv("dados/base_de_dados_proposta_redacoes.csv")
        st.dataframe(
            propostas_redacoes,
            column_config={
                "pdf_url": st.column_config.LinkColumn("PDF URL")
            },
            hide_index=True,
        )

    with st.expander("🙏 Agradecimentos"):
        with open("documentacao/secao_6_agradecimentos.md") as f:
            st.markdown(f.read())

# Seção para configurar o modelo do Google Gemini
with st.expander("⚙️ Configuracoes do modelo de Inteligência Artificial Gemini", expanded=True):
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
            placeholder="Acesse `https://aistudio.google.com/app/apikey` para criar esta chave",
            label_visibility="collapsed"
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

if not is_model_initialized:
    st.warning(
        "Por favor, adicione nas configurações acima sua chave de API do Google Gemini. Em seguida, comece a conversar com Dani Stella. Para criar uma chave de API nova, acesse: https://aistudio.google.com/app/apikey"
    )
else:
    st.info(
        "Dani Stella, sua professora digital de redações da Unicamp, está ansiosa para lhe ajudar. Informe no chat abaixo o número e ano da proposta que escolheu junto a sua redação para que Dani Stella lhe forneça uma avaliação detalhada."
    )


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
        with st.spinner(""):
            try:
                response_stream = chat_session.send_stream_message(prompt_input)
                response = st.write_stream(response_stream)
            except Exception as e:
                st.error("Error: " + str(e))

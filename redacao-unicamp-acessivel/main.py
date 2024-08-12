import json
import pandas
import streamlit as st
from chat_session import ChatSession
from llm_model import MockModel, GeminiModel
from sql_connection import get_database_session  # Import your SQLiteConnection class
import os  # Import os module for file operations

# Nome da plataforma
nome_da_plataforma = "Redação Unicamp Acessível: o caminho para a escrita leve e autoral"

# Configuração da página do Streamlit
st.set_page_config(
    page_title=nome_da_plataforma,
    page_icon="📚",
    layout="wide",  # Define o layout da página como "wide" para melhor visualização em telas maiores
    initial_sidebar_state="expanded",  # Define a barra lateral como expandida por padrão
)

# Conexão com o banco de dados SQLite
conn = get_database_session()

# Criação do objeto ChatSession (apenas uma vez)
if "chat_session" not in st.session_state:
    # Se a chave "chat_session" não existe na sessão do usuário, cria um novo objeto ChatSession
    st.session_state.chat_session = ChatSession(connection=conn)

# Define a variável chat_session como a sessão do usuário
chat_session = st.session_state.chat_session

# Função para criar um modelo Gemini (cache_resource garante que o modelo seja carregado apenas uma vez)
@st.cache_resource
def create_gemini_model(model_name, gemini_api_key, model_temperature):
    """Cria um modelo Gemini com base nos parâmetros fornecidos."""
    return GeminiModel(
        model_name=model_name,
        api_key=gemini_api_key,
        temperature=float(model_temperature),
    )

# --- Obtenção dos parâmetros da URL ---
google_token = st.query_params.get("google_token", "")  # Obtem o token do Google da URL
persona_name = st.query_params.get("persona_name", "dani_stella") # Obtem o nome da persona da URL
model_familly = st.query_params.get("model_familly", "Gemini") # Obtem a familia do modelo da URL
model_name = st.query_params.get("model_name", "gemini-1.5-flash") # Obtem o nome do modelo da URL
model_temperature = st.query_params.get("model_temperature", 1.0) # Obtem a temperatura do modelo da URL

# --- Carregamento da Persona ---
chat_session.load_persona(
    "personas/" + persona_name + "/" + persona_name + ".json"
) # Carrega a persona do arquivo JSON

# Flag para indicar se o modelo foi inicializado
is_model_initialized = False

# --- Layout da página ---
_, profile_image, _ = st.columns([0.35, 0.3, 0.35])  # Divide a página em três colunas
column1, column2 = st.columns(2)  # Divide a página em duas colunas

# --- Conteúdo da página ---
with column1:
    # Seção sobre a plataforma (expander permite expandir e recolher o conteúdo)
    with st.expander("✍️ Redação Unicamp Acessível: a chave para a escrita leve e autoral"):
        # Lê e exibe o conteúdo do arquivo Markdown
        with open("documentacao/secao_1_breve_descricao_plataforma.md") as f:
            st.markdown(f.read())

    # Seção sobre a Unicamp
    with st.expander("🌎 A Unicamp: um portal para o futuro"):
        # Lê e exibe o conteúdo do arquivo Markdown
        with open("documentacao/secao_2_a_unicamp.md") as f:
            st.markdown(f.read())

    # Seção sobre a redação da Unicamp
    with st.expander("🗝️ Redação Unicamp: desvendando os segredos da escrita"):
        # Lê e exibe o conteúdo do arquivo Markdown
        with open("documentacao/secao_3_a_prova_de_redacao_unicamp.md") as f:
            st.markdown(f.read())

with column2:
    # Seção sobre Dani Stella
    with st.expander("👩🏾‍🏫 Dani Stella: a professora digital que te guia na jornada da escrita autoral"):
        # Lê e exibe o conteúdo do arquivo Markdown
        with open("documentacao/secao_4_dani_stella_a_professora_digital.md") as f:
            # Converte a persona para JSON e codifica em UTF-8
            bin_prompt_persona = json.dumps(chat_session.persona).encode('utf-8')

            st.markdown(f.read())

            # Botão para download do prompt da persona
            st.download_button(
                label="Download do prompt de Dani Stella: a professora digital de redações",
                data=bin_prompt_persona,
                file_name="prompt_dani_stella.json",
                mime="application/json",
            )

    # Seção sobre provas passadas
    with st.expander("📚 Provas de Redação Passadas: desvendando os segredos da Unicamp"):
        # Lê e exibe o conteúdo do arquivo Markdown
        with open("documentacao/secao_5_prova_de_redacao_passadas.md") as f:
            st.markdown(f.read())

        # Lê a base de dados de provas de redação em formato CSV
        propostas_redacoes = pandas.read_csv("dados/base_de_dados_proposta_redacoes.csv")

        # Exibe a tabela com as provas de redação
        st.dataframe(
            propostas_redacoes,
            column_config={
                # Define a coluna "pdf_url" como um link para o PDF
                "pdf_url": st.column_config.LinkColumn("PDF URL")
            },
            hide_index=True,  # Oculta o índice da tabela
        )

    # Seção de agradecimentos
    with st.expander("🙏 Agradecimentos"):
        # Lê e exibe o conteúdo do arquivo Markdown
        with open("documentacao/secao_6_agradecimentos.md") as f:
            st.markdown(f.read())

# --- Seção de configuração do modelo Gemini ---
with st.expander("⚙️ Configurações do modelo de Inteligência Artificial Gemini", expanded=True):
    # Verifica se a familia de modelo é Mock
    if model_familly == "Mock":
        # Inicializa o modelo Mock
        chat_session.update_model(
            MockModel(model_name=model_name, temperature=float(model_temperature))
        )

        # Define a flag como True, indicando que o modelo foi inicializado
        is_model_initialized = True

    # Verifica se a familia de modelo é Gemini
    elif model_familly == "Gemini":
        # Campo de entrada para a chave de API do Google Gemini
        gemini_api_key = st.text_input(
            "Entre com sua chave de API Gemini",
            type="password",  # Define o campo como "password" para ocultar a chave
            value=google_token,  # Define o valor inicial da chave como o token obtido da URL
            placeholder="Acesse `https://aistudio.google.com/app/apikey` para criar esta chave",
            label_visibility="collapsed"  # Oculta o rótulo do campo
        )

        # Lista dos modelos Gemini disponíveis
        models = ("gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-pro-exp-0801")
        model_idx = models.index(model_name)  # Obtem o índice do modelo atual na lista

        # Caixa de seleção para escolher o modelo Gemini
        model_name = st.selectbox(
            "Modelo Gemini?",
            models,
            index=model_idx,  # Define o índice inicial da caixa de seleção
            placeholder="Selecione seu modelo Gemini...",
        )

        # Verifica se a chave de API foi fornecida
        if gemini_api_key:
            if chat_session.model_name != model_name:
                # Cria o modelo Gemini
                gemini_model = create_gemini_model(
                    model_name,
                    gemini_api_key,
                    model_temperature
                )
                # Define o modelo Gemini para a sessão
                chat_session.update_model(model_name, gemini_model)

            # Define a flag como True, indicando que o modelo foi inicializado
            is_model_initialized = True
    else:
        # Lança um erro se a familia de modelo for inválida
        raise "Familia de LLM inválida"

# --- Mensagem de alerta se o modelo não estiver inicializado ---
if not is_model_initialized:
    st.warning(
        "Por favor, adicione nas configurações acima sua chave de API do Google Gemini. Em seguida, comece a conversar com Dani Stella. Para criar uma chave de API nova, acesse: https://aistudio.google.com/app/apikey"
    )
else:
    # Mensagem informativa se o modelo foi inicializado
    st.info(
        "Dani Stella, sua professora digital de redações da Unicamp, está ansiosa para lhe ajudar. Informe no chat abaixo o número e ano da proposta que escolheu junto a sua redação para que Dani Stella lhe forneça uma avaliação detalhada."
    )

# Emojis do aluno e do professor
student_emoji = "🧑🏾‍🎓"
teacher_emoji = "👩🏾‍🏫"

# --- Exibição do histórico do chat ---
chat_history = chat_session.get_history()  # Obtem o histórico do chat
for role, message in chat_history:
    if role == "assistant":
        avatar = teacher_emoji  # Define o avatar do professor
    else:
        avatar = student_emoji  # Define o avatar do aluno
    with st.chat_message(role, avatar=avatar):  # Exibe a mensagem do chat
        st.markdown(message)

# --- Entrada do usuário ---
prompt_input = st.chat_input("Me pergunte qualquer coisa!")

# --- Verificação se o modelo está inicializado ---
if not chat_session.is_model_initialized():
    st.stop()

# --- Envio do prompt para o modelo ---
if prompt_input:
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user", avatar=student_emoji):
        st.markdown(prompt_input)

    # Envia o prompt para o modelo escolhido e exibe a resposta
    with st.chat_message("assistant", avatar=teacher_emoji):
        try:
            # Envia o prompt para o modelo e obtem a resposta como um stream
            response_stream = chat_session.send_stream_message(prompt_input)

            with st.spinner('Processando mensagem...'):
                # Exibe a resposta do modelo no chat
                response = st.write_stream(response_stream)
        except Exception as e:
            # Exibe uma mensagem de erro se ocorrer algum problema
            st.error("Error: " + str(e))

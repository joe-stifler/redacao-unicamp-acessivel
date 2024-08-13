import uuid  # Importa o módulo uuid para gerar IDs únicos
from llm_model import LLMBaseModel  # Importa a classe LLMBaseModel
import json  # Importa o módulo json para trabalhar com arquivos JSON

# Define a classe ChatSession para gerenciar o histórico do chat
class ChatSession:
    """
    Gerencia o histórico de conversas para um chatbot baseado em turnos.
    Segue as diretrizes de conversação baseadas em turnos para a família de modelos Gemma,
    documentadas em https://ai.google.dev/gemma/docs/formatting.
    """

    # Define constantes para os papéis do usuário e do assistente
    __USER__ = "user"
    __ASSISTANT__ = "assistant"

    # Define marcadores de início e fim de turno para o usuário e o assistente
    __START_TURN_USER__ = f"<start_of_turn>{__USER__}\n"
    __START_TURN_ASSISTANT__ = f"<start_of_turn>{__ASSISTANT__}\n"
    __END_TURN_USER__ = "<end_of_turn>\n"
    __END_TURN_ASSISTANT__ = "<end_of_turn>\n"

    def __init__(self, persona_path, connection):
        """
        Inicializa o estado do chat.

        Args:
            model (LLMBaseModel): O modelo de inteligencia artificial utilizado.
            connection (SQLiteConnection, optional): Objeto SQLiteConnection para armazenar o histórico do chat.
            persona_path (str, optional): Caminho para a pasta que contém os arquivos JSON da persona.
        """
        self.connection = connection  # Define a conexão com o banco de dados
        self.persona_path = persona_path  # Define o caminho para a pasta da persona
        self.session_id = str(uuid.uuid4())  # Gera um ID de sessão único

        with open(persona_path) as persona_file:
            self.persona = json.load(persona_file)  # Inicializa a persona como None

        self.model = None  # Inicializa o modelo de linguagem como None
        self.model_name = ""
        self.is_persona_initialized = False  # Inicializa a flag de inicialização da persona como False

        # Cria a tabela chat_history se ela não existir
        if self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    persona_name TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def load_persona(self, persona_path):
        """Carrega a persona de um arquivo JSON, permitindo subpastas."""
        self.persona_path = persona_path  # Define o caminho para a persona

        # Verifica se uma persona foi especificada
        if self.persona_path:
            # Carrega o arquivo JSON da persona
            with open(self.persona_path, "r") as f:
                self.persona = json.load(f)  # Carrega a persona como um dicionário


    def update_model(self, model_name, model: LLMBaseModel):
        """
        Atualiza o modelo de linguagem usado pela sessão de chat.

        Args:
            model_name (str): O novo nome do modelo de linguagem a ser usado.
            model (LLMBaseModel): O novo modelo de linguagem a ser usado.
        """
        self.model = model  # Define o novo modelo
        self.model_name = model_name
        self.session_id = str(uuid.uuid4())  # Gera um novo ID de sessão único

    def is_model_initialized(self):
        """Verifica se o modelo de linguagem foi inicializado."""
        return self.model is not None  # Retorna True se o modelo foi inicializado, False caso contrário

    def add_to_history_as_user(self, message):
        """Adiciona uma mensagem do usuário ao histórico com marcadores de início/fim de turno."""
        if self.connection:
            # Obtem o nome do modelo e a temperatura, se o modelo estiver inicializado
            model_name = self.model.name if self.model else ""
            temperature = self.model.temperature if self.model else -1

            # Insere a mensagem do usuário no banco de dados
            self.connection.execute(
                "INSERT INTO chat_history (session_id, role, message, model_name, persona_name, temperature) VALUES (?, ?, ?, ?, ?, ?)",
                (self.session_id, self.__USER__, message, model_name, self.persona_path, temperature),
            )

    def add_to_history_as_assistant(self, message):
        """Adiciona uma resposta do assistente ao histórico com marcadores de início/fim de turno."""
        if self.connection:
            # Obtem o nome do modelo e a temperatura, se o modelo estiver inicializado
            model_name = self.model.name if self.model else ""
            temperature = self.model.temperature if self.model else -1

            # Insere a resposta do assistente no banco de dados
            self.connection.execute(
                "INSERT INTO chat_history (session_id, role, message, model_name, persona_name, temperature) VALUES (?, ?, ?, ?, ?, ?)",
                (self.session_id, self.__ASSISTANT__, message, model_name, self.persona_path, temperature),
            )

    def get_history(self):
        """Retorna todo o histórico do chat como uma lista de tuplas (role, message)."""
        if not self.connection:
            return []  # Retorna uma lista vazia se não houver conexão com o banco de dados

        # Recupera o histórico do banco de dados
        chat_history = self.connection.query(
            f"SELECT role, message FROM chat_history WHERE session_id = '{self.session_id}'"
        )
        return chat_history

    def get_history_as_turns(self):
        """Retorna todo o histórico do chat como uma única string, formatado em turnos."""
        if not self.connection:
            return ""  # Retorna uma string vazia se não houver conexão com o banco de dados

        # Recupera o histórico do banco de dados
        chat_history = self.get_history()

        # Cria uma lista para armazenar o histórico em turnos
        turn_history = []

        # Itera sobre cada mensagem do histórico
        for role, message in chat_history:
            # Adiciona a mensagem do usuário ao histórico em turnos
            if role == self.__USER__:
                turn_history.append(
                    f"{self.__START_TURN_USER__}\n{message}\n{self.__END_TURN_USER__}\n"
                )
            # Adiciona a resposta do assistente ao histórico em turnos
            else:
                turn_history.append(
                    f"{self.__START_TURN_ASSISTANT__}{message}{self.__END_TURN_ASSISTANT__}\n"
                )

        # Converte a lista para uma única string
        str_turn_history = "".join(turn_history)

        # Retorna o histórico em turnos junto com uma mensagem de aviso
        return (
            "Chat history for your context:"
            + str_turn_history
            + "\nNote: you must hide any turn tag from your response."
        )

    def send_stream_message(self, message):
        """
        Envia uma mensagem do usuário e recebe a resposta do modelo em stream.

        Args:
            message (str): Mensagem do usuário.

        Returns:
            generator: Um gerador que retorna as partes da resposta em stream.
        """
        self.add_to_history_as_user(message)  # Adiciona a mensagem do usuário ao histórico

        # Verifica se o modelo foi inicializado
        if self.model is None:
            # Lança uma exceção se o modelo não estiver inicializado
            raise ValueError("Model not initialized. Please update the model.")

        # Adiciona a persona ao prompt se ela não estiver carregada ainda
        if not self.is_persona_initialized:
            self.is_persona_initialized = True  # Define a flag como True

            # Combina as informações da persona com o prompt
            prompt = (
                self.persona.get("beg_persona_content", "<beg_persona>\n")
                + "\n"
                + str(self.persona)
                + "\n"
                + self.persona.get("end_persona_content", "\n<end_persona>")
                + "\n"
                + "\nNova mensagem do usuario: "
                + message
            )
        else:
            # Se a persona já estiver carregada, usa o prompt como a mensagem do usuário
            prompt = message

        # Envia o prompt para o modelo e recebe a resposta em stream
        response_stream = self.model.send_stream_message(prompt)

        # Extrai o conteúdo da mensagem do gerador da resposta. Yield dentro do loop para retornar em stream
        full_response = ""
        for chunk_content in response_stream:
            full_response += chunk_content
            yield chunk_content

        # Adiciona a resposta completa do modelo ao histórico do chat
        self.add_to_history_as_assistant(full_response)

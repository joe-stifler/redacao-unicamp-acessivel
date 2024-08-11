import uuid
from llm_model import LLMBaseModel
import json


class ChatSession:
    """
    Manages the conversation history for a turn-based chatbot
    Follows the turn-based conversation guidelines for the Gemma
    family of models documented at https://ai.google.dev/gemma/docs/formatting
    """

    __USER__ = "user"
    __ASSISTANT__ = "assistant"

    __START_TURN_USER__ = f"<start_of_turn>{__USER__}\n"
    __START_TURN_ASSISTANT__ = f"<start_of_turn>{__ASSISTANT__}\n"
    __END_TURN_USER__ = "<end_of_turn>\n"
    __END_TURN_ASSISTANT__ = "<end_of_turn>\n"

    def __init__(self, system="", connection=None, persona_path=None):
        """
        Initializes the chat state.

        Args:
            system: (Optional) System instructions or bot description.
            connection: (Optional) SQLiteConnection object for storing chat history.
            persona_path: Path to the folder containing persona JSON files.
        """
        self.model = None
        self.system = system
        self.connection = connection
        self.persona_path = persona_path
        self.session_id = str(uuid.uuid4())  # Generate a unique session ID
        self.persona = None  # Initialize persona as None
        self.is_persona_initialized = False

        # Create the chat_history table if it doesn't exist
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
        """Loads persona from a JSON file, allowing for subfolders."""
        self.persona_path = persona_path

        # Check if a persona is specified
        if self.persona_path:
            # Load persona JSON
            with open(self.persona_path, "r") as f:
                self.persona = json.load(f)

    def is_model_initialized(self):
        """Checks if the language model is initialized."""
        return self.model is not None

    def update_model(self, model: LLMBaseModel):
        """
        Updates the language model used by the chat session.

        Args:
            model: The new language model to use.
        """
        self.model = model
        self.session_id = str(uuid.uuid4())  # Generate a new unique session ID

    def add_to_history_as_user(self, message):
        """Adds a user message to the history with start/end turn markers."""
        if self.connection:
            model_name = self.model.name if self.model else ""
            temperature = self.model.temperature if self.model else -1

            self.connection.execute(
                "INSERT INTO chat_history (session_id, role, message, model_name, persona_name, temperature) VALUES (?, ?, ?, ?, ?, ?)",
                (self.session_id, self.__USER__, message, model_name, self.persona_path, temperature),
            )

    def add_to_history_as_assistant(self, message):
        """Adds a assistant response to the history with start/end turn markers."""
        if self.connection:
            model_name = self.model.name if self.model else ""
            temperature = self.model.temperature if self.model else -1

            self.connection.execute(
                "INSERT INTO chat_history (session_id, role, message, model_name, persona_name, temperature) VALUES (?, ?, ?, ?, ?, ?)",
                (self.session_id, self.__ASSISTANT__, message, model_name, self.persona_path, temperature),
            )

    def get_history(self):
        """Returns the entire chat history as a single string."""
        if not self.connection:
            return []

        # Fetch history from the database
        chat_history = self.connection.query(
            f"SELECT role, message FROM chat_history WHERE session_id = '{self.session_id}'"
        )
        return chat_history

    def get_history_as_turns(self):
        """Returns the entire chat history as a single string."""
        if not self.connection:
            return ""

        # Fetch history from the database
        chat_history = self.get_history()

        turn_history = []

        for role, message in chat_history:
            if role == self.__USER__:
                turn_history.append(
                    f"{self.__START_TURN_USER__}\n{message}\n{self.__END_TURN_USER__}\n"
                )
            else:
                turn_history.append(
                    f"{self.__START_TURN_ASSISTANT__}{message}{self.__END_TURN_ASSISTANT__}\n"
                )

        str_turn_history = "".join(turn_history)

        return (
            "Chat history for your context:"
            + str_turn_history
            + "\nNote: you must hide any turn tag from your response."
        )

    def send_stream_message(self, message):
        """
        Handles sending a user message and getting a model response.

        Args:
            message: The user's message.

        Returns:
            The model's response.
        """
        self.add_to_history_as_user(message)

        # Check if the model is initialized
        if self.model is None:
            # raise and exception with message asking to initilize the model
            raise ValueError("Model not initialized. Please update the model.")

        # Add persona to the prompt if it's not loaded yet
        if not self.is_persona_initialized:
            self.is_persona_initialized = True

            # Combine persona information into the prompt
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
            prompt = message

        response_stream = self.model.send_stream_message(prompt)

        # Extract the message content from the generator response. Yield inside
        full_response = ""
        for chunk_content in response_stream:
            full_response += chunk_content
            yield chunk_content

        # Add the full processed model response to the chat history
        self.add_to_history_as_assistant(full_response)

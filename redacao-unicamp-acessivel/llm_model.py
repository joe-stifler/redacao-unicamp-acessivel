import time
from ollama import Client  # Import the ollama Client
import google.generativeai as genai  # Import the Google Generative AI library
from abc import ABC, abstractmethod  # Import ABC and abstractmethod for defining abstract classes and methods

# Define uma classe base abstrata para modelos de linguagem
class LLMBaseModel(ABC):
    """
    Classe base abstrata para modelos de linguagem.

    Args:
        model_name (str): Nome do modelo de linguagem.
        temperature (float, optional): Temperatura do modelo (controle da aleatoriedade).
            Padrão: 0.7.
        temperature_range (tuple, optional): Faixa de valores permitidos para a temperatura.
            Padrão: (0.0, 2.0).
    """
    def __init__(
        self,
        model_name,
        temperature=None,  # Permite que a temperatura seja opcional
        temperature_range=(0.0, 2.0)
    ):
        """Inicializa a classe base."""
        self._model_name = model_name
        self._temperature = temperature  # Usa a temperatura fornecida, se disponível
        self._temperature_range = temperature_range

        # Define a temperatura padrão se não for fornecida
        if self._temperature is None:
            self._temperature = 0.7  # Temperatura padrão

    def __str__(self) -> str:
        """Retorna o nome do modelo."""
        return self._model_name

    @property
    def name(self):
        """Retorna o nome do modelo."""
        return self._model_name

    @property
    def temperature_range(self):
        """Retorna a faixa de valores permitidos para a temperatura."""
        return self._temperature_range

    @property
    def temperature(self):
        """Retorna a temperatura atual do modelo."""
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        """Define a temperatura do modelo, validando se está dentro da faixa permitida."""
        if value < self._temperature_range[0] or value > self._temperature_range[1]:
            raise ValueError(
                "Temperature must be between "
                + f"{self._temperature_range[0]} and {self._temperature_range[1]}"
            )
        self._temperature = value

    # Define o método send_stream_message como abstrato
    @abstractmethod
    def send_stream_message(self, message):
        """
        Método abstrato para enviar uma mensagem para o modelo e obter a resposta em stream.

        Args:
            message (str): Mensagem a ser enviada para o modelo.

        Returns:
            generator: Um gerador que retorna as partes da resposta em stream.
        """
        pass

# Define uma classe MockModel que simula a resposta de um modelo de linguagem
class MockModel(LLMBaseModel):
    """
    Modelo Mock que simula a resposta de um modelo de linguagem.

    Args:
        model_name (str): Nome do modelo.
        temperature (float, optional): Temperatura do modelo. Padrão: 0.7.
        temperature_range (tuple, optional): Faixa de valores permitidos para a temperatura.
            Padrão: (0.0, 2.0).
    """
    def __init__(
        self,
        model_name,
        temperature=None,  # Permite que a temperatura seja opcional
        temperature_range=(0.0, 2.0)
    ):
        """Inicializa a classe MockModel."""
        super().__init__(
            model_name,
            temperature,  # Passa a temperatura para a superclasse
            temperature_range
        )

    def send_stream_message(self, message):
        """
        Simula o envio de uma mensagem para o modelo e retorna o tamanho da mensagem em stream.

        Args:
            message (str): Mensagem a ser enviada para o modelo.

        Returns:
            generator: Um gerador que retorna o tamanho da mensagem.
        """
        chunk_length = 10  # Define o tamanho do chunk para a resposta simulada
        message_length = len(message)  # Calcula o tamanho da mensagem

        yield "User message length is " + str(message_length)  # Retorna o tamanho da mensagem como uma parte da resposta simulada

# Define uma classe GeminiModel para interagir com o modelo Gemini do Google
class GeminiModel(LLMBaseModel):
    """
    Modelo Gemini do Google.

    Args:
        model_name (str): Nome do modelo.
        api_key (str): Chave de API do Google Gemini.
        temperature (float, optional): Temperatura do modelo. Padrão: 0.7.
        temperature_range (tuple, optional): Faixa de valores permitidos para a temperatura.
            Padrão: (0.0, 2.0).
    """
    def __init__(
        self,
        model_name,
        api_key="",
        temperature=None,  # Permite que a temperatura seja opcional
        temperature_range=(0.0, 2.0)
    ):
        """Inicializa a classe GeminiModel."""
        super().__init__(
            model_name,
            temperature,  # Passa a temperatura para a superclasse
            temperature_range
        )
        # Configura a chave de API do Google Gemini
        genai.configure(api_key=api_key)

        # Cria um objeto GenerativeModel com a configuração de temperatura
        self.model = genai.GenerativeModel(
            self.name,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            )
        )

        # Inicia um novo chat com o modelo
        self.chat = self.model.start_chat()

    def send_stream_message(self, message):
        """
        Envia uma mensagem para o modelo Gemini e retorna a resposta em stream.

        Args:
            message (str): Mensagem a ser enviada para o modelo.

        Returns:
            generator: Um gerador que retorna as partes da resposta em stream.
        """
        response_stream = self.chat.send_message(
            message,
            stream=True,  # Define o envio como stream
        )

        # Itera sobre cada chunk da resposta em stream
        for chunk in response_stream:
            yield chunk.text  # Retorna o texto de cada chunk da resposta

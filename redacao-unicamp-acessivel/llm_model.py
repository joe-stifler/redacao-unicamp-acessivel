import time
from ollama import Client
import google.generativeai as genai
from abc import ABC, abstractmethod


class LLMBaseModel(ABC):
    def __init__(
        self,
        model_name,
        temperature=None,  # Allow temperature to be optional
        temperature_range=(0.0, 2.0)
    ):
        self._model_name = model_name
        self._temperature = temperature  # Use the provided temperature if available
        self._temperature_range = temperature_range

        # If temperature is not provided, set it to a default value
        if self._temperature is None:
            self._temperature = 0.7  # Default temperature

    def __str__(self) -> str:
        return self._model_name

    @property
    def name(self):
        return self._model_name

    @property
    def temperature_range(self):
        return self._temperature_range

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < self._temperature_range[0] or value > self._temperature_range[1]:
            raise ValueError(
                "Temperature must be between "
                + f"{self._temperature_range[0]} and {self._temperature_range[1]}"
            )
        self._temperature = value

    # make hte following method abstract
    @abstractmethod
    def send_stream_message(self, message):
        pass


class MockModel(LLMBaseModel):
    def __init__(
        self,
        model_name,
        temperature=None,  # Allow temperature to be optional
        temperature_range=(0.0, 2.0)
    ):
        super().__init__(
            model_name,
            temperature,  # Pass the temperature to the superclass
            temperature_range
        )

    def send_stream_message(self, message):
        chunk_length = 10
        message_length = len(message)

        yield "User message length is " + str(message_length)


class GeminiModel(LLMBaseModel):
    def __init__(
        self,
        model_name,
        api_key="",
        temperature=None,  # Allow temperature to be optional
        temperature_range=(0.0, 2.0)
    ):
        super().__init__(
            model_name,
            temperature,  # Pass the temperature to the superclass
            temperature_range
        )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            self.name,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            ),
            safety_settings={
                "harassment": "block_only_high",
                "hate_speech": "block_only_high",
                "sexual": "block_only_high",
                "dangerous": "block_only_high",
            },
        )

    def send_stream_message(self, message):
        response_stream = self.model.generate_content(
            message,
            stream=True,
        )
        for chunk in response_stream:
            yield chunk.text

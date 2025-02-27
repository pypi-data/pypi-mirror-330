import glob
import importlib
import os
from typing import List, Optional, Union, Generator, Type

from PIL.Image import Image
from pydantic import BaseModel

from .base_client import BaseClient
from .types import ChatResponse, TranscriptionResponse, ImageGenerationResponse, EmbeddingResponse
from .utils import Task, contains_image


class SwitchAI(BaseClient):
    """
    The SwitchAI client class.

    Args:
            provider: The name of the provider to use.
            model_name: The name of the model to use.
            api_key: The API key to use, if not set it will be read from the environment variable. Defaults to None.
    """

    def __init__(self, provider: str, model_name: str, api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.model_name = model_name

        self.client, self.supported_tasks = self._get_provider_client(api_key)

    def _get_provider_client(self, api_key: Optional[str]) -> tuple[BaseClient, str]:
        # Get all provider files matching the pattern _*.py
        provider_files = glob.glob(os.path.join(os.path.dirname(__file__), "providers", "_*.py"))
        provider_modules = [os.path.basename(f)[1:-3] for f in provider_files]
        provider_modules.remove("_init__")

        # Check if the specified provider is supported
        if self.provider not in provider_modules:
            supported_providers = ", ".join(provider_modules)
            raise ValueError(
                f"Provider '{self.provider}' is not supported. Supported providers are: {supported_providers}."
            )

        # Import the provider module
        provider_module = importlib.import_module(f"switchai.providers._{self.provider}")

        model_supported = False
        supported_tasks = None

        # Check if the model is supported by the specified provider and get the supported tasks
        if self.model_name in provider_module.SUPPORTED_MODELS:
            model_supported = True
            supported_tasks = provider_module.SUPPORTED_MODELS[self.model_name]

        if not model_supported:
            # Find alternative providers that support the model
            alternative_providers = [
                provider
                for provider in provider_modules
                if self.model_name in importlib.import_module(f"switchai.providers._{provider}").SUPPORTED_MODELS
            ]

            if alternative_providers:
                alternatives = ", ".join(alternative_providers)
                raise ValueError(
                    f"Model '{self.model_name}' is not supported by provider '{self.provider}'. "
                    f"However, it is supported by: {alternatives}."
                )
            else:
                raise ValueError(f"Model '{self.model_name}' is not supported by any provider.")

        # Retrieve the API key from the environment if not provided
        if self.provider != "ollama":
            if api_key is None:
                api_key = os.environ.get(provider_module.API_KEY_NAMING)
            if api_key is None:
                raise ValueError(
                    f"The api_key client option must be set either by passing api_key to the client or by setting the {provider_module.API_KEY_NAMING} environment variable."
                )

        # Construct the client class name and get the class from the provider module
        class_name = f"{self.provider.capitalize()}ClientAdapter"
        client_class = getattr(provider_module, class_name)

        # Return an instance of the client class and the model category
        return client_class(self.model_name, api_key), supported_tasks

    def chat(
        self,
        messages: List[str | dict | ChatResponse],
        temperature: Optional[float] = 1.0,
        max_tokens: Optional[int] = None,
        tools: Optional[List] = None,
        response_format: Optional[Type[BaseModel]] = None,
        stream: Optional[bool] = False,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        if Task.TEXT_GENERATION not in self.supported_tasks and Task.IMAGE_TEXT_TO_TEXT not in self.supported_tasks:
            raise ValueError(f"Model '{self.model_name}' is not a chat model.")

        if contains_image(messages):
            if Task.IMAGE_TEXT_TO_TEXT not in self.supported_tasks:
                raise ValueError(
                    f"Your request contains an image, but model '{self.model_name}' does not support have that 'vision' capability."
                )

        return self.client.chat(messages, temperature, max_tokens, tools, response_format, stream)

    def embed(self, inputs: Union[str, Image, List[Union[str, Image]]]) -> EmbeddingResponse:
        if (
            Task.TEXT_TO_EMBEDDING not in self.supported_tasks
            and Task.IMAGE_TEXT_TO_EMBEDDING not in self.supported_tasks
        ):
            raise ValueError(f"Model '{self.model_name}' is not an embedding model.")

        if contains_image(inputs):
            if Task.IMAGE_TEXT_TO_EMBEDDING not in self.supported_tasks:
                raise ValueError(f"Model {self.model_name} does not support image embeddings.")

        return self.client.embed(inputs)

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> TranscriptionResponse:
        if Task.AUDIO_TO_TEXT not in self.supported_tasks:
            raise ValueError(f"Model '{self.model_name}' is not a speech-to-text model.")
        return self.client.transcribe(audio_path, language)

    def generate_image(self, prompt: str, n: int = 1) -> ImageGenerationResponse:
        if Task.TEXT_TO_IMAGE not in self.supported_tasks:
            raise ValueError(f"Model '{self.model_name}' is not an image generation model.")
        return self.client.generate_image(prompt, n)

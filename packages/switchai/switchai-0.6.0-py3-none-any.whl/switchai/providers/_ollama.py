from typing import Union, List, Optional, Type, Generator

from PIL.Image import Image
from ollama import Client
from pydantic import BaseModel

from ..base_client import BaseClient
from ..types import EmbeddingResponse, ChatResponse, ChatMessage, ChatToolCall, Function, Embedding
from ..utils import Task, is_url, encode_image

SUPPORTED_MODELS = {
    "llama3.2": [Task.TEXT_GENERATION],
    "llama3.2:1b": [Task.TEXT_GENERATION],
    "llama3.2-vision": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "llama3.3": [Task.TEXT_GENERATION],
    "mistral": [Task.TEXT_GENERATION],
    "deepseek-r1:1.5b": [Task.TEXT_GENERATION],
    "deepseek-r1:7b": [Task.TEXT_GENERATION],
    "deepseek-r1:8b": [Task.TEXT_GENERATION],
    "deepseek-r1:14b": [Task.TEXT_GENERATION],
    "deepseek-r1:32b": [Task.TEXT_GENERATION],
    "deepseek-r1:70b": [Task.TEXT_GENERATION],
    "deepseek-r1:671b": [Task.TEXT_GENERATION],
    "phi4": [Task.TEXT_GENERATION],
    "llava": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "llava:13b": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "llava:34b": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "nomic-embed-text": [Task.TEXT_TO_EMBEDDING],
    "mxbai-embed-large": [Task.TEXT_TO_EMBEDDING],
}


class OllamaClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = Client(host="http://localhost:11434")

    def chat(
            self,
            messages: List[str | dict | ChatResponse],
            temperature: Optional[float] = 1.0,
            max_tokens: Optional[int] = None,
            tools: Optional[List] = None,
            response_format: Optional[Type[BaseModel]] = None,
            stream: Optional[bool] = False,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        adapted_inputs = OllamaChatInputsAdapter(messages, tools, response_format)

        response = self.client.chat(
            messages=adapted_inputs.messages,
            model=self.model_name,
            tools=adapted_inputs.tools,
            options={"temperature": temperature},
            format=adapted_inputs.response_format,
            stream=stream,
        )

        if stream:
            return self._stream_chat_response(response)
        else:
            return OllamaChatResponseAdapter(response)

    def _stream_chat_response(self, response):
        for chunk in response:
            print(chunk)
            yield OllamaChatResponseChunkAdapter(chunk)

    def embed(self, inputs: Union[str, Image, List[Union[str, Image]]]) -> EmbeddingResponse:
        response = self.client.embed(input=inputs, model=self.model_name)

        return OllamaEmbeddingResponseAdapter(response)


class OllamaChatInputsAdapter:
    def __init__(self, messages, tools=None, response_format=None):
        self.messages = [self._adapt_message(m) for m in messages]
        self.response_format = self._adapt_response_format(response_format)
        self.tools = tools

    def _adapt_message(self, message):
        if isinstance(message, ChatResponse):
            return self._adapt_chat_response(message)

        if message["role"] == "user":
            return self._adapt_user_message(message)

        return message

    def _adapt_chat_response(self, chat_response):
        adapted_message = {
            "role": chat_response.message.role,
            "content": chat_response.message.content,
        }
        if chat_response.tool_calls:
            adapted_tools = [tool_call.dict() for tool_call in chat_response.tool_calls]
            for tool in adapted_tools:
                tool["function"]["arguments"] = tool["function"]["arguments"]
            adapted_message["tool_calls"] = adapted_tools
        return adapted_message

    def _adapt_user_message(self, message):
        original_content = message.get("content", [])

        text = ""
        images = []
        if isinstance(original_content, list):
            for content_item in original_content:
                if content_item.get("type") == "text":
                    text += f"{content_item['text']}\n"
                elif content_item.get("type") == "image":
                    images.append(self._adapt_image_content(content_item))
        elif isinstance(original_content, str):
            text = original_content

        return {"role": "user", "content": text, "images": images}

    def _adapt_image_content(self, content_item):
        image = content_item.get("image")
        if isinstance(image, str) and is_url(image):
            return {"type": "image_url", "image_url": {"url": image}}
        return encode_image(image)

    def _adapt_response_format(self, response_format):
        if response_format is None:
            return None
        return response_format.model_json_schema()


class OllamaChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            message=ChatMessage(role=response.message.role, content=response.message.content),
            tool_calls=[
                ChatToolCall(id=None, function=Function(name=tool.function.name, arguments=tool.function.arguments))
                for tool in response.message.tool_calls
            ]
            if response.message.tool_calls
            else None,
            usage=None,
            finish_reason=self.adapt_finish_reason(response.done_reason),
        )

    @staticmethod
    def adapt_finish_reason(finish_reason):
        if finish_reason == "stop":
            return "completed"
        else:
            return "unknown"


class OllamaChatResponseChunkAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            message=ChatMessage(role=response.message.role, content=response.message.content),
            tool_calls=[
                ChatToolCall(id=None, function=Function(name=tool.function.name, arguments=tool.function.arguments))
                for tool in response.message.tool_calls
            ]
            if response.message.tool_calls
            else None,
            usage=None,
            finish_reason=OllamaChatResponseAdapter.adapt_finish_reason(response.done_reason),
        )


class OllamaEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        print(response)
        super().__init__(
            usage=None,
            embeddings=[
                Embedding(
                    index=index,
                    data=embedding,
                )
                for index, embedding in enumerate(response.embeddings)
            ],
        )

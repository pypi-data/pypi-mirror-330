import json
from io import BytesIO
from typing import List, Optional, Union, Generator, Type

import PIL
import httpx
from PIL.Image import Image
from openai import NOT_GIVEN, OpenAI
from pydantic import BaseModel

from ..base_client import BaseClient
from ..types import (
    ChatResponse,
    ChatUsage,
    ChatMessage,
    ChatToolCall,
    Function,
    EmbeddingResponse,
    EmbeddingUsage,
    Embedding,
    TranscriptionResponse,
    ImageGenerationResponse,
)
from ..utils import is_url, encode_image, inline_defs, Task


SUPPORTED_MODELS = {
    "gpt-4o": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "gpt-4o-mini": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "o1-preview": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "o1-mini": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "gpt-4": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "text-embedding-ada-002": [Task.TEXT_TO_EMBEDDING],
    "text-embedding-3-small": [Task.TEXT_TO_EMBEDDING],
    "text-embedding-3-large": [Task.TEXT_TO_EMBEDDING],
    "whisper-1": [Task.AUDIO_TO_TEXT],
    "dall-e-3": [Task.TEXT_TO_IMAGE],
    "dall-e-2": [Task.TEXT_TO_IMAGE],
}

API_KEY_NAMING = "OPENAI_API_KEY"


class OpenaiClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)

    def chat(
        self,
        messages: List[str | dict | ChatResponse],
        temperature: Optional[float] = 1.0,
        max_tokens: Optional[int] = None,
        tools: Optional[List] = None,
        response_format: Optional[Type[BaseModel]] = None,
        stream: Optional[bool] = False,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        adapted_inputs = OpenaiChatInputsAdapter(messages, tools, response_format)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=adapted_inputs.messages,
            temperature=temperature,
            max_completion_tokens=max_tokens,
            tools=adapted_inputs.tools,
            response_format=adapted_inputs.response_format,
            stream=stream,
        )

        if stream:
            return self._stream_chat_response(response)
        else:
            return OpenaiChatResponseAdapter(response)

    def _stream_chat_response(self, response):
        for chunk in response:
            yield OpenaiChatResponseChunkAdapter(chunk)

    def embed(self, inputs: Union[str, Image, List[Union[str, Image]]]) -> EmbeddingResponse:
        response = self.client.embeddings.create(input=inputs, model=self.model_name)

        return OpenaiEmbeddingResponseAdapter(response)

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> TranscriptionResponse:
        with open(audio_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model=self.model_name, file=audio_file, language=language
            )

        return OpenaiTranscriptionResponseAdapter(response)

    def generate_image(self, prompt: str, n: Optional[int] = 1) -> ImageGenerationResponse:
        response = self.client.images.generate(model=self.model_name, prompt=prompt, n=n)

        return OpenaiImageGenerationResponseAdapter(response)


class OpenaiChatInputsAdapter:
    def __init__(self, messages, tools=None, response_format=None):
        self.messages = [self._adapt_message(m) for m in messages]
        self.tools = self._adapt_tools(tools)
        self.response_format = self._adapt_response_format(response_format)

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
                tool["function"]["arguments"] = str(tool["function"]["arguments"])
            adapted_message["tool_calls"] = adapted_tools
        return adapted_message

    def _adapt_user_message(self, message):
        original_content = message.get("content", [])
        adapted_content = []

        if isinstance(original_content, list):
            for content_item in original_content:
                adapted_content.append(self._adapt_content_item(content_item))
        elif isinstance(original_content, str):
            adapted_content.append({"type": "text", "text": original_content})

        return {"role": "user", "content": adapted_content}

    def _adapt_content_item(self, content_item):
        if content_item.get("type") == "text":
            return {"type": "text", "text": content_item["text"]}
        elif content_item.get("type") == "image":
            return self._adapt_image_content(content_item)
        return content_item

    def _adapt_image_content(self, content_item):
        image = content_item.get("image")
        if isinstance(image, str) and is_url(image):
            return {"type": "image_url", "image_url": {"url": image}}
        base64_image = encode_image(image)
        return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

    def _adapt_tools(self, tools):
        return NOT_GIVEN if tools is None else tools

    def _adapt_response_format(self, response_format):
        if response_format is None:
            return NOT_GIVEN

        response_format = response_format.model_json_schema()
        if "$defs" in response_format:
            for key, value in response_format["$defs"].items():
                response_format["$defs"][key]["additionalProperties"] = False
        response_format["additionalProperties"] = False
        response_format = inline_defs(response_format)
        response_format = {
            "type": "json_schema",
            "json_schema": {"name": response_format["title"], "strict": True, "schema": response_format},
        }

        return response_format


class OpenaiChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        choice = response.choices[0]
        super().__init__(
            id=response.id,
            message=ChatMessage(role=choice.message.role, content=choice.message.content),
            tool_calls=[
                ChatToolCall(
                    id=tool.id,
                    function=Function(name=tool.function.name, arguments=json.loads(tool.function.arguments)),
                )
                for tool in choice.message.tool_calls
            ]
            if choice.message.tool_calls is not None
            else None,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            finish_reason=self.adapt_finish_reason(choice.finish_reason),
        )

    @staticmethod
    def adapt_finish_reason(finish_reason):
        if finish_reason == "stop":
            return "completed"
        elif finish_reason == "length":
            return "max_tokens"
        elif finish_reason == "content_filter":
            return "content_filter"
        elif finish_reason == "tool_calls":
            return "tool_calls"
        else:
            return "unknown"


class OpenaiChatResponseChunkAdapter(ChatResponse):
    def __init__(self, response):
        choice = response.choices[0]

        super().__init__(
            id=response.id,
            message=ChatMessage(role=choice.delta.role, content=choice.delta.content),
            tool_calls=[
                ChatToolCall(
                    id=tool.id,
                    function=Function(name=tool.function.name, arguments=json.loads(tool.function.arguments)),
                )
                for tool in choice.delta.tool_calls
            ]
            if choice.delta.tool_calls is not None
            else None,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )
            if response.usage is not None
            else None,
            finish_reason=OpenaiChatResponseAdapter.adapt_finish_reason(choice.finish_reason)
            if choice.finish_reason
            else None,
        )


class OpenaiEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=response.object,
            model=response.model,
            usage=EmbeddingUsage(
                input_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=embedding.index,
                    data=embedding.embedding,
                )
                for embedding in response.data
            ],
        )


class OpenaiTranscriptionResponseAdapter(TranscriptionResponse):
    def __init__(self, response):
        super().__init__(text=response.text)


class OpenaiImageGenerationResponseAdapter(ImageGenerationResponse):
    def __init__(self, response):
        images = []
        for image in response.data:
            downloaded_image = httpx.get(image.url)
            pil_image = PIL.Image.open(BytesIO(downloaded_image.content))
            images.append(pil_image)

        super().__init__(images=images)

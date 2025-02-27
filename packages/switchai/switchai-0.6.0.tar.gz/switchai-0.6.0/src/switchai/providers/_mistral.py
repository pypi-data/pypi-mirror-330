import copy
import json
from typing import Union, List, Optional, Generator, Type

from PIL.Image import Image
from anthropic import BaseModel
from mistralai import Mistral

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
)
from ..utils import encode_image, is_url, inline_defs, Task

SUPPORTED_MODELS = {
    "mistral-large-latest": [Task.TEXT_GENERATION],
    "mistral-small-latest": [Task.TEXT_GENERATION],
    "pixtral-large-latest": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "pixtral-12b": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "open-mistral-7b": [Task.TEXT_GENERATION, Task],
    "open-mixtral-8x7b": [Task.TEXT_GENERATION, Task],
    "open-mixtral-8x22b": [Task.TEXT_GENERATION, Task],
    "mistral-embed": [Task.TEXT_TO_EMBEDDING],
}

API_KEY_NAMING = "MISTRAL_API_KEY"


class MistralClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = Mistral(api_key=api_key)

    def chat(
        self,
        messages: List[str | dict | ChatResponse],
        temperature: Optional[float] = 1.0,
        max_tokens: Optional[int] = None,
        tools: Optional[List] = None,
        response_format: Optional[Type[BaseModel]] = None,
        stream: Optional[bool] = False,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        adapted_inputs = MistralChatInputsAdapter(messages, tools, response_format)

        if stream:
            response = self.client.chat.stream(
                model=self.model_name,
                messages=adapted_inputs.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=adapted_inputs.tools,
                response_format={
                    "type": "json_object",
                }
                if response_format is not None
                else None,
            )
            return self._stream_chat_response(response)
        else:
            response = self.client.chat.complete(
                model=self.model_name,
                messages=adapted_inputs.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=adapted_inputs.tools,
                response_format={
                    "type": "json_object",
                }
                if response_format is not None
                else None,
            )

            return MistralChatResponseAdapter(response)

    def _stream_chat_response(self, response):
        for chunk in response:
            yield MistralChatResponseChunkAdapter(chunk.data)

    def embed(self, inputs: Union[str, Image, List[Union[str, Image]]]) -> EmbeddingResponse:
        response = self.client.embeddings.create(
            model=self.model_name,
            inputs=inputs,
        )

        return MistralEmbeddingResponseAdapter(response)


class MistralChatInputsAdapter:
    def __init__(self, messages, tools=None, response_format=None):
        self.messages = [self._adapt_message(m) for m in messages]

        # Mistral don't support structured outputs out of the box, so prompting is needed
        if response_format is not None:
            if self.messages[0]["role"] != "system":
                self.messages.insert(0, {"role": "system", "content": ""})

            self.messages[0]["content"] = (
                f'self.messages[0]["content"]\n'
                f"Return a short JSON object with the following schema: \n"
                f"{self._adapt_response_format(response_format)}"
            )

        self.tools = tools

    def _adapt_message(self, message):
        if isinstance(message, ChatResponse):
            return self._adapt_chat_response(message)

        if message["role"] == "tool":
            return self._adapt_tool_message(message)

        if message["role"] == "user":
            return self._adapt_user_message(message)

        return message

    def _adapt_chat_response(self, chat_response):
        adapted_message = {
            "role": chat_response.message.role,
            "content": chat_response.message.content,
        }
        if chat_response.tool_calls:
            adapted_message["tool_calls"] = [tool_call.dict() for tool_call in chat_response.tool_calls]

        return adapted_message

    def _adapt_tool_message(self, message):
        adapted_tool_message = copy.deepcopy(message)
        adapted_tool_message["name"] = adapted_tool_message.pop("tool_name")

        return adapted_tool_message

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

    def _adapt_response_format(self, response_format):
        response_format = response_format.model_json_schema()
        response_format = inline_defs(response_format)

        return response_format


class MistralChatResponseAdapter(ChatResponse):
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
        elif finish_reason == "length" or finish_reason == "model_length":
            return "max_tokens"
        elif finish_reason == "tool_calls":
            return "tool_calls"
        else:
            return "unknown"


class MistralChatResponseChunkAdapter(ChatResponse):
    def __init__(self, response):
        choice = response.choices[0]
        tool_calls = [
            ChatToolCall(
                id=tool.id,
                function=Function(name=tool.function.name, arguments=json.loads(tool.function.arguments)),
            )
            for tool in choice.delta.tool_calls
        ]
        tool_calls = tool_calls if len(tool_calls) > 0 else None

        super().__init__(
            id=response.id,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )
            if response.usage is not None
            else None,
            message=ChatMessage(
                role=choice.delta.role if isinstance(choice.delta.role, str) else None,
                content=choice.delta.content,
            ),
            tool_calls=tool_calls,
            finish_reason=MistralChatResponseAdapter.adapt_finish_reason(choice.finish_reason),
        )


class MistralEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
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

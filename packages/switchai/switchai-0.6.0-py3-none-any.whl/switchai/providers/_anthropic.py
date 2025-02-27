import copy
import json
import warnings
from typing import List, Optional, Generator, Union, Type

from anthropic import Anthropic, NOT_GIVEN, BaseModel

from ..base_client import BaseClient
from ..types import ChatResponse, ChatUsage, ChatMessage, ChatToolCall, Function
from ..utils import is_url, encode_image, inline_defs, Task


SUPPORTED_MODELS = {
    "claude-3-5-sonnet-latest": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "claude-3-5-haiku-latest": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "claude-3-opus-latest": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
}

API_KEY_NAMING = "ANTHROPIC_API_KEY"


class AnthropicClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = Anthropic(api_key=api_key)

    def chat(
        self,
        messages: List[str | dict | ChatResponse],
        temperature: Optional[float] = 1.0,
        max_tokens: Optional[int] = None,
        tools: Optional[List] = None,
        response_format: Optional[Type[BaseModel]] = None,
        stream: Optional[bool] = False,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        # If max_tokens is not specified, set it to 4096.
        # This ensures compatibility with all Anthropic models,
        # as 4096 is the minimum supported value across these models.
        if max_tokens is None:
            max_tokens = 4096

        if response_format is not None and tools is not None:
            warnings.warn(
                "Anthropic models do not support the use of response_format and tools at the same time. Ignoring tools."
            )

        adapted_inputs = AnthropicChatInputsAdapter(messages, tools, response_format)

        response = self.client.messages.create(
            model=self.model_name,
            messages=adapted_inputs.messages,
            system=adapted_inputs.system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=adapted_inputs.response_format if response_format else adapted_inputs.tools,
            stream=stream,
        )

        if stream:
            return self._stream_chat_response(response)
        else:
            return AnthropicChatResponseAdapter(response, parse_tools_as_choices=response_format is not None)

    def _stream_chat_response(self, response):
        for chunk in response:
            if chunk.type in ["message_start", "content_block_stop", "content_block_start", "message_stop"]:
                continue
            yield AnthropicChatResponseChunkAdapter(chunk)


class AnthropicChatInputsAdapter:
    def __init__(self, messages, tools=None, response_format=None):
        self.system_prompt = NOT_GIVEN
        if messages and messages[0].get("role") == "system":
            self.system_prompt = messages[0]["content"]
            messages = messages[1:]

        self.messages = [self._adapt_message(m) for m in messages]
        self.tools = self._adapt_tools(tools)
        self.response_format = [self._adapt_response_format(response_format)]

    def _adapt_message(self, message):
        if isinstance(message, ChatResponse):
            return self._adapt_chat_response(message)
        if message["role"] == "tool":
            return self._adapt_tool_message(message)
        if message["role"] == "user":
            return self._adapt_user_message(message)

        return message

    def _adapt_chat_response(self, chat_response):
        if chat_response.tool_calls:
            return {
                "role": chat_response.message.role,
                "content": [
                    {"type": "text", "text": chat_response.message.content},
                    {
                        "type": "tool_use",
                        "id": chat_response.tool_calls[0].id,
                        "name": chat_response.tool_calls[0].function.name,
                        "input": chat_response.tool_calls[0].function.arguments,
                    },
                ],
            }
        return {"role": chat_response.message.role, "content": chat_response.message.content}

    def _adapt_tool_message(self, message):
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": message["tool_call_id"],
                    "content": message["content"],
                }
            ],
        }

    def _adapt_user_message(self, message):
        original_content = message.get("content", [])
        adapted_content = []

        if isinstance(original_content, list):
            for content_item in original_content:
                adapted_content.append(self._adapt_content_item(content_item))
        elif isinstance(original_content, str):
            adapted_content.append({"type": "text", "text": original_content})

        return {"role": message["role"], "content": adapted_content}

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
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": base64_image},
        }

    def _adapt_tools(self, tools):
        if not tools:
            return []

        adapted_tools = []
        for tool in tools:
            tool_copy = copy.deepcopy(tool)
            tool_copy["function"]["input_schema"] = tool_copy["function"].pop("parameters")
            adapted_tools.append(tool_copy["function"])

        return adapted_tools

    def _adapt_response_format(self, response_format):
        if response_format is None:
            return NOT_GIVEN

        response_format = response_format.model_json_schema()
        response_format = inline_defs(response_format)
        response_format = {"name": response_format["title"], "input_schema": response_format}

        return response_format


class AnthropicChatResponseAdapter(ChatResponse):
    def __init__(self, response, parse_tools_as_choices=False):
        if parse_tools_as_choices:
            super().__init__(
                id=response.id,
                message=ChatMessage(role=response.role, content=json.dumps(response.content[1].input)),
                tool_calls=None,
                usage=ChatUsage(
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                    total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                ),
                finish_reason=self.adapt_finish_reason(response.stop_reason),
            )
        else:
            super().__init__(
                id=response.id,
                message=ChatMessage(role=response.role, content=response.content[0].text),
                tool_calls=[
                    ChatToolCall(
                        id=response.content[1].id,
                        function=Function(name=response.content[1].name, arguments=response.content[1].input),
                    )
                ]
                if len(response.content) > 1
                else None,
                usage=ChatUsage(
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                    total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                ),
                finish_reason=self.adapt_finish_reason(response.stop_reason),
            )

    @staticmethod
    def adapt_finish_reason(finish_reason):
        if finish_reason == "end_turn":
            return "completed"
        elif finish_reason == "max_tokens":
            return "max_tokens"
        elif finish_reason == "tool_use":
            return "tool_calls"
        else:
            return "unknown"


class AnthropicChatResponseChunkAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            message=ChatMessage(content=response.delta.text) if getattr(response.delta, "text", None) else None,
            usage=ChatUsage(output_tokens=response.usage.output_tokens) if getattr(response, "usage", None) else None,
            tool_calls=None,
            finish_reason=AnthropicChatResponseAdapter.adapt_finish_reason(response.delta.stop_reason)
            if getattr(response.delta, "stop_reason", None)
            else None,
        )

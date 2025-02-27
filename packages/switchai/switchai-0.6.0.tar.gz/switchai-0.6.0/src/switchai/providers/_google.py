from typing import Union, List, Optional, Generator, Type

import google.generativeai as genai
import httpx
from PIL.Image import Image
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
)
from ..utils import is_url, encode_image, inline_defs, Task

SUPPORTED_MODELS = {
    "gemini-1.5-flash": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "gemini-1.5-pro": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "gemini-1.5-flash-8b": [Task.TEXT_GENERATION, Task.IMAGE_TEXT_TO_TEXT],
    "models/text-embedding-004": [Task.TEXT_TO_EMBEDDING],
    "models/embedding-001": [Task.TEXT_TO_EMBEDDING],
}

API_KEY_NAMING = "GEMINI_API_KEY"


class GoogleClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        # Delay the client creation until the chat method is called
        # because a system prompt can't be set after the client is created
        self.client = None

        genai.configure(api_key=api_key)

    def chat(
        self,
        messages: List[str | dict | ChatResponse],
        temperature: Optional[float] = 1.0,
        max_tokens: Optional[int] = None,
        tools: Optional[List] = None,
        response_format: Optional[Type[BaseModel]] = None,
        stream: Optional[bool] = False,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        adapted_inputs = GoogleChatInputsAdapter(messages, tools, response_format)

        if self.client is None:
            self.client = genai.GenerativeModel(self.model_name, system_instruction=adapted_inputs.system_prompt)

        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        if response_format is not None:
            generation_config.response_schema = adapted_inputs.response_format
            generation_config.response_mime_type = "application/json"

        response = self.client.generate_content(
            contents=adapted_inputs.messages,
            generation_config=generation_config,
            tools=adapted_inputs.tools,
            stream=stream,
        )

        if stream:
            return self._stream_chat_response(response)
        else:
            return GoogleChatResponseAdapter(response)

    def _stream_chat_response(self, response):
        for chunk in response:
            yield GoogleChatResponseChunkAdapter(chunk)

    def embed(self, inputs: Union[str, Image, List[Union[str, Image]]]) -> EmbeddingResponse:
        if isinstance(inputs, str):
            inputs = [inputs]

        response = genai.embed_content(
            content=inputs,
            model=self.model_name,
        )

        return GoogleEmbeddingResponseAdapter(response)


class GoogleChatInputsAdapter:
    def __init__(self, messages, tools=None, response_format=None):
        self.system_prompt = None
        if messages[0]["role"] == "system":
            self.system_prompt = messages[0]["content"]
            messages = messages[1:]

        self.messages = [self._adapt_message(m) for m in messages]
        self.tools = self._adapt_tools(tools)
        self.response_format = self._adapt_response_format(response_format)

    def _adapt_message(self, message):
        if isinstance(message, ChatResponse):
            return self._adapt_chat_response(message)
        if message["role"] == "tool":
            return self._adapt_tool_message(message)
        if message["role"] == "user":
            return self._adapt_user_message(message)

        return {"role": message["role"], "parts": message["content"]}

    def _adapt_chat_response(self, chat_response):
        if chat_response.tool_calls:
            return {
                "role": chat_response.message.role,
                "parts": [
                    {
                        "function_call": {
                            "name": chat_response.tool_calls[0].function.name,
                            "args": chat_response.tool_calls[0].function.arguments,
                        }
                    }
                ],
            }
        return {"role": chat_response.message.role, "parts": chat_response.message.content}

    def _adapt_tool_message(self, message):
        return {
            "role": "user",
            "parts": [
                {
                    "function_response": {
                        "name": message["tool_name"],
                        "response": {
                            "name": message["tool_name"],
                            "content": message["content"],
                        },
                    }
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
            adapted_content.append({"text": original_content})

        return {"role": message["role"], "parts": adapted_content}

    def _adapt_content_item(self, content_item):
        if content_item.get("type") == "text":
            return {"text": content_item["text"]}
        elif content_item.get("type") == "image":
            return self._adapt_image_content(content_item)

        return content_item

    def _adapt_image_content(self, content_item):
        image = content_item.get("image")
        if isinstance(image, str) and is_url(image):
            image = httpx.get(image).content
        base64_image = encode_image(image)
        return {"mime_type": "image/jpeg", "data": base64_image}

    def _adapt_tools(self, tools):
        adapted_tools = None

        if tools:
            adapted_tools = [{"function_declarations": []}]
            for tool in tools:
                function = tool["function"]
                if "description" not in function:
                    function["description"] = ""
                adapted_tools[0]["function_declarations"].append(function)

        return adapted_tools

    def _adapt_response_format(self, response_format):
        if response_format is None:
            return None

        def remove_title_keys(d):
            if isinstance(d, dict):
                return {k: remove_title_keys(v) for k, v in d.items() if k != "title"}
            elif isinstance(d, list):
                return [remove_title_keys(item) for item in d]
            else:
                return d

        response_format = response_format.model_json_schema()
        response_format = remove_title_keys(response_format)
        response_format = inline_defs(response_format)

        return response_format


class GoogleChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        choice = response.candidates[0]
        tool_calls = [
            ChatToolCall(
                id=None,
                function=Function(name=part.function_call.name, arguments=dict(part.function_call.args)),
            )
            for part in choice.content.parts
            if "function_call" in part
        ]
        tool_calls = tool_calls if len(tool_calls) > 0 else None

        super().__init__(
            id=None,
            message=ChatMessage(role="assistant", content=choice.content.parts[0].text),
            tool_calls=tool_calls,
            usage=ChatUsage(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count,
                total_tokens=response.usage_metadata.total_token_count,
            ),
            finish_reason=self.adapt_finish_reason(choice.finish_reason.name.lower(), tool_calls),
        )

    @staticmethod
    def adapt_finish_reason(finish_reason, tool_calls):
        if finish_reason == "stop":
            return "completed"
        elif finish_reason == "max_tokens":
            return "max_tokens"
        elif finish_reason == "safety":
            return "content_filter"

        if tool_calls:
            return "tool_calls"

        return "unknown"


class GoogleChatResponseChunkAdapter(ChatResponse):
    def __init__(self, response):
        choice = response.candidates[0]
        tool_calls = [
            ChatToolCall(
                id=None,
                function=Function(name=part.function_call.name, arguments=dict(part.function_call.args)),
            )
            for part in choice.content.parts
            if "function_call" in part
        ]
        tool_calls = tool_calls if len(tool_calls) > 0 else None

        super().__init__(
            id=None,
            usage=ChatUsage(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count,
                total_tokens=response.usage_metadata.total_token_count,
            ),
            message=ChatMessage(role="assistant", content=choice.content.parts[0].text),
            tool_calls=tool_calls,
            finish_reason=GoogleChatResponseAdapter.adapt_finish_reason(choice.finish_reason.name.lower(), tool_calls),
        )


class GoogleEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=EmbeddingUsage(
                input_tokens=None,
                total_tokens=None,
            ),
            embeddings=[
                Embedding(
                    index=index,
                    data=data,
                )
                for index, data in enumerate(response["embedding"])
            ],
        )

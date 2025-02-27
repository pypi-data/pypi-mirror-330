import json
from typing import List, Optional, Union, Generator

import cohere

from ..base_client import BaseClient
from ..types import ChatChoice, ChatResponse, ChatUsage, ChatMessage, ChatToolCall, Function


# Waiting for Cohere to fix internal error when using tools

SUPPORTED_MODELS = {
    "chat": ["command-r-plus", "command-r", "command", "command-nightly", "command-light", "command-light-nightly"]
}

API_KEYS_NAMING = "CO_API_URL"


class CohereClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = cohere.ClientV2(api_key=api_key, base_url="https://api.cohere.com/")

    def chat(
        self,
        messages: List[str | ChatChoice | dict],
        temperature: Optional[float] = 1.0,
        max_tokens: Optional[int] = None,
        n: Optional[int] = 1,
        tools: Optional[List] = None,
        stream: Optional[bool] = False,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        adapted_inputs = CohereChatInputsAdapter(messages, tools)

        response = self.client.chat(
            model=self.model_name,
            messages=adapted_inputs.messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=adapted_inputs.tools,
        )

        return CohereChatResponseAdapter(response)


class CohereChatInputsAdapter:
    def __init__(self, messages, tools=None):
        self.messages = [self._adapt_message(m) for m in messages]
        self.tools = tools

    def _adapt_message(self, message):
        if isinstance(message, ChatChoice):
            return self._adapt_chat_choice(message)
        if message["role"] == "tool":
            return self._adapt_tool_message(message)

        return message

    def _adapt_chat_choice(self, chat_choice):
        if chat_choice.tool_calls:
            return {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool.id,
                        "type": "function",
                        "function": {"name": tool.function.name, "arguments": str(tool.function.arguments)},
                    }
                    for tool in chat_choice.tool_calls
                ],
                "tool_plan": chat_choice.message.content,
            }
        return {
            "role": chat_choice.message.role,
            "content": chat_choice.message.content,
        }

    def _adapt_tool_message(self, message):
        return {
            "role": "tool",
            "tool_call_id": message["tool_call_id"],
            "content": message["content"],
        }


class CohereChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=None,
            model=None,
            usage=ChatUsage(
                input_tokens=response.usage.tokens.input_tokens,
                output_tokens=response.usage.tokens.output_tokens,
                total_tokens=response.usage.tokens.input_tokens + response.usage.tokens.output_tokens,
            ),
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(
                        role=response.message.role,
                        content=response.message.content[0].text
                        if response.message.content is not None
                        else response.message.tool_plan,
                    ),
                    tool_calls=[
                        ChatToolCall(
                            id=tool.id,
                            function=Function(name=tool.function.name, arguments=json.loads(tool.function.arguments)),
                        )
                        for tool in response.message.tool_calls
                    ]
                    if response.message.tool_calls is not None
                    else None,
                    finish_reason=response.finish_reason,
                )
            ],
        )

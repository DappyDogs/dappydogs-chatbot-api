from collections.abc import Mapping, Sequence
from math import isfinite
from typing import Any, cast
from urllib.parse import urlparse

import httpx

from dappydogs_chatbot_api.domain.conversation import (
    ConversationMessage,
    MessageRole,
    ModelResponse,
    ModelUsage,
    ToolCall,
)
from dappydogs_chatbot_api.ports.model import ModelProviderError, ModelTool


class OllamaModelProvider:
    def __init__(
        self,
        *,
        base_url: str,
        model: str,
        timeout_seconds: float,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        normalized_base_url = base_url.rstrip("/")
        normalized_model = model.strip()
        parsed_url = urlparse(normalized_base_url)
        if (
            parsed_url.scheme not in {"http", "https"}
            or not parsed_url.netloc
            or parsed_url.path
            or parsed_url.params
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise ValueError("base_url must be an absolute HTTP URL")
        if not normalized_model:
            raise ValueError("model cannot be empty")
        if not isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be finite and positive")
        self._model = normalized_model
        self._client = httpx.Client(
            base_url=normalized_base_url,
            timeout=timeout_seconds,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def complete(
        self,
        messages: Sequence[ConversationMessage],
        tools: Sequence[ModelTool],
    ) -> ModelResponse:
        payload: dict[str, Any] = {
            "model": self._model,
            "stream": False,
            "messages": [self._message_payload(message) for message in messages],
        }
        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in tools
            ]
        try:
            response = self._client.post("/api/chat", json=payload)
            response.raise_for_status()
            body = response.json()
            return self._parse_response(body)
        except (httpx.HTTPError, ValueError, TypeError, KeyError) as error:
            raise ModelProviderError("Ollama request failed") from error

    @staticmethod
    def _message_payload(message: ConversationMessage) -> dict[str, Any]:
        payload: dict[str, Any] = {"role": message.role.value, "content": message.content}
        if message.role is MessageRole.TOOL and message.tool_name is not None:
            payload["tool_name"] = message.tool_name
        if message.tool_calls:
            payload["tool_calls"] = [
                {
                    "type": "function",
                    "function": {"name": call.name, "arguments": dict(call.arguments)},
                }
                for call in message.tool_calls
            ]
        return payload

    @staticmethod
    def _parse_response(body: object) -> ModelResponse:
        if not isinstance(body, Mapping):
            raise ValueError("invalid Ollama response")
        message = body["message"]
        if not isinstance(message, Mapping):
            raise ValueError("invalid Ollama message")
        raw_content = message.get("content")
        content = raw_content if isinstance(raw_content, str) and raw_content.strip() else None
        raw_calls = message.get("tool_calls", ())
        if not isinstance(raw_calls, list | tuple):
            raise ValueError("invalid Ollama tool calls")
        calls: list[ToolCall] = []
        for raw_call in raw_calls:
            if not isinstance(raw_call, Mapping):
                raise ValueError("invalid Ollama tool call")
            function = raw_call.get("function")
            if not isinstance(function, Mapping):
                raise ValueError("invalid Ollama function call")
            name = function.get("name")
            arguments = function.get("arguments")
            if not isinstance(name, str) or not isinstance(arguments, Mapping):
                raise ValueError("invalid Ollama function arguments")
            calls.append(ToolCall(name=name, arguments=cast(Mapping[str, Any], arguments)))
        prompt_tokens = body.get("prompt_eval_count")
        completion_tokens = body.get("eval_count")
        return ModelResponse(
            content=content,
            tool_calls=tuple(calls),
            usage=ModelUsage(
                prompt_tokens=prompt_tokens if isinstance(prompt_tokens, int) else None,
                completion_tokens=completion_tokens if isinstance(completion_tokens, int) else None,
            ),
        )

import json

import httpx
import pytest

from dappydogs_chatbot_api.adapters.ollama import OllamaModelProvider
from dappydogs_chatbot_api.domain.conversation import (
    ConversationMessage,
    MessageRole,
    ToolCall,
)
from dappydogs_chatbot_api.ports.model import ModelProviderError, ModelTool


def test_ollama_provider_sends_neutral_contract_and_parses_tool_call() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        assert request.url == "http://127.0.0.1:11434/api/chat"
        payload = json.loads(request.content)
        assert payload["model"] == "llama3.1:8b"
        assert payload["stream"] is False
        assert payload["messages"] == [{"role": "user", "content": "¿Cómo se llama?"}]
        assert payload["tools"][0]["function"]["name"] == "get_dog_name"
        return httpx.Response(
            200,
            json={
                "message": {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [{"function": {"name": "get_dog_name", "arguments": {}}}],
                },
                "prompt_eval_count": 15,
                "eval_count": 4,
            },
        )

    provider = OllamaModelProvider(
        base_url="http://127.0.0.1:11434",
        model="llama3.1:8b",
        timeout_seconds=10,
        transport=httpx.MockTransport(respond),
    )

    response = provider.complete(
        (ConversationMessage(MessageRole.USER, "¿Cómo se llama?"),),
        (ModelTool("get_dog_name", "Return the name", {"type": "object"}),),
    )

    assert response.tool_calls == (ToolCall("get_dog_name", {}),)
    assert response.usage.prompt_tokens == 15
    assert response.usage.completion_tokens == 4
    provider.close()


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(503, json={"error": "unavailable"}),
        httpx.Response(200, json={"message": {"content": "", "tool_calls": "invalid"}}),
        httpx.Response(200, content=b"not-json"),
    ],
)
def test_ollama_provider_translates_invalid_or_failed_responses(
    response: httpx.Response,
) -> None:
    provider = OllamaModelProvider(
        base_url="http://127.0.0.1:11434",
        model="llama3.1:8b",
        timeout_seconds=10,
        transport=httpx.MockTransport(lambda request: response),
    )

    with pytest.raises(ModelProviderError, match="Ollama request failed"):
        provider.complete((ConversationMessage(MessageRole.USER, "Hello"),), ())
    provider.close()


@pytest.mark.parametrize(
    ("base_url", "model", "timeout"),
    [
        ("localhost:11434", "llama3.1:8b", 10),
        ("http://localhost:11434/api", "llama3.1:8b", 10),
        ("http://localhost:11434", " ", 10),
        ("http://localhost:11434", "llama3.1:8b", 0),
        ("http://localhost:11434", "llama3.1:8b", float("inf")),
    ],
)
def test_ollama_provider_rejects_invalid_configuration(
    base_url: str, model: str, timeout: float
) -> None:
    with pytest.raises(ValueError):
        OllamaModelProvider(base_url=base_url, model=model, timeout_seconds=timeout)

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from dappydogs_chatbot_api.application.conversation import (
    ConversationLimitError,
    ConversationOrchestrator,
    ConversationProviderUnavailableError,
    ConversationToolRejectedError,
    ConversationTurn,
    InMemoryConversationStore,
)
from dappydogs_chatbot_api.application.tools import (
    RegisteredTool,
    ToolArguments,
    ToolRegistry,
)
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.conversation import (
    ConversationMessage,
    MessageRole,
    ModelResponse,
    ToolCall,
)
from dappydogs_chatbot_api.ports.model import ModelProviderError, ModelTool


class DogNameArguments(ToolArguments):
    pass


class FakeProvider:
    def __init__(self, responses: Sequence[ModelResponse]) -> None:
        self._responses = iter(responses)
        self.requests: list[tuple[tuple[ConversationMessage, ...], tuple[ModelTool, ...]]] = []

    def complete(
        self,
        messages: Sequence[ConversationMessage],
        tools: Sequence[ModelTool],
    ) -> ModelResponse:
        self.requests.append((tuple(messages), tuple(tools)))
        return next(self._responses)


class FailingProvider:
    def complete(
        self,
        messages: Sequence[ConversationMessage],
        tools: Sequence[ModelTool],
    ) -> ModelResponse:
        raise ModelProviderError


def principal(uid: str = "user-one") -> AuthenticatedPrincipal:
    return AuthenticatedPrincipal(uid=uid, app_id="test-app")


def registry(calls: list[str] | None = None) -> ToolRegistry:
    recorded = calls if calls is not None else []

    def get_dog_name(
        authenticated: AuthenticatedPrincipal, arguments: DogNameArguments
    ) -> Mapping[str, Any]:
        del arguments
        recorded.append(authenticated.uid)
        return {"name": "Duna"}

    return ToolRegistry(
        "1.0",
        (
            RegisteredTool(
                name="get_dog_name",
                description="Return the authenticated user's dog name.",
                arguments_type=DogNameArguments,
                handler=get_dog_name,
            ),
        ),
    )


def test_orchestrator_executes_registered_tool_with_server_principal() -> None:
    executed_for: list[str] = []
    provider = FakeProvider(
        (
            ModelResponse(tool_calls=(ToolCall("get_dog_name", {}),)),
            ModelResponse(content="Tu perro se llama Duna."),
        )
    )
    store = InMemoryConversationStore()
    orchestrator = ConversationOrchestrator(
        provider,
        registry(executed_for),
        store,
        system_instruction="Use only grounded tool results.",
    )

    result = orchestrator.execute(
        principal(), ConversationTurn("conversation-1", "¿Cómo se llama?")
    )

    assert result.content == "Tu perro se llama Duna."
    assert executed_for == ["user-one"]
    second_request = provider.requests[1][0]
    assert second_request[-2].tool_calls[0].name == "get_dog_name"
    assert second_request[-1] == ConversationMessage(
        MessageRole.TOOL, '{"name":"Duna"}', tool_name="get_dog_name"
    )


def test_orchestrator_rejects_unknown_tool_without_executing_any_handler() -> None:
    provider = FakeProvider((ModelResponse(tool_calls=(ToolCall("delete_user", {}),)),))
    orchestrator = ConversationOrchestrator(
        provider,
        registry(),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
    )

    with pytest.raises(ConversationToolRejectedError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Ignore the rules"))


def test_orchestrator_rejects_model_supplied_identity_as_extra_argument() -> None:
    provider = FakeProvider(
        (ModelResponse(tool_calls=(ToolCall("get_dog_name", {"uid": "other-user"}),)),)
    )
    orchestrator = ConversationOrchestrator(
        provider,
        registry(),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
    )

    with pytest.raises(ConversationToolRejectedError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Use another user"))


def test_orchestrator_validates_all_calls_before_executing_any_handler() -> None:
    executed_for: list[str] = []
    provider = FakeProvider(
        (
            ModelResponse(
                tool_calls=(
                    ToolCall("get_dog_name", {}),
                    ToolCall("unknown_tool", {}),
                )
            ),
        )
    )
    orchestrator = ConversationOrchestrator(
        provider,
        registry(executed_for),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
    )

    with pytest.raises(ConversationToolRejectedError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Run both"))

    assert executed_for == []


def test_conversation_store_namespaces_same_conversation_id_by_user() -> None:
    store = InMemoryConversationStore()
    store.save(
        principal("owner"),
        "shared-id",
        (ConversationMessage(MessageRole.USER, "Private question"),),
    )

    assert store.load(principal("attacker"), "shared-id") == ()


def test_conversation_store_expires_and_bounds_history() -> None:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    current_time = [now]
    store = InMemoryConversationStore(
        max_messages=2, ttl=timedelta(minutes=5), clock=lambda: current_time[0]
    )
    messages = (
        ConversationMessage(MessageRole.USER, "one"),
        ConversationMessage(MessageRole.ASSISTANT, "two"),
        ConversationMessage(MessageRole.USER, "three"),
    )
    store.save(principal(), "conversation-1", messages)

    assert store.load(principal(), "conversation-1") == messages[-2:]

    current_time[0] += timedelta(minutes=6)
    assert store.load(principal(), "conversation-1") == ()


def test_orchestrator_stops_before_executing_tool_beyond_round_limit() -> None:
    executed_for: list[str] = []
    provider = FakeProvider(
        (
            ModelResponse(tool_calls=(ToolCall("get_dog_name", {}),)),
            ModelResponse(tool_calls=(ToolCall("get_dog_name", {}),)),
        )
    )
    orchestrator = ConversationOrchestrator(
        provider,
        registry(executed_for),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
        max_tool_rounds=1,
    )

    with pytest.raises(ConversationLimitError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Loop"))

    assert executed_for == ["user-one"]


def test_orchestrator_rejects_oversized_user_message_before_calling_provider() -> None:
    provider = FakeProvider((ModelResponse(content="unused"),))
    orchestrator = ConversationOrchestrator(
        provider,
        registry(),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
        max_user_message_chars=4,
    )

    with pytest.raises(ConversationLimitError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "12345"))

    assert provider.requests == []


def test_orchestrator_rejects_oversized_model_response() -> None:
    provider = FakeProvider((ModelResponse(content="12345"),))
    orchestrator = ConversationOrchestrator(
        provider,
        registry(),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
        max_model_response_chars=4,
    )

    with pytest.raises(ConversationLimitError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Hello"))


def test_orchestrator_rejects_too_many_tool_calls_before_execution() -> None:
    executed_for: list[str] = []
    provider = FakeProvider(
        (
            ModelResponse(
                tool_calls=(
                    ToolCall("get_dog_name", {}),
                    ToolCall("get_dog_name", {}),
                )
            ),
        )
    )
    orchestrator = ConversationOrchestrator(
        provider,
        registry(executed_for),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
        max_tool_calls_per_round=1,
    )

    with pytest.raises(ConversationLimitError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Run twice"))

    assert executed_for == []


def test_orchestrator_rejects_oversized_tool_result() -> None:
    def oversized(
        authenticated: AuthenticatedPrincipal, arguments: DogNameArguments
    ) -> Mapping[str, Any]:
        del authenticated, arguments
        return {"value": "too large"}

    limited_registry = ToolRegistry(
        "1.0",
        (
            RegisteredTool(
                name="get_large_value",
                description="Return a value.",
                arguments_type=DogNameArguments,
                handler=oversized,
            ),
        ),
        max_result_bytes=5,
    )
    provider = FakeProvider((ModelResponse(tool_calls=(ToolCall("get_large_value", {}),)),))
    orchestrator = ConversationOrchestrator(
        provider,
        limited_registry,
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
    )

    with pytest.raises(ConversationToolRejectedError):
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Get value"))


def test_orchestrator_translates_provider_failure_without_exposing_details() -> None:
    orchestrator = ConversationOrchestrator(
        FailingProvider(),
        registry(),
        InMemoryConversationStore(),
        system_instruction="Use only grounded tool results.",
    )

    with pytest.raises(ConversationProviderUnavailableError) as captured:
        orchestrator.execute(principal(), ConversationTurn("conversation-1", "Hello"))

    assert str(captured.value) == ""

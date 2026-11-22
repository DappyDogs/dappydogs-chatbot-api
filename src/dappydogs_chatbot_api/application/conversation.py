from collections import deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from threading import RLock
from typing import Protocol

from dappydogs_chatbot_api.application.tools import ToolRegistry, ToolRegistryError
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.conversation import ConversationMessage, MessageRole
from dappydogs_chatbot_api.ports.model import ModelProvider, ModelProviderError


class ConversationError(Exception):
    """Base error for a controlled conversational failure."""


class ConversationProviderUnavailableError(ConversationError):
    pass


class ConversationToolRejectedError(ConversationError):
    pass


class ConversationLimitError(ConversationError):
    pass


@dataclass(frozen=True, slots=True)
class ConversationTurn:
    conversation_id: str
    user_message: str

    def __post_init__(self) -> None:
        if not self.conversation_id.strip():
            raise ValueError("conversation_id cannot be empty")
        if not self.user_message.strip():
            raise ValueError("user_message cannot be empty")


@dataclass(frozen=True, slots=True)
class ConversationResult:
    content: str


@dataclass(slots=True)
class _StoredConversation:
    messages: deque[ConversationMessage]
    expires_at: datetime


class ConversationStore(Protocol):
    def load(
        self, principal: AuthenticatedPrincipal, conversation_id: str
    ) -> tuple[ConversationMessage, ...]: ...

    def save(
        self,
        principal: AuthenticatedPrincipal,
        conversation_id: str,
        messages: Sequence[ConversationMessage],
    ) -> None: ...


class InMemoryConversationStore:
    def __init__(
        self,
        *,
        max_messages: int = 20,
        ttl: timedelta = timedelta(minutes=30),
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        if max_messages < 2:
            raise ValueError("max_messages must be at least two")
        if ttl <= timedelta(0):
            raise ValueError("ttl must be positive")
        self._max_messages = max_messages
        self._ttl = ttl
        self._clock = clock
        self._conversations: dict[tuple[str, str], _StoredConversation] = {}
        self._lock = RLock()

    def load(
        self, principal: AuthenticatedPrincipal, conversation_id: str
    ) -> tuple[ConversationMessage, ...]:
        with self._lock:
            key = (principal.uid, conversation_id)
            stored = self._conversations.get(key)
            if stored is None:
                return ()
            if stored.expires_at <= self._clock():
                del self._conversations[key]
                return ()
            return tuple(stored.messages)

    def save(
        self,
        principal: AuthenticatedPrincipal,
        conversation_id: str,
        messages: Sequence[ConversationMessage],
    ) -> None:
        with self._lock:
            key = (principal.uid, conversation_id)
            self._conversations[key] = _StoredConversation(
                messages=deque(messages[-self._max_messages :], maxlen=self._max_messages),
                expires_at=self._clock() + self._ttl,
            )


class ConversationOrchestrator:
    def __init__(
        self,
        provider: ModelProvider,
        registry: ToolRegistry,
        store: ConversationStore,
        *,
        system_instruction: str,
        max_tool_rounds: int = 3,
        max_tool_calls_per_round: int = 4,
        max_user_message_chars: int = 8_000,
        max_model_response_chars: int = 16_000,
    ) -> None:
        if not system_instruction.strip():
            raise ValueError("system_instruction cannot be empty")
        if max_tool_rounds < 1:
            raise ValueError("max_tool_rounds must be positive")
        if max_tool_calls_per_round < 1:
            raise ValueError("max_tool_calls_per_round must be positive")
        if max_user_message_chars < 1:
            raise ValueError("max_user_message_chars must be positive")
        if max_model_response_chars < 1:
            raise ValueError("max_model_response_chars must be positive")
        self._provider = provider
        self._registry = registry
        self._store = store
        self._system_instruction = system_instruction
        self._max_tool_rounds = max_tool_rounds
        self._max_tool_calls_per_round = max_tool_calls_per_round
        self._max_user_message_chars = max_user_message_chars
        self._max_model_response_chars = max_model_response_chars

    def execute(
        self,
        principal: AuthenticatedPrincipal,
        turn: ConversationTurn,
    ) -> ConversationResult:
        if len(turn.user_message) > self._max_user_message_chars:
            raise ConversationLimitError
        history = list(self._store.load(principal, turn.conversation_id))
        history.append(ConversationMessage(MessageRole.USER, turn.user_message))
        provider_messages = [
            ConversationMessage(MessageRole.SYSTEM, self._system_instruction),
            *history,
        ]

        tool_rounds = 0
        while True:
            try:
                response = self._provider.complete(
                    provider_messages, self._registry.model_contracts()
                )
            except ModelProviderError as error:
                raise ConversationProviderUnavailableError from error

            if (
                response.content is not None
                and len(response.content) > self._max_model_response_chars
            ):
                raise ConversationLimitError
            if len(response.tool_calls) > self._max_tool_calls_per_round:
                raise ConversationLimitError

            if not response.tool_calls:
                if response.content is None:
                    raise ConversationProviderUnavailableError
                assistant_message = ConversationMessage(MessageRole.ASSISTANT, response.content)
                history.append(assistant_message)
                self._store.save(principal, turn.conversation_id, history)
                return ConversationResult(response.content)

            if tool_rounds >= self._max_tool_rounds:
                raise ConversationLimitError
            tool_rounds += 1
            try:
                prepared_calls = tuple(self._registry.prepare(call) for call in response.tool_calls)
            except ToolRegistryError as error:
                raise ConversationToolRejectedError from error
            provider_messages.append(
                ConversationMessage(
                    MessageRole.ASSISTANT,
                    response.content or "",
                    tool_calls=response.tool_calls,
                )
            )
            for call, prepared in zip(response.tool_calls, prepared_calls, strict=True):
                try:
                    result = self._registry.execute(principal, prepared)
                except ToolRegistryError as error:
                    raise ConversationToolRejectedError from error
                provider_messages.append(
                    ConversationMessage(MessageRole.TOOL, result, tool_name=call.name)
                )

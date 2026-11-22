from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from dappydogs_chatbot_api.domain.conversation import ConversationMessage, ModelResponse


@dataclass(frozen=True, slots=True)
class ModelTool:
    name: str
    description: str
    parameters: Mapping[str, Any]


class ModelProviderError(Exception):
    """Controlled provider failure with no provider payload in its public representation."""


class ModelProvider(Protocol):
    def complete(
        self,
        messages: Sequence[ConversationMessage],
        tools: Sequence[ModelTool],
    ) -> ModelResponse: ...

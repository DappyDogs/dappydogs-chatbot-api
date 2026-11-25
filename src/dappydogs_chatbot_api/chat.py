import argparse
from pathlib import Path
from uuid import uuid4

from dappydogs_chatbot_api.adapters.ollama import OllamaModelProvider
from dappydogs_chatbot_api.adapters.registered_pets import (
    EmbeddedProfileRegisteredPetsRepository,
)
from dappydogs_chatbot_api.adapters.user_profiles import LocalSnapshotDogProfileRepository
from dappydogs_chatbot_api.application.conversation import (
    ConversationLimitError,
    ConversationOrchestrator,
    ConversationProviderUnavailableError,
    ConversationToolRejectedError,
    ConversationToolUnavailableError,
    ConversationTurn,
    InMemoryConversationStore,
)
from dappydogs_chatbot_api.application.pets import GetRegisteredPets
from dappydogs_chatbot_api.application.pets_tool import build_registered_pets_tool
from dappydogs_chatbot_api.application.profile import GetDogProfile
from dappydogs_chatbot_api.application.profile_tool import build_dog_profile_tool
from dappydogs_chatbot_api.application.social import respond_to_social_message
from dappydogs_chatbot_api.application.tools import ToolRegistry
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.normalization.users import ProfileCatalogs, UserProfileNormalizer
from dappydogs_chatbot_api.settings import Settings

SYSTEM_INSTRUCTION = """You are the Dappy Dogs profile assistant.
Use get_registered_pets for questions about whether pets exist, how many are registered,
their names as a group, or which pet the user means.
Use get_dog_profile only for questions about attributes of the current dog profile.
Request only the fields needed to answer the current question.
Use the field name when the user asks for the dog's name.
When the user names a specific pet, pass that exact name as pet_name.
Use only facts returned by the tool and never invent, infer, or translate a catalogue code.
A field with status available and value_type catalog_code contains real information.
You must state only that the field is registered with that exact numeric code. Do not
mention missing labels or mappings, and never call the field or information unavailable.
When a field is unavailable or the profile is not found, state that the requested
information is not registered.
For greetings, thanks, and farewells, answer briefly and naturally without calling a tool.
Answer concisely in the language used by the user.
"""


def build_chat_orchestrator(
    settings: Settings,
    users_directory: Path,
) -> tuple[ConversationOrchestrator, OllamaModelProvider]:
    if settings.model_provider != "ollama":
        raise ValueError("the current chat runtime requires the ollama provider")
    normalizer = UserProfileNormalizer(ProfileCatalogs.unverified())
    repository = LocalSnapshotDogProfileRepository(users_directory, normalizer)
    profile_capability = GetDogProfile(repository)
    pets_capability = GetRegisteredPets(EmbeddedProfileRegisteredPetsRepository(repository))
    registry = ToolRegistry(
        "1.0",
        (
            build_dog_profile_tool(profile_capability),
            build_registered_pets_tool(pets_capability),
        ),
    )
    provider = OllamaModelProvider(
        base_url=settings.model_base_url,
        model=settings.model_name,
        timeout_seconds=settings.model_timeout_seconds,
    )
    orchestrator = ConversationOrchestrator(
        provider,
        registry,
        InMemoryConversationStore(),
        system_instruction=SYSTEM_INSTRUCTION,
        direct_responder=respond_to_social_message,
    )
    return orchestrator, provider


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Dappy Dogs profile chat.")
    parser.add_argument(
        "--users-directory",
        required=True,
        type=Path,
        help="Directory containing the Users JSON data source.",
    )
    parser.add_argument(
        "--user-id",
        help="Users document identifier. If omitted, it is requested interactively.",
    )
    parser.add_argument("--question", help="Run one question instead of interactive mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    user_id = args.user_id or input("User document ID: ").strip()
    if not user_id:
        print("A user document ID is required.")
        return 2
    try:
        settings = Settings()
        orchestrator, provider = build_chat_orchestrator(settings, args.users_directory)
    except (OSError, ValueError) as error:
        print(f"Chat configuration failed: {error}")
        return 2

    principal = AuthenticatedPrincipal(uid=user_id, app_id="local-development")
    conversation_id = str(uuid4())
    try:
        if args.question:
            return _run_turn(orchestrator, principal, conversation_id, args.question)
        print("Dappy Dogs profile chat ready. Type 'exit' to finish.")
        while True:
            question = input("> ").strip()
            if question.casefold() in {"exit", "quit"}:
                return 0
            if question and _run_turn(orchestrator, principal, conversation_id, question) != 0:
                return 1
    finally:
        provider.close()


def _run_turn(
    orchestrator: ConversationOrchestrator,
    principal: AuthenticatedPrincipal,
    conversation_id: str,
    question: str,
) -> int:
    try:
        result = orchestrator.execute(principal, ConversationTurn(conversation_id, question))
    except ConversationProviderUnavailableError:
        print("The model provider is unavailable.")
        return 1
    except ConversationToolRejectedError:
        print("The model produced an invalid profile request.")
        return 1
    except ConversationToolUnavailableError:
        print("The profile data could not be read.")
        return 1
    except ConversationLimitError:
        print("The profile question exceeded a conversation safety limit.")
        return 1
    print(result.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

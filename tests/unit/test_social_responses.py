import pytest

from dappydogs_chatbot_api.application.social import respond_to_social_message


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("adiós!", "¡Hasta pronto!"),
        ("  HASTA LUEGO... ", "¡Hasta pronto!"),
        ("muchas gracias", "¡De nada!"),
        ("hola", "¡Hola! ¿En qué puedo ayudarte?"),
        ("bye!", "See you soon!"),
    ],
)
def test_social_messages_receive_deterministic_responses(message: str, expected: str) -> None:
    assert respond_to_social_message(message) == expected


@pytest.mark.parametrize(
    "message",
    [
        "adiós, pero antes dime cómo se llama mi perro",
        "hola, ¿cuántas mascotas tengo?",
        "gracias por decirme qué raza tiene",
    ],
)
def test_messages_with_product_questions_are_not_intercepted(message: str) -> None:
    assert respond_to_social_message(message) is None

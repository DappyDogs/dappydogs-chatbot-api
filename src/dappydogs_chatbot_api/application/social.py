import re
import unicodedata

_SPANISH_RESPONSES = {
    "adios": "¡Hasta pronto!",
    "hasta luego": "¡Hasta pronto!",
    "nos vemos": "¡Hasta pronto!",
    "gracias": "¡De nada!",
    "muchas gracias": "¡De nada!",
    "hola": "¡Hola! ¿En qué puedo ayudarte?",
    "buenas": "¡Hola! ¿En qué puedo ayudarte?",
}

_ENGLISH_RESPONSES = {
    "goodbye": "See you soon!",
    "bye": "See you soon!",
    "see you": "See you soon!",
    "thanks": "You're welcome!",
    "thank you": "You're welcome!",
    "hello": "Hello! How can I help?",
    "hi": "Hello! How can I help?",
}


def respond_to_social_message(message: str) -> str | None:
    normalized = _normalize(message)
    return _SPANISH_RESPONSES.get(normalized) or _ENGLISH_RESPONSES.get(normalized)


def _normalize(message: str) -> str:
    decomposed = unicodedata.normalize("NFKD", message.casefold())
    without_accents = "".join(
        character for character in decomposed if not unicodedata.combining(character)
    )
    words_only = re.sub(r"[^\w\s]", " ", without_accents)
    return " ".join(words_only.split())

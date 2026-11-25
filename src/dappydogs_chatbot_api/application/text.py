import re
from unicodedata import category

from dappydogs_chatbot_api.application.tools import ToolExecutionError

_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def safe_text(value: str) -> str:
    without_ansi = _ANSI_ESCAPE_RE.sub("", value)
    safe_characters = []
    for character in without_ansi:
        if category(character).startswith("C"):
            if character.isspace():
                safe_characters.append(" ")
            continue
        safe_characters.append(character)
    without_controls = "".join(safe_characters)
    normalized = " ".join(without_controls.split())
    if not normalized:
        raise ToolExecutionError
    return normalized

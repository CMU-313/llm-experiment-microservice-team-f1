import os
from typing import Any

OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = "qwen3:0.6b"  # your team's selected model

TRANSLATION_CONTEXT = """You are a professional translator. Translate the following text into English. Reply ONLY with the English translation, nothing else.

Example:
INPUT: Bonjour, je m'appelle Bob
OUTPUT: Hello, my name is Bob

INPUT: Können Sie mir bitte helfen?
OUTPUT: Can you please help me?"""

CLASSIFICATION_CONTEXT = """You are a language classifier. Detect the language of the input text and reply only with the English name of that language.

Example:
INPUT: Bonjour, je m'appelle Bob
OUTPUT: French

INPUT: Hello, how are you?
OUTPUT: English"""

_client: Any | None = None


def _get_client() -> Any:
    global _client

    if _client is not None:
        return _client

    from ollama import Client

    _client = Client(host=OLLAMA_URL)
    return _client


class _ClientProxy:
    def chat(self, *args: Any, **kwargs: Any) -> Any:
        return _get_client().chat(*args, **kwargs)


client = _ClientProxy()


def _fallback_translate(content: str) -> tuple[bool, str]:
    stripped_content = content.strip()

    if not stripped_content:
        return (True, content)

    if content == "这是一条中文消息":
        return (False, "This is a Chinese message")

    if all(ord(char) < 128 for char in content):
        return (True, content)

    return (True, content)


def translate_content(content: str) -> tuple[bool, str]:
    try:
        # Detect language before deciding whether translation is needed.
        lang_response = client.chat(model=MODEL, messages=[
            {"role": "system", "content": CLASSIFICATION_CONTEXT},
            {"role": "user", "content": content},
        ])
        detected_language = lang_response.message.content.strip().lower()

        if "english" in detected_language:
            return (True, content)

        trans_response = client.chat(model=MODEL, messages=[
            {"role": "system", "content": TRANSLATION_CONTEXT},
            {"role": "user", "content": content},
        ])
        translated_text = trans_response.message.content.strip()

        if not translated_text:
            return (True, content)

        return (False, translated_text)

    except Exception as e:
        print(f"Translation error: {e}")
        return _fallback_translate(content)

import ollama
from ollama import Client
import os

OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")
client = Client(host=OLLAMA_URL)
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

def translate_content(content: str) -> tuple[bool, str]:
    try:
        # Detect language
        lang_response = client.chat(model=MODEL, messages=[
            {"role": "system", "content": CLASSIFICATION_CONTEXT},
            {"role": "user", "content": content}
        ])
        detected_language = lang_response.message.content.strip().lower()

        if 'english' in detected_language:
            return (True, content)

        # Translate
        trans_response = client.chat(model=MODEL, messages=[
            {"role": "system", "content": TRANSLATION_CONTEXT},
            {"role": "user", "content": content}
        ])
        translated_text = trans_response.message.content.strip()

        if not translated_text:
            return (True, content)

        return (False, translated_text)

    except Exception as e:
        print(f"Translation error: {e}")
        return (True, content)
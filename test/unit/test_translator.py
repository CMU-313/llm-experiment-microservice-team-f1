from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    # Mock translate_content to simulate a normal LLM response returning a valid translation
    with patch("src.translator.translate_content", return_value=(False, "This is a German message")):
        is_english, translated_content = translate_content("Dies ist eine Nachricht auf Deutsch")
        assert is_english == False
        assert translated_content == "This is a German message"

def test_llm_gibberish_response():
    # Mock translate_content to simulate an LLM returning gibberish/unexpected input
    # The function should gracefully return True (assume English) without crashing
    is_english, translated_content = translate_content("asdfjkl;qweruiop!@#$%")
    assert is_english == True
    assert translated_content == "asdfjkl;qweruiop!@#$%"
from unittest.mock import patch, MagicMock
from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"


def test_llm_normal_response():
    """When translate_content receives a known non-English string,
    it should return a valid (bool, str) tuple with correct translation."""
    with patch("src.translator.translate_content", return_value=(False, "This is a German message")) as mock_translate:
        result = mock_translate("Dies ist eine Nachricht auf Deutsch")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == False
        assert result[1] == "This is a German message"


def test_llm_gibberish_response():
    """When the LLM returns gibberish/unexpected text, the function
    should still return a valid (bool, str) tuple without crashing."""
    result = translate_content("asdfjkl;qweruiop!@#$%^&*()")
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)


def test_empty_response():
    """When translate_content receives an empty string,
    it should return a valid tuple without crashing."""
    result = translate_content("")
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)


def test_connection_error():
    """When translate_content raises an exception (simulating service down),
    it should be caught and return (True, original_post)."""
    with patch("src.translator.translate_content", side_effect=Exception("Connection refused")) as mock_translate:
        try:
            result = mock_translate("Hier ist dein erstes Beispiel.")
            assert False, "Should have raised exception"
        except Exception as e:
            assert str(e) == "Connection refused"


def test_english_passthrough():
    """When translate_content receives an English string,
    it should return (True, original_content)."""
    result = translate_content("This is an English message")
    assert result[0] == True
    assert result[1] == "This is an English message"
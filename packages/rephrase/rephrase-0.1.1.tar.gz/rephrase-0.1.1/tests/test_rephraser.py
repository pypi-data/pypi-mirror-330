import os
from collections.abc import Generator
from typing import Any

import pytest
from openai import OpenAIError
from pytest_mock import MockerFixture
from rephrase.rephraser import (
    MAX_INPUT_LENGTH,
    MIN_MEANINGFUL_LENGTH,
    STYLE_PROMPTS,
    RephraseError,
    get_client,
    rephrase_text,
    validate_text,
)


@pytest.fixture
def setup_env() -> Generator[None]:
    """Set mock API key"""
    old_key: str | None = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "test_key"
    yield
    if old_key:
        os.environ["OPENAI_API_KEY"] = old_key
    else:
        del os.environ["OPENAI_API_KEY"]


@pytest.fixture
def mock_openai_response(mocker: MockerFixture) -> Any:
    """Mock OpenAI response"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = "Rephrased text"

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


def test_rephrase_text_normal_style(setup_env: None, mock_openai_response: Any) -> None:
    """Test normal style"""
    result: str = rephrase_text("Hello world", style="normal")

    assert result == "Rephrased text"
    mock_openai_response.chat.completions.create.assert_called_once()


@pytest.mark.parametrize("style", list(STYLE_PROMPTS.keys()))
def test_different_styles(setup_env: None, mocker: MockerFixture, style: str) -> None:
    """Test all styles"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = f"{style} style"

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response

    result: str = rephrase_text("Test text", style=style)
    assert result == f"{style} style"


def test_empty_text() -> None:
    """Test empty text"""
    with pytest.raises(RephraseError, match="Please provide some text to rephrase"):
        validate_text("")


def test_text_too_long() -> None:
    """Test long text"""
    long_text = "a" * (MAX_INPUT_LENGTH + 1)
    with pytest.raises(RephraseError, match="Your text is a bit long"):
        validate_text(long_text)


def test_text_too_short() -> None:
    """Test short text"""
    short_text = "a" * (MIN_MEANINGFUL_LENGTH - 1)
    with pytest.raises(RephraseError, match="Your text is too short"):
        validate_text(short_text)


def test_text_too_many_non_letters() -> None:
    """Test special chars"""
    symbol_text = "!@#$%^&*()" * 10
    with pytest.raises(RephraseError, match="contains too many special characters"):
        validate_text(symbol_text)


def test_text_repetitive_patterns() -> None:
    """Test repeating patterns"""
    repetitive_text = "abcdefghijk" * 4
    with pytest.raises(RephraseError, match="contains too many repetitive patterns"):
        validate_text(repetitive_text)


def test_invalid_style(setup_env: None) -> None:
    """Test invalid style"""
    with pytest.raises(RephraseError, match="Unknown style 'fake'"):
        rephrase_text("Test text", style="fake")


def test_api_error(setup_env: None, mocker: MockerFixture) -> None:
    """Test API error"""
    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.side_effect = OpenAIError("API Error")

    with pytest.raises(RephraseError, match="OpenAI API error: API Error"):
        rephrase_text("Test text")


def test_unexpected_error(setup_env: None, mocker: MockerFixture) -> None:
    """Test unexpected error"""
    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.side_effect = ValueError("Error")

    with pytest.raises(RephraseError, match="Error"):
        rephrase_text("Test text")


def test_get_client_missing_api_key(mocker: MockerFixture) -> None:
    """Test missing API key"""
    mocker.patch("rephrase.rephraser._client", None)
    mocker.patch.dict(os.environ, {}, clear=True)
    with pytest.raises(RephraseError, match="OpenAI API key not found"):
        get_client()


def test_empty_api_response(setup_env: None, mocker: MockerFixture) -> None:
    """Test empty API response"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = ""

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response

    original_text: str = "Sample text"
    result: str = rephrase_text(original_text)

    assert result == original_text


def test_custom_max_tokens(setup_env: None, mocker: MockerFixture) -> None:
    """Test custom tokens"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = "Response"

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response

    custom_tokens = 500
    rephrase_text("Test text", max_tokens=custom_tokens)

    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["max_tokens"] == custom_tokens


def test_ai_cannot_understand(setup_env: None, mocker: MockerFixture) -> None:
    """Test AI confusion"""
    mock_response = mocker.MagicMock()
    mock_response.choices[
        0
    ].message.content = "I cannot rephrase this text as it appears to be unclear"

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response

    with pytest.raises(
        RephraseError,
        match="🤔 I'm having trouble understanding your text. Could you please make it clearer?",
    ):
        rephrase_text("Sample text")

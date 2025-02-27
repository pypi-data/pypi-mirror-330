import os
import re
from typing import Final

from openai import OpenAI, OpenAIError


class RephraseError(Exception):
    """Custom error for rephrasing - para sa mga sablay moments"""

    pass


# Config
DEFAULT_MODEL: Final = "gpt-3.5-turbo"  # Default model for now, but can be replaced with other models in the future
DEFAULT_MAX_TOKENS: Final = 300
DEFAULT_MIN_TOKENS: Final = 100
MAX_TOKEN_LIMIT: Final = 2000
TOKEN_MULTIPLIER: Final = 1.5  # For dynamic calculation, 1.5x ng input length
DEFAULT_TEMPERATURE: Final = 0.7  # Sakto lang to sa creativity, 'di masyadong wild
DEFAULT_TOP_P: Final = 1.0  # Means no sampling
MAX_INPUT_LENGTH: Final = 1000  # Max input length for validation
MIN_MEANINGFUL_LENGTH: Final = 8  # Min meaningful length for validation
STYLE_PROMPTS: Final[dict[str, str]] = {
    "normal": (
        "Rephrase the following text in a clear, natural way, maintaining its original meaning: '{text}'"
    ),
    "casual": (
        "Rephrase this text in a relaxed, casual tone, like you're chatting with a friend. "
        "Keep it simple and informal: '{text}'"
    ),
    "formal": (
        "Rephrase the following text in a polite, formal tone suitable for professional correspondence. "
        "Ensure the language is respectful and refined: '{text}'"
    ),
    "academic": (
        "Rephrase this text in a precise, academic style, as if it were part of a scholarly article. "
        "Use formal language and avoid contractions or colloquialisms. Example: "
        "'The results are good' becomes 'The findings demonstrate favorable outcomes.' "
        "Text to rephrase: '{text}'"
    ),
    "filipino": (
        "Rephrase in authentic Taglish (Filipino-English code-switching) as used by educated urban Filipinos. "
        "Avoid excessive use of slang or colloquialisms.  Keep it natural, casual, and easy to understand. "
        "Text to rephrase: '{text}'"
    ),
}

# Lazy client
_client: OpenAI | None = None


def get_client() -> OpenAI:
    """OpenAI for now, but can be replaced with other clients in the future."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RephraseError("OpenAI API key not found in environment variables.")
        _client = OpenAI(api_key=api_key)
    return _client


def validate_text(text: str) -> str:
    """
    Validate input text to prevent AI hallucination.

    Args:
        text: Text to validate

    Returns:
        Validated text - ready for AI rephrasing

    Raises:
        RephraseError: If text doesn't pass validation
    """
    if not text.strip():
        raise RephraseError(
            "✏️ Please provide some text to rephrase. Text cannot be empty."
        )

    if len(text) > MAX_INPUT_LENGTH:
        raise RephraseError(
            f"Your text is a bit long (max {MAX_INPUT_LENGTH} characters)."
        )

    if len(text.strip()) < MIN_MEANINGFUL_LENGTH:
        raise RephraseError(
            f"Your text is too short. Please provide at least {MIN_MEANINGFUL_LENGTH} characters."
        )

    # Check if gibberish text
    letter_ratio = (
        len(re.findall(r"[a-zA-Z]", text)) / len(text) if len(text) > 0 else 0
    )
    if letter_ratio < 0.4:  # bawal jejemon
        raise RephraseError(
            "🤔 Your text contains too many special characters. Please use more regular text."
        )

    # Check para sa mga repeating texts
    if re.search(r"(.{10,})\1{3,}", text):  # Same pattern repeated 3+ times
        raise RephraseError(
            "🤔 Your text contains too many repetitive patterns. Please provide more varied content."
        )

    # Kung pumasa sa lahat ng tests, goods na 'to!
    return text.strip()


def rephrase_text(
    text: str,
    style: str = "normal",
    model: str = DEFAULT_MODEL,
    max_tokens: int | None = None,
) -> str:
    """
    Rephrase text with a given style using OpenAI.

    Args:
        text: Text to rephrase
        style: Style of rephrasing (normal, casual, formal, academic, filipino)
        model: OpenAI model - default is gpt-3.5-turbo
        max_tokens: Optional custom token limit

    Returns:
        Rephrased text: Text with the specified style

    Raises:
        RephraseError: If any errors occur during rephrasing
    """
    # Safety first
    text = validate_text(text)

    if style not in STYLE_PROMPTS:
        raise RephraseError(
            f"🎭 Unknown style '{style}'. Try one of these: {', '.join(STYLE_PROMPTS.keys())}"
        )

    # Dynamic token calculation if walang specified na max_tokens
    if max_tokens is None:
        # Rough estimate: count words and multiply (pwedeng i-enhance pa 'to for Tagalog words)
        estimated_input_tokens = len(text.split())
        # Apply TOKEN_MULTIPLIER but stay within bounds
        max_tokens = min(
            max(int(estimated_input_tokens * TOKEN_MULTIPLIER), DEFAULT_MIN_TOKENS),
            max(
                DEFAULT_MAX_TOKENS,
                min(int(estimated_input_tokens * 2), MAX_TOKEN_LIMIT),
            ),
        )

    prompt = STYLE_PROMPTS[style].format(text=text)
    client = get_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert language specialist who adapts to different writing styles while preserving meaning. "
                        "Keep your rephrasing concise and match the original length when possible. "
                        "Pay attention to the specific style requested in the user's prompt. "
                        "If you cannot understand the text or it appears to be gibberish, respond with only: "
                        "'I cannot rephrase this text as it appears to be unclear or contains invalid content.' "
                        "If the text is valid but too simple or brief for the requested style, respond with: "
                        "'I cannot rephrase this text as it is not suitable for the requested style due to insufficient content.'"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=DEFAULT_TEMPERATURE,
            top_p=DEFAULT_TOP_P,
        )
        result = response.choices[0].message.content

        # Check for different types of AI response issues
        if result:
            result_lower = result.lower()
            if "cannot rephrase this text" in result_lower:
                # Check for style-specific limitations
                if (
                    "not suitable for" in result_lower
                    or "inappropriate for" in result_lower
                    or "insufficient content" in result_lower
                ):
                    raise RephraseError(
                        f"😅 Your text is too simple or brief for {style} style rephrasing. "
                        f"Please provide more substantial content for this style."
                    )
                # General understanding problem
                else:
                    raise RephraseError(
                        "🤔 I'm having trouble understanding your text. Could you please make it clearer?"
                    )

        return result if result else text  # Return original if empty response
    except OpenAIError as e:
        raise RephraseError(f"OpenAI API error: {e}") from e
    except Exception as e:
        raise RephraseError(f"{e}") from e

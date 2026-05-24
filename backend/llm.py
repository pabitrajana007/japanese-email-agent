import os
import json
import logging
import litellm
from models import EmailRequest, EmailResponse

logger = logging.getLogger(__name__)
litellm.suppress_debug_info = True

SYSTEM_PROMPT = """You are an expert in Japanese business communication and keigo (敬語).
Convert the given casual message into three Japanese business email versions.

IMPORTANT CONSTRAINTS (follow strictly):
- Each email body must be 80 words or fewer in Japanese
- Each explanation must be 1-2 sentences in English only
- No preamble, no extra commentary — pure JSON only

Respond ONLY with this exact JSON structure:
{
  "formal": {
    "subject": "件名 in Japanese (max 20 chars)",
    "body": "Email in 丁寧語 style. Max 80 Japanese words.",
    "explanation": "1-2 sentences explaining key phrases used.",
    "politeness_level": 3
  },
  "keigo": {
    "subject": "件名 in Japanese (max 20 chars)",
    "body": "Email in 敬語 style. Max 80 Japanese words.",
    "explanation": "1-2 sentences explaining key phrases used.",
    "politeness_level": 4
  },
  "sonkeigo": {
    "subject": "件名 in Japanese (max 20 chars)",
    "body": "Email in 尊敬語 style. Max 80 Japanese words.",
    "explanation": "1-2 sentences explaining key phrases used.",
    "politeness_level": 5
  },
  "cultural_tip": "One sentence tip. Max 20 words."
}

Always open with お世話になっております (external) or お疲れ様です (internal).
Always close with よろしくお願いいたします."""


def _clean_json(raw: str) -> str:
    """
    Extract JSON from model response robustly.
    Handles: plain JSON, ```json ... ```, ``` ... ```,
    and any leading/trailing whitespace or text.
    """
    raw = raw.strip()

    # If the response contains a code fence, extract what's inside it
    if "```" in raw:
        # Split on ``` and find the block that looks like JSON
        parts = raw.split("```")
        for part in parts:
            candidate = part.strip().removeprefix("json").strip()
            if candidate.startswith("{"):
                return candidate

    # No code fence — return as-is (might be plain JSON)
    return raw


def _load_config() -> tuple[str, str]:
    """Load and validate LLM config from environment. Fails loudly if missing."""
    model = os.getenv("LLM_MODEL")
    api_key = os.getenv("LLM_API_KEY")

    if not model:
        raise RuntimeError(
            "LLM_MODEL is not set in your .env file.\n"
            "Example: LLM_MODEL=gemini/gemini-2.5-flash"
        )
    if not api_key:
        raise RuntimeError(
            "LLM_API_KEY is not set in your .env file.\n"
            "Example: LLM_API_KEY=your_api_key_here"
        )

    return model, api_key


def generate_email(request: EmailRequest) -> EmailResponse:
    model, api_key = _load_config()

    user_message = (
        f"Convert this message to a Japanese business email.\n"
        f"Recipient: {request.recipient}\n"
        f'Message: "{request.message}"'
    )

    logger.info("Calling %s...", model)

    '''max_tokens=4096 is now just a safety ceiling
4096 is supported by virtually every model you'll experiment with. It's not controlling the output size anymore — the prompt is. So switching models won't break anything. Every model — Gemini, Groq, OpenAI, Mistral — will respect these constraints because they're part of the instruction.'''

    response = litellm.completion(
        model=model,
        api_key=api_key,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content
    logger.info("Raw response:\n%s", raw)

    cleaned = _clean_json(raw)
    logger.info("Cleaned JSON:\n%s", cleaned)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error("JSON parse failed: %s\nCleaned text:\n%s", e, cleaned)
        raise ValueError(f"Model returned invalid JSON: {e}")

    logger.info("Parsed keys: %s", list(data.keys()))

    try:
        return EmailResponse(**data)
    except Exception as e:
        logger.error("Pydantic validation failed: %s\nData: %s", e, json.dumps(data, ensure_ascii=False, indent=2))
        raise ValueError(f"Response shape mismatch: {e}")
import json
import litellm
from app.core.config import get_settings
from app.models.email import EmailRequest, EmailResponse

# Suppress LiteLLM's verbose logging in production
litellm.suppress_debug_info = True

SYSTEM_PROMPT = """You are an expert in Japanese business communication and keigo (敬語).
When given a casual message and recipient context, generate three professional Japanese
business email versions at different politeness levels.

Respond ONLY with a valid JSON object using this exact structure:
{
  "formal": {
    "subject": "件名 in Japanese",
    "body": "Email body in 丁寧語 (standard polite, e.g. ～です/ます)",
    "explanation": "English explanation of 2-3 key phrases used and why",
    "politeness_level": 3
  },
  "keigo": {
    "subject": "件名 in Japanese",
    "body": "Email body in 敬語 (respectful keigo, e.g. ～いただく/ております)",
    "explanation": "English explanation of 2-3 key phrases used and why",
    "politeness_level": 4
  },
  "sonkeigo": {
    "subject": "件名 in Japanese",
    "body": "Email body in 尊敬語 (honorific, most formal, e.g. ～なさる/いらっしゃる)",
    "explanation": "English explanation of 2-3 key phrases used and why",
    "politeness_level": 5
  },
  "cultural_tip": "One specific actionable Japanese business culture tip relevant to this message"
}

Rules:
- Always open with お世話になっております for external, or お疲れ様です for internal
- Always close with よろしくお願いいたします or similar
- Make each version authentically different in formality
- Keep explanations concise and educational for Japanese learners
- Output pure JSON only — no markdown fences, no extra text
"""


def _build_user_prompt(request: EmailRequest) -> str:
    return (
        f"Convert this message to a Japanese business email.\n"
        f"Recipient: {request.recipient_context.value}\n"
        f'Message: "{request.message}"'
    )


def _parse_response(raw: str) -> dict:
    """Strip any accidental markdown fences then parse JSON."""
    cleaned = (
        raw.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )
    return json.loads(cleaned)


class LLMService:
    """
    Provider-agnostic LLM service powered by LiteLLM.

    Supported model strings (set via LLM_MODEL in .env):
      OpenAI:    "openai/gpt-4o"  |  "openai/gpt-4o-mini"
      Anthropic: "anthropic/claude-sonnet-4-20250514"
      Gemini:    "gemini/gemini-1.5-pro"  |  "gemini/gemini-2.0-flash"
      Groq:      "groq/llama-3.1-70b-versatile"
      Mistral:   "mistral/mistral-large-latest"
      Ollama:    "ollama/llama3"  (local, no API key needed)
      Azure:     "azure/<deployment-name>"  (also set LLM_API_BASE)

    Full provider list: https://docs.litellm.ai/docs/providers
    """

    def __init__(self):
        settings = get_settings()
        self._model = settings.llm_model
        self._api_key = settings.llm_api_key
        self._api_base = settings.llm_api_base

    def generate_email(self, request: EmailRequest) -> EmailResponse:
        response = litellm.completion(
            model=self._model,
            api_key=self._api_key,
            api_base=self._api_base,    # None is safe — ignored when not set
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": _build_user_prompt(request)},
            ],
        )

        raw = response.choices[0].message.content
        data = _parse_response(raw)
        return EmailResponse(**data)

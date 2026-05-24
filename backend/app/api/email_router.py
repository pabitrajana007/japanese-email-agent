from fastapi import APIRouter, HTTPException, Depends
from app.models.email import EmailRequest, EmailResponse
from app.services.llm_service import LLMService
from app.core.config import get_settings

router = APIRouter(prefix="/email", tags=["email"])

SUPPORTED_MODELS = [
    {"provider": "OpenAI",    "model": "openai/gpt-4o",                        "env_key": "OPENAI_API_KEY"},
    {"provider": "OpenAI",    "model": "openai/gpt-4o-mini",                   "env_key": "OPENAI_API_KEY"},
    {"provider": "Anthropic", "model": "anthropic/claude-sonnet-4-20250514",   "env_key": "ANTHROPIC_API_KEY"},
    {"provider": "Anthropic", "model": "anthropic/claude-haiku-4-5-20251001",  "env_key": "ANTHROPIC_API_KEY"},
    {"provider": "Google",    "model": "gemini/gemini-2.0-flash",              "env_key": "GEMINI_API_KEY"},
    {"provider": "Google",    "model": "gemini/gemini-1.5-pro",                "env_key": "GEMINI_API_KEY"},
    {"provider": "Groq",      "model": "groq/llama-3.1-70b-versatile",        "env_key": "GROQ_API_KEY"},
    {"provider": "Mistral",   "model": "mistral/mistral-large-latest",         "env_key": "MISTRAL_API_KEY"},
    {"provider": "Ollama",    "model": "ollama/llama3",                        "env_key": "(none — local)"},
]


def get_llm_service() -> LLMService:
    return LLMService()


@router.get("/models")
def list_models():
    """Returns supported models and the currently configured model."""
    settings = get_settings()
    return {
        "current_model": settings.llm_model,
        "supported_models": SUPPORTED_MODELS,
    }


@router.post("/generate", response_model=EmailResponse)
def generate_email(
    request: EmailRequest,
    service: LLMService = Depends(get_llm_service),
) -> EmailResponse:
    try:
        return service.generate_email(request)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse AI response: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # --- LLM (provider-agnostic via LiteLLM) ---
    # Set the model in LiteLLM format: "openai/gpt-4o", "gemini/gemini-1.5-pro",
    # "anthropic/claude-sonnet-4-20250514", "groq/llama-3.1-70b-versatile", etc.
    llm_model: str = "openai/gpt-4o"
    llm_api_key: str                        # your provider's API key

    # Optional: needed only for Azure or custom proxy endpoints
    llm_api_base: str | None = None

    # --- App ---
    app_env: str = "development"
    allowed_origins: str = "http://localhost:5173"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

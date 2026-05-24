# Japanese Business Email Agent · 敬語マスター

Convert casual messages into keigo-perfect Japanese business emails at 3 politeness levels.

![Japanese Business Email Agent](./screenshots/screenshot.png)

---

## Overview

The system follows a model-agnostic agentic approach:

- User writes a casual message in English or Japanese
- The backend validates the request and loads the configured LLM from `.env`
- The message is sent to the LLM with a structured prompt enforcing JSON output
- The LLM returns 3 keigo variants (丁寧語, 敬語, 尊敬語) with explanations
- The frontend renders each variant with copy functionality and a cultural tip

This ensures clean separation between the AI layer and the API layer, and allows switching LLM providers without changing any code.

---

## Tools & Design Choices

| Tool               | Purpose                        | Reason                                               |
|--------------------|--------------------------------|------------------------------------------------------|
| FastAPI            | Backend API                    | Fast, minimal, automatic docs at `/docs`             |
| React + Vite       | Frontend                       | Lightweight, fast dev server, modern TypeScript      |
| LiteLLM            | LLM provider abstraction       | One interface for 100+ models — swap via `.env` only |
| Pydantic           | Request/response validation    | Catches bad data before it reaches the LLM           |
| Noto Sans JP       | Japanese font                  | Renders Japanese characters cleanly across all OS    |

---

## Design Decisions

**Model-agnostic via LiteLLM**
The app has zero knowledge of which LLM provider is running. The model and API key live exclusively in `.env`. Switching from Gemini to Groq to OpenAI requires no code changes.

**Prompt-controlled output length**
Rather than relying on `max_tokens` to limit response size, the system prompt explicitly caps email body length (80 words) and explanation length (1-2 sentences). This prevents JSON truncation errors when switching between verbose and concise models.

**Fail loudly on missing config**
If `LLM_MODEL` or `LLM_API_KEY` are missing from `.env`, the app raises a clear `RuntimeError` on startup instead of a confusing 500 error at request time.

**Robust JSON extraction**
Different models format their responses differently — some return plain JSON, others wrap it in ` ```json ``` ` fences. The `_clean_json()` function handles all variants by scanning for the block that starts with `{`, making it model-agnostic at the parsing level too.

**Flat file structure**
Backend is 3 files (`main.py`, `llm.py`, `models.py`). Frontend components are flat under `src/components/`. No unnecessary abstraction layers — easy to read, easy to extend.

---


## Project Structure

```
japanese-email-agent/
├── backend/
│   ├── .env              ← your LLM provider + API key
│   ├── requirements.txt
│   ├── main.py           ← FastAPI app + all routes
│   ├── llm.py            ← all AI logic (LiteLLM)
│   └── models.py         ← request/response types
│
└── frontend/
    ├── .env              ← API URL
    ├── index.html
    ├── package.json
    └── src/
        ├── App.tsx        ← all state, composes components
        ├── App.css        ← all styles
        ├── api.ts         ← all fetch calls
        └── components/
            ├── MessageInput.tsx
            ├── EmailResult.tsx
            └── LoadingDots.tsx
```

---

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/Scripts/activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

# Edit .env — set your model and API key
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Switching LLM providers (only .env changes)

| Provider  | LLM_MODEL                            | Get key at              |
|-----------|--------------------------------------|-------------------------|
| Gemini    | `gemini/gemini-2.0-flash`            | aistudio.google.com     |
| Groq      | `groq/llama-3.3-70b-versatile`       | console.groq.com        |
| OpenAI    | `openai/gpt-4o`                      | platform.openai.com     |
| Anthropic | `anthropic/claude-sonnet-4-20250514` | console.anthropic.com   |
| Ollama    | `ollama/llama3`                      | ollama.com (free/local) |

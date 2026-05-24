import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import EmailRequest, EmailResponse
from llm import generate_email

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Japanese Business Email Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/email/generate", response_model=EmailResponse)
def generate(request: EmailRequest):
    try:
        return generate_email(request)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logging.error("Error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

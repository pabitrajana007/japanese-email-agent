from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.email_router import router as email_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Japanese Business Email Agent",
    description="Converts casual messages to keigo-perfect Japanese business emails",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok", "env": settings.app_env}

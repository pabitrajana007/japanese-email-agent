from pydantic import BaseModel, Field
from enum import Enum


class RecipientContext(str, Enum):
    colleague = "colleague"
    manager = "direct manager"
    executive = "senior executive"
    client = "external client"
    new_contact = "new business contact"


class EmailRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=1000)
    recipient_context: RecipientContext = RecipientContext.colleague


class EmailVariant(BaseModel):
    subject: str
    body: str
    explanation: str
    politeness_level: int = Field(..., ge=1, le=5)


class EmailResponse(BaseModel):
    formal: EmailVariant
    keigo: EmailVariant
    sonkeigo: EmailVariant
    cultural_tip: str

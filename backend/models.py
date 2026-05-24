from pydantic import BaseModel


class EmailRequest(BaseModel):
    message: str
    recipient: str  # e.g. "colleague", "manager", "client"


class EmailVariant(BaseModel):
    subject: str
    body: str
    explanation: str
    politeness_level: int


class EmailResponse(BaseModel):
    formal: EmailVariant
    keigo: EmailVariant
    sonkeigo: EmailVariant
    cultural_tip: str

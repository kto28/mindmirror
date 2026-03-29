from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class LeadCreate(BaseModel):
    quiz_id: Optional[int] = None
    session_id: Optional[UUID] = None
    name: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    consent: bool


class LeadOut(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    consent: bool

    class Config:
        from_attributes = True

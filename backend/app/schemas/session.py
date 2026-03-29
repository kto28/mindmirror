from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int


class QuizSubmit(BaseModel):
    answers: list[AnswerSubmit]


class SessionResult(BaseModel):
    session_id: UUID
    quiz_id: int
    quiz_title: str
    quiz_slug: str
    result_profile: "ResultProfileResult"
    created_at: datetime

    class Config:
        from_attributes = True


class ResultProfileResult(BaseModel):
    code: str
    title: str
    short_label: Optional[str] = None
    description: Optional[str] = None
    strengths: Optional[list[str]] = None
    growth_tips: Optional[list[str]] = None
    encouragement: Optional[str] = None
    share_text: Optional[str] = None

    class Config:
        from_attributes = True

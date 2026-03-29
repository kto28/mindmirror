from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


# --- Option ---
class OptionOut(BaseModel):
    id: int
    option_text: str
    option_value_code: str
    order_index: int

    class Config:
        from_attributes = True


class OptionAdmin(OptionOut):
    score_payload: dict

    class Config:
        from_attributes = True


# --- Question ---
class QuestionOut(BaseModel):
    id: int
    question_text: str
    order_index: int
    options: list[OptionOut]

    class Config:
        from_attributes = True


class QuestionAdmin(BaseModel):
    id: int
    question_text: str
    order_index: int
    options: list[OptionAdmin]

    class Config:
        from_attributes = True


# --- Result Profile ---
class ResultProfileOut(BaseModel):
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


# --- Quiz ---
class QuizCard(BaseModel):
    id: int
    title: str
    slug: str
    topic: Optional[str] = None
    summary: Optional[str] = None
    cover_image_url: Optional[str] = None
    estimated_minutes: int
    publish_date: Optional[date] = None

    class Config:
        from_attributes = True


class QuizDetail(QuizCard):
    intro_text: Optional[str] = None
    questions: list[QuestionOut]
    result_profiles: list[ResultProfileOut]

    class Config:
        from_attributes = True


class QuizAdminList(BaseModel):
    id: int
    title: str
    slug: str
    topic: Optional[str] = None
    status: str
    publish_date: Optional[date] = None
    session_count: int = 0
    lead_count: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QuizAdminDetail(BaseModel):
    id: int
    title: str
    slug: str
    topic: Optional[str] = None
    summary: Optional[str] = None
    intro_text: Optional[str] = None
    cover_image_url: Optional[str] = None
    estimated_minutes: int
    status: str
    publish_date: Optional[date] = None
    questions: list[QuestionAdmin]
    result_profiles: list[ResultProfileOut]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    title: str
    slug: str
    topic: Optional[str] = None
    summary: Optional[str] = None
    intro_text: Optional[str] = None
    cover_image_url: Optional[str] = None
    estimated_minutes: int = 3
    status: str = "draft"
    publish_date: Optional[date] = None
    questions: list["QuestionCreate"] = []
    result_profiles: list["ResultProfileCreate"] = []


class QuestionCreate(BaseModel):
    question_text: str
    order_index: int = 0
    options: list["OptionCreate"] = []


class OptionCreate(BaseModel):
    option_text: str
    option_value_code: str
    score_payload: dict = {}
    order_index: int = 0


class ResultProfileCreate(BaseModel):
    code: str
    title: str
    short_label: Optional[str] = None
    description: Optional[str] = None
    strengths: Optional[list[str]] = None
    growth_tips: Optional[list[str]] = None
    encouragement: Optional[str] = None
    share_text: Optional[str] = None


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    topic: Optional[str] = None
    summary: Optional[str] = None
    intro_text: Optional[str] = None
    cover_image_url: Optional[str] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = None
    publish_date: Optional[date] = None

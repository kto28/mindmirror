from pydantic import BaseModel
from typing import Optional


class GenerateQuizRequest(BaseModel):
    topic: str
    secret: str


class PublishQuizRequest(BaseModel):
    quiz_id: int
    secret: str


class IngestTopicRequest(BaseModel):
    topic: str
    secret: str


class GenerateQuizResponse(BaseModel):
    quiz_id: int
    slug: str
    title: str
    status: str
    question_count: int


class AdminLoginRequest(BaseModel):
    password: str


class AdminLoginResponse(BaseModel):
    token: str

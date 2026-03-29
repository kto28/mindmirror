import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    ForeignKey,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    topic = Column(String(300), nullable=True)
    summary = Column(Text, nullable=True)
    intro_text = Column(Text, nullable=True)
    cover_image_url = Column(String(1000), nullable=True)
    estimated_minutes = Column(Integer, default=3)
    status = Column(String(20), default="draft", nullable=False, index=True)
    publish_date = Column(Date, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan", order_by="Question.order_index")
    result_profiles = relationship("ResultProfile", back_populates="quiz", cascade="all, delete-orphan")
    sessions = relationship("QuizSession", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan", order_by="QuestionOption.order_index")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    option_text = Column(Text, nullable=False)
    option_value_code = Column(String(50), nullable=False)
    score_payload = Column(JSON, nullable=False, default=dict)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    question = relationship("Question", back_populates="options")


class ResultProfile(Base):
    __tablename__ = "result_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    short_label = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True, default=list)
    growth_tips = Column(JSON, nullable=True, default=list)
    encouragement = Column(Text, nullable=True)
    share_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    quiz = relationship("Quiz", back_populates="result_profiles")

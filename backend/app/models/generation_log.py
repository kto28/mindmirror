from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.core.database import Base


class GenerationLog(Base):
    __tablename__ = "generation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_topic = Column(String(500), nullable=True)
    prompt_version = Column(String(50), nullable=True)
    raw_payload = Column(JSON, nullable=True)
    generation_status = Column(String(20), default="pending")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

"""Automation API routes — for n8n and external triggers."""

from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_automation_secret
from app.models.quiz import Quiz
from app.services.generation import generate_quiz_from_topic
from app.schemas.automation import (
    GenerateQuizRequest,
    PublishQuizRequest,
    IngestTopicRequest,
    GenerateQuizResponse,
)

router = APIRouter(prefix="/api/automation", tags=["automation"])


@router.post("/generate-quiz", response_model=GenerateQuizResponse)
def automation_generate_quiz(
    body: GenerateQuizRequest,
    db: Session = Depends(get_db),
):
    """Generate a quiz from a topic using OpenAI. Called by n8n."""
    if not verify_automation_secret(body.secret):
        raise HTTPException(status_code=403, detail="Invalid automation secret")

    try:
        quiz = generate_quiz_from_topic(db, body.topic)
        return GenerateQuizResponse(
            quiz_id=quiz.id,
            slug=quiz.slug,
            title=quiz.title,
            status=quiz.status,
            question_count=len(quiz.questions),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)[:500]}")


@router.post("/publish-quiz")
def automation_publish_quiz(
    body: PublishQuizRequest,
    db: Session = Depends(get_db),
):
    """Publish a quiz by ID. Called by n8n after review."""
    if not verify_automation_secret(body.secret):
        raise HTTPException(status_code=403, detail="Invalid automation secret")

    quiz = db.query(Quiz).filter(Quiz.id == body.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz.status = "published"
    if not quiz.publish_date:
        quiz.publish_date = date.today()
    db.commit()

    return {"success": True, "quiz_id": quiz.id, "status": "published"}


@router.post("/ingest-topic")
def automation_ingest_topic(
    body: IngestTopicRequest,
    db: Session = Depends(get_db),
):
    """Receive a topic from n8n, generate quiz, and return metadata."""
    if not verify_automation_secret(body.secret):
        raise HTTPException(status_code=403, detail="Invalid automation secret")

    try:
        quiz = generate_quiz_from_topic(db, body.topic)
        return {
            "success": True,
            "quiz_id": quiz.id,
            "slug": quiz.slug,
            "title": quiz.title,
            "status": quiz.status,
            "message": f"Quiz '{quiz.title}' created as draft. Publish via /api/automation/publish-quiz.",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)[:500])

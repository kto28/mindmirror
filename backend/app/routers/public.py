"""Public API routes — no authentication required."""

import hashlib
from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models.quiz import Quiz, Question, QuestionOption, ResultProfile
from app.models.session import QuizSession, QuizAnswer
from app.models.lead import Lead
from app.schemas.quiz import QuizCard, QuizDetail
from app.schemas.session import QuizSubmit, SessionResult, ResultProfileResult
from app.schemas.lead import LeadCreate, LeadOut
from app.services.scoring import calculate_result

router = APIRouter(prefix="/api", tags=["public"])


@router.get("/quizzes/today", response_model=QuizCard | None)
def get_today_quiz(db: Session = Depends(get_db)):
    """Get today's published quiz."""
    quiz = (
        db.query(Quiz)
        .filter(Quiz.status == "published", Quiz.publish_date <= date.today())
        .order_by(Quiz.publish_date.desc())
        .first()
    )
    if not quiz:
        return None
    return quiz


@router.get("/quizzes", response_model=list[QuizCard])
def list_quizzes(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    """List published quizzes, newest first."""
    quizzes = (
        db.query(Quiz)
        .filter(Quiz.status == "published")
        .order_by(Quiz.publish_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return quizzes


@router.get("/quizzes/{slug}", response_model=QuizDetail)
def get_quiz_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a single quiz by slug with questions and result profiles."""
    quiz = (
        db.query(Quiz)
        .options(
            joinedload(Quiz.questions).joinedload(Question.options),
            joinedload(Quiz.result_profiles),
        )
        .filter(Quiz.slug == slug, Quiz.status == "published")
        .first()
    )
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.post("/quizzes/{slug}/submit", response_model=SessionResult)
def submit_quiz(slug: str, body: QuizSubmit, request: Request, db: Session = Depends(get_db)):
    """Submit answers for a quiz and get the result."""
    quiz = (
        db.query(Quiz)
        .options(joinedload(Quiz.result_profiles))
        .filter(Quiz.slug == slug)
        .first()
    )
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if not body.answers:
        raise HTTPException(status_code=400, detail="No answers provided")

    # Calculate result
    answers_data = [{"question_id": a.question_id, "selected_option_id": a.selected_option_id} for a in body.answers]
    result_code = calculate_result(db, quiz.id, answers_data)

    # Hash IP for privacy
    ip = request.client.host if request.client else "unknown"
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]

    # Create session
    session = QuizSession(
        quiz_id=quiz.id,
        result_profile_code=result_code,
        user_agent=request.headers.get("user-agent", "")[:500],
        ip_hash=ip_hash,
    )
    db.add(session)
    db.flush()

    # Save answers
    for a in body.answers:
        answer = QuizAnswer(
            session_id=session.id,
            question_id=a.question_id,
            selected_option_id=a.selected_option_id,
        )
        db.add(answer)

    db.commit()
    db.refresh(session)

    # Find result profile
    profile = next((p for p in quiz.result_profiles if p.code == result_code), None)
    if not profile:
        raise HTTPException(status_code=500, detail="Result profile not found")

    return SessionResult(
        session_id=session.id,
        quiz_id=quiz.id,
        quiz_title=quiz.title,
        quiz_slug=quiz.slug,
        result_profile=ResultProfileResult.model_validate(profile),
        created_at=session.created_at,
    )


@router.get("/results/{session_id}", response_model=SessionResult)
def get_result(session_id: UUID, db: Session = Depends(get_db)):
    """Get a previously saved quiz result by session ID."""
    session = (
        db.query(QuizSession)
        .options(joinedload(QuizSession.quiz).joinedload(Quiz.result_profiles))
        .filter(QuizSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Result not found")

    profile = next(
        (p for p in session.quiz.result_profiles if p.code == session.result_profile_code),
        None,
    )
    if not profile:
        raise HTTPException(status_code=500, detail="Result profile not found")

    return SessionResult(
        session_id=session.id,
        quiz_id=session.quiz_id,
        quiz_title=session.quiz.title,
        quiz_slug=session.quiz.slug,
        result_profile=ResultProfileResult.model_validate(profile),
        created_at=session.created_at,
    )


@router.post("/leads", response_model=LeadOut)
def create_lead(body: LeadCreate, db: Session = Depends(get_db)):
    """Collect a lead (email, whatsapp, etc.)."""
    if not body.consent:
        raise HTTPException(status_code=400, detail="Consent is required")

    lead = Lead(
        quiz_id=body.quiz_id,
        session_id=body.session_id,
        name=body.name,
        email=body.email,
        whatsapp=body.whatsapp,
        consent=body.consent,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

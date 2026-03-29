"""Admin API routes — JWT-protected."""

from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.config import get_settings
from app.core.security import create_admin_token, verify_admin_token
from app.models.quiz import Quiz, Question, QuestionOption, ResultProfile
from app.models.session import QuizSession
from app.models.lead import Lead
from app.schemas.quiz import (
    QuizAdminList,
    QuizAdminDetail,
    QuizCreate,
    QuizUpdate,
    QuestionAdmin,
    OptionAdmin,
    ResultProfileOut,
)
from app.schemas.automation import AdminLoginRequest, AdminLoginResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(body: AdminLoginRequest):
    """Simple password-based admin login."""
    settings = get_settings()
    if body.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Invalid password")
    token = create_admin_token()
    return AdminLoginResponse(token=token)


@router.get("/quizzes", response_model=list[QuizAdminList])
def admin_list_quizzes(
    _admin: str = Depends(verify_admin_token),
    db: Session = Depends(get_db),
):
    """List all quizzes with session/lead counts."""
    quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).all()
    results = []
    for q in quizzes:
        session_count = db.query(func.count(QuizSession.id)).filter(QuizSession.quiz_id == q.id).scalar() or 0
        lead_count = db.query(func.count(Lead.id)).filter(Lead.quiz_id == q.id).scalar() or 0
        results.append(
            QuizAdminList(
                id=q.id,
                title=q.title,
                slug=q.slug,
                topic=q.topic,
                status=q.status,
                publish_date=q.publish_date,
                session_count=session_count,
                lead_count=lead_count,
                created_at=q.created_at,
            )
        )
    return results


@router.get("/quizzes/{quiz_id}", response_model=QuizAdminDetail)
def admin_get_quiz(
    quiz_id: int,
    _admin: str = Depends(verify_admin_token),
    db: Session = Depends(get_db),
):
    """Get full quiz detail for admin editing."""
    quiz = (
        db.query(Quiz)
        .options(
            joinedload(Quiz.questions).joinedload(Question.options),
            joinedload(Quiz.result_profiles),
        )
        .filter(Quiz.id == quiz_id)
        .first()
    )
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.post("/quizzes", response_model=QuizAdminDetail)
def admin_create_quiz(
    body: QuizCreate,
    _admin: str = Depends(verify_admin_token),
    db: Session = Depends(get_db),
):
    """Create a new quiz with questions and result profiles."""
    existing = db.query(Quiz).filter(Quiz.slug == body.slug).first()
    if existing:
        raise HTTPException(status_code=409, detail="Slug already exists")

    quiz = Quiz(
        title=body.title,
        slug=body.slug,
        topic=body.topic,
        summary=body.summary,
        intro_text=body.intro_text,
        cover_image_url=body.cover_image_url,
        estimated_minutes=body.estimated_minutes,
        status=body.status,
        publish_date=body.publish_date,
    )
    db.add(quiz)
    db.flush()

    for qi, q_data in enumerate(body.questions):
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data.question_text,
            order_index=q_data.order_index or qi,
        )
        db.add(question)
        db.flush()
        for oi, opt_data in enumerate(q_data.options):
            option = QuestionOption(
                question_id=question.id,
                option_text=opt_data.option_text,
                option_value_code=opt_data.option_value_code,
                score_payload=opt_data.score_payload,
                order_index=opt_data.order_index or oi,
            )
            db.add(option)

    for rp_data in body.result_profiles:
        profile = ResultProfile(
            quiz_id=quiz.id,
            code=rp_data.code,
            title=rp_data.title,
            short_label=rp_data.short_label,
            description=rp_data.description,
            strengths=rp_data.strengths,
            growth_tips=rp_data.growth_tips,
            encouragement=rp_data.encouragement,
            share_text=rp_data.share_text,
        )
        db.add(profile)

    db.commit()

    return admin_get_quiz(quiz.id, _admin, db)


@router.put("/quizzes/{quiz_id}")
def admin_update_quiz(
    quiz_id: int,
    body: QuizUpdate,
    _admin: str = Depends(verify_admin_token),
    db: Session = Depends(get_db),
):
    """Update quiz metadata (not questions)."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(quiz, key, value)

    db.commit()
    return {"success": True, "id": quiz.id}


@router.post("/quizzes/{quiz_id}/publish")
def admin_publish_quiz(
    quiz_id: int,
    _admin: str = Depends(verify_admin_token),
    db: Session = Depends(get_db),
):
    """Publish a quiz (set status to published + publish_date to today)."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz.status = "published"
    if not quiz.publish_date:
        quiz.publish_date = date.today()
    db.commit()
    return {"success": True, "id": quiz.id, "status": "published"}


@router.post("/quizzes/{quiz_id}/archive")
def admin_archive_quiz(
    quiz_id: int,
    _admin: str = Depends(verify_admin_token),
    db: Session = Depends(get_db),
):
    """Archive a quiz."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz.status = "archived"
    db.commit()
    return {"success": True, "id": quiz.id, "status": "archived"}

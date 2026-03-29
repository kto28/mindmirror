"""OpenAI quiz generation service — generates a full quiz from a topic."""

import json
import re
from openai import OpenAI
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models.quiz import Quiz, Question, QuestionOption, ResultProfile
from app.models.generation_log import GenerationLog
from app.prompts.quiz_prompt import build_quiz_prompt, QUIZ_JSON_SCHEMA

PROMPT_VERSION = "v1"


def generate_quiz_from_topic(db: Session, topic: str) -> Quiz:
    """Call OpenAI to generate a full quiz, validate, and persist to DB."""
    settings = get_settings()
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    log = GenerationLog(
        source_topic=topic,
        prompt_version=PROMPT_VERSION,
        generation_status="pending",
    )
    db.add(log)
    db.flush()

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        messages = build_quiz_prompt(topic)

        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.8,
            max_tokens=4000,
        )

        raw_content = response.choices[0].message.content or ""
        payload = json.loads(raw_content)

        log.raw_payload = payload
        log.generation_status = "success"

        quiz = _persist_quiz(db, payload, topic)
        db.commit()
        return quiz

    except Exception as e:
        log.generation_status = "error"
        log.error_message = str(e)[:2000]
        db.commit()
        raise


def _persist_quiz(db: Session, payload: dict, topic: str) -> Quiz:
    """Validate and save the generated quiz payload to the database."""
    title = payload["title"]
    slug = _make_slug(title)

    existing = db.query(Quiz).filter(Quiz.slug == slug).first()
    if existing:
        slug = slug + "-" + str(int(__import__("time").time()))

    quiz = Quiz(
        title=title,
        slug=slug,
        topic=topic,
        summary=payload.get("summary", ""),
        intro_text=payload.get("intro_text", ""),
        cover_image_url=payload.get("cover_image_url"),
        estimated_minutes=payload.get("estimated_minutes", 3),
        status="draft",
    )
    db.add(quiz)
    db.flush()

    for qi, q_data in enumerate(payload.get("questions", [])):
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data["question_text"],
            order_index=qi,
        )
        db.add(question)
        db.flush()

        for oi, opt_data in enumerate(q_data.get("options", [])):
            option = QuestionOption(
                question_id=question.id,
                option_text=opt_data["option_text"],
                option_value_code=opt_data["value_code"],
                score_payload=opt_data.get("score_map", {}),
                order_index=oi,
            )
            db.add(option)

    for rp_data in payload.get("result_profiles", []):
        profile = ResultProfile(
            quiz_id=quiz.id,
            code=rp_data["code"],
            title=rp_data["title"],
            short_label=rp_data.get("short_label"),
            description=rp_data.get("description"),
            strengths=rp_data.get("strengths", []),
            growth_tips=rp_data.get("growth_tips", []),
            encouragement=rp_data.get("encouragement"),
            share_text=rp_data.get("share_text"),
        )
        db.add(profile)

    db.flush()
    return quiz


def _make_slug(title: str) -> str:
    """Generate a URL-safe slug from a Chinese/English title."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = slug[:180]
    return slug

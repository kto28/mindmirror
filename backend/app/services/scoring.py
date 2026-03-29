"""Quiz scoring service — calculates result profile from user answers."""

from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.quiz import QuestionOption, ResultProfile


def calculate_result(
    db: Session,
    quiz_id: int,
    answers: list[dict],
) -> str:
    """
    Given a list of {question_id, selected_option_id}, compute scores
    against each result profile and return the winning profile code.

    Tie-break: alphabetical by profile code (deterministic).
    """
    scores: dict[str, float] = defaultdict(float)

    option_ids = [a["selected_option_id"] for a in answers]
    options = db.query(QuestionOption).filter(QuestionOption.id.in_(option_ids)).all()

    for opt in options:
        payload = opt.score_payload or {}
        for profile_code, score_val in payload.items():
            scores[profile_code] += float(score_val)

    if not scores:
        profiles = (
            db.query(ResultProfile)
            .filter(ResultProfile.quiz_id == quiz_id)
            .order_by(ResultProfile.code)
            .all()
        )
        return profiles[0].code if profiles else "unknown"

    max_score = max(scores.values())
    top_codes = sorted([code for code, s in scores.items() if s == max_score])
    return top_codes[0]

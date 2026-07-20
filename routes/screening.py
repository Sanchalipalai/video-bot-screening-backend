from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import InterviewAnswer

router = APIRouter()


@router.get("/candidate/{candidate_id}/screening")
def get_screening(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    # Get only the latest 3 interview answers
    answers = (
        db.query(InterviewAnswer)
        .filter(InterviewAnswer.candidate_id == candidate_id)
        .order_by(InterviewAnswer.id.desc())
        .limit(3)
        .all()
    )

    # Show them in the correct order: Q1 → Q2 → Q3
    answers.reverse()

    return {
        "answers": [
            {
                "id": answer.id,
                "question": answer.question,
                "video": answer.video_path,
                "transcript": answer.transcript,
                "score": answer.score,
                "feedback": answer.feedback,
            }
            for answer in answers
        ]
    }
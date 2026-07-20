from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import InterviewAnswer
from ai_service import analyze_transcript


router = APIRouter()



@router.post("/analyze-answer/{answer_id}")
def analyze_answer(
    answer_id: int,
    db: Session = Depends(get_db)
):


    answer = db.query(
        InterviewAnswer
    ).filter(
        InterviewAnswer.id == answer_id
    ).first()


    if not answer:

        return {
            "error": "Answer not found"
        }



    result = analyze_transcript(
        answer.question,
        answer.transcript
    )



    answer.score = result.get(
        "overall_score",
        0
    )


    answer.feedback = result.get(
        "feedback",
        ""
    )


    db.commit()


    return {

        "message": "Analysis complete",

        "score": answer.score,

        "feedback": answer.feedback

    }
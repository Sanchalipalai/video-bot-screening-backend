from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from models import Candidate, InterviewAnswer
from dotenv import load_dotenv
from database import get_db
from models import Candidate
from email_service import send_invite_email
load_dotenv()
router = APIRouter()


@router.post("/invite")
async def invite(
    email: str,
    db: Session = Depends(get_db)
):

    candidate = Candidate(
        name=email.split("@")[0],
        email=email,
        status="Invited"
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    frontend_url = os.getenv("FRONTEND_URL")
    link = f"{frontend_url}/interview/{candidate.interview_token}"

    await send_invite_email(email, link)

    return {
        "message": "Candidate invited successfully",
        "candidate_id": candidate.id,
        "interview_link": link
    }

@router.delete("/candidates/{candidate_id}")
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    # delete interview answers first
    db.query(InterviewAnswer).filter(
        InterviewAnswer.candidate_id == candidate_id
    ).delete()

    # delete candidate
    db.delete(candidate)

    db.commit()

    return {
        "message": "Candidate deleted successfully"
    }
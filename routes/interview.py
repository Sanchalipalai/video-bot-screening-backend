from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
import uuid

from database import get_db
from models import Candidate, InterviewAnswer
from supabase_client import supabase


router = APIRouter()


# Get all candidates
@router.get("/candidates")
def get_candidates(
    db: Session = Depends(get_db)
):

    candidates = db.query(Candidate).all()

    return [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "score": c.score,
            "status": c.status
        }
        for c in candidates
    ]



@router.post("/submit-interview")
def submit_interview(
    data: dict,
    db: Session = Depends(get_db)
):

    candidate_id = data.get("candidate_id")

    answers = data.get("answers", [])


    for answer in answers:

        video_url = answer.get("video_url")


        record = InterviewAnswer(

            candidate_id=candidate_id,

            question=answer.get("question"),

            video_path=video_url,

            transcript="Processing AI...",

            score=0,

            feedback="Pending analysis"

        )


        db.add(record)


    db.commit()


    return {
        "message":"Interview submitted successfully",
        "answers_saved":len(answers)
    }


# Recruiter screening data
@router.get("/candidate/{candidate_id}/screening")
def get_screening(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    answers = db.query(
        InterviewAnswer
    ).filter(
        InterviewAnswer.candidate_id == candidate_id
    ).all()


    return {

        "candidate_id": candidate_id,

        "answers": [

            {

                "question": answer.question,

                # already stored as URL
                "video": answer.video_path or "",

                "transcript": answer.transcript,

                "score": answer.score,

                "feedback": answer.feedback

            }

            for answer in answers

        ]

    }




# Upload video to Supabase
@router.post("/upload-interview/{candidate_id}")
async def upload_interview(
    candidate_id: int,
    question: str = Form(None),
    video: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    if video is None:
        return {
            "error": "No video received"
        }


    file_name = f"{candidate_id}_{uuid.uuid4()}.webm"


    video_data = await video.read()


    supabase.storage.from_(
        "interview-videos"
    ).upload(
        file_name,
        video_data,
        {
            "content-type":"video/webm"
        }
    )


    video_url = supabase.storage.from_(
        "interview-videos"
    ).get_public_url(
        file_name
    )


    answer = InterviewAnswer(

        candidate_id=candidate_id,

        question=question or "Question",

        video_path=video_url,

        transcript="Processing AI...",

        score=0,

        feedback="Pending analysis"

    )


    db.add(answer)

    db.commit()


    return {
        "message":"Uploaded",
        "video_url":video_url
    }
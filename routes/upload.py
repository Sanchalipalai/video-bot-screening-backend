from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from transcribe import transcribe_video
from ai_evaluator import evaluate_candidate
from database import get_db
from models import Candidate, InterviewAnswer

import uuid
import os
import requests


router = APIRouter()


class InterviewUpload(BaseModel):
    video_url: str
    question: str



@router.post("/upload-interview/{token}")
async def upload_interview(
    token: str,
    data: InterviewUpload,
    db: Session = Depends(get_db)
):

    print("TOKEN RECEIVED:", token)


    # Find candidate

    candidate = db.query(Candidate).filter(
        Candidate.interview_token == token
    ).first()


    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )


    candidate_id = candidate.id


    video_url = data.video_url
    question = data.question


    print("VIDEO URL RECEIVED:", video_url)
    print("QUESTION:", question)



    try:

        # -------------------------
        # Download video temporarily
        # -------------------------

        video_response = requests.get(video_url)


        if video_response.status_code != 200:

            raise Exception(
                "Could not download video"
            )


        video_data = video_response.content


        print(
            "VIDEO SIZE:",
            len(video_data)
        )


        os.makedirs(
            "temp",
            exist_ok=True
        )


        temp_file = f"temp/{uuid.uuid4()}.webm"


        with open(temp_file, "wb") as f:

            f.write(video_data)



        # -------------------------
        # Transcription
        # -------------------------

        try:

            transcript = transcribe_video(
                temp_file
            )


            print(
                "TRANSCRIPT:",
                transcript
            )


        except Exception as e:

            print(
                "TRANSCRIPTION ERROR:",
                e
            )


            transcript = "No transcript generated"



        # -------------------------
        # Rule Based Evaluation
        # -------------------------

        try:

            ai_result = evaluate_candidate(
                transcript,
                question
            )


            print(
                "AI RESULT:",
                ai_result
            )


        except Exception as e:

            print(
                "EVALUATION ERROR:",
                e
            )


            ai_result = {

                "overall_score": 0,

                "feedback": "Evaluation failed"

            }



        # -------------------------
        # Save Answer
        # -------------------------

        answer = InterviewAnswer(

            candidate_id=candidate_id,

            question=question,

            video_path=video_url,

            transcript=transcript,

            score=ai_result.get(
                "overall_score",
                0
            ),

            feedback=ai_result.get(
                "feedback",
                ""
            )

        )


        db.add(answer)

        db.commit()

        db.refresh(answer)



        print(
            "ANSWER SAVED ID:",
            answer.id
        )



        # Remove temp file

        if os.path.exists(temp_file):

            os.remove(temp_file)



        return {

            "message": "Uploaded successfully",

            "answer_id": answer.id,

            "video_url": video_url,

            "transcript": transcript,

            "score": ai_result.get(
                "overall_score",
                0
            ),

            "feedback": ai_result.get(
                "feedback",
                ""
            )

        }



    except Exception as e:


        print(
            "UPLOAD ERROR:",
            e
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
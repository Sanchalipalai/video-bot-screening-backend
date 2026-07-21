from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from supabase_client import supabase
from transcribe import transcribe_video
from ai_service import analyze_transcript
from database import get_db
from models import InterviewAnswer

import uuid
import os


router = APIRouter()


@router.post("/upload-interview/{token}")
async def upload_interview(
    token: str,
    question: str = Form(None),
    video: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    
    # Find candidate using the interview token
    candidate = db.query(Candidate).filter(
        Candidate.interview_token == token
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    candidate_id = candidate.id

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
            "content-type": "video/webm"
        }
    )

    try:

        

        print("RECEIVED VIDEO:", video.filename)
        print("QUESTION:", question)


        # Read video
        video_data = await video.read()

        print("VIDEO SIZE:", len(video_data))


        # Save temporary video for transcription
        os.makedirs("temp", exist_ok=True)

        temp_file = f"temp/{uuid.uuid4()}.mp4"


        with open(temp_file, "wb") as f:
            f.write(video_data)



        # Generate transcript
        try:

            transcript = transcribe_video(temp_file)

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



        # Grok AI Evaluation
        try:

            ai_result = analyze_transcript(
                question,
                transcript
            )


            print(
                "AI RESULT:",
                ai_result
            )


        except Exception as e:

            print(
                "AI ANALYSIS ERROR:",
                e
            )

            ai_result = {

                "overall_score": 0,

                "feedback": "AI evaluation failed"

            }



        # Upload video to Supabase

        file_name = (
            f"{candidate_id}_{uuid.uuid4()}.webm"
        )


        supabase.storage.from_(
            "interview-videos"
        ).upload(
            file_name,
            video_data,
            {
                "content-type": "video/webm"
            }
        )


        video_url = supabase.storage.from_(
            "interview-videos"
        ).get_public_url(
            file_name
        )


        print(
            "VIDEO URL:",
            video_url
        )



        # Save everything to database

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



        # Delete temporary file

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


        return {

            "message": "Upload failed",

            "error": str(e)

        }
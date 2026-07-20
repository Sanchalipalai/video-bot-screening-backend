from sqlalchemy import Column, Integer, String, Float
from database import Base


class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False
    )

    score = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="Review"
    )



class InterviewAnswer(Base):

    __tablename__ = "interview_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidate_id = Column(
        Integer
    )

    question = Column(
        String
    )

    video_path = Column(
        String
    )

    transcript = Column(
        String
    )

    score = Column(
        Float,
        default=0
    )

    feedback = Column(
        String
    )
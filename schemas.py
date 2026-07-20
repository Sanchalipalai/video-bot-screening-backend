from pydantic import BaseModel


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    score: float | None = None
    status: str | None = None

    class Config:
        from_attributes = True


class CandidateCreate(BaseModel):
    name: str
    email: str
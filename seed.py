from database import SessionLocal
from models import Candidate

db = SessionLocal()

candidate = Candidate(
    name="John Smith",
    email="john@example.com",
    status="Completed",
    score=92
)

db.add(candidate)
db.commit()

print("Candidate added.")
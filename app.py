from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from database import Base, engine

from routes import auth
from routes import upload
from routes import interview
from routes import analysis
from routes import invite
from routes import screening


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Video Bot Screening"
)


# CORS
from fastapi.middleware.cors import CORSMiddleware
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5176"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("uploads", exist_ok=True)

# Static videos
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# Routes

app.include_router(
    invite.router
)


app.include_router(
    upload.router,
    prefix="/api",
    tags=["Upload"]
)


app.include_router(
    auth.router,
    prefix="/api",
    tags=["Auth"]
)


app.include_router(
    interview.router,
    prefix="/api",
    tags=["Interview"]
)


app.include_router(
    analysis.router,
    prefix="/api",
    tags=["Analysis"]
)


app.include_router(
    screening.router,
    prefix="/api",
    tags=["Screening"]
)



@app.get("/")
def home():
    return {
        "message": "Video Bot Screening API Running"
    }
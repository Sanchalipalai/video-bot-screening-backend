import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = "sqlite:///./videobot.db"

# Gmail SMTP
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Frontend URL
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

# OpenAI Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
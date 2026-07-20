import os
from dotenv import load_dotenv

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_EMAIL"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_SSL_TLS=True,
    MAIL_STARTTLS=False,
    USE_CREDENTIALS=True,
)


async def send_invite_email(candidate_email: str, interview_link: str):

    print("Preparing email for:", candidate_email)


    message = MessageSchema(
        subject="Video Interview Invitation",
        recipients=[candidate_email],
        body=f"""
Hello,

You have been invited for a Video Bot Screening interview.

Please click the link below to start your interview:

{interview_link}

Best of luck!
""",
        subtype="plain"
    )


    try:

        fm = FastMail(conf)

        await fm.send_message(message)

        print("EMAIL SENT SUCCESSFULLY")


    except Exception as e:

        print("EMAIL ERROR:", e)

        raise e
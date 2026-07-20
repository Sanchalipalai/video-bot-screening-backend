import os
from dotenv import load_dotenv
import httpx

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
MAIL_FROM = os.getenv("MAIL_FROM")


async def send_invite_email(candidate_email: str, interview_link: str):

    print("Sending email using Brevo")

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Video Bot Screening",
            "email": MAIL_FROM
        },
        "to": [
            {
                "email": candidate_email
            }
        ],
        "subject": "Video Interview Invitation",
        "textContent": f"""
Hello,

You have been invited for a Video Bot Screening interview.

Start your interview here:

{interview_link}

Best of luck!
"""
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.brevo.com/v3/smtp/email",
            headers=headers,
            json=data
        )

    print("Brevo response:", response.status_code, response.text)

    if response.status_code not in [200, 201]:
        raise Exception(response.text)

    print("EMAIL SENT SUCCESSFULLY")
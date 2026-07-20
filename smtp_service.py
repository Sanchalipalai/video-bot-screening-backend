import smtplib
from email.message import EmailMessage
from config import SMTP_EMAIL, SMTP_PASSWORD


def send_email(to_email, link):

    msg = EmailMessage()

    msg["Subject"] = "AI Video Interview Invitation"

    msg["From"] = SMTP_EMAIL

    msg["To"] = to_email


    msg.set_content(
        f"""
You are invited for an AI interview.

Click here:
{link}
"""
    )


    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()


    server.login(
        SMTP_EMAIL,
        SMTP_PASSWORD
    )


    server.send_message(msg)

    server.quit()
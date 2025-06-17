import smtplib
from email.message import EmailMessage
import os 
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email: str, subject: str, body: str):
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

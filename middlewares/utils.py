import smtplib
from email.message import EmailMessage


def send_email(to_email: str, subject: str, body: str):
    EMAIL = "noreplyfastapi123@gmail.com"
    PASSWORD = "rngp wxyf wavi cyer"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

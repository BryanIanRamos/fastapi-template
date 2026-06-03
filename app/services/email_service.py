import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_email(to: str, subject: str, body: str):
    """Sends an email using SMTP"""
    try:
        # Use settings for SMTP configuration
        smtp_server = getattr(settings, "SMTP_SERVER", "smtp.gmail.com")
        smtp_port = getattr(settings, "SMTP_PORT", 587)
        smtp_user = getattr(settings, "SMTP_USER", "")
        smtp_password = getattr(settings, "SMTP_PASSWORD", "")

        message = MIMEMultipart()
        message["From"] = smtp_user
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)
            
    except Exception as e:
        # Raise the exception so the calling service knows the email failed
        print(f"SMTP Error: {e}")
        raise e
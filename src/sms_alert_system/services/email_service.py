import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email: str, subject: str, body: str, simulation_mode: bool = True):
    """Send email through SMTP; simulation mode never contacts the mail server."""
    to_email = (to_email or "").strip()
    if not to_email:
        return {"success": False, "status": "SKIPPED", "error": "No email address configured."}
    if simulation_mode:
        print(f"[SIMULATION EMAIL] To={to_email} | Subject={subject} | Body={body}")
        return {"success": True, "status": "SIMULATED", "error": None}
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME", "")
    password = os.getenv("SMTP_APP_PASSWORD", "")
    sender = os.getenv("SMTP_FROM_EMAIL", username)
    if not username or not password or not sender:
        return {"success": False, "status": "FAILED", "error": "SMTP credentials are not configured."}
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        return {"success": True, "status": "SENT", "error": None}
    except Exception as exc:
        return {"success": False, "status": "FAILED", "error": str(exc)}

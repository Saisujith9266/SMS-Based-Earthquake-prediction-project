import logging
import time
from twilio.rest import Client
from services.config import settings

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self, simulation_mode=None):
        self.simulation_mode = settings.SIMULATION_MODE if simulation_mode is None else simulation_mode

    def send_sms(self, to_number: str, body: str):
        if self.simulation_mode:
            logger.info("[SIMULATION] SMS to %s: %s", to_number, body)
            return {"success": True, "sid": "SIMULATED", "error": None}

        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
            return {"success": False, "sid": None, "error": "Twilio credentials are not configured."}

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        last_error = None
        for attempt in range(1, settings.MAX_RETRIES + 1):
            try:
                msg = client.messages.create(body=body, from_=settings.TWILIO_PHONE_NUMBER, to=to_number)
                return {"success": True, "sid": msg.sid, "error": None, "status": msg.status}
            except Exception as exc:
                last_error = str(exc)
                logger.exception("Twilio attempt %s/%s failed", attempt, settings.MAX_RETRIES)
                if attempt < settings.MAX_RETRIES:
                    time.sleep(settings.RETRY_DELAY_SECONDS * attempt)
        return {"success": False, "sid": None, "error": last_error}

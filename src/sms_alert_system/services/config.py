import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}

@dataclass(frozen=True)
class Settings:
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///earthquake_alerts.db")
    SIMULATION_MODE: bool = env_bool("SIMULATION_MODE", True)
    DEFAULT_RADIUS_KM: float = float(os.getenv("DEFAULT_RADIUS_KM", "50"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY_SECONDS: float = float(os.getenv("RETRY_DELAY_SECONDS", "2"))

settings = Settings()

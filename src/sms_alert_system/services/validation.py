import re

E164_RE = re.compile(r"^\+[1-9]\d{7,14}$")

def validate_phone(phone: str):
    phone = phone.strip()
    if not E164_RE.fullmatch(phone):
        return False, "Use international E.164 format, for example +919876543210."
    return True, ""

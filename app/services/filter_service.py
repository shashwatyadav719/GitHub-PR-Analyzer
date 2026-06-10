import re

SENSITIVE_KEYS = [
    "api_key",
    "secret",
    "token",
    "password",
    "authorization",
    "private_key",
    "aws"
]

def filter_text(text: str):
    for key in SENSITIVE_KEYS:
        
        pattern = rf"{key}\s*[:=]\s*\S+"

        def replace(match):
            return f"{key} = [REDACTED]"

        text = re.sub(pattern, replace, text, flags=re.IGNORECASE)

    return text
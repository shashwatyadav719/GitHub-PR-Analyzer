from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


def _validate_env_var(var_name: str, required: bool = True) -> Optional[str]:
    """Validate environment variable and return its value or raise error."""
    value = os.getenv(var_name)
    if required and not value:
        raise ValueError(f"Required environment variable {var_name} is missing")
    return value


def _validate_jwt_secret(secret: str) -> str:
    """Validate JWT secret key meets security requirements."""
    if not secret:
        raise ValueError("JWT_SECRET_KEY is required")
    if len(secret) < 32:
        raise ValueError(
            f"JWT_SECRET_KEY must be at least 32 characters long for security. "
            f"Current length: {len(secret)}"
        )
    return secret


# Required environment variables
GITHUB_CLIENT_ID = _validate_env_var("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = _validate_env_var("GITHUB_CLIENT_SECRET")
OPENROUTER_API_KEY = _validate_env_var("OPENROUTER_API_KEY")
HF_TOKEN = _validate_env_var("HF_TOKEN")

# JWT configuration with validation
_jwt_secret = _validate_env_var("JWT_SECRET_KEY")
JWT_SECRET_KEY = _validate_jwt_secret(_jwt_secret)
JWT_ALGORITHM = _validate_env_var("JWT_ALGORITHM", required=False) or "HS256"

# Optional environment variables with defaults
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    _validate_env_var("ACCESS_TOKEN_EXPIRE_MINUTES", required=False) or "30"
)
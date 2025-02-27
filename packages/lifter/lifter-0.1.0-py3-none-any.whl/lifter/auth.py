import os

VALID_TOKENS = os.getenv("VALID_TOKENS", "").split(",")  # Store tokens in ENV

def authenticate(token: str) -> bool:
    """Validate if the provided token is authorized."""
    return token in VALID_TOKENS

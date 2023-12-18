""" Authentication-related utility functions.

utils/auth.py
"""

import hashlib
import secrets


def generate_token() -> str:
    """Generate a random session token."""
    return secrets.token_hex(16)


def hash_token(token: str) -> str:
    """Hash a session token."""
    return hashlib.sha256(token.encode()).hexdigest()

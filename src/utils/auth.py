""" Authentication-related utility functions.

utils/auth.py
"""

import hashlib
import secrets
import bcrypt


def generate_token() -> str:
    """Generate a random non-hashed session token."""
    return secrets.token_hex(16)


def hash_token(token: str) -> str:
    """Hash a session token using SHA-256."""
    return hashlib.sha256(token.encode()).hexdigest()


def hash_password(password: str) -> str:
    """Hash a password using the bcrypt password."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def compare_passwords(password_input: str, password_hash: str) -> bool:
    """Compare a password input with a bcrypt hashed-password."""
    return bcrypt.checkpw(password_input.encode(), password_hash.encode())

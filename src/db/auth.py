""" Functions for managing users and sessions.
db/auth.py
"""

from src.db.schemas import User
from src.db.schemas import Session as auth_Session
import utils.auth

from sqlalchemy.orm import Session
import random


# Functions used for creating users.
def create_user(db_session: Session, username: str, code: int, balance: int) -> User:
    """Add a user to the database."""
    db_session.add(User(username=username, code=code, balance=balance))
    db_session.commit()


def code_exists(db_session: Session, code: int) -> bool:
    """Check if a code exists in the database."""
    return db_session.query(User).filter(User.code == code).count() > 0


def user_exists(db_session: Session, username: str) -> bool:
    """Check if a username exists in the database."""
    return db_session.query(User).filter(User.username == username).count() > 0


def create_session(db_session: Session, user_id: int, token: str) -> None:
    """Create a session for a user given a non-hashed session token."""
    db_session.add(
        auth_Session(user=user_id, hashed_token=utils.auth.hash_token(token))
    )
    db_session.commit()


def session_token_is_valid(db_session: Session, user_id: int, token: str) -> bool:
    """Returns True if a session token and user_id are valid.
    This is the main function used for authentication using a session token.
    """
    hashed_token = utils.auth.hash_token(token)
    return (
        db_session.query(auth_Session)
        .filter(auth_Session.user == user_id, auth_Session.hashed_token == hashed_token)
        .count() == 1
    )


def random_valid_code(db_session: Session, max_tries: int = 10) -> int:
    """Generate a random valid code.

    Will try 10 random codes, afterwards it will increment the
    code by one until it finds a valid code.

    TODO: Find better way to generate pseudo-random codes. Keep track of unused codes.
    """

    # Try 10 random codes.
    for _ in range(max_tries):
        code = random.randint(100000, 999999)
        if not code_exists(db_session, code):
            return code

    # Increment the code by one until it finds a valid code.
    code = 100000
    while code < 999999:
        if not code_exists(db_session, code):
            return code
        code += 1
    raise Exception("No valid code found. Too many users.")

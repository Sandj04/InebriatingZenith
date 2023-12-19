""" Functions for managing users and sessions.
db/auth.py
"""

from src.db.schemas import User, Admin, AdminSession
from src.db.schemas import (
    Session as auth_Session,
)  # TODO: Refactor this name to AuthSession or UserSession.
import utils.auth

from sqlalchemy.orm import Session  # TODO: Refactor this name to DBSession.
import random


# Functions used for creating users.
def create_user(db_session: Session, username: str, code: int, balance: int) -> User:
    """Add a user to the database."""
    user = User(username=username, code=code, balance=balance)
    db_session.add(user)
    db_session.commit()
    return user


def code_exists(db_session: Session, code: int) -> bool:
    """Check if a code exists in the database."""
    return db_session.query(User).filter(User.code == code).count() > 0


def user_exists(db_session: Session, username: str) -> bool:
    """Check if a username exists in the database."""
    return db_session.query(User).filter(User.username == username).count() > 0


def create_session(db_session: Session, user_id: int) -> auth_Session:
    """Create a session for a user."""
    new_session = auth_Session(
        user=user_id, hashed_token=utils.auth.hash_token(utils.auth.generate_token())
    )
    db_session.add(new_session)
    db_session.commit()
    return new_session


def session_valid(db_session: Session, user_id: int, token: str) -> bool:
    """Returns True if a session token and user_id are valid.
    This is the main function used for authentication using a session token.
    """
    hashed_token = utils.auth.hash_token(token)
    return ( # TODO Should we retrieve the session token and check it on the server?
        db_session.query(auth_Session)
        .filter(auth_Session.user == user_id, auth_Session.hashed_token == hashed_token)
        .count()
        == 1
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


# Admin authentication.
def create_admin(db_session: Session, username: str, password: str) -> Admin:
    """Create an admin user."""
    new_admin = Admin(
        username=username,
        password=utils.auth.hash_password(password),
    )
    db_session.add(new_admin)
    db_session.commit()
    return new_admin


def admin_exists(db_session: Session, admin_username: str) -> bool:
    """Check if an admin exists."""
    return db_session.query(Admin).filter(Admin.username == admin_username).count() > 0


def admin_password_valid(
    db_session: Session, admin_username: str, password: str
) -> bool:
    """Check if an admin password is valid."""
    hashed_password = (
        db_session.query(Admin).filter(Admin.username == admin_username).first()
    )  # Retrieve the hashed password from the admins table.

    if hashed_password is None:  # Admin does not exist.
        return False

    return utils.auth.compare_passwords(password, hashed_password.password)


def create_admin_session(db_session: Session, admin_username: str) -> AdminSession:
    """Create a session for an admin."""
    new_session = auth_Session(
        admin=admin_username,
        hashed_token=utils.auth.hash_token(utils.auth.generate_token()),
    )
    db_session.add(new_session)
    db_session.commit()
    return new_session

def admin_session_valid(db_session: Session, admin_username: str, token: str) -> bool:
    """Returns True if a session token and admin_username are valid.
    This is the main function used for admin authentication using a session token.
    """
    hashed_token = utils.auth.hash_token(token)
    return ( # TODO Should we retrieve the session token and check it on the server?
        db_session.query(auth_Session)
        .filter(auth_Session.admin == admin_username, auth_Session.hashed_token == hashed_token)
        .count()
        == 1
    )
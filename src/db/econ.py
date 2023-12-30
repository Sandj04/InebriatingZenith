from src.db.schemas import User
from sqlalchemy.orm import Session as DBSession


def add_balance(db_session: DBSession, user_id: int, amount: int) -> None:
    """Add balance to a user's balance."""
    user = db_session.query(User).filter(User.id == user_id).first()
    if user is None:
        # Tried adding balance to a user that does not exist.
        print("User does not exist.")
        return
    user.balance += amount
    db_session.commit()
    return


def remove_balance(db_session: DBSession, user_id: int, amount: int) -> None:
    """Remove balance from a user's balance."""
    user = db_session.query(User).filter(User.id == user_id).first()
    if user is None:
        print("User does not exist.")
        return
    user.balance -= amount
    db_session.commit()
    return


def get_user_balance(db_session: DBSession, user_id: int) -> int:
    """Get a user's balance."""
    user = db_session.query(User).filter(User.id == user_id).first()
    if user is None:
        print("User does not exist.")
        return 0
    return user.balance

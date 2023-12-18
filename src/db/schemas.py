from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
import sqlalchemy

Base = declarative_base()  # Create a base class for all models to inherit from.


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement="auto",
    )  # The ID of the user.
    username: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(30), unique=True, nullable=False
    )  # The username of the user. Max length is 30 characters.
    code: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False,
    )  # A unique 6 digit code that is used to authenticate the user.
    balance: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False,
    )  # The balance of the user represented in hundreths.

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, code={self.code}, balance={self.balance})>"


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement="auto",
    )  # The ID of the user's session.
    user: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("users.id"), nullable=False,
    )  # The ID of the user.
    hashed_token: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(30), nullable=False, unique=True, # Should this be unique?
    )  # The token of the user's session.

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user={self.user}, hashed_token={self.hashed_token})>"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
import sqlalchemy
from datetime import datetime

Base = declarative_base()  # Create a base class for all models to inherit from.


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of the user.
    username: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(30), unique=True, nullable=False
    )  # The username of the user. Max length is 30 characters.
    code: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )  # A unique 6 digit code that is used to authenticate the user.
    balance: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )  # The balance of the user represented in hundreths.

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, code={self.code}, balance={self.balance})>"


class Session(Base):
    __tablename__ = "sessions"

    # TODO: Add expiry to sessions.

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of the user's session.
    user: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    )  # The ID of the user.
    hashed_token: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(64),
        nullable=False,  # TODO Index this column.
    )  # The token of the user's session.

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user={self.user}, hashed_token={self.hashed_token})>"


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of a user's cart.
    user: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    )  # The ID of the user.
    payed: Mapped[bool] = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable=False,
    )  # Whether the cart has been payed for or not.
    ready: Mapped[bool] = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable=False,
    )  # Whether the cart is ready for pickup or not.
    delivered: Mapped[bool] = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable=False,
    )  # Whether the cart has been delivered/picked up or not.

    def __repr__(self) -> str:
        return f"<Cart(id={self.id}, user={self.user}, payed={self.payed}, ready={self.ready}, delivered={self.delivered})>"


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of a cart item.
    cart: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("carts.id"),
        nullable=False,
    )  # The ID of the cart.
    product: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("products.id"),
        nullable=False,
    )  # The ID of the product.


def __repr__(self) -> str:
    return f"<CartItem(id={self.id}, cart={self.cart}, product={self.product}>"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of a product.
    name: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(30),
        nullable=False,
    )  # The name of the product.
    description: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(100),
        nullable=False,
    )  # The description of the product.
    category: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("categories.id"),
        nullable=False,
    )  # The ID of the category.
    price: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )  # The price of the product in hundreths.
    ingredients: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
    )  # The ingredients of the product. #TODO make this a json representation of a list of ingredients.
    unlock_time: Mapped[datetime] = sqlalchemy.Column(
        sqlalchemy.DateTime,
        nullable=True,
    )  # The time at which the product is unlocked.

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, description={self.description}, category={self.category}, price={self.price}, ingredients={self.ingredients}, unlock_time={self.unlock_time})>"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of a category.
    name: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(30),
        nullable=False,
    )  # The name of the category.
    icon_path: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
    )  # The path to the icon of the category.


class UserTask(Base):
    __tablename__ = "user_tasks"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of a user task.
    user: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    )  # The ID of the user.
    task: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("tasks.id"),
        nullable=False,
    )  # The ID of the task.
    completed: Mapped[bool] = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable=False,
    )  # Whether the task has been completed or not.

    def __repr__(self) -> str:
        return f"<UserTask(id={self.id}, user={self.user}, task={self.task}, completed={self.completed})>"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of a task.
    description: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(100),
        nullable=False,
    )  # The description of the task.
    reward: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )  # The reward of the task in hundreths.

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, name={self.name}, description={self.description}, category={self.category}, unlock_time={self.unlock_time})>"


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of an admin.
    username: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(30),
        nullable=False,
        unique=True,
    )  # The username of the admin.
    hashed_password: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
    )  # The password of the admin.

    def __repr__(self) -> str:
        return (
            f"<Admin(id={self.id}, username={self.username}, password={self.password})>"
        )


class AdminSession(Base):
    __tablename__ = "admin_sessions"

    id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement="auto",
    )  # The ID of an admin session.
    admin: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.ForeignKey("admins.id"),
        nullable=False,
    )  # The ID of the admin.
    hashed_token: Mapped[str] = sqlalchemy.Column(
        sqlalchemy.String(64),
        nullable=False,  # TODO Index this column.
    )  # The token of the admin's session.

    def __repr__(self) -> str:
        return f"<AdminSession(id={self.id}, admin={self.admin}, hashed_token={self.hashed_token})>"

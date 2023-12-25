""" Flask routing for admin utilities."""

from flask import Blueprint, render_template, request, make_response
from flask import g as FlaskGlobals
import src.utils.config
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from src.db import auth

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

db_engine = sqlalchemy.create_engine(
    src.utils.config.Config.get_database_connection_string(),
    echo=True,  # Set to True to see SQL queries in the console.
)

# Initialize connection to database.
db_conn = db_engine.connect()

# Create a session.
SessionMaker = sessionmaker(bind=db_engine)
db_session = SessionMaker()

@admin_blueprint.route("/", methods=["GET"])
def admin_index() -> str:
    return render_template("/admin/index.html")

@admin_blueprint.route("/api/login", methods=["POST"])
def login() -> str:
    username = request.args.get("username")
    password = request.args.get("password")
    
    if username is None or password is None:
        return "Invalid username or password."
    
    if auth.admin_password_valid(db_session, username, password):
        return "It works!"
    
    return "Something went wrong!"
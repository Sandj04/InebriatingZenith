""" Flask routing for admin utilities."""

from flask import (
    Blueprint,
    render_template,
    request,
    make_response,
    Response,
    jsonify,
    redirect,
)
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


@admin_blueprint.before_request
def check_credentials():
    """Check if the user is authenticated."""

    # Paths that do not require admin authentication.
    PATH_EXCLUSIONS = ["/admin/api/login", "/admin/"]

    if request.path not in PATH_EXCLUSIONS:
        admin_id = request.cookies.get("admin_id")
        token = request.cookies.get("token")

        if admin_id is None or not admin_id.isnumeric():
            print("1")
            return redirect("/admin")

        if token is None:
            print("2")
            return redirect("/admin")

        if len(token) != 64:
            print("3")
            return redirect("/admin")

        admin_id = int(admin_id)

        if not auth.admin_session_valid(db_session, token):
            print("4")
            return redirect("/admin")


@admin_blueprint.route("/", methods=["GET"])
def admin_index() -> str:
    return render_template("/admin/index.html")


@admin_blueprint.route("/dashboard", methods=["GET"])
def admin_dashboard() -> str:
    return "Hello, World!"


@admin_blueprint.route("/api/login", methods=["POST"])
def login() -> Response:
    username = request.form.get("username")
    password = request.form.get("password")

    print(username, password)

    if not username or not password:
        return jsonify(
            {
                "success": False,
                "message": "Missing username or password.",
            }
        )

    if auth.admin_password_valid(db_session, username, password):
        admin_id = auth.get_admin_id_from_username(db_session, username)
        if admin_id is None:
            raise Exception("Race condition happened. (admin username result is None)")
        return jsonify(
            {
                "success": True,
                "message": "Successfully logged in.",
                "token": auth.create_admin_session(db_session, admin_id).hashed_token,
                "admin_id": admin_id,
            }
        )

    return jsonify(
        {
            "success": False,
            "message": "Invalid credentials.",
        }
    )

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
            return redirect("/admin")

        if token is None:
            return redirect("/admin")

        if len(token) != 64:
            return redirect("/admin")

        admin_id = int(admin_id)

        if not auth.admin_session_valid(db_session, token):
            return redirect("/admin")


@admin_blueprint.route("/", methods=["GET"])
def index() -> str:
    return render_template("/admin/index.html")


@admin_blueprint.route("/dashboard", methods=["GET"])
def dashboard() -> str:
    return render_template("/admin/dashboard.html")


@admin_blueprint.route("/user_auth", methods=["GET"])
def user_authentication_management():
    return render_template("/admin/user_auth.html")

# TODO User balance management.
# TODO Order Management.
# TODO Product Management.

# --------------------------------------------------------------------------------------
# APIs
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


@admin_blueprint.route("/api/add_admin", methods=["POST"])
def add_admin() -> Response:
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify(
            {
                "success": False,
                "message": "Missing username or password.",
            }
        )

    if auth.admin_exists(db_session, username):
        return jsonify(
            {
                "success": False,
                "message": "Username already exists.",
            }
        )

    created = auth.create_admin(db_session, username, password)

    return jsonify(
        {
            "success": True,
            "message": f"Successfully added admin with ID {created.id}.",
            "admin_id": created.id,
        }
    )

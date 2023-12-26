import flask
from flask import render_template, request, redirect, make_response, jsonify
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# Local imports.
from src.db.schemas import Base
from src.db.products import load_products_from_yaml
from src.db.auth import session_valid, setup_root_admin
from src.db import ordering
from src import easy
from src.admin_client import admin_blueprint
import src.utils.config
from src.utils.realtime import OrderQueue

db_engine = sqlalchemy.create_engine(
    src.utils.config.Config.get_database_connection_string(),
    echo=True,  # ? Set to True to see SQL queries in the console.
)

# Globals
# --------------------------------------------------------------------------------------
# Start a flask app in development mode where the templates are reloaded upon change.
app = flask.Flask(
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
)

app.register_blueprint(admin_blueprint)

# Initialize connection to database.
db_conn = db_engine.connect()

# Create all tables using the metadata.
Base.metadata.create_all(db_engine)

# Create a session.
SessionMaker = sessionmaker(bind=db_engine)
db_session = SessionMaker()

ORDER_QUEUE = OrderQueue(db_session)
# --------------------------------------------------------------------------------------


# Routes
@app.route("/", methods=["GET"])
def index() -> flask.Response:
    session_token = request.cookies.get("session_token")
    user_id = request.cookies.get("user")

    if user_id is None or not user_id.isnumeric():
        res = make_response(render_template("index.html"))
        easy.reset_cookies(res)
        return res

    user_id = int(user_id)

    if session_token is None or not session_valid(db_session, user_id, session_token):
        res = make_response(render_template("index.html"))
        easy.reset_cookies(res)
        return res

    return make_response(redirect("/order_page"))


# Functions handled before each request.
# --------------------------------------------------------------------------------------
@app.before_request
def authentication_check():
    """Check if the user is authenticated."""

    # Paths that do not require authentication.
    PATH_EXCLUSIONS = ["/", "/api/login"]

    if request.path not in PATH_EXCLUSIONS:
        session_token = request.cookies.get("session_token")
        user_id = request.cookies.get("user")

        if user_id is None or not user_id.isnumeric():
            return jsonify(
                {
                    "success": False,
                    "message": "Invalid user ID.",
                }
            )

        user_id = int(user_id)

        if session_token is None or not session_valid(
            db_session, user_id, session_token
        ):
            return jsonify(
                {
                    "success": False,
                    "message": "Invalid session token.",
                }
            )


# API Routes
# --------------------------------------------------------------------------------------
@app.route("/api/add_to_cart", methods=["POST"])
def add_to_cart():
    user_id = request.cookies.get("user")

    if user_id is None or not user_id.isnumeric():
        return jsonify(
            {
                "success": False,
                "message": "Invalid user ID.",
            }
        )

    user_id = int(user_id)

    product_id = request.form.get("product_id")

    if product_id is None or not product_id.isnumeric():
        return make_response("Invalid product ID.", 200)

    product_id = int(product_id)

    ordering.add_to_cart(db_session, user_id, product_id)

    return make_response("OK", 200)


def init_dev_server() -> None:
    # Load all products from the 'products.yml' file.
    load_products_from_yaml(db_session)

    # Set up the root admin user.
    setup_root_admin(
        db_session,
        src.utils.config.Config.root_admin_username,
        src.utils.config.Config.root_admin_password,
    )

    app.run(debug=True, port=5000)

    print("Stopping the server...")
    db_conn.close()  # CLose the database connection.
    db_engine.dispose()  # Dispose of the database engine.
    print("Server stopped.")

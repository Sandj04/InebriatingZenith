import flask
from flask import render_template, request, redirect, make_response, jsonify
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# Local imports.
from src.db.schemas import Base
from src.db.products import load_products_from_yaml, get_product_by_id
from src.db import auth
from src.db import ordering
from src.db import tasks as TasksDB
from src.db import econ as EconDB
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

    if session_token is None or not auth.session_valid(
        db_session, user_id, session_token
    ):
        res = make_response(render_template("index.html"))
        easy.reset_cookies(res)
        return res

    return make_response(redirect("/order_page"))


@app.route("/api/login", methods=["POST"])
def login():
    code = request.form.get("code")

    if code is None or not code.isnumeric():
        return jsonify({"success": False, "message": "Invalid code."})

    code = int(code)

    user = auth.get_user_by_code(db_session, code)

    if user is None:
        return jsonify(
            {"success": False, "message": "User does not exist or code is invalid."}
        )

    session = auth.create_session(db_session, user.id)

    return jsonify(
        {
            "success": True,
            "message": "Login successful.",
            "session_token": session.hashed_token,
            "user_id": user.id,
            "username": user.username,
        }
    )


# TODO add logout route.


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

        if session_token is None or not auth.session_valid(
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
    user_id = request.cookies.get("user")  # TODO get from globals

    if user_id is None or not user_id.isnumeric():  # TODO User ID is already checked.
        return jsonify(
            {
                "success": False,
                "message": "Invalid user ID.",
            }
        )

    user_id = int(user_id)

    product_id = request.form.get("product_id")

    if product_id is None or not product_id.isnumeric():
        return jsonify({"success": False, "message": "Invalid product ID."})

    product_id = int(product_id)

    if not ordering.user_has_cart(db_session, user_id):
        ordering.create_cart(db_session, user_id)

    user_cart = ordering.get_cart_by_user(db_session, user_id)

    if not ordering.product_exists(db_session, product_id):
        return jsonify({"success": False, "message": "Product does not exist."})

    ordering.add_to_cart(db_session, user_cart.id, product_id)

    return jsonify({"success": True, "message": "Product added."})


@app.route("/api/remove_from_cart", methods=["POST"])
def remove_from_cart():
    user_id = request.cookies.get("user")  # TODO get from globals

    if user_id is None or not user_id.isnumeric():  # TODO User ID is already checked.
        return jsonify(
            {
                "success": False,
                "message": "Invalid user ID.",
            }
        )

    user_id = int(user_id)

    product_id = request.form.get("product_id")

    if product_id is None or not product_id.isnumeric():
        return jsonify({"success": False, "message": "Invalid product ID."})

    product_id = int(product_id)

    if not ordering.user_has_cart(db_session, user_id):
        return jsonify({"success": False, "message": "User has no cart."})

    user_cart = ordering.get_cart_by_user(db_session, user_id)

    item = ordering.get_cart_item_from_product(db_session, user_cart.id, product_id)

    if item is None:
        return jsonify({"success": False, "message": "Product is not in cart."})

    ordering.remove_cart_item(db_session, item.id)

    return jsonify(
        {"success": True, "message": f"Product {product_id} removed from cart."}
    )


@app.route("/api/get_cart", methods=["GET"])
def get_cart():
    user_id = request.cookies.get("user")  # TODO get from globals

    if user_id is None or not user_id.isnumeric():  # TODO User ID is already checked.
        return jsonify(
            {
                "success": False,
                "message": "Invalid user ID.",
            }
        )

    user_id = int(user_id)

    if not ordering.user_has_cart(db_session, user_id):
        ordering.create_cart(db_session, user_id)

    user_cart = ordering.get_cart_by_user(db_session, user_id)

    cart_items = ordering.get_cart_items(db_session, user_cart.id)

    output: list[dict[str, int | str]] = []
    price_total = 0
    for citem in cart_items:
        product = get_product_by_id(db_session, citem.product)

        price_total += product.price

        output.append(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
            }
        )

    return jsonify(
        {
            "success": True,
            "cart": output,
            "total": price_total,
        }
    )


@app.route("/api/complete_task", methods=["POST"])
def complete_task():
    """Given a task ID and user ID, mark the task as completed."""
    user_id = request.cookies.get("user")

    if user_id is None or not user_id.isnumeric():
        return jsonify({"success": False, "message": "Invalid user ID."})

    user_id = int(user_id)

    task_id = request.form.get("task_id")

    if task_id is None or not task_id.isnumeric():
        return jsonify({"success": False, "message": "Invalid task ID."})

    task_id = int(task_id)

    if not ordering.user_has_cart(db_session, user_id):
        ordering.create_cart(db_session, user_id)

    user_cart = ordering.get_cart_by_user(db_session, user_id)

    task = TasksDB.get_task_by_id(db_session, task_id)

    if task is None:
        return jsonify({"success": False, "message": "Task does not exist."})

    # Add the task to the user tasks
    user_task = TasksDB.add_user_task(db_session, user_id, task_id)
    TasksDB.set_user_task_completed(db_session, user_task.id)

    EconDB.add_balance(db_session, user_id, task.reward)

    return jsonify({"success": True, "message": "Task completed."})


@app.route("/api/checkout", methods=["POST"])
def checkout():
    user_id = request.cookies.get("user")

    if user_id is None or not user_id.isnumeric():
        return jsonify({"success": False, "message": "Invalid user ID."})

    user_id = int(user_id)

    if not ordering.user_has_cart(db_session, user_id):
        ordering.create_cart(db_session, user_id)
        return jsonify({"success": False, "message": "User had no cart."})

    user_cart = ordering.get_cart_by_user(db_session, user_id)

    cart_total = ordering.get_cart_total(db_session, user_cart.id)

    if cart_total == 0:
        return jsonify({"success": False, "message": "Cart is empty."})

    if cart_total > EconDB.get_user_balance(db_session, user_id):
        return jsonify({"success": False, "message": "Insufficient funds."})

    # Get all the items in the cart.
    cart_items = ordering.get_cart_items(db_session, user_cart.id)

    # Pay for the cart.
    EconDB.remove_balance(db_session, user_id, cart_total)
    ordering.set_cart_is_payed(db_session, user_cart.id)

    # Add the items to the order queue.
    for item in cart_items:
        ORDER_QUEUE.add(user_cart.id)

    return jsonify({"success": True, "message": "Cart payed."})


def init_dev_server() -> None:
    # Load all products from the 'products.yml' file.
    load_products_from_yaml(db_session)

    # Set up the root admin user.
    auth.setup_root_admin(
        db_session,
        src.utils.config.Config.root_admin_username,
        src.utils.config.Config.root_admin_password,
    )

    app.run(debug=True, port=5000)

    print("Stopping the server...")
    db_conn.close()  # CLose the database connection.
    db_engine.dispose()  # Dispose of the database engine.
    print("Server stopped.")

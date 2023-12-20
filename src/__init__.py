import flask
from flask import render_template, request, redirect, make_response
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# Local imports.
from src.db.schemas import Base
from src.db.products import load_products_from_yaml
from src.db.auth import session_valid
from src import easy
import src.utils.config

db_engine = sqlalchemy.create_engine(
    src.utils.config.Config.get_database_connection_string(),
    echo=True,  # Set to True to see SQL queries in the console.
)

# Globals
# --------------------------------------------------------------------------------------
# Start a flask app in development mode where the templates are reloaded upon change.
app = flask.Flask(
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
)

# Initialize connection to database.
db_conn = db_engine.connect()

# Create all tables using the metadata.
Base.metadata.create_all(db_engine)

# Create a session.
SessionMaker = sessionmaker(bind=db_engine)
db_session = SessionMaker()
# --------------------------------------------------------------------------------------

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
    
    


def init_dev_server() -> None:
    
    
    load_products_from_yaml(db_session)

    app.run(debug=True, port=5000)

    print("Stopping the server...")
    db_conn.close()  # CLose the database connection.
    db_engine.dispose()  # Dispose of the database engine.
    print("Server stopped.")

""" This module contains all routes for the announcement page.
"""

from flask import Blueprint, render_template
import src.utils.config
import sqlalchemy
from sqlalchemy.orm import sessionmaker

announcement_blueprint = Blueprint("announcement", __name__, url_prefix="/announcement")

db_engine = sqlalchemy.create_engine(
    src.utils.config.Config.get_database_connection_string(),
    echo=True,  # Set to True to see SQL queries in the console.
    # TODO Add config for echo.
)

# Initialize connection to database.
db_conn = db_engine.connect()

# Create a session.
SessionMaker = sessionmaker(bind=db_engine)
db_session = SessionMaker()

@announcement_blueprint.route("/", methods=["GET"])
def index():
    print("Hello, World!")
    return render_template("/announcement/ns.html")
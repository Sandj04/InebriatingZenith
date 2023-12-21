""" Flask routing for admin utilities."""

from flask import Blueprint, render_template, request, make_response
from flask import g as FlaskGlobals

from src.db import auth

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

@admin_blueprint.route("/", methods=["GET"])
def admin_index() -> str:
    return render_template("/admin/index.html")

@admin_blueprint.route("/api/login", methods=["GET"])
def login() -> str:
    username = request.args.get("username")
    password = request.args.get("password")
    
    if username is None or password is None:
        return "Invalid username or password."
    
    # TODO Add globals
    # if auth.admin_password_valid(db_session, username, password):
    #     return "Invalid username or password."
    
    return "Something went wrong!"
from flask import Blueprint, redirect, url_for

calc_bp = Blueprint("calc_bp", __name__)

@calc_bp.route("/", methods=["GET"])
def index():
    return "Index of Calculator."

@calc_bp.route("/add/<int:x>/<int:y>", methods=["GET"])
def add(x, y):
    return str(x + y)

@calc_bp.route("/subtract/<int:x>/<int:y>", methods=["GET"])
def subtract(x, y):
    return str(x - y)

@calc_bp.route("/go_to_hello", methods=["GET"])
def go_to_hello():
    return redirect( url_for("helloworld_bp.hello") )
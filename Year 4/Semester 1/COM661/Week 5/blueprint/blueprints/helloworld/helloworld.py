from flask import Blueprint

helloworld_bp = Blueprint("helloworld_bp", __name__)

@helloworld_bp.route("/", methods=["GET"])
def index():
    return "Index of Hello World."

@helloworld_bp.route("/hello", methods=["GET"])
def hello():
    return "Hello World!"

@helloworld_bp.route("/hello/<string:name>", methods=["GET"])
def hello_name(name):
    return "Hello " + name
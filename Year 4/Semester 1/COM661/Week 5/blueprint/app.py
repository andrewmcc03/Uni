from flask import Flask
from blueprints.helloworld.helloworld import helloworld_bp
from blueprints.calculator.calculator import calc_bp

app = Flask(__name__)

app.register_blueprint(helloworld_bp)
app.register_blueprint(calc_bp, url_prefix="/calculator")

if __name__ == "__main__":
    app.run(debug=True, port=4999)
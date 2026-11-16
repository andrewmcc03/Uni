from flask import Flask
from globals import secret_key

from blueprints.movies.movies import movies_bp
from blueprints.reviews.reviews import reviews_bp
from blueprints.tags.tags import tags_bp
from blueprints.queries.queries import queries_bp
from blueprints.auth.auth import auth_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key

app.register_blueprint(movies_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(tags_bp)
app.register_blueprint(queries_bp)
app.register_blueprint(auth_bp)

"""

movies_app/
│
├── movies_app.py       - main application
│
├── blueprints/
├────── movies.py       - movie CRUD endpoints
├────── reviews.py      - review CRUD endpoints
├────── tags.py         - tag CRUD endpoints
├────── queries.py      - statistics and aggregation endpoints
├────── auth.py         - registration, login and logout
│
├── globals.py          - global database connections and settings
└── decorators.py       - jwt_required and admin_required (token and admin auth)

"""

#########################################################################################################
# API documentation:    https://documenter.getpostman.com/view/58637944/2sBYHYscHk
#########################################################################################################

if __name__ == "__main__":
    app.run(debug = True, port=4999)
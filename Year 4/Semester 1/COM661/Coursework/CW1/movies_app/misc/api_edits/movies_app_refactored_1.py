"""
Movie API for COM661 Coursework 1
---------------------------------
Single-file version. The routes can later be moved into Flask Blueprints.

Expected MongoDB database:
    moviesDB
        movies
        users
        blacklist

Expected movie fields follow the prepared MovieLens dataset:
    title, releaseYear, genres, grossProfits, averageRating,
    ratingCount, weightedRating, reviewCount, tagCount,
    reviews[], tags[], externalIds{}

Application-created reviews use:
    _id, userId, name, comment, rating, date

Imported MovieLens reviews retain sourceUserId and are not editable by
application users because they are not linked to registered accounts.

Set MOVIES_SECRET_KEY in your environment before running this app.
"""

import os
import re
import math
import datetime as dt
from functools import wraps

import bcrypt
import jwt
from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask, jsonify, make_response, request
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import DuplicateKeyError


# ---------------------------------------------------------------------------
# App and database configuration
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("MOVIES_SECRET_KEY", "change-this-development-secret")

client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017"))
db = client["moviesDB"]
movies = db["movies"]
users = db["users"]
blacklist = db["blacklist"]

# Enforce unique account names (also required for reliable duplicate checks).
users.create_index("username", unique=True)

TOKEN_LIFETIME_MINUTES = 30
PAGE_SIZE_DEFAULT = 10
PAGE_SIZE_MAX = 100
ALLOWED_MOVIE_FIELDS = {"title", "releaseYear", "genres", "grossProfits", "externalIds"}
PRIOR_RATING = 3.5
PRIOR_COUNT = 20


# ---------------------------------------------------------------------------
# Common response, validation and serialisation helpers
# ---------------------------------------------------------------------------

def error(message, status):
    return make_response(jsonify({"error": message}), status)


def json_body():
    """Return a JSON object, or None when the request body is not an object."""
    body = request.get_json(silent=True)
    return body if isinstance(body, dict) else None


def serialise(value):
    """Convert MongoDB values into values Flask's JSON provider can serialise."""
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (dt.datetime, dt.date)):
        if isinstance(value, dt.datetime) and value.tzinfo is None:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, list):
        return [serialise(item) for item in value]
    if isinstance(value, dict):
        return {key: serialise(item) for key, item in value.items()}
    return value


def movie_response(movie):
    return jsonify(serialise(movie))


def parse_object_id(value, label="ID"):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise ValueError(f"Invalid {label}.")


def parse_genres(value):
    if isinstance(value, str):
        genres = [item.strip() for item in value.split(",")]
    elif isinstance(value, list):
        genres = [str(item).strip() for item in value]
    else:
        raise ValueError("Genres must be a list or comma-separated string.")
    genres = [genre for genre in genres if genre]
    if not genres:
        raise ValueError("At least one genre is required.")
    return genres


def parse_iso_date(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("A valid date is required.")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Date must be an ISO 8601 date/time.")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def get_movie_or_404(movie_id):
    try:
        oid = parse_object_id(movie_id, "movie ID")
    except ValueError as exc:
        return None, error(str(exc), 400)
    movie = movies.find_one({"_id": oid})
    if movie is None:
        return None, error("Movie not found.", 404)
    return movie, None


def update_rating_statistics(movie_id):
    """Recalculate the denormalised rating fields from the embedded reviews."""
    movie = movies.find_one({"_id": movie_id}, {"reviews.rating": 1})
    if movie is None:
        return

    ratings = [
        float(review["rating"])
        for review in movie.get("reviews", [])
        if isinstance(review.get("rating"), (int, float))
    ]
    count = len(ratings)
    average = sum(ratings) / count if count else 0.0
    weighted = (
        (count / (count + PRIOR_COUNT)) * average
        + (PRIOR_COUNT / (count + PRIOR_COUNT)) * PRIOR_RATING
        if count + PRIOR_COUNT else 0.0
    )

    movies.update_one(
        {"_id": movie_id},
        {"$set": {
            "averageRating": round(average, 2),
            "weightedRating": round(weighted, 2),
            "reviewCount": count,
            "ratingCount": count
        }}
    )


# ---------------------------------------------------------------------------
# JWT authentication and authorisation
# ---------------------------------------------------------------------------

def current_token():
    token = request.headers.get("x-access-token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
    return token


def jwt_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = current_token()
        if not token:
            return error("Authentication token is required.", 401)
        if blacklist.find_one({"token": token}):
            return error("This token has been logged out.", 401)
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return error("Authentication token has expired.", 401)
        except jwt.InvalidTokenError:
            return error("Invalid authentication token.", 401)

        user = users.find_one({"username": payload.get("user")})
        if user is None:
            return error("User account not found.", 401)

        request.current_user = user
        request.jwt_payload = payload
        return function(*args, **kwargs)
    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not getattr(request, "current_user", {}).get("admin", False):
            return error("Administrator access is required.", 403)
        return function(*args, **kwargs)
    return wrapper


def review_owner_or_admin(movie_id, review_id):
    """Check ownership of an application-created review."""
    movie, response = get_movie_or_404(movie_id)
    if response:
        return None, response

    try:
        review_oid = parse_object_id(review_id, "review ID")
    except ValueError as exc:
        return None, error(str(exc), 400)

    review = next(
        (item for item in movie.get("reviews", []) if item.get("_id") == review_oid),
        None
    )
    if review is None:
        return None, error("Review not found.", 404)

    user = request.current_user
    if not user.get("admin") and review.get("userId") != user.get("username"):
        return None, error("You can only modify your own reviews.", 403)

    # Imported records have sourceUserId but no application userId.
    if not review.get("userId") and not user.get("admin"):
        return None, error("Imported reviews cannot be modified by application users.", 403)

    return (movie, review, review_oid), None


# ---------------------------------------------------------------------------
# Movie endpoints
# ---------------------------------------------------------------------------

@app.route("/api/v1.0/movies", methods=["GET"])
def list_movies():
    """List movies with filters, sorting and page metadata.

    Query parameters: pn, ps, q, genre, year, minRating, maxRating, sort.
    """
    try:
        page = int(request.args.get("pn", 1))
        page_size = int(request.args.get("ps", PAGE_SIZE_DEFAULT))
        if page < 1 or page_size < 1 or page_size > PAGE_SIZE_MAX:
            raise ValueError
    except ValueError:
        return error(f"pn must be >= 1 and ps must be between 1 and {PAGE_SIZE_MAX}.", 400)

    query = {}
    search_text = request.args.get("q", "").strip()
    if search_text:
        query["title"] = {"$regex": re.escape(search_text), "$options": "i"}

    genre = request.args.get("genre", "").strip()
    if genre:
        query["genres"] = {"$regex": f"^{re.escape(genre)}$", "$options": "i"}

    try:
        if request.args.get("year"):
            query["releaseYear"] = int(request.args["year"])
        rating_conditions = {}
        if request.args.get("minRating") is not None:
            rating_conditions["$gte"] = float(request.args["minRating"])
        if request.args.get("maxRating") is not None:
            rating_conditions["$lte"] = float(request.args["maxRating"])
        if rating_conditions:
            query["averageRating"] = rating_conditions
    except ValueError:
        return error("Year and rating filters must be numeric.", 400)

    sort_options = {
        "title": ("title", ASCENDING),
        "year": ("releaseYear", DESCENDING),
        "rating": ("averageRating", DESCENDING),
        "weightedRating": ("weightedRating", DESCENDING),
        "grossProfits": ("grossProfits", DESCENDING),
        "reviews": ("reviewCount", DESCENDING)
    }
    sort_name = request.args.get("sort", "title")
    if sort_name not in sort_options:
        return error("Unsupported sort value.", 400)

    sort_field, sort_direction = sort_options[sort_name]
    total = movies.count_documents(query)
    results = list(
        movies.find(query)
        .sort(sort_field, sort_direction)
        .skip((page - 1) * page_size)
        .limit(page_size)
    )

    return jsonify({
        "data": serialise(results),
        "pagination": {
            "page": page,
            "pageSize": page_size,
            "totalResults": total,
            "totalPages": math.ceil(total / page_size) if total else 0
        }
    }), 200


@app.route("/api/v1.0/movies/<string:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie, response = get_movie_or_404(movie_id)
    if response:
        return response
    return movie_response(movie), 200


@app.route("/api/v1.0/movies", methods=["POST"])
@jwt_required
@admin_required
def create_movie():
    body = json_body()
    if body is None:
        return error("Request body must be a JSON object.", 400)

    try:
        title = body.get("title")
        year = int(body.get("releaseYear"))
        genres = parse_genres(body.get("genres"))
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required.")
        if year < 1888 or year > dt.datetime.now().year + 5:
            raise ValueError("Release year is outside the accepted range.")

        movie = {
            "title": title.strip(),
            "releaseYear": year,
            "genres": genres,
            "grossProfits": float(body.get("grossProfits", 0)),
            "averageRating": 0.0,
            "weightedRating": round(PRIOR_RATING, 2),
            "ratingCount": 0,
            "reviewCount": 0,
            "tagCount": 0,
            "reviews": [],
            "tags": [],
            "externalIds": body.get("externalIds", {})
        }
        if movie["grossProfits"] < 0:
            raise ValueError("grossProfits cannot be negative.")
        if not isinstance(movie["externalIds"], dict):
            raise ValueError("externalIds must be an object.")
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)

    result = movies.insert_one(movie)
    return jsonify({
        "message": "Movie created.",
        "id": str(result.inserted_id),
        "url": request.host_url.rstrip("/") + f"/api/v1.0/movies/{result.inserted_id}"
    }), 201


@app.route("/api/v1.0/movies/<string:movie_id>", methods=["PATCH"])
@jwt_required
@admin_required
def update_movie(movie_id):
    try:
        oid = parse_object_id(movie_id, "movie ID")
    except ValueError as exc:
        return error(str(exc), 400)

    body = json_body()
    if body is None:
        return error("Request body must be a JSON object.", 400)

    updates = {}
    for field in ALLOWED_MOVIE_FIELDS:
        if field not in body:
            continue
        value = body[field]
        try:
            if field == "title":
                if not isinstance(value, str) or not value.strip():
                    raise ValueError("Title cannot be empty.")
                value = value.strip()
            elif field == "releaseYear":
                value = int(value)
                if value < 1888 or value > dt.datetime.now().year + 5:
                    raise ValueError("Release year is outside the accepted range.")
            elif field == "genres":
                value = parse_genres(value)
            elif field == "grossProfits":
                value = float(value)
                if value < 0:
                    raise ValueError("grossProfits cannot be negative.")
            elif field == "externalIds" and not isinstance(value, dict):
                raise ValueError("externalIds must be an object.")
        except (TypeError, ValueError) as exc:
            return error(str(exc), 400)
        updates[field] = value

    if not updates:
        return error("No supported movie fields were supplied.", 400)

    result = movies.update_one({"_id": oid}, {"$set": updates})
    if result.matched_count == 0:
        return error("Movie not found.", 404)
    return jsonify({"message": "Movie updated.", "id": movie_id}), 200


@app.route("/api/v1.0/movies/<string:movie_id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_movie(movie_id):
    try:
        oid = parse_object_id(movie_id, "movie ID")
    except ValueError as exc:
        return error(str(exc), 400)
    result = movies.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return error("Movie not found.", 404)
    return "", 204


# ---------------------------------------------------------------------------
# Review endpoints (embedded in each movie document)
# ---------------------------------------------------------------------------

@app.route("/api/v1.0/movies/<string:movie_id>/reviews", methods=["GET"])
def list_reviews(movie_id):
    movie, response = get_movie_or_404(movie_id)
    if response:
        return response
    reviews = serialise(movie.get("reviews", []))
    return jsonify({"data": reviews, "totalResults": len(reviews)}), 200


@app.route("/api/v1.0/movies/<string:movie_id>/reviews", methods=["POST"])
@jwt_required
def create_review(movie_id):
    movie, response = get_movie_or_404(movie_id)
    if response:
        return response

    body = json_body()
    if body is None:
        return error("Request body must be a JSON object.", 400)

    comment = body.get("comment")
    try:
        rating = float(body.get("rating"))
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment is required.")
        if len(comment.strip()) > 2000:
            raise ValueError("Comment must be 2,000 characters or fewer.")
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)

    user = request.current_user
    review = {
        "_id": ObjectId(),
        "userId": user["username"],
        "name": user.get("displayName") or user["username"],
        "comment": comment.strip(),
        "rating": rating,
        "date": dt.datetime.now(dt.timezone.utc)
    }

    movies.update_one({"_id": movie["_id"]}, {"$push": {"reviews": review}})
    update_rating_statistics(movie["_id"])

    return jsonify({
        "message": "Review created.",
        "review": serialise(review),
        "url": request.host_url.rstrip("/") +
               f"/api/v1.0/movies/{movie_id}/reviews/{review['_id']}"
    }), 201


@app.route("/api/v1.0/movies/<string:movie_id>/reviews/<string:review_id>", methods=["GET"])
def get_review(movie_id, review_id):
    movie, response = get_movie_or_404(movie_id)
    if response:
        return response
    try:
        review_oid = parse_object_id(review_id, "review ID")
    except ValueError as exc:
        return error(str(exc), 400)

    review = next(
        (item for item in movie.get("reviews", []) if item.get("_id") == review_oid),
        None
    )
    if review is None:
        return error("Review not found for this movie.", 404)
    return jsonify(serialise(review)), 200


@app.route("/api/v1.0/movies/<string:movie_id>/reviews/<string:review_id>", methods=["PATCH"])
@jwt_required
def update_review(movie_id, review_id):
    owned, response = review_owner_or_admin(movie_id, review_id)
    if response:
        return response
    movie, review, review_oid = owned

    body = json_body()
    if body is None:
        return error("Request body must be a JSON object.", 400)
    updates = {}

    if "comment" in body:
        comment = body["comment"]
        if not isinstance(comment, str) or not comment.strip() or len(comment.strip()) > 2000:
            return error("Comment must contain 1–2,000 characters.", 400)
        updates["reviews.$.comment"] = comment.strip()

    if "rating" in body:
        try:
            rating = float(body["rating"])
            if not 1 <= rating <= 5:
                raise ValueError
        except (TypeError, ValueError):
            return error("Rating must be a number between 1 and 5.", 400)
        updates["reviews.$.rating"] = rating

    if not updates:
        return error("Supply a comment and/or rating to update.", 400)

    result = movies.update_one(
        {"_id": movie["_id"], "reviews._id": review_oid},
        {"$set": updates}
    )
    if result.matched_count == 0:
        return error("Review not found.", 404)
    update_rating_statistics(movie["_id"])
    return jsonify({"message": "Review updated.", "reviewId": review_id}), 200


@app.route("/api/v1.0/movies/<string:movie_id>/reviews/<string:review_id>", methods=["DELETE"])
@jwt_required
def delete_review(movie_id, review_id):
    owned, response = review_owner_or_admin(movie_id, review_id)
    if response:
        return response
    movie, review, review_oid = owned

    movies.update_one(
        {"_id": movie["_id"]},
        {"$pull": {"reviews": {"_id": review_oid}}}
    )
    update_rating_statistics(movie["_id"])
    return "", 204


# ---------------------------------------------------------------------------
# Dataset-specific discovery and aggregation endpoints
# ---------------------------------------------------------------------------

@app.route("/api/v1.0/genres", methods=["GET"])
def list_genres():
    pipeline = [
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "movieCount": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    genres = [{"genre": row["_id"], "movieCount": row["movieCount"]}
              for row in movies.aggregate(pipeline)]
    return jsonify({"data": genres}), 200


@app.route("/api/v1.0/movies/top-rated", methods=["GET"])
def top_rated_movies():
    try:
        limit = int(request.args.get("limit", 10))
        minimum_reviews = int(request.args.get("minReviews", 10))
        if not 1 <= limit <= 100 or minimum_reviews < 0:
            raise ValueError
    except ValueError:
        return error("limit must be 1–100 and minReviews must be 0 or greater.", 400)

    results = list(
        movies.find({"reviewCount": {"$gte": minimum_reviews}})
        .sort([("weightedRating", DESCENDING), ("reviewCount", DESCENDING)])
        .limit(limit)
    )
    return jsonify({"data": serialise(results), "totalResults": len(results)}), 200


@app.route("/api/v1.0/movies/statistics", methods=["GET"])
def movie_statistics():
    pipeline = [
        {"$group": {
            "_id": None,
            "movieCount": {"$sum": 1},
            "averageMovieRating": {"$avg": "$averageRating"},
            "averageGrossProfits": {"$avg": "$grossProfits"},
            "totalReviews": {"$sum": "$reviewCount"},
            "averageReleaseYear": {"$avg": "$releaseYear"}
        }},
        {"$project": {"_id": 0}}
    ]
    result = list(movies.aggregate(pipeline))
    if not result:
        return jsonify({
            "movieCount": 0,
            "averageMovieRating": 0,
            "averageGrossProfits": 0,
            "totalReviews": 0,
            "averageReleaseYear": None
        }), 200
    return jsonify(serialise(result[0])), 200


# ---------------------------------------------------------------------------
# Account endpoints
# ---------------------------------------------------------------------------

@app.route("/api/v1.0/register", methods=["POST"])
def register():
    body = json_body()
    if body is None:
        return error("Request body must be a JSON object.", 400)

    username = body.get("username")
    password = body.get("password")
    display_name = body.get("displayName") or username

    if not isinstance(username, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{3,30}", username):
        return error("Username must be 3–30 characters (letters, numbers, _, . or -).", 400)
    if not isinstance(password, str) or len(password) < 8:
        return error("Password must be at least 8 characters.", 400)
    if not isinstance(display_name, str) or not display_name.strip():
        return error("displayName must be a non-empty string.", 400)

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        result = users.insert_one({
            "username": username,
            "displayName": display_name.strip(),
            "password": hashed,
            "admin": False,
            "createdAt": dt.datetime.now(dt.timezone.utc)
        })
    except DuplicateKeyError:
        return error("That username is already registered.", 409)

    return jsonify({"message": "Account created.", "userId": str(result.inserted_id)}), 201


@app.route("/api/v1.0/login", methods=["POST"])
def login():
    body = json_body()
    if body is None:
        return error("Request body must be a JSON object.", 400)

    username = body.get("username")
    password = body.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return error("Username and password are required.", 400)

    user = users.find_one({"username": username})
    if user is None or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return error("Invalid username or password.", 401)

    token = jwt.encode({
        "user": user["username"],
        "admin": bool(user.get("admin", False)),
        "exp": dt.datetime.now(dt.timezone.utc) +
               dt.timedelta(minutes=TOKEN_LIFETIME_MINUTES)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({
        "token": token,
        "tokenType": "Bearer",
        "expiresIn": TOKEN_LIFETIME_MINUTES * 60
    }), 200


@app.route("/api/v1.0/logout", methods=["POST"])
@jwt_required
def logout():
    token = current_token()
    blacklist.insert_one({
        "token": token,
        "createdAt": dt.datetime.now(dt.timezone.utc)
    })
    return jsonify({"message": "Logout successful."}), 200


# ---------------------------------------------------------------------------
# Run locally
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=4999)

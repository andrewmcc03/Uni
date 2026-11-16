from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from bson.errors import InvalidId # for validation
import re # more input format validation
from pymongo import ASCENDING, DESCENDING

from decorators import jwt_required, admin_required # decorator(s)
from globals import movies, serialise_document, BASE_URL
# tokens taken from Postman in x-access-token header

movies_bp = Blueprint("movies_bp", __name__)

#########################################################################################################
#### MAIN MOVIES API ENDPOINTS ##########################################################################
#########################################################################################################

#MOVIES
# GET all movies (ordered)
@movies_bp.route("/api/v1.0/movies", methods=["GET"])
# No auth required
def get_all_movies():
    # pagination: /movies?pn=1&ps=10
    try:
        page_num = max(1, int(request.args.get("pn", 1)))
        page_size = min(100, max(1, int(request.args.get("ps", 10))))
    except ValueError:
        return make_response( jsonify( { "error" : "Page number and page size must be whole numbers." } ), 400 )

    # optional query filters: q, genre, year, minYear, maxYear, minRating, maxRating
    query = {}
    if request.args.get("q"):
        query["title"] = {"$regex": request.args["q"], "$options": "i"}
    # MULTI-GENRE filtering
    genres_param = request.args.get("genres")
    # retain backwards compatibility with existing single genre searches
    if not genres_param:
        genres_param = request.args.get("genre")
    if genres_param:
        selected_genres = [genre.strip() for genre in genres_param.split(",") if genre.strip()]
        if not selected_genres:
            return make_response( jsonify( { "error" : "At least one valid genre must be provided." } ), 400 )
        # default genre mode set to any if not provided in URL
        genre_mode = request.args.get("genreMode", "any").strip().lower()
        if genre_mode not in ["any", "all"]:
            return make_response( jsonify( { "error" : "Genre must be either 'any' or 'all'." } ), 400 )
        # match regardless of case (upper / lower) - for each genre in given genres
        # re.escape(genre) prevents special regex chars in input from being interpreted as regex instructions
        genre_regex = [ {"$regex": "^" + re.escape(genre) + "$", "$options": "i"} for genre in selected_genres]
        # if any or all ($in = ANY)
        if genre_mode == "any":
            query["$or"] = [{"genres": regex} for regex in genre_regex] # uses $or as $in would cause an error as it doesn't support regular expression operator docs inside the array
        else:
            query["$and"] = [{"genres": regex} for regex in genre_regex] # uses $and as $all would cause an error as it doesn't support regular expression operator docs inside the array
    try:
        if request.args.get("year"):
            query["releaseYear"] = int(request.args["year"])
        elif request.args.get("minYear") or request.args.get("maxYear"):
            query["releaseYear"] = {}
            if request.args.get("minYear"):
                query["releaseYear"]["$gte"] = int(request.args["minYear"])
            if request.args.get("maxYear"):
                query["releaseYear"]["$lte"] = int(request.args["maxYear"])
        if request.args.get("minRating") or request.args.get("maxRating"):
            query["averageRating"] = {}
            if request.args.get("minRating"):
                query["averageRating"]["$gte"] = float(request.args["minRating"])
            if request.args.get("maxRating"):
                query["averageRating"]["$lte"] = float(request.args["maxRating"])
    except ValueError:
        return make_response( jsonify( { "error" : "Year and rating filters must be valid numbers." } ), 400 )
    # sort in better readable order
    sort_fields = {
        "title": "title",
        "year": "releaseYear",
        "rating": "averageRating",
        "grossProfits": "grossProfits",
        "reviewCount": "reviewCount"
    }
    sort_by = request.args.get("sortBy", "title")
    sort_order = DESCENDING if request.args.get("order", "asc").lower() == "desc" else ASCENDING
    if sort_by not in sort_fields:
        return make_response( jsonify( { "error" : "'Sort By' must be Title, Year, Rating, Gross Profits or Review Count." } ), 400 )

    total_movies = movies.count_documents(query)
    data_to_return = [serialise_document(movie) for movie in movies.find(query)
                      .sort(sort_fields[sort_by], sort_order)
                      .skip((page_num - 1) * page_size).limit(page_size)]
    # returns sum of stats for DB as below
    return make_response( jsonify( {
        "page": page_num,
        "pageSize": page_size,
        "totalMovies": total_movies,
        "totalPages": (total_movies + page_size - 1) // page_size,
        "movies": data_to_return
    } ), 200 )

# GET movie
@movies_bp.route("/api/v1.0/movies/<string:id>", methods=["GET"])
# No auth required
def get_one_movie(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 400 )
    # passed validation
    movie = movies.find_one( { "_id": movie_id } )
    if movie is not None:
        movie = serialise_document(movie)
        return make_response( jsonify(movie), 200)
    else:
        return make_response( jsonify( { "error" : "Movie not found." } ), 404 )

# ADD movie
@movies_bp.route("/api/v1.0/movies", methods=["POST"])
@jwt_required   # user authed
def add_movie():
    required_fields = ["title", "releaseYear", "genres"] # REQUIRED: Title, Release Year, Genres
    if not all(request.form.get(field, "").strip() for field in required_fields):
        return make_response( jsonify( { "error" : "Title, Release Year and at least one Genre are required." } ), 400 )
    try:
        release_year = int(request.form["releaseYear"])
        gross_profits = float(request.form.get("grossProfits", 0))
    except ValueError:
        return make_response( jsonify( { "error" : "Release Year must be a whole number and Gross Profits must be numeric." } ), 400 )
    if release_year < 1890 or gross_profits < 0:
        return make_response( jsonify( { "error" : "Enter a valid Release Year (after 1890) and positive Gross Profits value." } ), 400 )

    genres = [genre.strip() for genre in request.form["genres"].split(",") if genre.strip()]
    if not genres:
        return make_response( jsonify( { "error" : "At least one genre is required." } ), 400 )

    tmdb_id = request.form.get("tmdbId")
    if tmdb_id:
        try:
            tmdb_id = int(tmdb_id)
        except ValueError:
            return make_response( jsonify( { "error" : "TMDb ID must be a whole number." } ), 400 )

    new_movie = {
        "title": request.form["title"].strip(),
        "releaseYear": release_year,
        "genres": genres,
        "grossProfits": gross_profits,
        "averageRating": 0.0,
        "ratingCount": 0,
        "weightedRating": 0.0,
        "reviewCount": 0,
        "tagCount": 0,
        "reviews": [],
        "tags": [],
        "externalIds": {
            "imdbId": request.form.get("imdbId", "").strip() or None,
            "tmdbId": tmdb_id
        }
    }
    result = movies.insert_one(new_movie)
    return make_response( jsonify( { "url" : BASE_URL + "/movies/" + str(result.inserted_id) } ), 201 )

# EDIT (PATCH) movie
@movies_bp.route("/api/v1.0/movies/<string:id>", methods=["PATCH"])
@jwt_required   # user authed
def edit_movie(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID."}), 400)
    # passed validation

    # partial updates are accepted - submit only the fields to change
    allowed_fields = ["title", "releaseYear", "genres", "grossProfits", "imdbId", "tmdbId"]
    updates = {}
    for field in allowed_fields:
        if field not in request.form:
            continue
        value = request.form[field]
        if field == "title":
            value = value.strip()
            if not value:
                return make_response( jsonify( { "error" : "Title cannot be empty." } ), 400 )
        elif field == "releaseYear":
            try:
                value = int(value)
            except ValueError:
                return make_response( jsonify( { "error" : "Release Year must be a whole number." } ), 400 )
            if value < 1890:
                return make_response( jsonify( { "error" : "Enter a valid Release Year (after 1890)." } ), 400 )
        elif field == "grossProfits":
            try:
                value = float(value)
            except ValueError:
                return make_response( jsonify ( {"error" : "Gross Profits must be a valid decimal number." } ), 400 )
            if value < 0:
                return make_response( jsonify( { "error" : "Gross Profits cannot be negative." } ), 400 )
        elif field == "genres":
            value = [genre.strip() for genre in value.split(",") if genre.strip()]
            if not value:
                return make_response( jsonify( { "error" : "At least one genre is required." } ), 400 )
        elif field == "tmdbId":
            try:
                value = int(value) if value.strip() else None
            except ValueError:
                return make_response( jsonify( { "error" : "TMDb ID must be a whole number." } ), 400 )
        elif field == "imdbId":
            value = value.strip() or None

        if field in ["imdbId", "tmdbId"]:
            updates["externalIds." + field] = value
        else:
            updates[field] = value

    if not updates:
        return make_response( jsonify( { "error" : "No movie data given or fields invalid." } ), 400 )
    result = movies.update_one( {"_id": movie_id}, {"$set": updates} )
    if result.matched_count == 0:
        return make_response( jsonify( { "error" : "Movie not found." } ), 404 )
    return make_response( jsonify( { "url" : BASE_URL + "/movies/" + id } ), 200 )

# DELETE movie
@movies_bp.route("/api/v1.0/movies/<string:id>", methods=["DELETE"])
@jwt_required   # user authed
@admin_required # admin authed
def delete_movie(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 400 )
    result = movies.delete_one( {"_id": movie_id} )
    if result.deleted_count == 1:
        return make_response( {}, 204 )
    return make_response( jsonify( { "error" : "Movie not found." } ), 404 )
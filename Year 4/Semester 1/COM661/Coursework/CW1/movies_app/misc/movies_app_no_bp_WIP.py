from flask import Flask, request, jsonify, make_response, g
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
import jwt
import datetime
from functools import wraps
import bcrypt
from bson.errors import InvalidId # for validation
import re # more input format validation
from decorators import jwt_required, admin_required # decorators
import globals
# tokens taken from Postman in x-access-token header

"""
TODO
- DONE      | POTENTIAL: Add multi-genre searching to demonstrate more complex queries
- DONE      | POTENTIAL: Add review and tag filtering
- DONE      | POTENTIAL: Add pagination to reviews
- DONE      | Add more filters/stats/aggrs endpoints
- ONGOING   | Complete Postman documentation
- ONGOING   | Add more to testing in Postman
- DONE      | Check/test review stat calcs

- DONE      | **SPLIT ENDPOINTS INTO BLUEPRINTS**


**ENDPOINTS TO BE FULLY TESTED**:
Movies
get_all_movies()                    DONE
get_one_movie(id)                   DONE
add_movie()                         DONE
PATCH edit_movie(id)                DONE
delete_movie(id)                    DONE

Reviews
get_all_reviews(id)                 DONE
get_one_review(m_id, r_id)          DONE
add_new_review(id)                  DONE
PATCH edit_review(m_id, r_id)       DONE
delete_review(m_id, r_id)           DONE

Tags
get_all_movie_tags(id)              DONE
get_one_movie(id)                   DONE
add_new_tag(id)                     DONE
PATCH edit_movie_tag(m_id, t_id)    DONE
delete_movie_tag(m_id, t_id)        DONE

Additional/filters/aggrs
movie_overview()                    DONE
genre_statistics()                  DONE
top_rated_movies()                  DONE
highest_grossing_movies()           DONE
reviewer_statistics()               DONE
popular_tags()                      DONE

Auth/accounts
register()                          DONE
login()                             DONE
logout()                            DONE

"""

app = Flask(__name__)
app.config["SECRET_KEY"] = "andrewsk" #!!! will move this to globals.py later

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.moviesDB
movies = db.movies
users = db.users
blacklist = db.blacklist

BASE_URL = "http://localhost:4999/api/v1.0" # for shortening link refs

# format document - convert MongoDB ObjectIds and date/times into JSON values
def serialise_document(document):
    if isinstance(document, list):
        return [serialise_document(item) for item in document]
    if isinstance(document, dict):
        return {key: serialise_document(value) for key, value in document.items()}
    if isinstance(document, ObjectId):
        return str(document)
    if isinstance(document, datetime.datetime):
        return document.isoformat() + ("Z" if document.tzinfo is None else "")
    return document

# convert Unix timestamp into UTC datetime for records
# **method removed as no need atm**

#########################################################################################################
#### MAIN API ENDPOINTS #################################################################################
#########################################################################################################

#MOVIES
# GET all movies (ordered)
@app.route("/api/v1.0/movies", methods=["GET"])
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
@app.route("/api/v1.0/movies/<string:id>", methods=["GET"])
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
@app.route("/api/v1.0/movies", methods=["POST"])
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
@app.route("/api/v1.0/movies/<string:id>", methods=["PATCH"])
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
@app.route("/api/v1.0/movies/<string:id>", methods=["DELETE"])
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

#########################################################################################################
# REVIEWS (embedded in each movie doc) ##################################################################
#########################################################################################################

# GET all reviews
@app.route("/api/v1.0/movies/<string:id>/reviews", methods=["GET"])
def get_all_reviews(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 400 )

    movie = movies.find_one( {"_id": movie_id}, {"reviews": 1} )

    if movie is None:
        return make_response( jsonify( { "error" : "Movie not found." } ), 404 )

    reviews = movie.get("reviews", [])

    # optional minimum rating filter
    try:
        if request.args.get("minRating"):
            min_rating = float(request.args["minRating"])
            if min_rating < 1 or min_rating > 5:
                return make_response( jsonify( { "error" : "Minimum rating must be between 1-5." } ), 400 )
            reviews = [review for review in reviews if review.get("rating", 0) >= min_rating]
        if request.args.get("maxRating"):
            max_rating = float(request.args["maxRating"])
            if max_rating < 1 or max_rating > 5:
                return make_response( jsonify( { "error" : "Maximum rating must be between 1-5." } ), 400 )
            reviews = [review for review in reviews if review.get("rating", 0) <= max_rating]
    except ValueError:
        return make_response( jsonify( { "error" : "Rating filters must be numeric." } ), 400 )
    # sorting
    sort_by = request.args.get("sortBy", "createdAt")
    if sort_by not in ["rating", "createdAt"]:
        return make_response( jsonify( { "error" : "'Sort By' must be Rating or Created At date." } ), 400 )
    # passed validation
    
    # set order (desc/asc)
    sort_order = DESCENDING if request.args.get("order", "desc").lower() == "desc" else ASCENDING
    reviews.sort( key=lambda review: review.get(sort_by, 0), reverse=(sort_order == DESCENDING) )

    # pagination of reviews (similar to get all movies method)
    try:
        page_num = max(1, int(request.args.get("pn", 1)))
        page_size = min(100, max(1, int(request.args.get("ps", 10))))
    except ValueError:
        return make_response( jsonify( { "error" : "Page number and page size must be whole numbers." } ), 400 )

    total_reviews = len(reviews)

    reviews = reviews[(page_num - 1) * page_size:page_num * page_size]

    return make_response( jsonify( {
        "page": page_num,
        "pageSize": page_size,
        "totalReviews": total_reviews,
        "totalPages": (total_reviews + page_size - 1) // page_size,
        "reviews": serialise_document(reviews)
    }), 200)

# GET review
@app.route("/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>", methods=["GET"])
# No auth required
def get_one_review(m_id, r_id):
    try:
        movie_id = ObjectId(m_id)
        review_id = ObjectId(r_id)
    except InvalidId:
        return make_response(jsonify( { "error" : "Invalid movie or review ID." } ), 400 )
    movie = movies.find_one( {"_id": movie_id, "reviews._id": review_id}, {"reviews.$": 1} )
    if movie is None:
        return make_response( jsonify( { "error" : "Movie or review not found." } ), 404 )
    return make_response( jsonify(serialise_document(movie["reviews"][0])), 200 )

# ADD review
@app.route("/api/v1.0/movies/<string:id>/reviews", methods=["POST"])
@jwt_required   # user authed
def add_new_review(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 400 )
    comment = request.form.get("comment", "").strip()
    if not comment or not request.form.get("rating"):
        return make_response( jsonify( { "error" : "Comment and Rating are required." } ), 400 )
    try:
        rating = float(request.form["rating"])
    except ValueError:
        return make_response( jsonify( { "error" : "Rating must be numeric." } ), 400 )
    if rating < 1 or rating > 5:
        return make_response( jsonify( { "error" : "Rating must be between 1-5." } ), 400 )

    new_review = {
        "_id": ObjectId(),
        "name": g.current_user["name"], # gets display name and username from current user (see decorator)
        "username": g.current_user["username"],
        "comment": comment,
        "rating": rating,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    }
    result = movies.update_one( { "_id": movie_id }, { "$push": {"reviews" : new_review} } )
    if result.matched_count == 0:
        return make_response( jsonify( { "error" : "Movie not found." } ), 404 )

    # keep movie"s review stats in step with its embedded reviews
    movies.update_one({"_id": movie_id}, [{"$set": {
        "reviewCount": {"$size": "$reviews"},
        "ratingCount": {"$size": "$reviews"},
        "averageRating": {"$ifNull": [{"$round": [{"$avg": "$reviews.rating"}, 2]}, 0]},
        "weightedRating": {"$round": [{"$divide": [{"$add": [{"$multiply": [{"$avg": "$reviews.rating"}, {"$size": "$reviews"}]}, 70]}, {"$add": [{"$size": "$reviews"}, 20]}]}, 2]}
    }}])
    return make_response( jsonify( { "url" : BASE_URL + "/movies/" + id + "/reviews/" + str(new_review["_id"]) } ), 201 )

# EDIT (PATCH) review
@app.route("/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>", methods=["PATCH"])
@jwt_required   # user authed
def edit_review(m_id, r_id):
    try:
        movie_id = ObjectId(m_id)
        review_id = ObjectId(r_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie or review ID." } ), 400 )

    movie = movies.find_one( {"_id": movie_id, "reviews._id": review_id}, {"reviews.$": 1} )
    if movie is None:
        return make_response( jsonify( { "error" : "Movie or review not found." } ), 404 )
    
    review = movie["reviews"][0]
    # reviews only editable by sending user or admin user
    if review.get("username") != g.current_user["username"] and not g.current_user["admin"]:
        return make_response( jsonify( { "error" : "You can only edit your own reviews." } ), 403 )

    updates = {}
    if "comment" in request.form:
        comment = request.form["comment"].strip()
        if not comment:
            return make_response( jsonify( { "error" : "Comment cannot be empty." } ), 400 )
        updates["reviews.$.comment"] = comment
    if "rating" in request.form:
        try:
            rating = float(request.form["rating"])
        except ValueError:
            return make_response( jsonify( { "error" : "Rating must be numeric." } ), 400 )
        if rating < 1 or rating > 5:
            return make_response( jsonify( { "error" : "Rating must be between 1-5." } ), 400 )
        updates["reviews.$.rating"] = rating
    if not updates:
        return make_response( jsonify( { "error" : "You must enter a comment and/or rating to update." } ), 400 )
    
    # add 'editedAt' field when an edit is made
    updates["reviews.$.editedAt"] = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    # update with given fields
    movies.update_one({"_id": movie_id, "reviews._id": review_id}, {"$set": updates})

    # update dynamic fields for movie document record stats
    movies.update_one({"_id": movie_id}, [{"$set": {
        "reviewCount": {"$size": "$reviews"},
        "ratingCount": {"$size": "$reviews"},
        "averageRating": {"$ifNull": [{"$round": [{"$avg": "$reviews.rating"}, 2]}, 0]},
        "weightedRating": {"$round": [{"$divide": [{"$add": [{"$multiply": [{"$avg": "$reviews.rating"}, {"$size": "$reviews"}]}, 70]}, {"$add": [{"$size": "$reviews"}, 20]}]}, 2]}
    }}])
    return make_response( jsonify( { "url" : BASE_URL + "/movies/" + m_id + "/reviews/" + r_id } ), 200 )

# DELETE review
@app.route("/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>", methods=["DELETE"])
@jwt_required   # user authed
def delete_review(m_id, r_id):
    try:
        movie_id = ObjectId(m_id)
        review_id = ObjectId(r_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie or review ID." } ), 400)

    movie = movies.find_one( {"_id": movie_id, "reviews._id": review_id}, {"reviews.$": 1} )
    if movie is None:
        return make_response( jsonify( { "error" : "Movie or review not found." } ), 404 )
    
    review = movie["reviews"][0]
    # IF username not that of the current logged in user AND user is NOT an admin, return error
    if review.get("username") != g.current_user["username"] and not g.current_user["admin"]:
        return make_response( jsonify( { "error" : "You must be an admin to delete other user reviews.", } ), 403 )

    # update dynamic fields
    movies.update_one({"_id": movie_id}, {"$pull": {"reviews": {"_id": review_id}}})
    movies.update_one({"_id": movie_id}, [{"$set": {
        "reviewCount": {"$size": "$reviews"},
        "ratingCount": {"$size": "$reviews"},
        "averageRating": {"$ifNull": [{"$round": [{"$avg": "$reviews.rating"}, 2]}, 0]},
        "weightedRating": {"$round": [{"$divide": [{"$add": [{"$multiply": [{"$ifNull": [{"$avg": "$reviews.rating"}, 0]}, {"$size": "$reviews"}]}, 70]}, {"$add": [{"$size": "$reviews"}, 20]}]}, 2]}
    }}])
    return make_response( jsonify( {} ), 204 )

#########################################################################################################
# TAGS (also embedded in each movie) ####################################################################
#########################################################################################################

# GET all tags
@app.route("/api/v1.0/movies/<string:id>/tags", methods=["GET"])
# No auth required
def get_all_movie_tags(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID."}), 400)
    movie = movies.find_one({"_id": movie_id}, {"tags": 1})
    if movie is None:
        return make_response( jsonify( { "error" : "Movie not found."}), 404)
    return make_response(jsonify(serialise_document(movie.get("tags", []))), 200)

# GET tag
@app.route("/api/v1.0/movies/<string:m_id>/tags/<string:t_id>", methods=["GET"])
# No auth required
def get_one_tag(m_id, t_id):
    try:
        movie_id = ObjectId(m_id)
        tag_id = ObjectId(t_id)
    except InvalidId:
        return make_response(jsonify( { "error" : "Invalid movie or tag ID." } ), 400 )
    movie = movies.find_one( {"_id": movie_id, "tags._id": tag_id}, {"tags.$": 1} )
    if movie is None:
        return make_response( jsonify( { "error" : "Movie or tag not found." } ), 404 )
    return make_response( jsonify(serialise_document(movie["tags"][0])), 200 )

# ADD movie tag
@app.route("/api/v1.0/movies/<string:id>/tags", methods=["POST"])
@jwt_required   # user authed
def add_new_tag(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 400 )
    tag = request.form.get("tag", "").strip()
    if not tag:
        return make_response( jsonify( { "error" : "Tag field is required." } ), 400 )
    
    new_tag = {
        "_id": ObjectId(),
        "sourceUserId": "N/A", # field is marked 'not applicable' for new tags as only imported dataset data has relevant ID values
        "name": g.current_user["name"], # gets display name and username from current user (see decorator)
        "username": g.current_user["username"],
        "tag": tag,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    }
    result = movies.update_one({"_id": movie_id}, {"$push": {"tags": new_tag}})
    if result.matched_count == 0:
        return make_response( jsonify( { "error" : "Movie not found."}), 404)

    # update dynamic fields
    movies.update_one( {"_id": movie_id}, [ {"$set": { "tagCount": {"$size": "$tags"} }} ] )
    return make_response( jsonify( { "url" : BASE_URL + "/movies/" + id + "/tags/" + str(new_tag["_id"]) } ), 201 )

# EDIT (PATCH) movie tag
@app.route("/api/v1.0/movies/<string:m_id>/tags/<string:t_id>", methods=["PATCH"])
@jwt_required   # user authed
def edit_movie_tag(m_id, t_id):
    try:
        movie_id = ObjectId(m_id)
        tag_id = ObjectId(t_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID or tag ID." } ), 400 )

    movie = movies.find_one( {"_id": movie_id, "tags._id": tag_id}, {"tags.$": 1} )
    if movie is None:
        return make_response( jsonify( { "error" : "Movie or tag not found." } ), 404 )

    tag = movie["tags"][0]
    # only tag creator or admin can edit
    if (tag.get("username") and tag.get("username") != g.current_user["username"] and not g.current_user["admin"]):
        return make_response( jsonify( { "error" : "You can only edit your own tags." } ), 403 )

    updated_tag = request.form.get("tag", "").strip()
    if not updated_tag:
        return make_response( jsonify( { "error" : "Tag field is required." } ), 400 )
    
    # add 'editedAt' field when an edit is made (similar to edit_review method)
    edited_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    # update with fields
    result = movies.update_one( { "_id": movie_id, "tags._id": tag_id}, {"$set": {"tags.$.tag": updated_tag, "tags.$.editedAt": edited_at} } )
    if result.matched_count == 0:
        return make_response( jsonify( { "error" : "Movie or tag not found." } ), 404 )

    return make_response( jsonify( { "url" : BASE_URL + "/movies/" + m_id + "/tags/" + t_id } ), 200 )

# DELETE movie tag
@app.route("/api/v1.0/movies/<string:m_id>/tags/<string:t_id>", methods=["DELETE"])
@jwt_required   # user authed
def delete_movie_tag(m_id, t_id):
    try:
        movie_id = ObjectId(m_id)
        tag_id = ObjectId(t_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID or tag ID." } ), 400 )
    # passed validation
    movie = movies.find_one( {"_id": movie_id, "tags._id": tag_id}, {"tags.$": 1} )
    if movie is None:
        return make_response( jsonify( { "error" : "Movie or tag not found." } ), 404 )
    
    tag = movie["tags"][0]
    if tag.get("username") and tag.get("username") != g.current_user["username"] and not g.current_user["admin"]:
        return make_response( jsonify( { "error" : "You can only delete your own tags." } ), 403 )
    
    movies.update_one( {"_id": movie_id}, {"$pull": {"tags": {"_id": tag_id}}} )
    movies.update_one( {"_id": movie_id}, [{"$set": {"tagCount": {"$size": "$tags"}}}] )

    return make_response( jsonify( {} ), 204 )

#########################################################################################################
# DATASET-SPECIFIC QUERIES / AGGREGATIONS ###############################################################
#########################################################################################################

# stats overview filter page
@app.route("/api/v1.0/stats/overview", methods=["GET"])
def movie_overview():
    result = list(movies.aggregate([
        {"$group": {
            "_id": None,
            "movieCount": {"$sum": 1},
            "averageMovieRating": {"$avg": "$averageRating"},
            "averageGrossProfits": {"$avg": "$grossProfits"},
            "totalReviews": {"$sum": "$reviewCount"},
            "totalTags": {"$sum": "$tagCount"}
        }},
        {"$project": {"_id": 0, "movieCount": 1,
                      "averageMovieRating": {"$round": ["$averageMovieRating", 2]},
                      "averageGrossProfits": {"$round": ["$averageGrossProfits", 2]},
                      "totalReviews": 1, "totalTags": 1}}
    ]))
    if not result:
        return make_response( jsonify( { "message" : "No movies found." } ), 404 )
    return make_response( jsonify( serialise_document(result[0]) ), 200 )

# genre aggregation
@app.route("/api/v1.0/stats/genres", methods=["GET"])
def genre_statistics():
    result = list(movies.aggregate([
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "movieCount": {"$sum": 1},
                    "averageRating": {"$avg": "$averageRating"},
                    "totalReviews": {"$sum": "$reviewCount"}}},
        {"$sort": {"movieCount": -1, "_id": 1}},
        {"$project": {"_id": 0, "genre": "$_id", "movieCount": 1,
                      "averageRating": {"$round": ["$averageRating", 2]}, "totalReviews": 1}}
    ]))
    return make_response( jsonify( serialise_document(result) ), 200 )

# top rated movies filter
@app.route("/api/v1.0/movies/top-rated", methods=["GET"])
def top_rated_movies():
    try:
        limit = min(50, max(1, int(request.args.get("limit", 10))))
        minimum_reviews = max(0, int(request.args.get("minReviews", 5)))
    except ValueError:
        return make_response( jsonify( { "error" : "Limit and Minimum Reviews must be whole numbers." } ), 400 )
    
    result = movies.find( {"reviewCount": {"$gte": minimum_reviews}} ).sort(
        [("weightedRating", DESCENDING), ("reviewCount", DESCENDING)]).limit(limit)
    return make_response( jsonify( [serialise_document(movie) for movie in result] ), 200 )

# highest grossing/profiting movies
@app.route("/api/v1.0/movies/highest-grossing", methods=["GET"])
def highest_grossing_movies():
    try:
        limit = min(50, max(1, int(request.args.get("limit", 10))))
    except ValueError:
        return make_response( jsonify( { "error" : "Limit must be a whole number." } ), 400 )

    result = movies.find( {"grossProfits": {"$gt": 0}}).sort("grossProfits", DESCENDING).limit(limit)

    return make_response( jsonify( [serialise_document(movie) for movie in result] ), 200 )

# review statistics grouped by user
@app.route("/api/v1.0/stats/reviewers", methods=["GET"])
def reviewer_statistics():
    result = list(movies.aggregate([
        {"$unwind": "$reviews"},
        {"$group": {
            "_id": "$reviews.username",
            "reviewCount": {"$sum": 1},
            "averageRating": {"$avg": "$reviews.rating"}
        }},
        {"$sort": {"reviewCount": -1}},
        {"$project": {
            "_id": 0,
            "username": "$_id",
            "reviewCount": 1,
            "averageRating": {"$round": ["$averageRating", 2]}
        }}
    ]))
    return make_response( jsonify( serialise_document(result) ), 200 )

# most popular tags
@app.route("/api/v1.0/stats/tags", methods=["GET"])
def popular_tags():
    try:
        limit = min(50, max(1, int(request.args.get("limit", 10))))
    except ValueError:
        return make_response( jsonify( { "error" : "Limit must be a whole number." } ), 400 )
    
    result = list(movies.aggregate([
        {"$unwind": "$tags"},
        {"$group": {
            "_id": "$tags.tag",
            "tagCount": {"$sum": 1}
        }},
        {"$sort": {"tagCount": -1}},
        {"$limit": limit},
        {"$project": {
            "_id": 0,
            "tag": "$_id",
            "tagCount": 1
        }}
    ]))
    return make_response( jsonify( serialise_document(result) ), 200 )

#########################################################################################################
# AUTH ENDPOINTS ########################################################################################
#########################################################################################################

#REGISTER
@app.route("/api/v1.0/register", methods=["POST"])
def register():
    # reg new user
    if not request.form:
        return make_response( jsonify( { "error" : "You must enter a valid username and password to register." } ), 400)

    username = request.form.get("username", "").strip()             # REQUIRED
    password = request.form.get("password", "")                     # REQUIRED
    email = request.form.get("email", "").strip() or None           # optional
    name = request.form.get("name", "") or username  # defaults to username as display name if none provided

    if not username or not re.fullmatch(r"[A-Za-z0-9_.-]{3,20}", username): # uname should be between 3-20 and use valid chars only (i.e., letters, numbers, underscores/full stops, etc.)
        return make_response( jsonify( { "error" : "Username must be 3–20 characters (letters, numbers, _, . or -)." } ), 400 )
    if not password or len(password) < 8 or len(password) > 24: # pw should be between 8-24 chars
        return make_response( jsonify( { "error" : "Password must be 8-24 characters." } ), 400 )
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email): # email format check validation
        return make_response( jsonify( { "error" : "Please enter a valid email address." } ), 400 )
    if not name.strip():
        return make_response( jsonify( { "error" : "Name cannot be an empty string." } ), 400 )
    # check if username already exists
    if users.find_one({"username": username}):
        return make_response( jsonify( { "error" : "Username is already registered. Please try again." } ), 409 )
    
    hashed_pw = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()) # hash the pw
    # passed validation - insert new user to users collection
    result = users.insert_one({
        "name": name.strip(),
        "username": username,
        "password": hashed_pw,
        "email" : email,
        "admin": False,
        "createdAt": datetime.datetime.now( datetime.UTC )
    })
    return make_response( jsonify( { "message" : "Account created successfully. Welcome!",
                                     "userId" : str(result.inserted_id),
                                     "username" : username } ), 201 )

#LOGIN
@app.route("/api/v1.0/login", methods=["GET"])
def login():
    # in Postman: Basic Auth with valid account user and pw
    auth = request.authorization
    if not auth:
        return make_response( jsonify( { "error" : "Authentication required. Please enter a valid username and password." } ), 401 )
    user = users.find_one( { "username": auth.username } )
    if user is None:
        return make_response( jsonify( { "error" : "Bad username." } ), 401)
    if not bcrypt.checkpw( auth.password.encode("utf-8"), user["password"]):
        return make_response( jsonify( { "error" : "Bad password." } ), 401 )

    token = jwt.encode( {
        "user": auth.username,
        "admin": user.get("admin", False),
        "exp": datetime.datetime.now( datetime.UTC ) + datetime.timedelta( minutes=30 )
    }, globals.secret_key, algorithm="HS256" )
    return make_response( jsonify( {"token": token} ), 200 )

#LOGOUT
@app.route("/api/v1.0/logout", methods=["GET"])
@jwt_required   # user authed
def logout():
    token = request.headers["x-access-token"]   # can assume user is authed if reaching logout stage, so can grab token from header
    blacklist.insert_one( {"token": token} )
    return make_response( jsonify( { "message" : "Logout successful. Goodbye!" } ), 200 )

#########################################################################################################

if __name__ == "__main__":
    app.run(debug=True, port=4999)
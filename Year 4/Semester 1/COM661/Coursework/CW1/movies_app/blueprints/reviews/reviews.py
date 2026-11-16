from flask import Blueprint, request, make_response, jsonify, g
from bson import ObjectId
from bson.errors import InvalidId # for validation
import datetime
from pymongo import ASCENDING, DESCENDING

from decorators import jwt_required # decorator(s)
from globals import movies, serialise_document, BASE_URL
# tokens taken from Postman in x-access-token header

reviews_bp = Blueprint("reviews_bp", __name__)

#########################################################################################################
# REVIEWS (embedded in each movie doc) ##################################################################
#########################################################################################################

# GET all reviews
@reviews_bp.route("/api/v1.0/movies/<string:id>/reviews", methods=["GET"])
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
    if sort_by == "createdAt":
        reviews.sort( key=lambda review: str(review.get("createdAt", "")), reverse=(sort_order == DESCENDING) )
    else:
        reviews.sort( key=lambda review: float(review.get("rating", 0)), reverse=(sort_order == DESCENDING) )

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
@reviews_bp.route("/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>", methods=["GET"])
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
@reviews_bp.route("/api/v1.0/movies/<string:id>/reviews", methods=["POST"])
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
@reviews_bp.route("/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>", methods=["PATCH"])
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
@reviews_bp.route("/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>", methods=["DELETE"])
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
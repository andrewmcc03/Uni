from flask import Blueprint, request, make_response, jsonify
from pymongo import ASCENDING, DESCENDING

from globals import movies, serialise_document

queries_bp = Blueprint("queries_bp", __name__)

#########################################################################################################
# DATASET-SPECIFIC QUERIES / AGGREGATIONS ###############################################################
#########################################################################################################

# stats overview filter page
@queries_bp.route("/api/v1.0/stats/overview", methods=["GET"])
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
@queries_bp.route("/api/v1.0/stats/genres", methods=["GET"])
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
@queries_bp.route("/api/v1.0/movies/top-rated", methods=["GET"])
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
@queries_bp.route("/api/v1.0/movies/highest-grossing", methods=["GET"])
def highest_grossing_movies():
    try:
        limit = min(50, max(1, int(request.args.get("limit", 10))))
    except ValueError:
        return make_response( jsonify( { "error" : "Limit must be a whole number." } ), 400 )

    result = movies.find( {"grossProfits": {"$gt": 0}}).sort("grossProfits", DESCENDING).limit(limit)

    return make_response( jsonify( [serialise_document(movie) for movie in result] ), 200 )

# review statistics grouped by user
@queries_bp.route("/api/v1.0/stats/reviewers", methods=["GET"])
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
@queries_bp.route("/api/v1.0/stats/tags", methods=["GET"])
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
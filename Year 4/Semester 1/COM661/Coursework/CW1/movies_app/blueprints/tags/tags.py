from flask import Blueprint, request, make_response, jsonify, g
from bson import ObjectId
from bson.errors import InvalidId # for validation
import datetime

from decorators import jwt_required # decorator(s)
from globals import movies, serialise_document, BASE_URL
# tokens taken from Postman in x-access-token header

tags_bp = Blueprint("tags_bp", __name__)

#########################################################################################################
# TAGS (also embedded in each movie) ####################################################################
#########################################################################################################

# GET all tags
@tags_bp.route("/api/v1.0/movies/<string:id>/tags", methods=["GET"])
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
@tags_bp.route("/api/v1.0/movies/<string:m_id>/tags/<string:t_id>", methods=["GET"])
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
@tags_bp.route("/api/v1.0/movies/<string:id>/tags", methods=["POST"])
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
@tags_bp.route("/api/v1.0/movies/<string:m_id>/tags/<string:t_id>", methods=["PATCH"])
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
@tags_bp.route("/api/v1.0/movies/<string:m_id>/tags/<string:t_id>", methods=["DELETE"])
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
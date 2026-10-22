from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals

reviews_bp = Blueprint("reviews_bp", __name__)

businesses = globals.db.biz

@reviews_bp.route('/api/v1.0/businesses/<string:id>/reviews', methods=['POST'])
@jwt_required   # user authed
def add_new_review(id):
    new_review = {
        "_id" : ObjectId(),
        "username" : request.form["username"],
        "comment" : request.form["comment"],
        "stars" : request.form["stars"]
    }
    result = businesses.update_one({"_id" : ObjectId(id)}, {
        "$push" : { "reviews" : new_review}
    })
    if result.matched_count == 1:
        new_review_link = "http://localhost:4999/api/v1.0/businesses/" \
            + id + "/reviews/" + str(new_review["_id"])
        return make_response( jsonify( {"url" : new_review_link} ), 201 )
    else:
        return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )

@reviews_bp.route('/api/v1.0/businesses/<string:id>/reviews', methods=['GET'])
def fetch_all_reviews(id):
    data_to_return = []
    business = businesses.find_one({"_id" : ObjectId(id)}, {"reviews" : 1, "_id" : 0})
    for review in business["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)

    return make_response( jsonify( data_to_return ), 200 )

@reviews_bp.route('/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>', methods=['GET'])
def fetch_one_review(b_id, r_id):
    business = businesses.find_one({"reviews._id" : ObjectId(r_id)}, {
        "_id" : 0, "reviews.$" : 1
    })
    if business is None:
        return make_response( jsonify( { "error" : "Invalid business ID or review ID." } ), 404 )
    business["reviews"][0]["_id"] = str(business["reviews"][0]["_id"])
    
    return make_response( jsonify( business["reviews"][0] ), 200 )

@reviews_bp.route('/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>', methods=['PUT'])
@jwt_required   # user authed
def edit_review(b_id, r_id):
    edited_review = {
        "reviews.$.username" : request.form["username"],
        "reviews.$.comment" : request.form["comment"],
        "reviews.$.stars" : request.form["stars"]
    }
    businesses.update_one({
        "reviews._id" : ObjectId(r_id)
    }, {
        "$set" : edited_review
    })
    edited_review_url = "http://localhost:4999/api/v1.0/businesses/" \
        + b_id + "/reviews/" + r_id
    return make_response( jsonify( { "url" : edited_review_url } ), 200 )

@reviews_bp.route('/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>', methods=['DELETE'])
@jwt_required   # user authed
@admin_required # admin authed
def delete_review(b_id, r_id):
    businesses.update_one({
        "_id" : ObjectId(b_id)
    }, {
        "$pull" : {"reviews" : {"_id" : ObjectId(r_id)}}
    })
    
    return make_response( jsonify( {} ), 204 )
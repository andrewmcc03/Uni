from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals

businesses_bp = Blueprint("businesses_bp", __name__)

businesses = globals.db.biz

@businesses_bp.route('/api/v1.0/businesses', methods=['GET'])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)

    data_to_return = []
    for business in businesses.find().skip(page_start).limit(page_size):
        business["_id"] = str(business["_id"])
        for review in business["reviews"]:
            review["_id"] = str(review["_id"])
        data_to_return.append(business)
    
    return make_response( jsonify( data_to_return ), 200 )

@businesses_bp.route('/api/v1.0/businesses/<string:id>', methods=['GET'])
#@jwt_required   # user authed
def show_one_business(id):
    business = businesses.find_one({'_id' : ObjectId(id)})
    if business is not None:
        business['_id'] = str(business['_id'])
        for review in business['reviews']:
            review["_id"] = str(review["_id"])
        return make_response( jsonify( business ), 200 )
    else:
        return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )

@businesses_bp.route('/api/v1.0/businesses', methods=['POST'])
@jwt_required   # user authed
def add_business():
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        new_business = {
            "name" : request.form["name"],
            "town" : request.form["town"],
            "rating" : request.form["rating"],
            "reviews" : []
        }
        new_business_id = businesses.insert_one(new_business)
        new_business_link = "http://localhost:4999/api/v1.0/businesses/" \
            + str(new_business_id.inserted_id)
        return make_response( jsonify( { "url" : new_business_link } ), 201 )
    else:
        return make_response( jsonify( { "error" : "Missing form data." } ), 400 )

@businesses_bp.route('/api/v1.0/businesses/<string:id>', methods=['PUT'])
@jwt_required   # user authed
def edit_business(id):
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        result = businesses.update_one({"_id" : ObjectId(id)}, {
            "$set" : {
                "name" : request.form["name"],
                "town" : request.form["town"],
                "rating" : request.form["rating"]
            }
        })
        if result.matched_count == 1:
            edited_business_link = "http://localhost:4999/api/v1.0/businesses/" + id
            return make_response( jsonify( { "url" : edited_business_link } ), 200 )
        else:
            return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )
    else:
        return make_response( jsonify( { "error" : "Missing form data." } ), 404 )

@businesses_bp.route('/api/v1.0/businesses/<string:id>', methods=['DELETE'])
@jwt_required   # user authed
@admin_required # admin authed
def delete_business(id):
    result = businesses.delete_one({"_id" : ObjectId(id)})
    if result.deleted_count == 1:
        return make_response( jsonify( {} ), 204 )
    else:
        return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )
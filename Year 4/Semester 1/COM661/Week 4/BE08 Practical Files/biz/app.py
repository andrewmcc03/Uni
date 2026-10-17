from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId
import jwt
import datetime
from functools import wraps
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'andrewsk'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz
users = db.users
blacklist = db.blacklist

# auth decorator function
def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        #token = request.args.get('token')
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response( jsonify( { 'message' : 'Token is missing.' } ), 401 )
        try:
            data = jwt.decode( token, app.config['SECRET_KEY'], algorithms='HS256' )
        except:
            return make_response( jsonify( { 'message' : 'Token is invalid.' } ), 401 )
        # check blacklist (used tokens) DB
        bl_token = blacklist.find_one( { 'token' : token } )
        if bl_token is not None:
            return make_response( jsonify( { 'message' : 'Token has been cancelled.' } ), 401 )
        return func(*args, **kwargs)
    return jwt_required_wrapper

# admin auth decorator function
def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers['x-access-token']
        data = jwt.decode( token, app.config['SECRET_KEY'], algorithms='HS256' )
        if data['admin']:
            return func(*args, **kwargs)
        else:
            return make_response( jsonify( { 'message' : 'Admin access is required.' } ), 401 )
    return admin_required_wrapper


###############################################################################################


@app.route('/api/v1.0/businesses', methods=['GET'])
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

@app.route('/api/v1.0/businesses/<string:id>', methods=['GET'])
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

@app.route('/api/v1.0/businesses', methods=['POST'])
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

@app.route('/api/v1.0/businesses/<string:id>', methods=['PUT'])
@jwt_required   # user authed
def edit_business(id):
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        result = businesses.update_one({"_id" : ObjectId(id)}, {
            "$set" : {
                "name" : request.form["name"],
                "town" : request.form["town"],
                "rating" : request.form["rating"],
                "reviews" : []
            }
        })
        if result.matched_count == 1:
            edited_business_link = "http://localhost:4999/api/v1.0/businesses/" + id
            return make_response( jsonify( { "url" : edited_business_link } ), 200 )
        else:
            return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )
    else:
        return make_response( jsonify( { "error" : "Missing form data." } ), 404 )

@app.route('/api/v1.0/businesses/<string:id>', methods=['DELETE'])
@jwt_required   # user authed
@admin_required # admin authed
def delete_business(id):
    result = businesses.delete_one({"_id" : ObjectId(id)})
    if result.deleted_count == 1:
        return make_response( jsonify( {} ), 204 )
    else:
        return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )

@app.route('/api/v1.0/businesses/<string:id>/reviews', methods=['POST'])
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
        return make_response( jsonify( { "error" : "Invalid business ID" } ), 404 )

@app.route('/api/v1.0/businesses/<string:id>/reviews', methods=['GET'])
def fetch_all_reviews(id):
    data_to_return = []
    business = businesses.find_one({"_id" : ObjectId(id)}, {"reviews" : 1, "_id" : 0})
    for review in business["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)

    return make_response( jsonify( data_to_return ), 200 )

@app.route('/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>', methods=['GET'])
def fetch_one_review(b_id, r_id):
    business = businesses.find_one({"reviews._id" : ObjectId(r_id)}, {
        "_id" : 0, "reviews.$" : 1
    })
    if business is None:
        return make_response( jsonify( { "error" : "Invalid business ID or review ID." } ), 404 )
    business["reviews"][0]["_id"] = str(business["reviews"][0]["_id"])
    
    return make_response( jsonify( business["reviews"][0] ), 200 )

@app.route('/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>', methods=['PUT'])
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

@app.route('/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>', methods=['DELETE'])
@jwt_required   # user authed
@admin_required # admin authed
def delete_review(b_id, r_id):
    businesses.update_one({
        "_id" : ObjectId(b_id)
    }, {
        "$pull" : {"reviews" : {"_id" : ObjectId(r_id)}}
    })
    
    return make_response( jsonify( {} ), 200 )

#LOGIN
@app.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization
    #if auth and auth.password == 'password':
    if auth:
        user = users.find_one( { 'username' : auth.username } )
        if user is not None:
            if bcrypt.checkpw( bytes( auth.password, 'UTF-8' ), user['password'] ):
                token = jwt.encode( {
                    'user' : auth.username,
                    'admin' : user['admin'],
                    'exp' : datetime.datetime.now( datetime.UTC ) + datetime.timedelta( minutes=30 )
                }, app.config['SECRET_KEY'], algorithm='HS256' )
                return make_response( jsonify( { 'token' : token } ), 200 )
            else:
                return make_response( jsonify( { 'message' : 'Bad password.' } ), 401 )
        else:
            return make_response( jsonify( { 'message' : 'Bad username.' } ), 401 )
    return make_response( jsonify( { 'message' : 'Authentication required.' } ), 401 )

#LOGOUT
@app.route('/api/v1.0/logout', methods=['GET'])
@jwt_required   # user authed
def logout():
    token = request.headers['x-access-token']   # can assume user is authed if reaching logout stage, so can grab token from header
    blacklist.insert_one( { 'token' : token } )
    return make_response( jsonify( { 'message' : 'Logout successful. Goodbye!' } ), 200 )


if __name__ == "__main__":
    app.run(debug = True, port=4999)